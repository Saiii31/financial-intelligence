import { ArrowRight } from 'lucide-react';

const PRIORITY_CLASS = {
  HIGH: 'rec-priority--high',
  MEDIUM: 'rec-priority--medium',
  LOW: 'rec-priority--low',
};

export default function Recommendations({ recommendations }) {
  const top = (recommendations ?? []).slice(0, 3);

  return (
    <section className="card recommendations-card">
      <div className="section-head">
        <div>
          <h3 className="section-head__title">What you should do</h3>
          <p className="section-head__sub">Prioritized actions from recommendation rules</p>
        </div>
      </div>
      {top.length === 0 ? (
        <p className="empty-state">No recommendations at this time.</p>
      ) : (
        <ol className="rec-list">
          {top.map((rec, index) => (
            <li key={`${rec.title}-${index}`} className="rec-item card--interactive">
              <div className="rec-item__index">{String(index + 1).padStart(2, '0')}</div>
              <div className="rec-item__content">
                <div className="rec-item__head">
                  {rec.priority && (
                    <span className={`rec-priority ${PRIORITY_CLASS[rec.priority] ?? ''}`}>
                      {rec.priority}
                    </span>
                  )}
                  <h4 className="rec-item__title">{rec.title}</h4>
                  <ArrowRight size={16} className="rec-item__arrow" aria-hidden="true" />
                </div>
                {rec.description && <p className="rec-item__desc">{rec.description}</p>}
              </div>
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}
