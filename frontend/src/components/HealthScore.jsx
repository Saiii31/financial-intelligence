import { getHealthStatus, getHealthSummary } from '../utils/healthCopy';

const BREAKDOWN_ORDER = ['savings', 'cash_flow', 'stability', 'debt'];

function formatDim(key) {
  return key.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

export default function HealthScore({ score, breakdown }) {
  const value = score ?? '—';
  const numeric = typeof score === 'number' ? score : 0;
  const { label, tone } = getHealthStatus(score);
  const { headline, body } = getHealthSummary(score, breakdown);
  const ringClass =
    tone === 'good' ? 'health-score--good' : tone === 'low' ? 'health-score--low' : 'health-score--fair';

  const breakdownMap =
    breakdown && typeof breakdown === 'object'
      ? Object.fromEntries(Object.entries(breakdown).filter(([, v]) => v != null))
      : {};

  const orderedKeys = [
    ...BREAKDOWN_ORDER.filter((k) => breakdownMap[k] != null),
    ...Object.keys(breakdownMap).filter((k) => !BREAKDOWN_ORDER.includes(k)),
  ];

  return (
    <section className={`health-hero card card--interactive ${ringClass}`}>
      <div className="health-hero__main">
        <div className="health-hero__ring-wrap">
          <div className="health-hero__ring" aria-hidden="true">
            <svg viewBox="0 0 120 120" className="health-score__svg">
              <circle className="health-score__track" cx="60" cy="60" r="52" />
              <circle
                className="health-score__fill"
                cx="60"
                cy="60"
                r="52"
                style={{
                  strokeDasharray: `${(numeric / 100) * 327} 327`,
                }}
              />
            </svg>
            <div className="health-score__center">
              <span className="health-score__number">{value}</span>
              <span className="health-score__max">/ 100</span>
            </div>
          </div>
          <span className={`health-hero__badge health-hero__badge--${tone}`}>{label}</span>
        </div>

        <div className="health-hero__copy">
          <p className="health-hero__eyebrow">Financial Health</p>
          <h2 className="health-hero__headline">{headline}</h2>
          <p className="health-hero__body">{body}</p>
        </div>
      </div>

      {orderedKeys.length > 0 && (
        <ul className="health-hero__breakdown">
          {orderedKeys.map((key) => {
            const val = Number(breakdownMap[key]);
            return (
              <li key={key} className="health-hero__dim">
                <div className="health-hero__dim-top">
                  <span>{formatDim(key)}</span>
                  <span className="health-hero__dim-val">{breakdownMap[key]}</span>
                </div>
                <div className="health-hero__bar" aria-hidden="true">
                  <span style={{ width: `${Math.min(100, Math.max(0, val))}%` }} />
                </div>
              </li>
            );
          })}
        </ul>
      )}
    </section>
  );
}
