import {
  ArrowDownRight,
  ArrowUpRight,
  IndianRupee,
  Minus,
  PiggyBank,
  Scale,
  Wallet,
} from 'lucide-react';
import { formatINRCompact, formatPercent } from '../utils/format';

function MiniSparkline({ series }) {
  const values = (series ?? []).map(Number).filter((n) => !Number.isNaN(n));
  if (values.length < 2) return null;

  const w = 72;
  const h = 28;
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;
  const points = values
    .map((v, i) => {
      const x = (i / (values.length - 1)) * w;
      const y = h - ((v - min) / range) * (h - 4) - 2;
      return `${x},${y}`;
    })
    .join(' ');

  return (
    <svg className="kpi-sparkline" viewBox={`0 0 ${w} ${h}`} aria-hidden="true">
      <polyline points={points} fill="none" stroke="currentColor" strokeWidth="1.5" />
    </svg>
  );
}

function Trend({ current, previous, invert = false }) {
  if (current == null || previous == null) return null;
  const cur = Number(current);
  const prev = Number(previous);
  if (Number.isNaN(cur) || Number.isNaN(prev) || prev === 0) return null;

  const delta = ((cur - prev) / Math.abs(prev)) * 100;
  if (Math.abs(delta) < 0.05) {
    return (
      <span className="kpi-trend kpi-trend--flat">
        <Minus size={14} /> Stable vs prior month
      </span>
    );
  }

  const up = delta > 0;
  const good = invert ? !up : up;
  const Icon = up ? ArrowUpRight : ArrowDownRight;

  return (
    <span className={`kpi-trend ${good ? 'kpi-trend--good' : 'kpi-trend--muted'}`}>
      <Icon size={14} />
      {Math.abs(delta).toFixed(1)}% vs prior month
    </span>
  );
}

function KPICard({ label, value, tone = 'default', icon: Icon, trend, sparkline, hint }) {
  return (
    <div className={`kpi-card card--interactive kpi-card--${tone}`}>
      <div className="kpi-card__top">
        <span className="kpi-card__icon" aria-hidden="true">
          <Icon size={18} strokeWidth={1.75} />
        </span>
        {sparkline}
      </div>
      <span className="kpi-card__label">{label}</span>
      <span className="kpi-card__value">{value}</span>
      {trend}
      {hint && <span className="kpi-card__hint">{hint}</span>}
    </div>
  );
}

export default function KPICards({ metrics, monthlyCashflow }) {
  const m = metrics ?? {};
  const flow = monthlyCashflow ?? [];
  const last = flow[flow.length - 1];
  const prev = flow[flow.length - 2];
  const netWorthTone = Number(m.net_worth) < 0 ? 'negative' : 'positive';

  const incomeSeries = flow.map((row) => row.income);
  const expenseSeries = flow.map((row) => row.expenses);
  const netSeries = flow.map((row) => row.net);

  return (
    <section className="kpi-section">
      <div className="section-head">
        <h3 className="section-head__title">Key financial metrics</h3>
        <p className="section-head__sub">Verified totals from your analytics pipeline</p>
      </div>
      <div className="kpi-grid">
        <KPICard
          label="Total Income"
          value={formatINRCompact(m.total_income)}
          icon={IndianRupee}
          sparkline={<MiniSparkline series={incomeSeries} />}
          trend={<Trend current={last?.income} previous={prev?.income} />}
          hint="Period total"
        />
        <KPICard
          label="Total Expenses"
          value={formatINRCompact(m.total_expenses)}
          icon={Wallet}
          sparkline={<MiniSparkline series={expenseSeries} />}
          trend={<Trend current={last?.expenses} previous={prev?.expenses} invert />}
          hint="Period total"
        />
        <KPICard
          label="Savings Rate"
          value={formatPercent(m.savings_rate)}
          tone="accent"
          icon={PiggyBank}
          hint="From verified analytics"
        />
        <KPICard
          label="Net Worth"
          value={formatINRCompact(m.net_worth)}
          tone={netWorthTone}
          icon={Scale}
          hint="Assets minus liabilities"
        />
        {m.monthly_emi != null && (
          <KPICard
            label="Monthly EMI"
            value={formatINRCompact(m.monthly_emi)}
            icon={Wallet}
            sparkline={<MiniSparkline series={netSeries} />}
            trend={<Trend current={last?.net} previous={prev?.net} />}
            hint="Scheduled obligations"
          />
        )}
      </div>
    </section>
  );
}
