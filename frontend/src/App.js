import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import './App.css';
import bannerFondo from './banner-fondo.png';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

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


const getErrorMessage = (err, fallback) => {
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
  const [activeProjectId, setActiveProjectId] = useState('');
  const [processes, setProcesses] = useState([]);
  const [projectForm, setProjectForm] = useState({ name: '', client: '', address: '' });
  const [referencia, setReferencia] = useState(1);
  const [mostrarGuia, setMostrarGuia] = useState(false);
  const [loading, setLoading] = useState('');
  const [error, setError] = useState('');

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
    if (!activeProjectId && res.data[0]) setActiveProjectId(String(res.data[0].id));
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
    if (!token) return;
    Promise.all([refreshMe(), refreshProjects()]).catch(() => {
      localStorage.removeItem('arqia_token');
      setToken('');
      setMe(null);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  useEffect(() => {
    if (activeProjectId) refreshProcesses(activeProjectId);
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
      const res = await axios.post(`${API_URL}${path}`, payload);
      localStorage.setItem('arqia_token', res.data.token);
      setToken(res.data.token);
    } catch (err) {
      setError(getErrorMessage(err, authMode === 'login' ? 'No se pudo iniciar sesion.' : 'No se pudo crear la cuenta.'));
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
    } catch (err) {
      setError(getErrorMessage(err, 'No se pudo exportar la obra.'));
    }
  };

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
          <button className="nav-btn" onClick={() => setMostrarGuia(!mostrarGuia)}>Guia</button>
          <button className="nav-btn" onClick={abrirCheckout} disabled={loading === 'billing'}>
            Suscripcion
          </button>
          <button className="nav-btn" onClick={logout}>Salir</button>
        </div>
      </header>

      {mostrarGuia && (
        <section className="guide-band">
          <strong>Guia de colores:</strong> escala verde fluor con medida cerca; muros rojo; pisos gris/naranja; agua fria azul; agua caliente magenta; cloacas naranja/sepia; electricidad amarillo; techo violeta; terrenos gris oscuro.
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
              <label className="scale-control">
                Escala manual
                <input type="number" min="0.1" step="0.1" value={referencia} onChange={(e) => setReferencia(e.target.value)} />
                m
              </label>
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
