import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import './App.css';
import bannerFondo from './banner-fondo.png';

const DEFAULT_API_URL =
  window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : `https://api.${window.location.hostname.replace(/^www\./, '')}`;
const ENV_API_URL = (process.env.REACT_APP_API_URL || '').trim();
// Siempre usar la URL configurada en build (p. ej. backend en Render). Forzar
// api.{dominio} solo cuando no hay variable de entorno (subdominio propio).
const API_URL = (ENV_API_URL || DEFAULT_API_URL).replace(/\/+$/, '');

/** Subir al cambiar la imagen de muestra en public/ (invalida cache CDN). */
const PLANO_MUESTRA_VER = '5';

const SITE_NAME = (process.env.REACT_APP_SITE_NAME || 'ARC-IA').trim();
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
  { tipo: 'muros', titulo: 'Estructura y terminaciones', icono: 'M' },
  { tipo: 'agua', titulo: 'Instalacion sanitaria y gas', icono: 'A' },
  { tipo: 'luz', titulo: 'Instalacion electrica', icono: 'E' },
  { tipo: 'techo', titulo: 'Techos y losas', icono: 'T' },
  { tipo: 'terreno', titulo: 'Medicion de terrenos y lotes', icono: 'L' },
];

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

function ColorGuidePanel({ onClose }) {
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

function App() {
  const [token, setToken] = useState(() => localStorage.getItem('arqia_token') || '');
  const [authMode, setAuthMode] = useState('login');
  const [authForm, setAuthForm] = useState({
    studio_name: '',
    name: '',
    email: '',
    password: '',
  });
  const [me, setMe] = useState(null);
  const [projects, setProjects] = useState([]);
  const [activeProjectId, setActiveProjectId] = useState(() => localStorage.getItem('arqia_project_id') || '');
  const [processes, setProcesses] = useState([]);
  const [projectForm, setProjectForm] = useState({ name: '', client: '', address: '' });
  const [referencia, setReferencia] = useState(1);
  const [mostrarGuia, setMostrarGuia] = useState(false);
  const [loading, setLoading] = useState('');
  const [error, setError] = useState('');
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
  const granTotal = processes
    .filter((process) => process.tipo !== 'terreno')
    .reduce((acc, process) => acc + Number(process.total || 0), 0);
  const lastProcess = processes[0];
  const planStatus = me?.studio?.plan_status === 'active' ? 'Plan activo' : 'Plan inicial';

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
  }, [token, demoMode]);

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

  const submitAuth = async (event) => {
    event.preventDefault();
    setError('');

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

  const subirPlanoDemo = async (archivo, tipo) => {
    if (!archivo) return;
    const formData = new FormData();
    formData.append('file', archivo);
    formData.append('referencia_metros', referencia);
    formData.append('tipo_plano', tipo);

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
    try {
      const r = await fetch(`${window.location.origin}/plano-muestra.png?v=${PLANO_MUESTRA_VER}`, { cache: 'no-store' });
      if (!r.ok) throw new Error('missing');
      const blob = await r.blob();
      const f = new File([blob], 'plano-muestra.png', { type: 'image/png' });
      if (enDemo) await subirPlanoDemo(f, tipo);
      else await subirPlano(f, tipo);
    } catch (err) {
      setError('No se encontro plano-muestra.png en el sitio. Volvé a desplegar el frontend con el archivo en public/.');
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
    const formData = new FormData();
    formData.append('file', archivo);
    formData.append('referencia_metros', referencia);
    formData.append('tipo_plano', tipo);

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
      setError(getErrorMessage(err, 'Stripe todavia no esta configurado.'));
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
    try {
      const res = await api.post('/studio/invitations', {
        email: inviteForm.email.trim(),
        role: inviteForm.role,
      });
      setLastInviteUrl(res.data.invite_url || '');
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
            </div>

            <div className="sample-actions">
              <span className="eyebrow">Plano de muestra</span>
              <p className="sample-preview-caption">
                Mini plano de referencia (no es una obra real). Verde = escala, negro = metros, rojo = muros, gris = piso.
              </p>
              <img
                className="sample-thumb"
                src={`${window.location.origin}/plano-muestra.png?v=${PLANO_MUESTRA_VER}`}
                alt="Vista previa del plano de muestra ARC-IA"
              />
              <button type="button" className="nav-btn" disabled={loading === 'muros'} onClick={() => cargarPlanoMuestra('muros', true)}>
                {loading === 'muros' ? 'Procesando muestra...' : 'Probar plano de muestra (Muros)'}
              </button>
              <small className="auth-help">
                Si el total no cambia, forzá recarga del sitio (Ctrl+F5): a veces el CDN sirve una imagen vieja en cache.
              </small>
            </div>

            <div className="module-grid">
              {modulos.map((modulo) => (
                <div className="modulo-card" key={modulo.tipo}>
                  <div className="card-header">
                    <span className="module-icon">{modulo.icono}</span>
                    <div>
                      <h3>{modulo.titulo}</h3>
                      <p>Procesamiento puntual, sin guardar en tu estudio.</p>
                    </div>
                  </div>
                  <label className="custom-file-upload">
                    <input disabled={loading === modulo.tipo} type="file" accept="image/png,image/jpeg,image/webp" onChange={(e) => subirPlanoDemo(e.target.files[0], modulo.tipo)} />
                    {loading === modulo.tipo ? 'Procesando...' : 'Cargar plano'}
                  </label>
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
            <h2>{authMode === 'login' ? 'Ingresar al estudio' : 'Crear un estudio'}</h2>
          </div>
          <div className="segmented">
            <button type="button" className={authMode === 'login' ? 'active' : ''} onClick={() => { setAuthMode('login'); setError(''); }}>
              Ingresar
            </button>
            <button type="button" className={authMode === 'register' ? 'active' : ''} onClick={() => { setAuthMode('register'); setError(''); }}>
              Crear estudio
            </button>
          </div>

          {authMode === 'login' && <small className="auth-help">Si no tenes cuenta todavia, primero crea tu usuario en "Crear estudio".</small>}

          {authMode === 'register' && (
            <>
              <input placeholder="Nombre del estudio" value={authForm.studio_name} onChange={(e) => setAuthForm({ ...authForm, studio_name: e.target.value })} />
              <input placeholder="Tu nombre" value={authForm.name} onChange={(e) => setAuthForm({ ...authForm, name: e.target.value })} />
            </>
          )}
          <input type="email" placeholder="Email" value={authForm.email} onChange={(e) => setAuthForm({ ...authForm, email: e.target.value })} />
          <input type="password" placeholder="Clave" value={authForm.password} onChange={(e) => setAuthForm({ ...authForm, password: e.target.value })} />
          {error && <div className="error-box">{error}</div>}
          <button className="primary-btn" disabled={loading === 'auth'}>
            {loading === 'auth' ? 'Procesando...' : authMode === 'login' ? 'Entrar' : 'Crear cuenta'}
          </button>
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
        </form>
        )}
        <div className="precios-bar auth-precios">{preciosInfo ? textoLineaPrecios(preciosInfo) : 'Precios: conectando...'}</div>
        </div>
      </div>
    );
  }

  const ultimoPlanoObra = activeProjectId ? lastUploadByProject[String(activeProjectId)] : null;

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
        <div className="top-actions">
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
          <button className="nav-btn" onClick={abrirCheckout} disabled={loading === 'billing'}>
            Suscripcion
          </button>
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

      <main className="workspace">
        <aside className="sidebar">
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
                  Invita por email con rol editor o solo lectura. La persona abre el enlace, elige clave y entra a este estudio.
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
                    {loading === 'invite' ? 'Creando...' : 'Crear invitacion'}
                  </button>
                </form>
                {lastInviteUrl && (
                  <div className="invite-url-box">
                    <p className="auth-help">Enlace (copialo y envialo por el canal que uses):</p>
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
            <div className="panel-header panel-header--split">
              <div>
                <span className="eyebrow">Panel de computo</span>
                <h2>{activeProject?.name || 'Selecciona una obra'}</h2>
                <p>{activeProject?.client || 'Los planos procesados quedan guardados dentro de la obra.'}</p>
              </div>
              <div className="panel-header-aside">
                <ScalePanel
                  ultimo={lastProcess}
                  onAplicarManual={ultimoPlanoObra ? () => subirPlano(ultimoPlanoObra.file, ultimoPlanoObra.tipo) : null}
                />
                <div className="panel-toolbar">
                  <button className="nav-btn" disabled={!activeProjectId || processes.length === 0} onClick={exportarCsv}>
                    Exportar CSV
                  </button>
                  <button className="nav-btn" disabled={!activeProjectId || processes.length === 0} onClick={exportarPdf}>
                    Exportar PDF
                  </button>
                  <button className="nav-btn" disabled={!activeProjectId} onClick={eliminarObra}>
                    Eliminar obra
                  </button>
                </div>
              </div>
            </div>

          {error && <div className="error-box">{error}</div>}

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


          {activeProjectId && !workspaceOnboardingHecho && (
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
                <li className={activeProjectId ? 'done' : ''}>
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

          <div className="module-grid">
            {modulos.map((modulo) => (
              <div className="modulo-card" key={modulo.tipo}>
                <div className="card-header">
                  <span className="module-icon">{modulo.icono}</span>
                  <div>
                    <h3>{modulo.titulo}</h3>
                    <p>Procesa y guarda el resultado en esta obra.</p>
                  </div>
                </div>
                <label className={activeProjectId ? 'custom-file-upload' : 'custom-file-upload disabled'}>
                  <input disabled={!activeProjectId || loading === modulo.tipo} type="file" accept="image/png,image/jpeg,image/webp" onChange={(e) => subirPlano(e.target.files[0], modulo.tipo)} />
                  {loading === modulo.tipo ? 'Procesando...' : 'Cargar plano'}
                </label>
              </div>
            ))}
          </div>

          {activeProjectId && (
            <div className="sample-actions">
              <span className="eyebrow">Demo rapida</span>
              <button type="button" className="nav-btn" disabled={loading === 'muros'} onClick={() => cargarPlanoMuestra('muros', false)}>
                {loading === 'muros' ? 'Procesando muestra...' : 'Probar plano de muestra (Muros)'}
              </button>
              <small className="auth-help">Mismo PNG de demostracion; se guarda como un analisis mas en esta obra.</small>
            </div>
          )}

          {processes.length === 0 && (
            <div className="empty-state">
              <h2>{activeProjectId ? 'Carga el primer plano de esta obra' : 'Crea o selecciona una obra'}</h2>
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
                <h2>Historial guardado</h2>
                {processes.map((process) => (
                  <article className="history-card" key={process.id}>
                    <div className="history-meta">
                      <div>
                        <h3>{process.filename}</h3>
                        <p>{process.tipo} - {new Date(process.created_at).toLocaleString('es-AR')}</p>
                        {process.meta?.escala_modo && (
                          <p className="escala-modo-pill">
                            Escala: {process.meta.escala_modo === 'ocr' ? 'OCR sobre verde' : process.meta.escala_modo === 'manual' ? 'Manual (sin OCR)' : 'Sin linea verde'}
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
                    <button className="nav-btn" onClick={() => eliminarAnalisis(process.id)}>Eliminar analisis</button>
                    <img className="img-audit" src={`data:image/png;base64,${process.imagen}`} alt="Auditoria visual" />
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

export default App;
