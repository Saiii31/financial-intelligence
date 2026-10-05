import {
  Area,
  CartesianGrid,
  ComposedChart,
  Legend,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { formatINRCompact, formatMonthLabel } from '../utils/format';

function ChartTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="chart-tooltip chart-tooltip--rich">
      <p className="chart-tooltip__title">{formatMonthLabel(label)}</p>
      <ul className="chart-tooltip__list">
        {payload.map((entry) => (
          <li key={entry.dataKey}>
            <span className="chart-tooltip__dot" style={{ background: entry.color }} />
            <span>{entry.name}</span>
            <strong>{formatINRCompact(entry.value)}</strong>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function CashFlowChart({ monthlyCashflow }) {
  const data = monthlyCashflow ?? [];

  if (data.length === 0) {
    return (
      <div className="card chart-card">
        <div className="section-head">
          <h3 className="section-head__title">Monthly cash flow</h3>
        </div>
        <p className="empty-state">No cash flow data available yet.</p>
      </div>
    );
  }

  const chartData = data.map((row) => ({
    ...row,
    label: formatMonthLabel(row.month),
  }));

  return (
    <div className="card chart-card card--interactive">
      <div className="section-head">
        <div>
          <h3 className="section-head__title">Monthly cash flow</h3>
          <p className="section-head__sub">Income, expenses, and net across verified months</p>
        </div>
      </div>
      <div className="chart-wrap chart-wrap--tall">
        <ResponsiveContainer width="100%" height={320}>
          <ComposedChart data={chartData} margin={{ top: 12, right: 12, left: 4, bottom: 4 }}>
            <defs>
              <linearGradient id="incomeFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="var(--chart-income)" stopOpacity={0.18} />
                <stop offset="100%" stopColor="var(--chart-income)" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="expenseFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="var(--chart-expense)" stopOpacity={0.12} />
                <stop offset="100%" stopColor="var(--chart-expense)" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="var(--chart-grid)" strokeDasharray="4 4" vertical={false} />
            <XAxis
              dataKey="label"
              tick={{ fill: 'var(--text-muted)', fontSize: 12 }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              tickFormatter={(v) => `${(v / 1000).toFixed(0)}k`}
              tick={{ fill: 'var(--text-muted)', fontSize: 12 }}
              axisLine={false}
              tickLine={false}
              width={48}
            />
            <Tooltip content={<ChartTooltip />} cursor={{ stroke: 'var(--border-strong)' }} />
            <Legend verticalAlign="top" height={36} iconType="circle" />
            <Area
              type="monotone"
              dataKey="income"
              name="Income"
              stroke="var(--chart-income)"
              fill="url(#incomeFill)"
              strokeWidth={2}
              dot={false}
            />
            <Area
              type="monotone"
              dataKey="expenses"
              name="Expenses"
              stroke="var(--chart-expense)"
              fill="url(#expenseFill)"
              strokeWidth={2}
              dot={false}
            />
            <Line
              type="monotone"
              dataKey="net"
              name="Net cash flow"
              stroke="var(--chart-net)"
              strokeWidth={2.5}
              dot={{ r: 3, strokeWidth: 0, fill: 'var(--chart-net)' }}
              activeDot={{ r: 5 }}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
