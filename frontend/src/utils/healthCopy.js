export function getHealthStatus(score) {
  if (typeof score !== 'number') {
    return { label: '—', tone: 'fair' };
  }
  if (score >= 70) return { label: 'Healthy', tone: 'good' };
  if (score >= 50) return { label: 'Fair', tone: 'fair' };
  return { label: 'Needs attention', tone: 'low' };
}

function formatDim(key) {
  return key.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

/** Narrative derived from score + breakdown only (no invented metrics). */
export function getHealthSummary(score, breakdown) {
  const { label, tone } = getHealthStatus(score);
  const entries =
    breakdown && typeof breakdown === 'object'
      ? Object.entries(breakdown).filter(([, v]) => v != null)
      : [];

  if (entries.length === 0) {
    if (tone === 'good') {
      return {
        headline: `You're financially ${label.toLowerCase()}`,
        body: 'Your overall score reflects balanced income, spending, and savings behavior.',
      };
    }
    return {
      headline: `Financial health: ${label}`,
      body: 'Review cash flow, savings, and debt below to see what drives your score.',
    };
  }

  const sorted = [...entries].sort((a, b) => Number(a[1]) - Number(b[1]));
  const weakest = formatDim(sorted[0][0]);
  const strongest = formatDim(sorted[sorted.length - 1][0]);

  if (tone === 'good') {
    return {
      headline: `You're financially ${label.toLowerCase()}`,
      body: `Your ${strongest.toLowerCase()} and cash discipline are strengths; ${weakest.toLowerCase()} may need ongoing attention.`,
    };
  }
  if (tone === 'fair') {
    return {
      headline: `Financial health is ${label.toLowerCase()}`,
      body: `${weakest} is pulling your score down while ${strongest.toLowerCase()} remains relatively stronger.`,
    };
  }
  return {
    headline: 'Your finances need focused attention',
    body: `${weakest} is the weakest area; prioritize improvements there while protecting ${strongest.toLowerCase()}.`,
  };
}
