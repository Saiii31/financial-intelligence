/** Demo payload for UI development when the API is unavailable. */
export const mockDashboard = {
  health_score: 74,
  health_breakdown: {
    savings: 82,
    debt: 45,
    cash_flow: 78,
    stability: 70,
  },

  metrics: {
    total_income: 223000,
    total_expenses: 142000,
    net_cashflow: 81000,
    savings_rate: 36.3,
    total_assets: 860000,
    total_debt: 3338000,
    net_worth: -2478000,
    monthly_emi: 46700,
    debt_to_income: 21.8,
  },

  spending: [
    { category: 'Housing', amount: 80000 },
    { category: 'Food', amount: 45000 },
    { category: 'Travel', amount: 30000 },
    { category: 'Shopping', amount: 22000 },
    { category: 'Utilities', amount: 15000 },
  ],

  monthly_cashflow: [
    { month: '2025-11', income: 210000, expenses: 145000, net: 65000 },
    { month: '2025-12', income: 215000, expenses: 148000, net: 67000 },
    { month: '2026-01', income: 200000, expenses: 150000, net: 50000 },
    { month: '2026-02', income: 220000, expenses: 160000, net: 60000 },
    { month: '2026-03', income: 223000, expenses: 142000, net: 81000 },
  ],

  debt: {
    highest_interest_debt: {
      type: 'Credit Card',
      interest_rate: 32,
      outstanding: 500000,
    },
  },

  anomalies: [
    'Travel spending increased 41%',
    'High-interest credit card debt detected',
    'Cash flow is positive',
  ],

  recommendations: [
    {
      priority: 'HIGH',
      title: 'Prioritize high-interest debt',
      description: 'Credit card has the highest interest rate.',
    },
    {
      priority: 'MEDIUM',
      title: 'Review travel spending',
      description: 'Travel spending increased significantly.',
    },
    {
      priority: 'MEDIUM',
      title: 'Maintain savings discipline',
      description: 'Your savings rate is currently healthy.',
    },
  ],
};
