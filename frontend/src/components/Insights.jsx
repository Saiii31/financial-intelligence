import { AlertTriangle, CheckCircle2, Info, TrendingUp } from 'lucide-react';
import { classifyInsight } from '../utils/insightMeta';

const META = {
  positive: { label: 'Positive', Icon: CheckCircle2, className: 'insight--positive' },
  warning: { label: 'Warning', Icon: AlertTriangle, className: 'insight--warning' },
  risk: { label: 'Risk', Icon: AlertTriangle, className: 'insight--risk' },
  opportunity: { label: 'Opportunity', Icon: TrendingUp, className: 'insight--opportunity' },
};

function parseInsight(text) {
  const clean = String(text).replace(/^[✓⚠]\s*/, '');
  const parts = clean.split(/[.:—–-]\s+/);
  if (parts.length > 1 && parts[0].length < 48) {
    return { title: parts[0], body: parts.slice(1).join(' — ') || clean };
  }
  return { title: clean, body: 'Detected in your verified transaction analytics.' };
}

export default function Insights({ anomalies }) {
  const items = anomalies ?? [];

  return (
    <section id="section-insights" className="card insights-card">
      <div className="section-head">
        <div>
          <h3 className="section-head__title">Key insights</h3>
          <p className="section-head__sub">Trends and anomalies from the analytics engine</p>
        </div>
      </div>
      {items.length === 0 ? (
        <p className="empty-state">No insights detected for this period.</p>
      ) : (
        <ul className="insights-grid">
          {items.map((text, i) => {
            const type = classifyInsight(text);
            const { label, Icon, className } = META[type] ?? META.warning;
            const { title, body } = parseInsight(text);
            return (
              <li key={`${i}-${text}`} className={`insight-tile card--interactive ${className}`}>
                <div className="insight-tile__icon">
                  <Icon size={16} strokeWidth={1.75} />
                </div>
                <div>
                  <span className="insight-tile__type">{label}</span>
                  <h4 className="insight-tile__title">{title}</h4>
                  <p className="insight-tile__body">{body}</p>
                </div>
                <Info size={14} className="insight-tile__info" aria-hidden="true" />
              </li>
            );
          })}
        </ul>
      )}
    </section>
  );
}
