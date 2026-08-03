import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  bannerMessage,
  fetchPlatformStatus,
  shouldShowDegradationBanner,
} from '../infrastructure/platformStatus';

/**
 * Consumes exclusively GET /v1/platform/status (via platformStatus.js).
 * Does not call /ready or /health. Announce-only — no client-side enforcement.
 */
export default function DegradationBanner({ apiBase }) {
  const [status, setStatus] = useState(null);

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        const data = await fetchPlatformStatus(apiBase, axios);
        if (!cancelled) setStatus(data);
      } catch {
        if (!cancelled) setStatus(null);
      }
    };
    load();
    const id = setInterval(load, 45000);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, [apiBase]);

  if (!shouldShowDegradationBanner(status)) return null;

  return (
    <div
      className="degradation-banner"
      role="status"
      data-platform-mode={status.mode}
      style={{
        background: '#5c4a1f',
        color: '#fff8e7',
        padding: '10px 16px',
        textAlign: 'center',
        fontSize: '0.95rem',
      }}
    >
      {bannerMessage(status)}
    </div>
  );
}
