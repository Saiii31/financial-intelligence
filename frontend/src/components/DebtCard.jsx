import { AlertTriangle } from 'lucide-react';
import { formatINRCompact, formatPercent } from '../utils/format';

export default function DebtCard({ metrics, debt }) {
  const m = metrics ?? {};
  const highest = debt?.highest_interest_debt ?? debt?.highestInterestDebt;
  const debtToIncome = m.debt_to_income ?? debt?.debt_to_income ?? debt?.debtToIncome;
  const highRate = highest?.interest_rate != null && Number(highest.interest_rate) >= 20;
  const dtiValue = debtToIncome != null ? Math.min(100, Math.max(0, Number(debtToIncome))) : null;

  return (
    <div className="card debt-card card--interactive">
      <div className="section-head">
        <div>
          <h3 className="section-head__title">Debt overview</h3>
          <p className="section-head__sub">Liabilities and repayment pressure</p>
        </div>
      </div>

      <div className="debt-grid">
        <div className="debt-metric">
          <span className="debt-metric__label">Total debt</span>
          <span className="debt-metric__value">{formatINRCompact(m.total_debt)}</span>
        </div>
        <div className="debt-metric">
          <span className="debt-metric__label">Monthly EMI</span>
          <span className="debt-metric__value">{formatINRCompact(m.monthly_emi)}</span>
        </div>
        {debtToIncome != null && (
          <div className="debt-metric debt-metric--wide">
            <div className="debt-metric__row">
              <span className="debt-metric__label">Debt-to-income</span>
              <span className="debt-metric__value debt-metric__value--sm">
                {formatPercent(debtToIncome)}
              </span>
            </div>
            <div className="debt-meter" aria-hidden="true">
              <span
                className={`debt-meter__fill ${dtiValue > 35 ? 'debt-meter__fill--high' : ''}`}
                style={{ width: `${dtiValue}%` }}
              />
            </div>
          </div>
        )}
      </div>

      {highest && (
        <div className={`debt-highlight ${highRate ? 'debt-highlight--alert' : ''}`}>
          <div className="debt-highlight__head">
            {highRate && <AlertTriangle size={16} strokeWidth={1.75} />}
            <span className="debt-highlight__label">Highest interest liability</span>
          </div>
          <p className="debt-highlight__main">
            {highest.type ?? 'Liability'} — {formatPercent(highest.interest_rate)}
          </p>
          {highest.outstanding != null && (
            <p className="debt-highlight__sub">
              Outstanding {formatINRCompact(highest.outstanding)}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
