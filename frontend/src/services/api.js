import axios from 'axios';
import { mockDashboard } from './mockDashboard';

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000/api';

/** Set VITE_USE_MOCK=true in .env to develop without the backend. */
export const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK === 'true';

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
});

function normalizeDashboard(raw) {
  if (!raw || typeof raw !== 'object') return raw;
  return {
    health_score: raw.health_score ?? raw.healthScore,
    health_breakdown:
      raw.health_breakdown ?? raw.healthBreakdown ?? raw.score_breakdown,
    metrics: raw.metrics ?? {},
    spending: raw.spending ?? raw.expenses_by_category ?? [],
    monthly_cashflow: raw.monthly_cashflow ?? raw.monthlyCashflow ?? [],
    debt: raw.debt ?? {},
    anomalies: raw.anomalies ?? raw.insights ?? [],
    recommendations: raw.recommendations ?? [],
  };
}

export async function fetchDashboard() {
  if (USE_MOCK_DATA) {
    await new Promise((r) => setTimeout(r, 400));
    return normalizeDashboard(mockDashboard);
  }

  // Fetch data from multiple backend endpoints
  const [dashboardRes, cashflowRes, expensesRes, liabilitiesRes, recommendationsRes] = await Promise.all([
    client.get('/dashboard'),
    client.get('/cashflow'),
    client.get('/expenses'),
    client.get('/liabilities'),
    client.get('/recommendations')
  ]);

  // Combine all data into a single dashboard object
  const dashboard = dashboardRes.data;
  const cashflow = cashflowRes.data.cashflow;
  const expenses = expensesRes.data.expenses;
  const liabilities = liabilitiesRes.data.liabilities;
  const recommendations = recommendationsRes.data.recommendations;

  // Find highest interest debt
  const highestInterestDebt = liabilities.reduce((max, debt) => {
    return (debt.interest_rate > (max?.interest_rate || 0)) ? debt : max;
  }, null);

  return normalizeDashboard({
    health_score: dashboard.health_score,
    health_breakdown: {
      savings: dashboard.savings_rate * 5, // Approximate score from rate
      debt: 100 - (dashboard.debt_to_income > 75 ? 50 : dashboard.debt_to_income),
      cash_flow: dashboard.savings > 0 ? 100 : 50,
      stability: 75, // Placeholder
    },
    metrics: {
      total_income: dashboard.income,
      total_expenses: dashboard.expenses,
      net_cashflow: dashboard.savings,
      savings_rate: dashboard.savings_rate,
      total_assets: dashboard.assets,
      total_debt: dashboard.liabilities,
      net_worth: dashboard.net_worth,
      monthly_emi: dashboard.monthly_emi || 46700,
      debt_to_income: dashboard.debt_to_income,
    },
    spending: expenses.map(e => ({
      category: e.category,
      amount: e.amount,
      percentage: e.percentage
    })),
    monthly_cashflow: cashflow.map(c => ({
      month: c.month,
      income: c.income,
      expenses: c.expenses,
      net: c.savings
    })),
    debt: {
      highest_interest_debt: highestInterestDebt ? {
        type: highestInterestDebt.type,
        interest_rate: highestInterestDebt.interest_rate,
        outstanding: highestInterestDebt.outstanding,
      } : null,
    },
    anomalies: [],
    recommendations: recommendations.map(r => ({
      priority: r.priority,
      title: r.category,
      description: r.recommendation,
    })),
  });
}

export async function askFinancialQuestion(question) {
  const { data } = await client.post('/ask', { question });
  return (
    data?.answer ??
    data?.response ??
    data?.message ??
    (typeof data === 'string' ? data : null)
  );
}
