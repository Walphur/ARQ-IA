/**
 * Propagates X-Request-Id only. trace_id is backend-exclusive (E01-F01).
 */

const STORAGE_KEY = 'arqia_request_id';

function randomId() {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return `req_${Date.now().toString(16)}_${Math.random().toString(16).slice(2)}`;
}

export function getOrCreateSessionRequestId() {
  try {
    const existing = sessionStorage.getItem(STORAGE_KEY);
    if (existing && existing.length <= 128) return existing;
    const created = randomId();
    sessionStorage.setItem(STORAGE_KEY, created);
    return created;
  } catch {
    return randomId();
  }
}

export function attachRequestIdInterceptor(axiosInstance) {
  axiosInstance.interceptors.request.use((config) => {
    const headers = config.headers || {};
    if (!headers['X-Request-Id'] && !headers['x-request-id']) {
      headers['X-Request-Id'] = getOrCreateSessionRequestId();
    }
    config.headers = headers;
    return config;
  });
}
