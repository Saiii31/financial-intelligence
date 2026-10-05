import { useEffect, useState } from 'react';

import AIChat from '../components/AIChat';

import CashFlowChart from '../components/CashFlowChart';

import DebtCard from '../components/DebtCard';

import ExpenseChart from '../components/ExpenseChart';

import HealthScore from '../components/HealthScore';

import Insights from '../components/Insights';

import KPICards from '../components/KPICards';

import QuickInsight from '../components/QuickInsight';

import Recommendations from '../components/Recommendations';

import Sidebar from '../components/Sidebar';

import TopHeader from '../components/TopHeader';

import { fetchDashboard, USE_MOCK_DATA } from '../services/api';



function getGreeting() {

  const hour = new Date().getHours();

  if (hour < 12) return 'Good morning';

  if (hour < 17) return 'Good afternoon';

  return 'Good evening';

}



function DashboardShell({ children, sidebarCollapsed, onToggleSidebar, showDemoBadge }) {
  return (
    <div className="app-shell">
      <Sidebar collapsed={sidebarCollapsed} onToggle={onToggleSidebar} />
      <div className={`app-main ${sidebarCollapsed ? 'app-main--sidebar-collapsed' : ''}`}>
        <TopHeader showDemoBadge={showDemoBadge} />
        <div className="dashboard-content">{children}</div>
      </div>
    </div>
  );
}



export default function Dashboard() {

  const [data, setData] = useState(null);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState(null);

  const [sidebarCollapsed, setSidebarCollapsed] = useState(() =>

    typeof window !== 'undefined' ? window.innerWidth < 1024 : false,

  );



  useEffect(() => {

    let cancelled = false;



    async function load() {

      setLoading(true);

      setError(null);

      try {

        const dashboard = await fetchDashboard();

        if (!cancelled) setData(dashboard);

      } catch (err) {

        if (!cancelled) {

          setError(

            err.response?.data?.detail ??

              err.message ??

              'Failed to load dashboard. Is the API running on port 8000?',

          );

        }

      } finally {

        if (!cancelled) setLoading(false);

      }

    }



    load();

    return () => {

      cancelled = true;

    };

  }, []);



  useEffect(() => {

    function onResize() {

      if (window.innerWidth >= 1024) {

        setSidebarCollapsed(false);

      }

    }

    window.addEventListener('resize', onResize);

    return () => window.removeEventListener('resize', onResize);

  }, []);



  const toggleSidebar = () => setSidebarCollapsed((c) => !c);



  if (loading) {

    return (

      <DashboardShell

        sidebarCollapsed={sidebarCollapsed}

        onToggleSidebar={toggleSidebar}

        showDemoBadge={USE_MOCK_DATA}

      >

        <div className="dashboard-state">

          <div className="skeleton skeleton--hero" />

          <div className="skeleton skeleton--row" />

          <p className="loading-state">Loading your financial overview…</p>

        </div>

      </DashboardShell>

    );

  }



  if (error) {

    return (

      <DashboardShell

        sidebarCollapsed={sidebarCollapsed}

        onToggleSidebar={toggleSidebar}

        showDemoBadge={USE_MOCK_DATA}

      >

        <div className="dashboard-state">

          <div className="banner banner--error banner--large">

            <strong>Could not load dashboard</strong>

            <p>{error}</p>

            <p className="banner__hint">

              Tip: set <code>VITE_USE_MOCK=true</code> in <code>frontend/.env</code> to use demo

              data, or start FastAPI at <code>GET /api/dashboard</code>.

            </p>

          </div>

        </div>

      </DashboardShell>

    );

  }



  return (

    <DashboardShell

      sidebarCollapsed={sidebarCollapsed}

      onToggleSidebar={toggleSidebar}

      showDemoBadge={USE_MOCK_DATA}

    >

      <div id="top" className="page-intro">

        <h1 className="page-intro__title">

          {getGreeting()}, User <span aria-hidden="true">👋</span>

        </h1>

        <p className="page-intro__sub">Here&apos;s your financial health at a glance.</p>

      </div>



      <div className="hero-row">

        <HealthScore score={data.health_score} breakdown={data.health_breakdown} />

        <QuickInsight

          anomalies={data.anomalies}

          recommendations={data.recommendations}

          monthlyCashflow={data.monthly_cashflow}

        />

      </div>



      <KPICards metrics={data.metrics} monthlyCashflow={data.monthly_cashflow} />



      <section id="section-analytics" className="analytics-section">

        <CashFlowChart monthlyCashflow={data.monthly_cashflow} />

        <div className="two-col">

          <ExpenseChart spending={data.spending} totalExpenses={data.metrics?.total_expenses} />

          <DebtCard metrics={data.metrics} debt={data.debt} />

        </div>

      </section>



      <Insights anomalies={data.anomalies} />



      <Recommendations recommendations={data.recommendations} />



      <AIChat />

    </DashboardShell>

  );

}

