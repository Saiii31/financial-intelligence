import { ArrowUpRight, Lightbulb } from 'lucide-react';
import { pickQuickInsight } from '../utils/insightMeta';

export default function QuickInsight({ anomalies, recommendations, monthlyCashflow }) {
  const insight = pickQuickInsight({ anomalies, recommendations, monthlyCashflow });

  if (!insight) {
    return (
      <aside className="card quick-insight quick-insight--empty">
        <Lightbulb size={18} strokeWidth={1.75} />
        <p className="quick-insight__empty">Insights will appear when analytics data is available.</p>
      </aside>
    );
  }

  return (
    <aside className={`card quick-insight quick-insight--${insight.type}`}>
      <div className="quick-insight__head">
        <Lightbulb size={18} strokeWidth={1.75} />
        <span className="quick-insight__title">{insight.title}</span>
        <ArrowUpRight size={16} className="quick-insight__arrow" aria-hidden="true" />
      </div>
      <p className="quick-insight__text">{insight.text}</p>
    </aside>
  );
}
