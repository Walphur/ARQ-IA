/**
 * Platform status client for E01-F02.
 * DegradationBanner must use ONLY this module → GET /v1/platform/status.
 * Never call /ready from UI banner paths.
 */

const CACHE_TTL_MS = 45000;

let _cache = null;
let _cacheAt = 0;

export function clearPlatformStatusCache() {
  _cache = null;
  _cacheAt = 0;
}

export async function fetchPlatformStatus(apiBase, axiosInstance) {
  const now = Date.now();
  if (_cache && now - _cacheAt < CACHE_TTL_MS) {
    return _cache;
  }
  const base = String(apiBase || '').replace(/\/+$/, '');
  const res = await axiosInstance.get(`${base}/v1/platform/status`, { timeout: 8000 });
  _cache = res.data;
  _cacheAt = now;
  return _cache;
}

export function shouldShowDegradationBanner(status) {
  if (!status) return false;
  if (status.degraded === true) return true;
  return status.mode && status.mode !== 'normal';
}

export function bannerMessage(status) {
  if (!status) return '';
  const mode = status.mode || 'unknown';
  if (mode === 'maintenance') {
    return 'La plataforma está en mantenimiento. Algunas operaciones pueden no estar disponibles.';
  }
  if (mode === 'readonly') {
    return 'La plataforma está en modo solo lectura.';
  }
  if (mode === 'degraded') {
    return 'La plataforma opera en modo degradado. Puede haber funcionalidad limitada.';
  }
  return 'Estado operativo especial de la plataforma.';
}
