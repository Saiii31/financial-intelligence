import { Bell, Calendar, Search } from 'lucide-react';

export default function TopHeader({ showDemoBadge }) {
  return (
    <header className="top-header">
      <div className="top-header__search">
        <Search size={18} strokeWidth={1.75} className="top-header__search-icon" />
        <input
          type="search"
          className="top-header__search-input"
          placeholder="Search transactions, categories…"
          aria-label="Search"
        />
      </div>

      <div className="top-header__actions">
        {showDemoBadge && (
          <span className="badge badge--mock" title="Using local mock data">
            Demo data
          </span>
        )}
        <button type="button" className="top-header__chip" aria-label="Date range">
          <Calendar size={16} strokeWidth={1.75} />
          <span>Last 6 months</span>
        </button>
        <button type="button" className="top-header__icon-btn" aria-label="Notifications">
          <Bell size={18} strokeWidth={1.75} />
        </button>
        <div className="top-header__user">
          <div className="top-header__avatar" aria-hidden="true">
            US
          </div>
          <div className="top-header__user-text">
            <span className="top-header__user-name">User</span>
            <span className="top-header__user-role">Personal Account</span>
          </div>
        </div>
      </div>
    </header>
  );
}
