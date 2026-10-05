export function classifyInsight(text) {
  const t = String(text).toLowerCase();
  if (
    t.includes('positive') ||
    (t.includes('healthy') && !t.includes('unhealthy')) ||
    t.includes('on track') ||
    t.startsWith('✓')
  ) {
    return 'positive';
  }
  if (t.includes('debt') || t.includes('interest') || t.includes('risk')) {
    return 'risk';
  }
  if (t.includes('increased') || t.includes('decrease') || t.includes('spike')) {
    return 'warning';
  }
  if (t.includes('review') || t.includes('maintain') || t.includes('consider')) {
    return 'opportunity';
  }
  return 'warning';
}

export function pickQuickInsight({ anomalies, recommendations, monthlyCashflow }) {
  const list = anomalies ?? [];
  const positive = list.find((item) => classifyInsight(item) === 'positive');
  if (positive) {
    return {
      type: 'positive',
      title: 'Quick insight',
      text: positive.replace(/^[✓⚠]\s*/, ''),
    };
  }

  const flow = monthlyCashflow ?? [];
  if (flow.length >= 2) {
    const last = flow[flow.length - 1];
    const prev = flow[flow.length - 2];
    if (last?.net != null && prev?.net != null && last.net > prev.net) {
      return {
        type: 'positive',
        title: 'Cash flow trend',
        text: 'Net cash flow improved compared to the previous month in your verified series.',
      };
    }
  }

  const topRec = (recommendations ?? [])[0];
  if (topRec?.title) {
    return {
      type: topRec.priority === 'HIGH' ? 'risk' : 'opportunity',
      title: 'Recommended focus',
      text: topRec.description ? `${topRec.title} — ${topRec.description}` : topRec.title,
    };
  }

  const first = list[0];
  if (first) {
    return {
      type: classifyInsight(first),
      title: 'Needs attention',
      text: first.replace(/^[✓⚠]\s*/, ''),
    };
  }

  return null;
}
