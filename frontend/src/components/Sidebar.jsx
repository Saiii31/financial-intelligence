import {
  Bot,
  ChevronLeft,
  LayoutDashboard,
  LineChart,
  Lightbulb,
  Menu,
  Settings,
  Sparkles,
  Target,
  Wallet,
} from 'lucide-react';

const NAV = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, href: '#top', active: true },
  { id: 'analytics', label: 'Analytics', icon: LineChart, href: '#section-analytics' },
  { id: 'insights', label: 'Insights', icon: Lightbulb, href: '#section-insights' },
  { id: 'ai', label: 'AI Assistant', icon: Bot, href: '#section-ai' },
  { id: 'goals', label: 'Goals', icon: Target, disabled: true },
  { id: 'transactions', label: 'Transactions', icon: Wallet, disabled: true },
  { id: 'settings', label: 'Settings', icon: Settings, disabled: true },
];

export default function Sidebar({ collapsed, onToggle }) {
  return (
    <>
      <button
        type="button"
        className="sidebar-mobile-toggle"
        aria-label="Toggle navigation"
        onClick={onToggle}
      >
        <Menu size={20} />
      </button>
      <aside className={`sidebar ${collapsed ? 'sidebar--collapsed' : ''}`}>
        <div className="sidebar__brand">
          <div className="sidebar__logo" aria-hidden="true">
            F
          </div>
          {!collapsed && (
            <div>
              <p className="sidebar__name">Finova</p>
              <p className="sidebar__tagline">Financial Intelligence</p>
            </div>
          )}
          <button
            type="button"
            className="sidebar__collapse"
            aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
            onClick={onToggle}
          >
            <ChevronLeft size={18} className={collapsed ? 'sidebar__chev--flip' : ''} />
          </button>
        </div>

        <nav className="sidebar__nav" aria-label="Main">
          {NAV.map(({ id, label, icon: Icon, href, active, disabled }) => {
            if (disabled) {
              return (
                <span key={id} className="sidebar__link sidebar__link--disabled" title="Coming soon">
                  <Icon size={18} strokeWidth={1.75} />
                  {!collapsed && <span>{label}</span>}
                </span>
              );
            }
            return (
              <a
                key={id}
                href={href}
                className={`sidebar__link ${active ? 'sidebar__link--active' : ''}`}
              >
                <Icon size={18} strokeWidth={1.75} />
                {!collapsed && <span>{label}</span>}
              </a>
            );
          })}
        </nav>

        {!collapsed && (
          <div className="sidebar__promo">
            <Sparkles size={16} strokeWidth={1.75} />
            <div>
              <p className="sidebar__promo-title">Smart Insights</p>
              <p className="sidebar__promo-text">
                Anomalies and recommendations update from your verified analytics pipeline.
              </p>
            </div>
          </div>
        )}
      </aside>
      {!collapsed && (
        <button
          type="button"
          className="sidebar-backdrop"
          aria-label="Close navigation"
          onClick={onToggle}
        />
      )}
    </>
  );
}
