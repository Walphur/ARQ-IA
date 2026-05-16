import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import './App.css';
import bannerFondo from './banner-fondo.png';

const DEFAULT_API_URL = window.location.hostname === 'localhost' ? 'http://localhost:8000' : `https://api.${window.location.hostname.replace(/^www\./, '')}`;
const ENV_API_URL = (process.env.REACT_APP_API_URL || '').trim();
const useDefaultApi = window.location.hostname !== 'localhost' && ENV_API_URL.includes('.onrender.com');
const API_URL = ((useDefaultApi ? DEFAULT_API_URL : (ENV_API_URL || DEFAULT_API_URL))).replace(/\/+$/, '');

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

const getErrorMessage = (err, fallback, authMode = null) => {
  const detail = String(err?.response?.data?.detail || '').toLowerCase();
  if (authMode === 'login' && (detail.includes('email o clave incorrectos') || err?.response?.status === 401)) {
    return 'No existe una cuenta con esos datos o la clave es incorrecta. Primero crea tu usuario en "Crear estudio".';
  }
  if (err?.response?.data?.detail) return err.response.data.detail;
  if (err?.message === 'Network Error') {
    return 'No se pudo conectar con el servidor. Verifica REACT_APP_API_URL, CORS y que la API este online.';
  }
  return fallback;
};

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
    if (token) {
      setDemoMode(false);
      setDemoRuns([]);
    }
  }, [token]);

  useEffect(() => {
    if (!token) return;
    Promise.all([refreshMe(), refreshProjects()]).catch(() => {
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
      setDemoRuns((prev) => [{ id, filename: archivo.name || 'plano', tipo: data.tipo || tipo, ...data }, ...prev].slice(0, 6));
    } catch (err) {
      setError(getErrorMessage(err, 'No se pudo procesar el plano en modo prueba.'));
    } finally {
      setLoading('');
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
      await Promise.all([refreshProcesses(activeProjectId), refreshMe(), refreshProjects()]);
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
    try {
      await api.delete(`/projects/${activeProjectId}`);
      setActiveProjectId('');
      await Promise.all([refreshProjects(), refreshMe()]);
      setProcesses([]);
    } catch (err) {
      setError(getErrorMessage(err, 'No se pudo eliminar la obra.'));
    }
  };

  const demoGranTotal = demoRuns.filter((r) => r.tipo !== 'terreno').reduce((acc, r) => acc + Number(r.total || 0), 0);
  const demoUltimo = demoRuns[0];

  if (!token && demoMode) {
    return (
      <div className="App demo-app">
        <header className="topbar demo-topbar" style={{ backgroundImage: `linear-gradient(to bottom, rgba(10,10,10,0.82), rgba(10,10,10,0.98)), url(${bannerFondo})` }}>
          <div className="brand-block">
            <img src="/logo.png" alt="ARC-IA" className="logo-img" />
            <div>
              <h1>ARC-IA</h1>
              <p>Modo prueba — no guarda obras ni consume tu cupo</p>
            </div>
          </div>
          <div className="top-actions">
            <button type="button" className="nav-btn" onClick={() => setMostrarGuia(!mostrarGuia)}>Guia de colores</button>
            <button
              type="button"
              className="nav-btn"
              onClick={() => {
                setAuthMode('register');
                setDemoMode(false);
                setError('');
              }}
            >
              Crear estudio
            </button>
            <button type="button" className="nav-btn" onClick={() => { setDemoMode(false); setError(''); }}>
              Volver al login
            </button>
          </div>
        </header>

        {mostrarGuia && (
          <section className="guide-band">
            <strong>Referencia rapida:</strong> Terrenos gris oscuro; Escala: linea verde fluor + medida en negro; Muros rojo; Pisos gris u naranja; Aberturas cian; Sanitario: azul (fria), magenta (caliente), sepia (cloaca); Electrico amarillo; Techos violeta fluor.
          </section>
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
                  <small>Linea verde fluor + numero legible (OCR). Si falla, usa escala manual abajo.</small>
                  {!demoColoresOk && (
                    <button type="button" className="nav-btn step-ack" onClick={marcarDemoColoresOk}>
                      Entendido
                    </button>
                  )}
                </li>
                <li className={demoRuns.length > 0 ? 'done' : ''}>
                  <span className="step-title">Subi un PNG, JPG o WebP</span>
                  <small>Elegi un modulo y cargá tu plano. El resultado aparece al lado (no se guarda en servidor).</small>
                </li>
                <li>
                  <span className="step-title">Guardar obra y CSV</span>
                  <button type="button" className="nav-btn step-ack" onClick={() => { setAuthMode('register'); setDemoMode(false); setError(''); }}>
                    Crear estudio gratis
                  </button>
                </li>
              </ol>
            </div>
          </aside>

          <section className="main-panel">
            <div className="panel-header">
              <div>
                <span className="eyebrow">Panel de computo</span>
                <h2>Modo demostracion</h2>
                <p>Los analisis se muestran solo en este navegador. La API usa el mismo motor que en produccion, sin persistencia.</p>
              </div>
              <div className="panel-actions">
                <label className="scale-control">
                  Escala manual (m)
                  <input type="number" min="0.1" step="0.1" value={referencia} onChange={(e) => setReferencia(e.target.value)} />
                </label>
                <div className="usage-pill">Escala detectada IA: {demoUltimo?.escala_detectada != null ? `${Number(demoUltimo.escala_detectada).toFixed(2)} m` : '-'}</div>
              </div>
            </div>

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
                        </div>
                        {run.tipo !== 'terreno' && <strong>{formatoMoneda(run.total)}</strong>}
                      </div>
                      <div className="desglose-list">
                        {(run.items || []).map((item, index) => (
                          <div key={index} className="desglose-item">
                            <span>{item.nom}</span>
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
          <img src="/logo.png" alt="ARC-IA" className="auth-logo" />
          <div>
            <span className="eyebrow">SaaS para estudios de arquitectura</span>
            <h1>ARC-IA</h1>
            <p>Computo de obra, terrenos e instalaciones con auditoria visual, historial por proyecto y exportacion.</p>
            <div className="auth-points">
              <span>Historial por obra</span>
              <span>Reportes exportables</span>
              <span>Control por estudio</span>
            </div>
          </div>
        </div>

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
              setError('');
              setMostrarGuia(false);
            }}
          >
            Probar sin cuenta
          </button>
          <small className="auth-help">En modo prueba podes subir planos con el motor real; no se guardan en tu estudio.</small>
        </form>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="topbar" style={{ backgroundImage: `linear-gradient(to bottom, rgba(10,10,10,0.82), rgba(10,10,10,0.98)), url(${bannerFondo})` }}>
        <div className="brand-block">
          <img src="/logo.png" alt="ARC-IA" className="logo-img" />
          <div>
            <h1>ARC-IA</h1>
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
          <button className="nav-btn" onClick={() => setMostrarGuia(!mostrarGuia)}>Guia</button>
          <button className="nav-btn" onClick={abrirCheckout} disabled={loading === 'billing'}>
            Suscripcion
          </button>
          <a className="nav-btn" href="https://wa.me/5490000000000" target="_blank" rel="noreferrer">Soporte</a>
          <button className="nav-btn" onClick={logout}>Salir</button>
        </div>
      </header>

      {mostrarGuia && (
        <section className="guide-band">
          <strong>Guia de Calibracion Rapida:</strong> Terrenos/Lotes gris oscuro; Escala automatica: linea verde fluor + medida en negro; Muros: paredes rojo y pisos gris o naranja; Sanitario: azul (agua fria), magenta/fucsia (agua caliente), naranja/sepia (cloacas); Electrico: amarillo.
        </section>
      )}

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
        </aside>

        <section className="main-panel">
          <div className="panel-header">
            <div>
              <span className="eyebrow">Panel de computo</span>
              <h2>{activeProject?.name || 'Selecciona una obra'}</h2>
              <p>{activeProject?.client || 'Los planos procesados quedan guardados dentro de la obra.'}</p>
            </div>
            <div className="panel-actions">
              <button className="nav-btn" disabled={!activeProjectId || processes.length === 0} onClick={exportarCsv}>Exportar CSV</button>
                            <button className="nav-btn" disabled={!activeProjectId} onClick={eliminarObra}>Eliminar obra</button>
              <label className="scale-control">
                Escala manual
                <input type="number" min="0.1" step="0.1" value={referencia} onChange={(e) => setReferencia(e.target.value)} />
                m
              </label>
              <div className="usage-pill">Escala detectada IA: {lastProcess?.escala_detectada ? `${Number(lastProcess.escala_detectada).toFixed(2)} m` : "-"}</div>
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
                      </div>
                      {process.tipo !== 'terreno' && <strong>{formatoMoneda(process.total)}</strong>}
                    </div>
                    <div className="desglose-list">
                      {process.items.map((item, index) => (
                        <div key={index} className="desglose-item">
                          <span>{item.nom}</span>
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
