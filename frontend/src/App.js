import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import './App.css';
import bannerFondo from './banner-fondo.jpg';

const DEFAULT_API_URL =
  window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : `https://api.${window.location.hostname.replace(/^www\./, '')}`;
const ENV_API_URL = (process.env.REACT_APP_API_URL || '').trim();
// Siempre usar la URL configurada en build (p. ej. backend en Render). Forzar
// api.{dominio} solo cuando no hay variable de entorno (subdominio propio).
const API_URL = (ENV_API_URL || DEFAULT_API_URL).replace(/\/+$/, '');

/** Subir al cambiar la imagen de muestra en public/ (invalida cache CDN). */
const PLANO_MUESTRA_VER = '6';

const SITE_NAME = (process.env.REACT_APP_SITE_NAME || 'ARQ-IA').trim();
const SUPPORT_WA_DIGITS = (process.env.REACT_APP_SUPPORT_WHATSAPP || '').replace(/\D/g, '');
const SUPPORT_WA_HREF = SUPPORT_WA_DIGITS ? `https://wa.me/${SUPPORT_WA_DIGITS}` : null;

const textoLineaPrecios = (info) => {
  if (!info || !info.actualizado_en) return 'Precios: aun no sincronizados con el servidor.';
  const when = new Date(info.actualizado_en).toLocaleString('es-AR');
  const fuente = info.fuente === 'google_sheets' ? 'Google Sheets (CSV)' : 'lista local (fallback)';
  const cache = info.desde_cache ? ' · sirviendo desde cache' : '';
  return `${fuente} · ref. ${when}${cache}`;
};

const fetchPreciosInfoPublico = async () => {
  try {
    const r = await axios.get(`${API_URL}/precios-info`);
    return r.data;
  } catch (err) {
    if (err?.response?.status === 404) {
      const r = await axios.get(`${API_URL}/api/precios-info`);
      return r.data;
    }
    return null;
  }
};

const modulos = [
  { tipo: 'muros', titulo: 'Estructura y terminaciones', icono: 'M', plan: 'free' },
  { tipo: 'agua', titulo: 'Instalacion sanitaria y gas', icono: 'A', plan: 'pro' },
  { tipo: 'luz', titulo: 'Instalacion electrica', icono: 'E', plan: 'pro' },
  { tipo: 'techo', titulo: 'Techos y losas', icono: 'T', plan: 'pro' },
  { tipo: 'terreno', titulo: 'Medicion de terrenos y lotes', icono: 'L', plan: 'free' },
];

const MODULOS_PRO = new Set(modulos.filter((m) => m.plan === 'pro').map((m) => m.tipo));

/** PNG en public/: planos de referencia usados para calibrar el motor. */
const MUESTRA_ASSET = {
  muros: 'plano-muestra-muros',
  agua: 'plano-muestra-agua',
  luz: 'plano-muestra-luz',
  techo: 'plano-muestra-techo',
  terreno: 'plano-muestra-terreno',
};

function ModuleIconSvg({ tipo }) {
  return (
    <img
      className="module-icon-img"
      src={`/icons/modulo-${tipo}.svg?v=1`}
      alt=""
      width={24}
      height={24}
      loading="lazy"
      decoding="async"
    />
  );
}

const formatoMoneda = (valor) =>
  new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    maximumFractionDigits: 0,
  }).format(Number(valor || 0));


const postAuthWithFallback = async (path, payload) => {
  try {
    return await axios.post(`${API_URL}${path}`, payload);
  } catch (err) {
    if (err?.response?.status === 404) {
      return axios.post(`${API_URL}/api${path}`, payload);
    }
    throw err;
  }
};

const postDemoCalcular = async (formData) => {
  try {
    return await axios.post(`${API_URL}/calcular`, formData);
  } catch (err) {
    if (err?.response?.status === 404) {
      return axios.post(`${API_URL}/api/calcular`, formData);
    }
    throw err;
  }
};

const getPublicWithFallback = async (pathWithQuery) => {
  try {
    return await axios.get(`${API_URL}${pathWithQuery}`);
  } catch (err) {
    if (err?.response?.status === 404) {
      return axios.get(`${API_URL}/api${pathWithQuery}`);
    }
    throw err;
  }
};

const getErrorMessage = (err, fallback, authMode = null) => {
  const status = err?.response?.status;
  const detail = String(err?.response?.data?.detail || '').trim();
  if (status === 429 && detail) return detail;
  if (status === 413 && detail) return detail;
  if (status === 413) return 'El archivo es demasiado grande. Comprimí la imagen o subi menor resolucion.';
  if (status === 403 && detail) return detail;
  if (status === 403) return 'No tenes permiso para esta accion con tu rol actual.';
  if (status === 400 && detail) return detail;
  if (status === 500 && detail) return detail;
  const detailLower = detail.toLowerCase();
  if (authMode === 'login' && (detailLower.includes('email o clave incorrectos') || status === 401)) {
    return 'No existe una cuenta con esos datos o la clave es incorrecta. Primero crea tu usuario en "Crear estudio".';
  }
  if (detail) return detail;
  if (err?.message === 'Network Error') {
    return 'No se pudo conectar con el servidor. Verifica REACT_APP_API_URL, CORS y que la API este online.';
  }
  return fallback;
};

const PALETA_GUIA = [
  { id: 'terreno', nombre: 'Terreno / lote cerrado', muestras: ['#424242'], texto: 'Poligono del lote relleno en gris oscuro uniforme.' },
  { id: 'escala', nombre: 'Escala automatica', muestras: ['#00ff5c'], texto: 'Linea verde fluor + numero en negro al lado (el motor lee el numero con OCR).' },
  { id: 'muros', nombre: 'Muros y cerramientos', muestras: ['#d32f2f'], texto: 'Muros portantes y tabiques en rojo intenso (HSV rojo).' },
  {
    id: 'pisos',
    nombre: 'Pisos (carpeta / ceramicos)',
    muestras: ['#9e9e9e', '#ff9800'],
    texto: 'Gris claro o naranja segun capa de piso o contrapiso.',
  },
  { id: 'aberturas', nombre: 'Aberturas', muestras: ['#00bcd4'], texto: 'Contorno o relleno cian para puertas y ventanas.' },
  { id: 'agua_fria', nombre: 'Agua fria', muestras: ['#1e88e5'], texto: 'Trazos azules.' },
  { id: 'agua_caliente', nombre: 'Agua caliente', muestras: ['#e040fb'], texto: 'Magenta o fucsia.' },
  { id: 'cloacas', nombre: 'Cloacas / desagues', muestras: ['#795548'], texto: 'Marron / sepia / naranja apagado segun plano.' },
  { id: 'luz', nombre: 'Electricidad', muestras: ['#ffeb3b'], texto: 'Amarillo para canalizaciones electricas.' },
  { id: 'techo', nombre: 'Techos y losas', muestras: ['#b388ff'], texto: 'Violeta o fluor violeta para losas o cubiertas.' },
];

function useEscapeClose(onClose) {
  useEffect(() => {
    const onKey = (e) => {
      if (e.key === 'Escape') onClose();
    };
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    window.addEventListener('keydown', onKey);
    return () => {
      document.body.style.overflow = prev;
      window.removeEventListener('keydown', onKey);
    };
  }, [onClose]);
}

function ColorGuidePanel({ onClose }) {
  useEscapeClose(onClose);

  return (
    <div className="color-guide-overlay" onClick={onClose} role="presentation">
      <div
        className="color-guide-sheet"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-labelledby="guia-colores-titulo"
      >
        <header className="color-guide-head">
          <div>
            <span className="eyebrow">Referencia visual</span>
            <h2 id="guia-colores-titulo">Colores que entiende el motor</h2>
            <p className="color-guide-lead">
              No hace falta un hex exacto: el motor busca rangos de color en la imagen. Estos tonos son los mas seguros para coincidir con la calibracion.
            </p>
          </div>
          <button type="button" className="color-guide-close nav-btn" onClick={onClose}>
            Cerrar
          </button>
        </header>
        <ul className="color-guide-list">
          {PALETA_GUIA.map((row) => (
            <li key={row.id} className="color-guide-item">
              <div className="color-guide-swatches" aria-hidden>
                {row.muestras.map((hex) => (
                  <span key={hex} className="color-swatch" style={{ backgroundColor: hex }} title={hex} />
                ))}
              </div>
              <div className="color-guide-copy">
                <strong>{row.nombre}</strong>
                <span>{row.texto}</span>
              </div>
            </li>
          ))}
        </ul>
        <p className="color-guide-foot">
          Plantilla editable:{' '}
          <a className="link-inline" href="/plantilla-paleta-arq-ia.svg" download="plantilla-paleta-arq-ia.svg">
            plantilla-paleta-arq-ia.svg
          </a>
          . Tecla <kbd>Esc</kbd> cierra esta ventana.
        </p>
      </div>
    </div>
  );
}

function PlansPanel({ onClose, billing, onSubscribe, canSubscribe, loadingBilling }) {
  useEscapeClose(onClose);
  const freeLimit = billing?.free_monthly_limit ?? 20;
  const paidLimit = billing?.paid_monthly_limit ?? 500;
  const amount = billing?.amount;
  const currency = billing?.currency || 'ARS';

  return (
    <div className="color-guide-overlay" onClick={onClose} role="presentation">
      <div
        className="color-guide-sheet plans-sheet"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-labelledby="planes-titulo"
      >
        <header className="color-guide-head">
          <div>
            <span className="eyebrow">Planes</span>
            <h2 id="planes-titulo">Free vs Plan Pro</h2>
            <p className="color-guide-lead">
              Empeza gratis. Cuando el estudio crece, activa el plan con Mercado Pago en pesos argentinos.
            </p>
          </div>
          <button type="button" className="color-guide-close nav-btn" onClick={onClose}>
            Cerrar
          </button>
        </header>
        <div className="plans-grid">
          <article className="plan-card">
            <span className="eyebrow">Inicial</span>
            <h3>Free</h3>
            <p className="plan-price">$ 0 <small>/ mes</small></p>
            <ul>
              <li>Hasta {freeLimit} planos por mes</li>
              <li>Modulos Free: muros y terrenos</li>
              <li>Export CSV y PDF</li>
              <li>Invitaciones al equipo</li>
            </ul>
          </article>
          <article className="plan-card plan-card--pro">
            <span className="eyebrow">Recomendado</span>
            <h3>Pro</h3>
            <p className="plan-price">
              {amount != null ? formatoMoneda(amount) : 'Consultar'}{' '}
              <small>/ mes {currency}</small>
            </p>
            <ul>
              <li>Hasta {paidLimit} planos por mes</li>
              <li>Agua/gas, electricidad y techos</li>
              <li>Todos los modulos Free incluidos</li>
              <li>Cobro local con Mercado Pago</li>
            </ul>
            {canSubscribe && (
              <button type="button" className="primary-btn" disabled={loadingBilling} onClick={onSubscribe}>
                {loadingBilling ? 'Redirigiendo...' : 'Activar con Mercado Pago'}
              </button>
            )}
          </article>
        </div>
      </div>
    </div>
  );
}

function ComparePanel({ left, right, onClose }) {
  useEscapeClose(onClose);
  const leftItems = left?.items || [];
  const rightItems = right?.items || [];
  const names = Array.from(new Set([...leftItems.map((i) => i.nom), ...rightItems.map((i) => i.nom)]));
  const mapVal = (items, nom) => {
    const hit = items.find((i) => i.nom === nom);
    return hit ? hit.val : null;
  };

  return (
    <div className="color-guide-overlay" onClick={onClose} role="presentation">
      <div
        className="color-guide-sheet compare-sheet"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-labelledby="compare-titulo"
      >
        <header className="color-guide-head">
          <div>
            <span className="eyebrow">Comparacion</span>
            <h2 id="compare-titulo">Dos analisis lado a lado</h2>
            <p className="color-guide-lead">
              {left?.filename} ({left?.tipo}) vs {right?.filename} ({right?.tipo})
            </p>
          </div>
          <button type="button" className="color-guide-close nav-btn" onClick={onClose}>
            Cerrar
          </button>
        </header>
        <div className="compare-totals">
          <div>
            <span>Total A</span>
            <strong>{left?.tipo === 'terreno' ? '—' : formatoMoneda(left?.total)}</strong>
          </div>
          <div>
            <span>Total B</span>
            <strong>{right?.tipo === 'terreno' ? '—' : formatoMoneda(right?.total)}</strong>
          </div>
          <div>
            <span>Diferencia</span>
            <strong>
              {left?.tipo === 'terreno' || right?.tipo === 'terreno'
                ? '—'
                : formatoMoneda(Number(right?.total || 0) - Number(left?.total || 0))}
            </strong>
          </div>
        </div>
        <div className="compare-table-wrap">
          <table className="compare-table">
            <thead>
              <tr>
                <th>Item</th>
                <th>Analisis A</th>
                <th>Analisis B</th>
              </tr>
            </thead>
            <tbody>
              {names.map((nom) => {
                const a = mapVal(leftItems, nom);
                const b = mapVal(rightItems, nom);
                return (
                  <tr key={nom}>
                    <td>{nom}</td>
                    <td>{a == null ? '—' : left?.tipo === 'terreno' ? String(a) : formatoMoneda(a)}</td>
                    <td>{b == null ? '—' : right?.tipo === 'terreno' ? String(b) : formatoMoneda(b)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
        <div className="compare-images">
          {left?.imagen && <img src={`data:image/png;base64,${left.imagen}`} alt="Auditoria A" />}
          {right?.imagen && <img src={`data:image/png;base64,${right.imagen}`} alt="Auditoria B" />}
        </div>
      </div>
    </div>
  );
}

function App() {
  const [token, setToken] = useState(() => localStorage.getItem('arqia_token') || '');
  const [authMode, setAuthMode] = useState('login'); // login | register | forgot | reset
  const [authForm, setAuthForm] = useState({
    studio_name: '',
    name: '',
    email: '',
    password: '',
  });
  const [resetToken, setResetToken] = useState('');
  const [authNotice, setAuthNotice] = useState('');
  const [lastInviteEmailSent, setLastInviteEmailSent] = useState(null);
  const [me, setMe] = useState(null);
  const [projects, setProjects] = useState([]);
  const [activeProjectId, setActiveProjectId] = useState(() => localStorage.getItem('arqia_project_id') || '');
  const [processes, setProcesses] = useState([]);
  const [projectForm, setProjectForm] = useState({ name: '', client: '', address: '' });
  const [referencia, setReferencia] = useState(1);
  const [sistemaMuro, setSistemaMuro] = useState('ladrillo_hueco_12');
  const [alturaMuro, setAlturaMuro] = useState(2.6);
  const [mostrarGuia, setMostrarGuia] = useState(false);
  const [mostrarPlanes, setMostrarPlanes] = useState(false);
  const [editProjectForm, setEditProjectForm] = useState({ name: '', client: '', address: '' });
  const [compareIds, setCompareIds] = useState([]);
  const [mostrarCompare, setMostrarCompare] = useState(false);
  const [mobileNavOpen, setMobileNavOpen] = useState(false);
  const [loading, setLoading] = useState('');
  const [error, setError] = useState('');
  const [billingPublic, setBillingPublic] = useState(null);
  const [demoMode, setDemoMode] = useState(false);
  const [demoRuns, setDemoRuns] = useState([]);
  const [paletteDescargada, setPaletteDescargada] = useState(() => localStorage.getItem('arqia_palette_ok') === '1');
  const [demoColoresOk, setDemoColoresOk] = useState(() => localStorage.getItem('arqia_demo_colores_ok') === '1');
  const [workspaceOnboardingHecho, setWorkspaceOnboardingHecho] = useState(
    () => localStorage.getItem('arqia_onboard_ws') === '1',
  );
  const [exportasteCsv, setExportasteCsv] = useState(false);
  const [preciosInfo, setPreciosInfo] = useState(null);
  const [inviteInfo, setInviteInfo] = useState(null);
  const [inviteLoading, setInviteLoading] = useState(false);
  const [invitations, setInvitations] = useState([]);
  const [inviteForm, setInviteForm] = useState({ email: '', role: 'editor' });
  const [lastInviteUrl, setLastInviteUrl] = useState('');
  const [lastDemoUpload, setLastDemoUpload] = useState(null);
  const [lastUploadByProject, setLastUploadByProject] = useState({});

  const api = useMemo(() => {
    const instance = axios.create({ baseURL: API_URL });
    instance.interceptors.request.use((config) => {
      if (token) config.headers.Authorization = `Bearer ${token}`;
      return config;
    });
    return instance;
  }, [token]);

  const activeProject = projects.find((project) => project.id === Number(activeProjectId));
  // Mientras /me carga, no ocultar acciones; al confirmar viewer, bloquear mutaciones.
  const canEdit = !me || (me.role !== 'viewer' && me.can_edit !== false);
  const canManageBilling = !me || me.can_manage_billing === true || me.role === 'owner';
  const isPro = me?.studio?.plan_status === 'active';
  const hasActiveObra = Boolean(activeProjectId && activeProject);
  const granTotal = processes
    .filter((process) => process.tipo !== 'terreno')
    .reduce((acc, process) => acc + Number(process.total || 0), 0);
  const lastProcess = processes[0];
  const planStatus = isPro
    ? 'Plan Pro'
    : me?.studio?.plan_status === 'paused'
      ? 'Plan pausado'
      : 'Plan Free';
  const moduloBloqueado = (tipo) => MODULOS_PRO.has(tipo) && !isPro;

  const refreshMe = async () => {
    const res = await api.get('/me');
    setMe(res.data);
  };

  const refreshProjects = async () => {
    const res = await api.get('/projects');
    setProjects(res.data);
    const savedId = localStorage.getItem('arqia_project_id');
    const exists = res.data.some((p) => String(p.id) === String(savedId));
    if (exists) setActiveProjectId(String(savedId));
    else if (res.data[0]) setActiveProjectId(String(res.data[0].id));
  };

  const refreshProcesses = async (projectId = activeProjectId) => {
    if (!projectId) {
      setProcesses([]);
      return;
    }
    const res = await api.get(`/projects/${projectId}/processes`);
    setProcesses(res.data);
  };

  useEffect(() => {
    fetchPreciosInfoPublico().then(setPreciosInfo).catch(() => setPreciosInfo(null));
    getPublicWithFallback('/billing/info')
      .then((r) => setBillingPublic(r.data))
      .catch(() => setBillingPublic(null));
  }, [token, demoMode]);

  useEffect(() => {
    if (!activeProject) {
      setEditProjectForm({ name: '', client: '', address: '' });
      return;
    }
    setEditProjectForm({
      name: activeProject.name || '',
      client: activeProject.client || '',
      address: activeProject.address || '',
    });
  }, [activeProject]);

  useEffect(() => {
    setCompareIds([]);
    setMostrarCompare(false);
  }, [activeProjectId]);

  useEffect(() => {
    if (token) {
      setDemoMode(false);
      setDemoRuns([]);
      setLastDemoUpload(null);
    }
  }, [token]);

  useEffect(() => {
    if (token) {
      setInviteInfo(null);
      setInviteLoading(false);
      return;
    }
    const params = new URLSearchParams(window.location.search);
    const reset = params.get('reset');
    if (reset) {
      setResetToken(reset);
      setAuthMode('reset');
      setInviteInfo(null);
      setInviteLoading(false);
      setError('');
      setAuthNotice('Elegi una nueva clave para tu cuenta.');
      return;
    }
    const raw = params.get('invite');
    if (!raw) {
      setInviteInfo(null);
      setInviteLoading(false);
      return;
    }
    let cancelled = false;
    setInviteLoading(true);
    setError('');
    (async () => {
      try {
        const r = await getPublicWithFallback(`/invites/verify?token=${encodeURIComponent(raw)}`);
        if (!cancelled) {
          setInviteInfo({
            token: raw,
            email: r.data.email,
            studioName: r.data.studio_name || 'el estudio',
            role: r.data.role,
          });
          setAuthForm((f) => ({ ...f, email: r.data.email, name: '', password: '' }));
        }
      } catch (err) {
        if (!cancelled) {
          setInviteInfo(null);
          setError(getErrorMessage(err, 'Invitacion invalida o vencida.'));
        }
      } finally {
        if (!cancelled) setInviteLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [token]);

  useEffect(() => {
    if (!token || !me?.can_manage_invites) {
      setInvitations([]);
      return;
    }
    api
      .get('/studio/invitations')
      .then((res) => setInvitations(res.data))
      .catch(() => setInvitations([]));
  }, [token, me?.can_manage_invites, api]);

  useEffect(() => {
    if (!token) return;
    Promise.all([refreshMe(), refreshProjects()]).catch((err) => {
      const msg = err?.response?.data?.detail || 'No se pudo validar la sesion. Volvé a iniciar sesion.';
      setError(String(msg));
      localStorage.removeItem('arqia_token');
      setToken('');
      setMe(null);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  useEffect(() => {
    if (activeProjectId) {
      localStorage.setItem('arqia_project_id', String(activeProjectId));
      refreshProcesses(activeProjectId).catch(() => {
        localStorage.removeItem('arqia_token');
        setToken('');
        setMe(null);
      });
    }
    setExportasteCsv(false);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeProjectId]);

  const salirDeFlujoInvitacion = () => {
    setInviteInfo(null);
    setInviteLoading(false);
    setError('');
    const u = new URL(window.location.href);
    u.searchParams.delete('invite');
    const qs = u.searchParams.toString();
    window.history.replaceState({}, '', `${u.pathname}${qs ? `?${qs}` : ''}`);
    setAuthMode('login');
  };

  const submitInviteRegister = async (event) => {
    event.preventDefault();
    if (!inviteInfo) return;
    if (!authForm.name.trim()) {
      setError('Ingresa tu nombre.');
      return;
    }
    setLoading('auth');
    setError('');
    try {
      const res = await postAuthWithFallback('/auth/register-invite', {
        token: inviteInfo.token,
        name: authForm.name.trim(),
        password: authForm.password,
      });
      const u = new URL(window.location.href);
      u.searchParams.delete('invite');
      const qs = u.searchParams.toString();
      window.history.replaceState({}, '', `${u.pathname}${qs ? `?${qs}` : ''}`);
      setInviteInfo(null);
      localStorage.setItem('arqia_token', res.data.token);
      setDemoMode(false);
      setDemoRuns([]);
      setLastUploadByProject({});
      setToken(res.data.token);
    } catch (err) {
      setError(getErrorMessage(err, 'No se pudo completar el registro con la invitacion.'));
    } finally {
      setLoading('');
    }
  };

  const clearResetQuery = () => {
    const u = new URL(window.location.href);
    u.searchParams.delete('reset');
    const qs = u.searchParams.toString();
    window.history.replaceState({}, '', `${u.pathname}${qs ? `?${qs}` : ''}`);
    setResetToken('');
  };

  const submitAuth = async (event) => {
    event.preventDefault();
    setError('');
    setAuthNotice('');

    if (authMode === 'forgot') {
      if (!authForm.email.trim()) {
        setError('Ingresa tu email.');
        return;
      }
      setLoading('auth');
      try {
        const res = await postAuthWithFallback('/auth/forgot-password', { email: authForm.email.trim() });
        if (res.data.dev_reset_url) {
          setAuthNotice(`${res.data.detail || 'Listo.'} Enlace de desarrollo: ${res.data.dev_reset_url}`);
        } else if (res.data.email_sent) {
          setAuthNotice('Email enviado. Revisá bandeja de entrada y Spam.');
        } else if (res.data.email_error) {
          setError(`No se pudo enviar el email: ${res.data.email_error}`);
        } else {
          setAuthNotice(
            'Si ese email tiene cuenta, deberia llegar el enlace. Si no llega: revisá Spam, confirma que el usuario exista (Crear estudio) y que EMAIL_FROM en Resend pueda enviar a ese destinatario (con onboarding@resend.dev solo llega al email de tu cuenta Resend).',
          );
        }
      } catch (err) {
        setError(getErrorMessage(err, 'No se pudo enviar el email de recuperacion.'));
      } finally {
        setLoading('');
      }
      return;
    }

    if (authMode === 'reset') {
      if (!resetToken) {
        setError('Falta el token de recuperacion. Pedi un enlace nuevo.');
        return;
      }
      if ((authForm.password || '').length < 8) {
        setError('La clave debe tener al menos 8 caracteres.');
        return;
      }
      setLoading('auth');
      try {
        const res = await postAuthWithFallback('/auth/reset-password', {
          token: resetToken,
          password: authForm.password,
        });
        clearResetQuery();
        setAuthMode('login');
        setAuthNotice(res.data.detail || 'Clave actualizada. Ya podes ingresar.');
        setAuthForm((f) => ({ ...f, password: '' }));
      } catch (err) {
        setError(getErrorMessage(err, 'No se pudo restablecer la clave.'));
      } finally {
        setLoading('');
      }
      return;
    }

    if (authMode === 'register') {
      if (!authForm.studio_name.trim() || !authForm.name.trim()) {
        setError('Completa nombre del estudio y tu nombre para crear la cuenta.');
        return;
      }
    }

    setLoading('auth');
    try {
      const path = authMode === 'login' ? '/auth/login' : '/auth/register';
      const payload =
        authMode === 'login'
          ? { email: authForm.email, password: authForm.password }
          : authForm;
      const res = await postAuthWithFallback(path, payload);
      localStorage.setItem('arqia_token', res.data.token);
      setDemoMode(false);
      setDemoRuns([]);
      setLastUploadByProject({});
      setToken(res.data.token);
    } catch (err) {
      setError(getErrorMessage(err, authMode === 'login' ? 'No se pudo iniciar sesion.' : 'No se pudo crear la cuenta.', authMode));
    } finally {
      setLoading('');
    }
  };

  const logout = () => {
    localStorage.removeItem('arqia_token');
    setToken('');
    setMe(null);
    setProjects([]);
    setProcesses([]);
    setLastDemoUpload(null);
    setLastUploadByProject({});
  };

  const createProject = async (event) => {
    event.preventDefault();
    if (!projectForm.name.trim()) return;
    setLoading('project');
    setError('');
    try {
      const res = await api.post('/projects', projectForm);
      setProjectForm({ name: '', client: '', address: '' });
      await refreshProjects();
      setActiveProjectId(String(res.data.id));
    } catch (err) {
      setError(getErrorMessage(err, 'No se pudo crear la obra.'));
    } finally {
      setLoading('');
    }
  };

  const updateProject = async (event) => {
    event.preventDefault();
    if (!activeProjectId || !editProjectForm.name.trim()) return;
    setLoading('project-edit');
    setError('');
    try {
      await api.patch(`/projects/${activeProjectId}`, editProjectForm);
      await refreshProjects();
    } catch (err) {
      setError(getErrorMessage(err, 'No se pudo actualizar la obra.'));
    } finally {
      setLoading('');
    }
  };

  const toggleCompare = (processId) => {
    setCompareIds((prev) => {
      if (prev.includes(processId)) return prev.filter((id) => id !== processId);
      if (prev.length >= 2) return [prev[1], processId];
      return [...prev, processId];
    });
  };

  const appendCalculoFields = (formData, tipo) => {
    formData.append('referencia_metros', referencia);
    formData.append('tipo_plano', tipo);
    formData.append('sistema_muro', sistemaMuro);
    formData.append('altura_muro', String(alturaMuro));
  };

  const subirPlanoDemo = async (archivo, tipo) => {
    if (!archivo) return;
    const formData = new FormData();
    formData.append('file', archivo);
    appendCalculoFields(formData, tipo);

    setLoading(tipo);
    setError('');
    try {
      const res = await postDemoCalcular(formData);
      const data = res.data;
      const id = `demo-${Date.now()}`;
      const meta = {
        escala_modo: data.escala_modo,
        metros_referencia_usados: data.metros_referencia_usados,
        avisos: data.avisos || [],
        precios_info: data.precios_info || {},
      };
      setDemoRuns((prev) =>
        [
          {
            id,
            filename: archivo.name || 'plano',
            tipo: data.tipo || tipo,
            items: data.items || [],
            total: data.total,
            imagen: data.imagen,
            escala_detectada: data.escala_detectada,
            meta,
          },
          ...prev,
        ].slice(0, 6),
      );
      setLastDemoUpload({ file: archivo, tipo: data.tipo || tipo });
      fetchPreciosInfoPublico().then(setPreciosInfo).catch(() => {});
    } catch (err) {
      setError(getErrorMessage(err, 'No se pudo procesar el plano en modo prueba.'));
    } finally {
      setLoading('');
    }
  };

  const cargarPlanoMuestra = async (tipo, enDemo) => {
    setError('');
    const assetBase = MUESTRA_ASSET[tipo] || MUESTRA_ASSET.muros;
    try {
      const r = await fetch(`${window.location.origin}/${assetBase}.png?v=${PLANO_MUESTRA_VER}`, { cache: 'no-store' });
      if (!r.ok) throw new Error('missing');
      const blob = await r.blob();
      const f = new File([blob], `${assetBase}.png`, { type: 'image/png' });
      if (enDemo) await subirPlanoDemo(f, tipo);
      else await subirPlano(f, tipo);
    } catch (err) {
      setError('No se encontro el plano de ejemplo en el sitio. Volvé a desplegar el frontend con los PNG en public/.');
    }
  };

  const marcarPaletaDescargada = () => {
    localStorage.setItem('arqia_palette_ok', '1');
    setPaletteDescargada(true);
  };

  const marcarDemoColoresOk = () => {
    localStorage.setItem('arqia_demo_colores_ok', '1');
    setDemoColoresOk(true);
  };

  const cerrarOnboardingWorkspace = () => {
    localStorage.setItem('arqia_onboard_ws', '1');
    setWorkspaceOnboardingHecho(true);
  };

  const subirPlano = async (archivo, tipo) => {
    if (!archivo || !activeProjectId) return;
    if (moduloBloqueado(tipo)) {
      setError('Este modulo es Plan Pro. Activa la suscripcion con Mercado Pago para usarlo.');
      return;
    }
    const formData = new FormData();
    formData.append('file', archivo);
    appendCalculoFields(formData, tipo);

    setLoading(tipo);
    setError('');
    try {
      await api.post(`/projects/${activeProjectId}/calcular`, formData);
      setLastUploadByProject((m) => ({ ...m, [String(activeProjectId)]: { file: archivo, tipo } }));
      await Promise.all([refreshProcesses(activeProjectId), refreshMe(), refreshProjects()]);
      fetchPreciosInfoPublico().then(setPreciosInfo).catch(() => {});
    } catch (err) {
      setError(getErrorMessage(err, 'No se pudo procesar el plano.'));
    } finally {
      setLoading('');
    }
  };

  const abrirCheckout = async () => {
    setLoading('billing');
    setError('');
    try {
      const res = await api.post('/billing/create-checkout-session');
      window.location.href = res.data.url;
    } catch (err) {
      setError(getErrorMessage(err, 'Mercado Pago todavia no esta configurado.'));
    } finally {
      setLoading('');
    }
  };

  const cancelarSuscripcion = async () => {
    if (!window.confirm('Cancelar la suscripcion de Mercado Pago de este estudio?')) return;
    setLoading('billing-cancel');
    setError('');
    try {
      await api.post('/billing/cancel');
      await refreshMe();
    } catch (err) {
      setError(getErrorMessage(err, 'No se pudo cancelar la suscripcion.'));
    } finally {
      setLoading('');
    }
  };

  const exportarCsv = async () => {
    if (!activeProjectId) return;
    setError('');
    try {
      const res = await api.get(`/projects/${activeProjectId}/export.csv`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.download = `arq-ia-obra-${activeProjectId}.csv`;
      link.click();
      window.URL.revokeObjectURL(url);
      setExportasteCsv(true);
    } catch (err) {
      setError(getErrorMessage(err, 'No se pudo exportar la obra.'));
    }
  };

  const exportarPdf = async () => {
    if (!activeProjectId) return;
    setError('');
    try {
      const res = await api.get(`/projects/${activeProjectId}/export.pdf`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }));
      const link = document.createElement('a');
      link.href = url;
      link.download = `arq-ia-obra-${activeProjectId}.pdf`;
      link.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(getErrorMessage(err, 'No se pudo exportar el PDF.'));
    }
  };

  const crearInvitacion = async (event) => {
    event.preventDefault();
    if (!inviteForm.email.trim()) return;
    setLoading('invite');
    setError('');
    setLastInviteEmailSent(null);
    try {
      const res = await api.post('/studio/invitations', {
        email: inviteForm.email.trim(),
        role: inviteForm.role,
      });
      setLastInviteUrl(res.data.invite_url || '');
      setLastInviteEmailSent(Boolean(res.data.email_sent));
      if (!res.data.email_sent && res.data.email_error) {
        setError(`Invitacion creada, pero el email no se envio: ${res.data.email_error}. Copia el enlace abajo.`);
      }
      setInviteForm({ email: '', role: 'editor' });
      const list = await api.get('/studio/invitations');
      setInvitations(list.data);
    } catch (err) {
      setError(getErrorMessage(err, 'No se pudo crear la invitacion.'));
    } finally {
      setLoading('');
    }
  };

  const revocarInvitacion = async (inviteId) => {
    if (!window.confirm('Revocar esta invitacion?')) return;
    setError('');
    try {
      await api.delete(`/studio/invitations/${inviteId}`);
      const list = await api.get('/studio/invitations');
      setInvitations(list.data);
    } catch (err) {
      setError(getErrorMessage(err, 'No se pudo revocar la invitacion.'));
    }
  };

  const copiarTexto = async (texto) => {
    try {
      await navigator.clipboard.writeText(texto);
      setError('');
    } catch {
      setError('No se pudo copiar al portapapeles.');
    }
  };

  const eliminarAnalisis = async (processId) => {
    if (!window.confirm('Eliminar este analisis?')) return;
    setError('');
    try {
      await api.delete(`/processes/${processId}`);
      await Promise.all([refreshProcesses(activeProjectId), refreshProjects(), refreshMe()]);
    } catch (err) {
      setError(getErrorMessage(err, 'No se pudo eliminar el analisis.'));
    }
  };

  const eliminarObra = async () => {
    if (!activeProjectId || !window.confirm('Eliminar esta obra y todo su historial?')) return;
    setError('');
    const pid = String(activeProjectId);
    try {
      await api.delete(`/projects/${activeProjectId}`);
      setActiveProjectId('');
      setLastUploadByProject((m) => {
        const n = { ...m };
        delete n[pid];
        return n;
      });
      await Promise.all([refreshProjects(), refreshMe()]);
      setProcesses([]);
    } catch (err) {
      setError(getErrorMessage(err, 'No se pudo eliminar la obra.'));
    }
  };

  const eliminarDemoRun = (runId) => {
    setDemoRuns((prev) => prev.filter((r) => r.id !== runId));
  };

  const ScalePanel = ({ ultimo, onAplicarManual }) => {
    const modo = ultimo?.meta?.escala_modo;
    const ocrRaw = ultimo?.escala_detectada;
    const ocrNum = ocrRaw != null && ocrRaw !== '' && !Number.isNaN(Number(ocrRaw)) ? Number(ocrRaw) : null;
    const aplicadoRaw = ultimo?.meta?.metros_referencia_usados ?? ultimo?.metros_referencia_usados;
    let aplicadoNum =
      aplicadoRaw != null && aplicadoRaw !== '' && !Number.isNaN(Number(aplicadoRaw)) ? Number(aplicadoRaw) : null;
    if (aplicadoNum == null && ultimo && ocrNum != null) aplicadoNum = ocrNum;
    if (aplicadoNum == null && ultimo) {
      const r = Number(referencia);
      if (!Number.isNaN(r) && r > 0) aplicadoNum = r;
    }

    const tieneDato = aplicadoNum != null && !Number.isNaN(aplicadoNum);
    const valorTexto = tieneDato ? `${aplicadoNum.toFixed(2)} m` : '—';

    return (
      <div className="scale-panel">
        <div className="scale-panel-head">
          <span className="eyebrow">Calibracion</span>
          <strong className="scale-panel-title">Escala del plano</strong>
        </div>
        <div className="scale-panel-cols">
          <div className="scale-field">
            <label htmlFor="ref-metros">Respaldo manual</label>
            <form
              className="scale-manual-form"
              onSubmit={(e) => {
                e.preventDefault();
                if (onAplicarManual) onAplicarManual();
              }}
            >
              <div className="scale-input-wrap">
                <input
                  id="ref-metros"
                  type="number"
                  min="0.1"
                  step="0.1"
                  value={referencia}
                  onChange={(e) => setReferencia(e.target.value)}
                />
                <span className="scale-suffix">m</span>
              </div>
              {onAplicarManual && (
                <div className="scale-apply-row">
                  <button type="submit" className="scale-apply-btn nav-btn">
                    Aplicar escala
                  </button>
                  <span className="scale-apply-hint">Enter reaplica el ultimo plano subido.</span>
                </div>
              )}
            </form>
            <p className="scale-hint">Metros del segmento verde si el OCR no lee el numero.</p>
          </div>
          <div className={`scale-field scale-readout${!tieneDato ? ' is-empty' : ''}`}>
            <span className="scale-readout-label">Escala aplicada al calculo</span>
            <p className="scale-readout-value">{valorTexto}</p>
            {!ultimo && <p className="scale-readout-meta">Procesa un plano para ver la escala usada en el calculo.</p>}
            {ultimo && tieneDato && modo === 'ocr' && (
              <p className="scale-readout-meta">
                {ocrNum != null ? `Lectura OCR: ${ocrNum.toFixed(2)} m.` : 'Escala leida por OCR sobre la linea verde.'}
              </p>
            )}
            {ultimo && tieneDato && modo === 'manual' && (
              <p className="scale-readout-meta">OCR sin lectura; se uso el respaldo manual.</p>
            )}
            {ultimo && tieneDato && modo === 'sin_linea' && (
              <p className="scale-readout-meta">Sin traza verde; se uso el respaldo manual.</p>
            )}
            {ultimo && tieneDato && ocrNum != null && aplicadoNum != null && Math.abs(ocrNum - aplicadoNum) >= 0.02 && (
              <p className="scale-readout-meta">
                OCR leyo {ocrNum.toFixed(2)} m; el calculo uso {aplicadoNum.toFixed(2)} m.
              </p>
            )}
          </div>
        </div>
      </div>
    );
  };

  const ComputeOptionsPanel = () => (
    <div className="compute-options">
      <div className="scale-panel-head">
        <span className="eyebrow">Parametros de muro</span>
        <strong className="scale-panel-title">Sistema y altura</strong>
      </div>
      <div className="compute-options-cols">
        <label className="compute-field">
          <span>Sistema constructivo</span>
          <select value={sistemaMuro} onChange={(e) => setSistemaMuro(e.target.value)}>
            <option value="ladrillo_hueco_12">Ladrillo hueco 12 cm</option>
            <option value="ladrillo_comun_12">Ladrillo comun 12 cm</option>
          </select>
        </label>
        <label className="compute-field">
          <span>Altura de muro (m)</span>
          <div className="scale-input-wrap">
            <input
              type="number"
              min="1.8"
              max="6"
              step="0.1"
              value={alturaMuro}
              onChange={(e) => setAlturaMuro(e.target.value)}
            />
            <span className="scale-suffix">m</span>
          </div>
        </label>
      </div>
      <p className="scale-hint">Se aplica al modulo de muros (superficie vertical y materiales). Rango 1,8–6,0 m.</p>
    </div>
  );

  const demoGranTotal = demoRuns.filter((r) => r.tipo !== 'terreno').reduce((acc, r) => acc + Number(r.total || 0), 0);
  const demoUltimo = demoRuns[0];

  if (!token && demoMode) {
    return (
      <div className="App demo-app">
        <header className="topbar demo-topbar" style={{ backgroundImage: `linear-gradient(to bottom, rgba(10,10,10,0.82), rgba(10,10,10,0.98)), url(${bannerFondo})` }}>
          <div className="brand-block">
            <img src="/logo.png" alt={SITE_NAME} className="logo-img" />
            <div>
              <h1>{SITE_NAME}</h1>
              <p>Modo prueba — no guarda obras ni consume tu cupo</p>
            </div>
          </div>
          <div className="top-actions">
            <button type="button" className={`nav-btn${mostrarGuia ? ' nav-btn--active' : ''}`} onClick={() => setMostrarGuia(!mostrarGuia)}>
              {mostrarGuia ? 'Cerrar guia' : 'Guia de colores'}
            </button>
            <button type="button" className="nav-btn" onClick={() => setMostrarPlanes(true)}>
              Planes
            </button>
            <button
              type="button"
              className="nav-btn"
              onClick={() => {
                setAuthMode('register');
                setDemoMode(false);
                setLastDemoUpload(null);
                setError('');
              }}
            >
              Crear estudio
            </button>
            <button type="button" className="nav-btn" onClick={() => { setDemoMode(false); setLastDemoUpload(null); setError(''); }}>
              Volver al login
            </button>
          </div>
        </header>
        <div className="precios-bar">{preciosInfo ? textoLineaPrecios(preciosInfo) : 'Precios: conectando con la API...'}</div>

        {mostrarGuia && <ColorGuidePanel onClose={() => setMostrarGuia(false)} />}
        {mostrarPlanes && (
          <PlansPanel
            onClose={() => setMostrarPlanes(false)}
            billing={billingPublic || {}}
            canSubscribe={false}
          />
        )}

        <main className="workspace demo-workspace">
          <aside className="sidebar demo-sidebar">
            <div className="onboarding-card">
              <span className="eyebrow">Primeros pasos</span>
              <h2>Proba el motor en vivo</h2>
              <p className="onboarding-lead">Segui la lista: no requiere cuenta. Para historial, exportacion y equipos, crea tu estudio.</p>
              <ol className="onboarding-steps">
                <li className={paletteDescargada ? 'done' : ''}>
                  <span className="step-title">Descarga la paleta oficial (SVG)</span>
                  <a
                    className="link-inline"
                    href="/plantilla-paleta-arq-ia.svg"
                    download="plantilla-paleta-arq-ia.svg"
                    onClick={marcarPaletaDescargada}
                  >
                    plantilla-paleta-arq-ia.svg
                  </a>
                </li>
                <li className={demoColoresOk ? 'done' : ''}>
                  <span className="step-title">Revisa colores y escala en el plano</span>
                  <small>Usá el boton Guia de colores arriba para ver cada tono. Linea verde + numero para OCR.</small>
                  {!demoColoresOk && (
                    <button type="button" className="nav-btn step-ack" onClick={marcarDemoColoresOk}>
                      Entendido
                    </button>
                  )}
                </li>
                <li className={demoRuns.length > 0 ? 'done' : ''}>
                  <span className="step-title">Subi un PNG, JPG o WebP</span>
                  <small>Elegi un modulo y cargá tu plano. El resultado aparece abajo (no se guarda en servidor).</small>
                </li>
                <li>
                  <span className="step-title">Guardar obra y CSV</span>
                  <button type="button" className="nav-btn step-ack" onClick={() => { setAuthMode('register'); setDemoMode(false); setLastDemoUpload(null); setError(''); }}>
                    Crear estudio gratis
                  </button>
                </li>
              </ol>
            </div>
          </aside>

          <section className="main-panel demo-main">
            <header className="demo-panel-intro">
              <span className="eyebrow">Panel de computo</span>
              <h2>Modo demostracion</h2>
              <p>Los analisis se muestran solo en este navegador. La API usa el mismo motor que en produccion, sin persistencia.</p>
            </header>

            {error && <div className="error-box">{error}</div>}

            <div className="kpi-grid kpi-grid--demo">
              <div className="kpi-card">
                <span>Total estimado (demo)</span>
                <strong>{formatoMoneda(demoGranTotal)}</strong>
              </div>
              <div className="kpi-card">
                <span>Analisis en esta sesion</span>
                <strong>{demoRuns.length}</strong>
              </div>
              <div className="kpi-card">
                <span>Ultimo modulo</span>
                <strong>{demoUltimo?.tipo || 'Sin datos'}</strong>
              </div>
            </div>

            <div className="demo-calibration-card">
              <ScalePanel
                ultimo={demoUltimo}
                onAplicarManual={lastDemoUpload ? () => subirPlanoDemo(lastDemoUpload.file, lastDemoUpload.tipo) : null}
              />
              <ComputeOptionsPanel />
            </div>

            <div className="sample-actions">
              <span className="eyebrow">Planos de referencia</span>
              <p className="sample-preview-caption">
                Son los PNG con los que calibramos el motor (muros, agua, luz, techo, terreno). Vista previa del de muros:
              </p>
              <img
                className="sample-thumb"
                src={`${window.location.origin}/plano-muestra-muros.png?v=${PLANO_MUESTRA_VER}`}
                alt="Vista previa plano de referencia muros"
              />
              <button type="button" className="nav-btn" disabled={loading === 'muros'} onClick={() => cargarPlanoMuestra('muros', true)}>
                {loading === 'muros' ? 'Procesando muestra...' : 'Probar ejemplo: muros'}
              </button>
              <small className="auth-help">
                En cada modulo abajo tenes el mismo plano de ejemplo acorde al tipo (M, A, E, T, L). Si ves una imagen vieja, Ctrl+F5.
              </small>
            </div>

            <div className="module-grid">
              {modulos.map((modulo) => (
                <div className="modulo-card" key={modulo.tipo}>
                  <div className="card-header">
                    <span className="module-icon" aria-hidden>
                      <ModuleIconSvg tipo={modulo.tipo} />
                    </span>
                    <div>
                      <h3>{modulo.titulo}</h3>
                      <p>Procesamiento puntual, sin guardar en tu estudio.</p>
                    </div>
                  </div>
                  <label className="custom-file-upload">
                    <input disabled={loading === modulo.tipo} type="file" accept="image/png,image/jpeg,image/webp" onChange={(e) => subirPlanoDemo(e.target.files[0], modulo.tipo)} />
                    {loading === modulo.tipo ? 'Procesando...' : 'Cargar plano'}
                  </label>
                  <button
                    type="button"
                    className="nav-btn sample-modulo-btn"
                    disabled={loading === modulo.tipo}
                    onClick={() => cargarPlanoMuestra(modulo.tipo, true)}
                  >
                    Plano ejemplo ({modulo.icono})
                  </button>
                </div>
              ))}
            </div>

            {demoRuns.length === 0 && (
              <div className="empty-state">
                <h2>Todavia no procesaste ningun plano</h2>
                <p>Usá la checklist a la izquierda y subi una imagen en cualquier modulo para ver desglose, total e imagen auditada.</p>
              </div>
            )}

            {demoRuns.length > 0 && (
              <>
                <div className="total-band">
                  <span>Total acumulado (solo visual, esta sesion)</span>
                  <strong>{formatoMoneda(demoGranTotal)}</strong>
                </div>
                <div className="history-list">
                  <h2>Resultados de prueba</h2>
                  {demoRuns.map((run) => (
                    <article className="history-card" key={run.id}>
                      <div className="history-meta">
                        <div>
                          <h3>{run.filename}</h3>
                          <p>{run.tipo} — analisis local de demostracion</p>
                          {run.meta?.escala_modo && (
                            <p className="escala-modo-pill">Escala: {run.meta.escala_modo === 'ocr' ? 'OCR sobre verde' : run.meta.escala_modo === 'manual' ? 'Manual (sin OCR)' : 'Sin linea verde'}</p>
                          )}
                        </div>
                        <div className="history-meta-aside">
                          {run.tipo !== 'terreno' && <strong>{formatoMoneda(run.total)}</strong>}
                          <button type="button" className="nav-btn history-quitar-btn" onClick={() => eliminarDemoRun(run.id)}>
                            Quitar
                          </button>
                        </div>
                      </div>
                      {(run.meta?.avisos || []).length > 0 && (
                        <div className="meta-avisos">
                          {(run.meta.avisos || []).map((a, i) => (
                            <p key={i}>{a}</p>
                          ))}
                        </div>
                      )}
                      <div className="desglose-list">
                        {(run.items || []).map((item, index) => (
                          <div key={index} className="desglose-item">
                            <div>
                              <span>{item.nom}</span>
                              {item.origen && <small className="item-origen">{item.origen}</small>}
                            </div>
                            <span className="precio-val">{run.tipo === 'terreno' ? item.val : formatoMoneda(item.val)}</span>
                          </div>
                        ))}
                      </div>
                      {run.imagen && <img className="img-audit" src={`data:image/png;base64,${run.imagen}`} alt="Auditoria visual" />}
                    </article>
                  ))}
                </div>
              </>
            )}
          </section>
        </main>
      </div>
    );
  }

  if (!token) {
    return (
      <div className="auth-page" style={{ backgroundImage: `linear-gradient(rgba(8,8,8,.78), rgba(8,8,8,.95)), url(${bannerFondo})` }}>
        <div className="auth-shell">
          <img src="/logo.png" alt={SITE_NAME} className="auth-logo" />
          <div>
            <span className="eyebrow">SaaS para estudios de arquitectura</span>
            <h1>{SITE_NAME}</h1>
            <p>Computo de obra, terrenos e instalaciones con auditoria visual, historial por proyecto y exportacion.</p>
            <div className="auth-points">
              <span>Historial por obra</span>
              <span>Reportes exportables</span>
              <span>Control por estudio</span>
            </div>
          </div>
        </div>

        <div className="auth-right-column">
        {inviteLoading && (
          <div className="auth-card">
            <span className="eyebrow">Invitacion</span>
            <h2>Verificando enlace...</h2>
            <p className="auth-help">Un momento mientras validamos la invitacion.</p>
          </div>
        )}
        {!inviteLoading && inviteInfo && (
          <form className="auth-card" onSubmit={submitInviteRegister}>
            <div>
              <span className="eyebrow">Invitacion al estudio</span>
              <h2>Unite a {inviteInfo.studioName}</h2>
              <p className="auth-help">
                Vas a ingresar como <strong>{inviteInfo.email}</strong>
                {inviteInfo.role === 'viewer' ? ' (solo lectura)' : ' (editor)'}.
              </p>
            </div>
            <input placeholder="Tu nombre" value={authForm.name} onChange={(e) => setAuthForm({ ...authForm, name: e.target.value })} />
            <input type="password" placeholder="Elegi una clave (min. 8 caracteres)" value={authForm.password} onChange={(e) => setAuthForm({ ...authForm, password: e.target.value })} />
            {error && <div className="error-box">{error}</div>}
            <button className="primary-btn" disabled={loading === 'auth'}>
              {loading === 'auth' ? 'Creando cuenta...' : 'Aceptar invitacion'}
            </button>
            <button type="button" className="ghost-btn" disabled={loading === 'auth'} onClick={salirDeFlujoInvitacion}>
              Cancelar y usar otra cuenta
            </button>
          </form>
        )}
        {!inviteLoading && !inviteInfo && (
        <form className="auth-card" onSubmit={submitAuth}>
          <div>
            <span className="eyebrow">Acceso privado</span>
            <h2>
              {authMode === 'login' && 'Ingresar al estudio'}
              {authMode === 'register' && 'Crear un estudio'}
              {authMode === 'forgot' && 'Recuperar clave'}
              {authMode === 'reset' && 'Nueva clave'}
            </h2>
          </div>
          {(authMode === 'login' || authMode === 'register') && (
            <div className="segmented">
              <button type="button" className={authMode === 'login' ? 'active' : ''} onClick={() => { setAuthMode('login'); setError(''); setAuthNotice(''); }}>
                Ingresar
              </button>
              <button type="button" className={authMode === 'register' ? 'active' : ''} onClick={() => { setAuthMode('register'); setError(''); setAuthNotice(''); }}>
                Crear estudio
              </button>
            </div>
          )}

          {authMode === 'login' && <small className="auth-help">Si no tenes cuenta todavia, primero crea tu usuario en "Crear estudio".</small>}
          {authMode === 'forgot' && <small className="auth-help">Te enviamos un enlace al email para elegir una clave nueva.</small>}
          {authMode === 'reset' && <small className="auth-help">Minimo 8 caracteres.</small>}

          {authMode === 'register' && (
            <>
              <input placeholder="Nombre del estudio" value={authForm.studio_name} onChange={(e) => setAuthForm({ ...authForm, studio_name: e.target.value })} />
              <input placeholder="Tu nombre" value={authForm.name} onChange={(e) => setAuthForm({ ...authForm, name: e.target.value })} />
            </>
          )}
          {(authMode === 'login' || authMode === 'register' || authMode === 'forgot') && (
            <input type="email" placeholder="Email" value={authForm.email} onChange={(e) => setAuthForm({ ...authForm, email: e.target.value })} />
          )}
          {(authMode === 'login' || authMode === 'register' || authMode === 'reset') && (
            <input
              type="password"
              placeholder={authMode === 'reset' ? 'Nueva clave (min. 8)' : 'Clave'}
              value={authForm.password}
              onChange={(e) => setAuthForm({ ...authForm, password: e.target.value })}
            />
          )}
          {authMode === 'login' && (
            <button
              type="button"
              className="link-btn"
              disabled={loading === 'auth'}
              onClick={() => { setAuthMode('forgot'); setError(''); setAuthNotice(''); }}
            >
              ¿Olvidaste tu clave?
            </button>
          )}
          {authNotice && <div className="auth-help" style={{ color: '#d4af37' }}>{authNotice}</div>}
          {error && <div className="error-box">{error}</div>}
          <button className="primary-btn" disabled={loading === 'auth'}>
            {loading === 'auth'
              ? 'Procesando...'
              : authMode === 'login'
                ? 'Entrar'
                : authMode === 'register'
                  ? 'Crear cuenta'
                  : authMode === 'forgot'
                    ? 'Enviar enlace'
                    : 'Guardar clave'}
          </button>
          {(authMode === 'login' || authMode === 'register') && (
            <button type="button" className="link-btn" onClick={() => setMostrarPlanes(true)}>
              Ver planes Free vs Pro
            </button>
          )}
          {mostrarPlanes && !token && (
            <PlansPanel
              onClose={() => setMostrarPlanes(false)}
              billing={billingPublic || {}}
              canSubscribe={false}
            />
          )}
          {(authMode === 'forgot' || authMode === 'reset') && (
            <button
              type="button"
              className="ghost-btn"
              disabled={loading === 'auth'}
              onClick={() => { clearResetQuery(); setAuthMode('login'); setError(''); setAuthNotice(''); }}
            >
              Volver a ingresar
            </button>
          )}
          {(authMode === 'login' || authMode === 'register') && (
            <>
              <button
                type="button"
                className="ghost-btn"
                disabled={loading === 'auth'}
                onClick={() => {
                  setDemoMode(true);
                  setLastDemoUpload(null);
                  setError('');
                  setMostrarGuia(false);
                }}
              >
                Probar sin cuenta
              </button>
              <small className="auth-help">En modo prueba podes subir planos con el motor real; no se guardan en tu estudio.</small>
            </>
          )}
        </form>
        )}
        <div className="precios-bar auth-precios">{preciosInfo ? textoLineaPrecios(preciosInfo) : 'Precios: conectando...'}</div>
        </div>
      </div>
    );
  }

  const ultimoPlanoObra = activeProjectId ? lastUploadByProject[String(activeProjectId)] : null;
  const compareLeft = processes.find((p) => p.id === compareIds[0]);
  const compareRight = processes.find((p) => p.id === compareIds[1]);
  const billingForPlans = billingPublic || me?.billing || {};

  return (
    <div className="App">
      <header className="topbar" style={{ backgroundImage: `linear-gradient(to bottom, rgba(10,10,10,0.82), rgba(10,10,10,0.98)), url(${bannerFondo})` }}>
        <div className="brand-block">
          <img src="/logo.png" alt={SITE_NAME} className="logo-img" />
          <div>
            <h1>{SITE_NAME}</h1>
            <p>{me?.studio?.name || 'Estudio'}</p>
          </div>
        </div>
        <button
          type="button"
          className={`nav-btn mobile-menu-btn${mobileNavOpen ? ' nav-btn--active' : ''}`}
          aria-expanded={mobileNavOpen}
          aria-controls="top-actions-menu"
          onClick={() => setMobileNavOpen((v) => !v)}
        >
          {mobileNavOpen ? 'Cerrar' : 'Menu'}
        </button>
        <div id="top-actions-menu" className={`top-actions${mobileNavOpen ? ' is-open' : ''}`}>
          <div className="usage-pill">
            {me?.studio?.used_this_month || 0}/{me?.studio?.monthly_limit || 0} planos
          </div>
          <div className="plan-pill">{planStatus}</div>
          <a className="nav-btn" href="/plantilla-paleta-arq-ia.svg" download="plantilla-paleta-arq-ia.svg">
            Paleta SVG
          </a>
          <button type="button" className={`nav-btn${mostrarGuia ? ' nav-btn--active' : ''}`} onClick={() => setMostrarGuia(!mostrarGuia)}>
            {mostrarGuia ? 'Cerrar guia' : 'Guia'}
          </button>
          <button type="button" className={`nav-btn${mostrarPlanes ? ' nav-btn--active' : ''}`} onClick={() => setMostrarPlanes(true)}>
            Planes
          </button>
          {canManageBilling && (
            isPro ? (
              <button
                className="nav-btn"
                onClick={cancelarSuscripcion}
                disabled={loading === 'billing-cancel'}
                title="Cancelar cobro recurrente en Mercado Pago"
              >
                {loading === 'billing-cancel' ? 'Cancelando...' : 'Cancelar plan'}
              </button>
            ) : (
              <button
                className="nav-btn"
                onClick={abrirCheckout}
                disabled={loading === 'billing'}
                title="Pagar con Mercado Pago (ARS)"
              >
                {loading === 'billing' ? 'Redirigiendo...' : 'Pasar a Pro'}
              </button>
            )
          )}
          {SUPPORT_WA_HREF && (
            <a className="nav-btn" href={SUPPORT_WA_HREF} target="_blank" rel="noreferrer">
              Soporte
            </a>
          )}
          <button className="nav-btn" onClick={logout}>Salir</button>
        </div>
      </header>
      <div className="precios-bar">{preciosInfo ? textoLineaPrecios(preciosInfo) : 'Precios: conectando...'}</div>

      {mostrarGuia && <ColorGuidePanel onClose={() => setMostrarGuia(false)} />}
      {mostrarPlanes && (
        <PlansPanel
          onClose={() => setMostrarPlanes(false)}
          billing={billingForPlans}
          canSubscribe={canManageBilling && me?.studio?.plan_status !== 'active'}
          loadingBilling={loading === 'billing'}
          onSubscribe={() => {
            setMostrarPlanes(false);
            abrirCheckout();
          }}
        />
      )}
      {mostrarCompare && compareLeft && compareRight && (
        <ComparePanel left={compareLeft} right={compareRight} onClose={() => setMostrarCompare(false)} />
      )}

      <main className="workspace">
        <aside className="sidebar">
          {canEdit ? (
            <form className="project-form" onSubmit={createProject}>
              <span className="eyebrow">Gestion</span>
              <h2>Nueva obra</h2>
              <input placeholder="Nombre de obra" value={projectForm.name} onChange={(e) => setProjectForm({ ...projectForm, name: e.target.value })} />
              <input placeholder="Cliente" value={projectForm.client} onChange={(e) => setProjectForm({ ...projectForm, client: e.target.value })} />
              <input placeholder="Direccion" value={projectForm.address} onChange={(e) => setProjectForm({ ...projectForm, address: e.target.value })} />
              <button className="primary-btn" disabled={loading === 'project'}>
                {loading === 'project' ? 'Creando...' : 'Crear obra'}
              </button>
            </form>
          ) : (
            <div className="onboarding-card">
              <span className="eyebrow">Solo lectura</span>
              <h2>Modo viewer</h2>
              <p className="onboarding-lead">
                Podes ver obras, historial y exportar. Para subir planos o crear obras, pedile al dueño rol editor.
              </p>
            </div>
          )}

          <div className="project-list">
            <div className="section-label">
              <span className="eyebrow">Workspace</span>
              <h2>Obras</h2>
            </div>
            {projects.map((project) => (
              <button
                key={project.id}
                className={String(project.id) === String(activeProjectId) ? 'project-item active' : 'project-item'}
                onClick={() => setActiveProjectId(String(project.id))}
              >
                <span>{project.name}</span>
                <small>{project.process_count} analisis</small>
              </button>
            ))}
            {projects.length === 0 && <p className="empty-text">Crea una obra para empezar a guardar historial.</p>}
          </div>

          <div className="onboarding-card equipo-card">
            <span className="eyebrow">Equipo</span>
            <h2>Invitaciones</h2>
            {me?.can_manage_invites ? (
              <>
                <p className="onboarding-lead">
                  Invita por email con rol editor o solo lectura. Si Resend esta configurado, el colega recibe el enlace automaticamente.
                </p>
                <form className="invite-form" onSubmit={crearInvitacion}>
                  <input
                    type="email"
                    placeholder="Email del colega"
                    value={inviteForm.email}
                    onChange={(e) => setInviteForm({ ...inviteForm, email: e.target.value })}
                  />
                  <select value={inviteForm.role} onChange={(e) => setInviteForm({ ...inviteForm, role: e.target.value })}>
                    <option value="editor">Editor</option>
                    <option value="viewer">Solo lectura</option>
                  </select>
                  <button type="submit" className="primary-btn" disabled={loading === 'invite'}>
                    {loading === 'invite' ? 'Enviando...' : 'Invitar por email'}
                  </button>
                </form>
                {lastInviteUrl && (
                  <div className="invite-url-box">
                    <p className="auth-help">
                      {lastInviteEmailSent
                        ? 'Email enviado. Tambien podes copiar el enlace:'
                        : 'Enlace (copialo si el email no salio):'}
                    </p>
                    <code className="invite-url-code">{lastInviteUrl}</code>
                    <button type="button" className="nav-btn" onClick={() => copiarTexto(lastInviteUrl)}>
                      Copiar enlace
                    </button>
                  </div>
                )}
                <ul className="invite-list">
                  {invitations.map((inv) => (
                    <li key={inv.id} className="invite-list-item">
                      <div>
                        <strong>{inv.email}</strong>
                        <small>
                          {' '}
                          · {inv.role === 'viewer' ? 'Solo lectura' : 'Editor'}
                          {inv.accepted ? ' · aceptada' : ' · pendiente'}
                        </small>
                      </div>
                      {!inv.accepted && (
                        <button type="button" className="nav-btn" onClick={() => revocarInvitacion(inv.id)}>
                          Revocar
                        </button>
                      )}
                    </li>
                  ))}
                </ul>
                {invitations.length === 0 && <p className="empty-text">Todavia no hay invitaciones.</p>}
              </>
            ) : (
              <p className="onboarding-lead">
                Solo el dueño del estudio puede enviar invitaciones. Tu rol actual: <strong>{me?.role || '—'}</strong>.
              </p>
            )}
          </div>
        </aside>

          <section className="main-panel">
          {error && <div className="error-box">{error}</div>}

          {!hasActiveObra ? (
            <div className="empty-state empty-state--hero">
              <span className="eyebrow">Workspace listo</span>
              <h2>Primero crea o selecciona una obra</h2>
              <p>
                Sin una obra activa no se muestran modulos, carga de planos ni exportacion.
                Usa el formulario de la izquierda: nombre, cliente y direccion.
              </p>
              <ul className="empty-hero-points">
                <li>Free: muros y terrenos</li>
                <li>Pro: agua/gas, electricidad y techos</li>
                <li>Cada plano queda guardado en el historial de la obra</li>
              </ul>
              {!isPro && canManageBilling && (
                <button type="button" className="primary-btn" onClick={() => setMostrarPlanes(true)}>
                  Ver Plan Pro
                </button>
              )}
            </div>
          ) : (
            <>
            <div className="panel-header panel-header--split">
              <div>
                <span className="eyebrow">Panel de computo</span>
                <h2>{activeProject?.name || 'Obra'}</h2>
                <p>{activeProject?.client || activeProject?.address || 'Los planos procesados quedan guardados dentro de la obra.'}</p>
              </div>
              <div className="panel-header-aside">
                <ScalePanel
                  ultimo={lastProcess}
                  onAplicarManual={
                    canEdit && ultimoPlanoObra ? () => subirPlano(ultimoPlanoObra.file, ultimoPlanoObra.tipo) : null
                  }
                />
                {canEdit && <ComputeOptionsPanel />}
                <div className="panel-toolbar">
                  <button className="nav-btn" disabled={processes.length === 0} onClick={exportarCsv}>
                    Exportar CSV
                  </button>
                  <button className="nav-btn" disabled={processes.length === 0} onClick={exportarPdf}>
                    Exportar PDF
                  </button>
                  <button
                    className="nav-btn"
                    disabled={compareIds.length !== 2}
                    onClick={() => setMostrarCompare(true)}
                    title="Elegi 2 analisis del historial"
                  >
                    Comparar ({compareIds.length}/2)
                  </button>
                  {canEdit && (
                    <button className="nav-btn" onClick={eliminarObra}>
                      Eliminar obra
                    </button>
                  )}
                </div>
              </div>
            </div>

          {canEdit && (
            <form className="edit-project-form" onSubmit={updateProject}>
              <div className="edit-project-head">
                <span className="eyebrow">Obra seleccionada</span>
                <h3>Editar datos</h3>
              </div>
              <div className="edit-project-grid">
                <input
                  placeholder="Nombre de obra"
                  value={editProjectForm.name}
                  onChange={(e) => setEditProjectForm({ ...editProjectForm, name: e.target.value })}
                />
                <input
                  placeholder="Cliente"
                  value={editProjectForm.client}
                  onChange={(e) => setEditProjectForm({ ...editProjectForm, client: e.target.value })}
                />
                <input
                  placeholder="Direccion"
                  value={editProjectForm.address}
                  onChange={(e) => setEditProjectForm({ ...editProjectForm, address: e.target.value })}
                />
                <button className="primary-btn" disabled={loading === 'project-edit'}>
                  {loading === 'project-edit' ? 'Guardando...' : 'Guardar cambios'}
                </button>
              </div>
            </form>
          )}

          <div className="kpi-grid">
            <div className="kpi-card">
              <span>Total estimado</span>
              <strong>{formatoMoneda(granTotal)}</strong>
            </div>
            <div className="kpi-card">
              <span>Analisis guardados</span>
              <strong>{processes.length}</strong>
            </div>
            <div className="kpi-card">
              <span>Ultimo modulo</span>
              <strong>{lastProcess?.tipo || 'Sin datos'}</strong>
            </div>
            <div className="kpi-card">
              <span>Uso mensual</span>
              <strong>{me?.studio?.used_this_month || 0}/{me?.studio?.monthly_limit || 0}</strong>
            </div>
          </div>

          {!workspaceOnboardingHecho && (
            <div className="onboarding-card workspace-onboarding">
              <div className="onboarding-card-head">
                <div>
                  <span className="eyebrow">Primera obra en este workspace</span>
                  <h2>Checklist guiada</h2>
                  <p className="onboarding-lead">Segui estos pasos la primera vez; despues lo ocultas con un clic.</p>
                </div>
                <button type="button" className="nav-btn" onClick={cerrarOnboardingWorkspace}>
                  No volver a mostrar
                </button>
              </div>
              <ol className="onboarding-steps">
                <li className="done">
                  <span className="step-title">Obra seleccionada</span>
                  <small>Crea una obra en la barra lateral o elegi una existente.</small>
                </li>
                <li className={processes.length > 0 ? 'done' : ''}>
                  <span className="step-title">Escala y primer plano</span>
                  <small>Linea verde fluor + numero en el plano, o ajusta escala manual. Subi PNG/JPG/WebP en el modulo que corresponda.</small>
                </li>
                <li className={processes.length > 0 ? 'done' : ''}>
                  <span className="step-title">Revisa auditoria visual</span>
                  <small>En el historial verifica mascaras y totales antes de comprometer presupuesto.</small>
                </li>
                <li className={exportasteCsv ? 'done' : ''}>
                  <span className="step-title">Exporta CSV (opcional)</span>
                  <small>Comparti desglose con cliente u homologacion interna.</small>
                </li>
              </ol>
              <a className="link-inline" href="/plantilla-paleta-arq-ia.svg" download="plantilla-paleta-arq-ia.svg">
                Descargar plantilla de colores (SVG)
              </a>
            </div>
          )}

          {(me?.studio?.used_this_month || 0) >= Math.floor((me?.studio?.monthly_limit || 1) * 0.8) && (
            <div className="error-box">
              Estas usando mas del 80% del plan mensual. Considera actualizar tu suscripcion para no frenar el flujo.
            </div>
          )}

          {!isPro && (
            <div className="premium-banner">
              <div>
                <span className="eyebrow">Plan Free</span>
                <strong>Desbloquea agua, electricidad y techos con Pro</strong>
                <p>Muros y terrenos estan incluidos. El resto requiere suscripcion Mercado Pago.</p>
              </div>
              {canManageBilling && (
                <button type="button" className="primary-btn" onClick={abrirCheckout} disabled={loading === 'billing'}>
                  {loading === 'billing' ? 'Redirigiendo...' : 'Pasar a Pro'}
                </button>
              )}
            </div>
          )}

          {canEdit ? (
            <div className="module-grid">
              {modulos.map((modulo) => {
                const locked = moduloBloqueado(modulo.tipo);
                return (
                  <div className={`modulo-card${locked ? ' is-locked' : ''}`} key={modulo.tipo}>
                    <div className="card-header">
                      <span className="module-icon" aria-hidden>
                        <ModuleIconSvg tipo={modulo.tipo} />
                      </span>
                      <div>
                        <h3>
                          {modulo.titulo}
                          {locked && <span className="pro-badge">Pro</span>}
                        </h3>
                        <p>{locked ? 'Incluido en Plan Pro.' : 'Procesa y guarda el resultado en esta obra.'}</p>
                      </div>
                    </div>
                    {locked ? (
                      <button type="button" className="nav-btn" onClick={() => (canManageBilling ? abrirCheckout() : setMostrarPlanes(true))}>
                        Desbloquear con Pro
                      </button>
                    ) : (
                      <>
                        <label className="custom-file-upload">
                          <input
                            disabled={loading === modulo.tipo}
                            type="file"
                            accept="image/png,image/jpeg,image/webp"
                            onChange={(e) => subirPlano(e.target.files[0], modulo.tipo)}
                          />
                          {loading === modulo.tipo ? 'Procesando...' : 'Cargar plano'}
                        </label>
                        <button
                          type="button"
                          className="nav-btn sample-modulo-btn"
                          disabled={loading === modulo.tipo}
                          onClick={() => cargarPlanoMuestra(modulo.tipo, false)}
                        >
                          Plano ejemplo ({modulo.icono})
                        </button>
                      </>
                    )}
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="empty-state">
              <h2>Vista de solo lectura</h2>
              <p>Revisa el historial y exporta CSV/PDF. Las cargas estan deshabilitadas para tu rol.</p>
            </div>
          )}

          {canEdit && (
            <div className="sample-actions">
              <span className="eyebrow">Planos de referencia</span>
              <p className="sample-preview-caption">Los mismos PNG de calibracion que en la demo; se guardan como analisis en esta obra.</p>
              <div className="sample-multi-actions">
                {modulos.map((m) => (
                  <button
                    key={m.tipo}
                    type="button"
                    className="nav-btn sample-chip"
                    title={moduloBloqueado(m.tipo) ? `${m.titulo} (Pro)` : m.titulo}
                    disabled={loading === m.tipo || moduloBloqueado(m.tipo)}
                    onClick={() => cargarPlanoMuestra(m.tipo, false)}
                  >
                    {loading === m.tipo ? '...' : m.icono}
                  </button>
                ))}
              </div>
              <small className="auth-help">M = muros · A = agua · E = electricidad · T = techo · L = terreno</small>
            </div>
          )}

          {processes.length === 0 && (
            <div className="empty-state">
              <h2>Carga el primer plano de esta obra</h2>
              <p>El sistema guardara cada procesamiento con su desglose, total, escala detectada e imagen auditada.</p>
            </div>
          )}

          {processes.length > 0 && (
            <>
              <div className="total-band">
                <span>Inversion total obra</span>
                <strong>{formatoMoneda(granTotal)}</strong>
              </div>

              <div className="history-list">
                <div className="history-list-head">
                  <h2>Historial guardado</h2>
                  <small className="auth-help">Marca hasta 2 analisis y usa Comparar.</small>
                </div>
                {processes.map((process) => (
                  <article className={`history-card${compareIds.includes(process.id) ? ' is-compare' : ''}`} key={process.id}>
                    <div className="history-meta">
                      <div>
                        <label className="compare-check">
                          <input
                            type="checkbox"
                            checked={compareIds.includes(process.id)}
                            onChange={() => toggleCompare(process.id)}
                          />
                          Comparar
                        </label>
                        <h3>{process.filename}</h3>
                        <p>{process.tipo} - {new Date(process.created_at).toLocaleString('es-AR')}</p>
                        {process.meta?.escala_modo && (
                          <p className="escala-modo-pill">
                            Escala: {process.meta.escala_modo === 'ocr' ? 'OCR sobre verde' : process.meta.escala_modo === 'manual' ? 'Manual (sin OCR)' : 'Sin linea verde'}
                          </p>
                        )}
                        {(process.meta?.sistema_muro || process.meta?.altura_muro) && process.tipo === 'muros' && (
                          <p className="escala-modo-pill">
                            Muro: {process.meta.sistema_muro === 'ladrillo_comun_12' ? 'comun 12' : 'hueco 12'}
                            {process.meta.altura_muro != null ? ` · ${Number(process.meta.altura_muro).toFixed(2)} m` : ''}
                          </p>
                        )}
                      </div>
                      {process.tipo !== 'terreno' && <strong>{formatoMoneda(process.total)}</strong>}
                    </div>
                    {(process.meta?.avisos || []).length > 0 && (
                      <div className="meta-avisos">
                        {(process.meta.avisos || []).map((a, i) => (
                          <p key={i}>{a}</p>
                        ))}
                      </div>
                    )}
                    <div className="desglose-list">
                      {process.items.map((item, index) => (
                        <div key={index} className="desglose-item">
                          <div>
                            <span>{item.nom}</span>
                            {item.origen && <small className="item-origen">{item.origen}</small>}
                          </div>
                          <span className="precio-val">{process.tipo === 'terreno' ? item.val : formatoMoneda(item.val)}</span>
                        </div>
                      ))}
                    </div>
                    {canEdit && (
                      <button className="nav-btn" onClick={() => eliminarAnalisis(process.id)}>
                        Eliminar analisis
                      </button>
                    )}
                    <img className="img-audit" src={`data:image/png;base64,${process.imagen}`} alt="Auditoria visual" />
                  </article>
                ))}
              </div>
            </>
          )}
            </>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
