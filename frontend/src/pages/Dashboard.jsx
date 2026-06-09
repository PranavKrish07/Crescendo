import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { fetchProfile, fetchQuests } from "../api/dashboard";
import QuestList from "../components/QuestList";
import CreateQuestModal from "../components/CreateQuestModal";
import { classEmblems } from "../utils/emblems";
import logoImg from "../images/class-emblems/Main-Logo.png";

const RANK_LABELS = {
  E: "E — Unranked",
  D: "D — Novice",
  C: "C — Apprentice",
  B: "B — Adept",
  A: "A — Elite",
  S: "S — Sovereign",
};

const STAT_ICONS = {
  STR: "⚔️",
  END: "🛡️",
  AGI: "⚡",
  INT: "🧠",
  CHA: "💬",
  WIL: "🔥",
};

export default function Dashboard() {
  const [profile, setProfile] = useState(null);
  const [quests, setQuests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [isQuestModalOpen, setIsQuestModalOpen] = useState(false);
  const { logout } = useAuth();
  const navigate = useNavigate();

  const [geminiKeyModalOpen, setGeminiKeyModalOpen] = useState(false);
  const [tempKey, setTempKey] = useState('');

  const loadDashboardData = async () => {
    try {
      const [profileData, questsData] = await Promise.all([
        fetchProfile(),
        fetchQuests()
      ]);
      setProfile(profileData);
      setQuests(questsData);
    } catch (err) {
      setError("Failed to load profile and quests.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
    const storedKey = localStorage.getItem('geminiApiKey');
    if (storedKey) setTempKey(storedKey);
  }, []);

  const handleSaveGeminiKey = () => {
    localStorage.setItem('geminiApiKey', tempKey);
    setGeminiKeyModalOpen(false);
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="dashboard-loading">
          <div className="awakening-loading-spinner"></div>
          <p>Loading your profile...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-container">
        <div className="dashboard-error">
          <p>{error}</p>
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginTop: '1rem' }}>
            <button className="quest-btn-primary" onClick={() => window.location.reload()}>Retry</button>
            <button className="quest-btn-secondary" onClick={logout}>Log Out</button>
          </div>
        </div>
      </div>
    );
  }

  const archetypeColors = {
    Grimward: "#DC2626",
    Ashborne: "#7C3AED",
    Goldveil: "#F59E0B",
  };
  const accentColor = archetypeColors[profile.archetype] || "#0D9488";
  const emblemSrc = classEmblems[profile.char_class] || logoImg;

  const expForNextLevel = profile.max_exp || 100;
  const expPercent = Math.min((profile.exp / expForNextLevel) * 100, 100);

  return (
    <div className="dashboard-container">
      {/* ── Top Bar ── */}
      <header className="dashboard-header">
        <img src={logoImg} alt="Crescendo" className="dashboard-logo" />
        <nav className="dashboard-nav">
          <button className="dashboard-nav-btn" onClick={() => setGeminiKeyModalOpen(true)}>Gemini API</button>
          <button className="dashboard-nav-btn" onClick={() => navigate("/my-class")}>My Class</button>
          <button className="dashboard-nav-btn dashboard-nav-btn--logout" onClick={logout}>Log Out</button>
        </nav>
      </header>

      {/* ── Main Content ── */}
      <div className="dashboard-content">

        {/* ── Profile Card ── */}
        <section className="dashboard-profile-card" style={{ "--accent": accentColor }}>
          <div className="dashboard-profile-emblem">
            <img src={emblemSrc} alt={profile.char_class} />
          </div>
          <div className="dashboard-profile-info">
            <h1 className="dashboard-profile-name">{profile.name}</h1>
            <p className="dashboard-profile-class" style={{ color: accentColor }}>
              {profile.char_class} <span className="dashboard-profile-archetype">• {profile.archetype}</span>
            </p>
            <p className="dashboard-profile-email">{profile.email}</p>
          </div>
        </section>

        {/* ── Stats Row ── */}
        <div className="dashboard-stats-row">

          {/* Rank & Level Card */}
          <section className="dashboard-card dashboard-rank-card" style={{ "--accent": accentColor }}>
            <div className="dashboard-rank-badge" style={{ borderColor: accentColor, color: accentColor }}>
              {profile.rank}
            </div>
            <p className="dashboard-rank-label">{RANK_LABELS[profile.rank] || profile.rank}</p>
            <div className="dashboard-level-row">
              <span className="dashboard-level-tag">Lv. {profile.level}</span>
              <span className="dashboard-exp-text">{profile.exp} / {expForNextLevel} EXP</span>
            </div>
            <div className="dashboard-exp-track">
              <div className="dashboard-exp-fill" style={{ width: `${expPercent}%`, background: accentColor }}></div>
            </div>
            <p className="dashboard-aura-text">Aura: <strong>{profile.aura}</strong></p>
          </section>

          {/* Base Stats Card */}
          <section className="dashboard-card dashboard-base-stats-card">
            <h3 className="dashboard-card-title">Base Stats</h3>
            <div className="dashboard-stat-bars">
              {Object.entries(profile.scores).map(([stat, val]) => (
                <div className="dashboard-stat-bar" key={stat}>
                  <span className="dashboard-stat-icon">{STAT_ICONS[stat]}</span>
                  <span className="dashboard-stat-label">{stat}</span>
                  <div className="dashboard-stat-track">
                    <div
                      className="dashboard-stat-fill"
                      style={{
                        width: `${Math.min((val / 15) * 100, 100)}%`,
                        background: accentColor,
                      }}
                    ></div>
                  </div>
                  <span className="dashboard-stat-val">{val}</span>
                </div>
              ))}
            </div>
          </section>

          {/* Growth Points Card */}
          <section className="dashboard-card dashboard-growth-card">
            <h3 className="dashboard-card-title">Growth Points</h3>
            <div className="dashboard-stat-bars">
              {Object.entries(profile.growth_points).map(([stat, val]) => (
                <div className="dashboard-stat-bar" key={stat}>
                  <span className="dashboard-stat-icon">{STAT_ICONS[stat]}</span>
                  <span className="dashboard-stat-label">{stat}</span>
                  <div className="dashboard-stat-track">
                    <div
                      className="dashboard-stat-fill"
                      style={{
                        width: `${Math.min((val / 50) * 100, 100)}%`,
                        background: `var(--primary-light)`,
                      }}
                    ></div>
                  </div>
                  <span className="dashboard-stat-val">{val}</span>
                </div>
              ))}
            </div>
          </section>
        </div>

        {/* ── Quests Hub ── */}
        <section className="dashboard-card dashboard-quests-section">
          <div className="quests-header">
            <h3 className="dashboard-card-title" style={{ marginBottom: 0 }}>Active Quests</h3>
            <button className="quest-btn-primary" onClick={() => setIsQuestModalOpen(true)}>+ Create Quest</button>
          </div>
          <div className="quests-content">
            <QuestList quests={quests} onQuestUpdate={loadDashboardData} accentColor={accentColor} />
          </div>
        </section>

      </div>
      
      <CreateQuestModal 
        isOpen={isQuestModalOpen} 
        onClose={() => setIsQuestModalOpen(false)} 
        onCreated={loadDashboardData} 
      />

      {geminiKeyModalOpen && (
        <div className="modal-overlay" style={{ zIndex: 2000 }}>
          <div className="modal-content quest-modal" style={{ maxWidth: '400px' }}>
            <button className="modal-close" onClick={() => setGeminiKeyModalOpen(false)}>×</button>
            <h3 style={{ marginBottom: '1rem', color: 'var(--primary-light)', fontSize: '1.3rem' }}>Gemini AI Configuration</h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '1.5rem', lineHeight: '1.5' }}>
              Bring Your Own Key (BYOK) to enable AI task generation. Your key is stored securely in your browser's local storage.
            </p>
            <div className="form-group" style={{ marginBottom: '0.5rem' }}>
              <label style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)', textTransform: 'uppercase' }}>API Key</label>
              <input 
                type="password" 
                value={tempKey} 
                onChange={(e) => setTempKey(e.target.value)} 
                placeholder="AIzaSy..." 
                style={{ width: '100%', padding: '0.75rem', background: 'rgba(0,0,0,0.3)', border: '1px solid var(--border)', borderRadius: '4px', color: 'var(--text-primary)' }}
              />
            </div>
            <button 
              className="quest-btn-primary" 
              onClick={handleSaveGeminiKey}
              style={{ width: '100%', marginTop: '1.5rem', padding: '0.75rem', fontSize: '0.9rem' }}
            >
              Save Key
            </button>
          </div>
        </div>
      )}

    </div>
  );
}
