import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts';
import { formatINRCompact, formatPercent } from '../utils/format';

const COLORS = ['#312E81', '#4338CA', '#6366F1', '#0F766E', '#0D9488', '#64748B'];

function ExpenseTooltip({ active, payload, totalExpenses }) {
  if (!active || !payload?.length) return null;
  const { name, value } = payload[0].payload;
  const pct =
    totalExpenses && Number(totalExpenses) > 0
      ? (Number(value) / Number(totalExpenses)) * 100
      : null;
  return (
    <div className="chart-tooltip chart-tooltip--rich">
      <p className="chart-tooltip__title">{name}</p>
      <p>{formatINRCompact(value)}</p>
      {pct != null && <p className="chart-tooltip__muted">{formatPercent(pct)} of period spend</p>}
    </div>
  );
}

function DonutCenter({ totalExpenses }) {
  if (totalExpenses == null) return null;
  return (
    <div className="donut-center">
      <span className="donut-center__label">Total spending</span>
      <span className="donut-center__value">{formatINRCompact(totalExpenses)}</span>
    </div>
  );
}

export default function ExpenseChart({ spending, totalExpenses }) {
  const data = (spending ?? []).map((row) => ({
    name: row.category ?? row.name ?? 'Other',
    value: row.amount ?? row.total ?? 0,
  }));

  if (data.length === 0) {
    return (
      <div className="card chart-card">
        <div className="section-head">
          <h3 className="section-head__title">Spending breakdown</h3>
        </div>
        <p className="empty-state">No spending categories to show.</p>
      </div>
    );
  }

  const total = totalExpenses ?? null;

  return (
    <div className="card chart-card card--interactive">
      <div className="section-head">
        <div>
          <h3 className="section-head__title">Spending breakdown</h3>
          <p className="section-head__sub">Share of verified category totals</p>
        </div>
      </div>
      <div className="expense-layout">
        <div className="chart-wrap chart-wrap--donut">
          <DonutCenter totalExpenses={total} />
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie
                data={data}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                innerRadius={72}
                outerRadius={96}
                paddingAngle={2}
                stroke="var(--surface)"
                strokeWidth={2}
              >
                {data.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip content={<ExpenseTooltip totalExpenses={total} />} />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <ul className="expense-legend">
          {data.map((row, index) => {
            const pct =
              total && Number(total) > 0 ? (Number(row.value) / Number(total)) * 100 : null;
            return (
              <li key={row.name}>
                <span className="expense-legend__swatch" style={{ background: COLORS[index % COLORS.length] }} />
                <span className="expense-legend__name">{row.name}</span>
                <span className="expense-legend__amt">{formatINRCompact(row.value)}</span>
                {pct != null && (
                  <span className="expense-legend__pct">{formatPercent(pct)}</span>
                )}
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}
