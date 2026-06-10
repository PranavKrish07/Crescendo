import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { fetchProfile, fetchQuests, checkInUser, fetchActiveRitual, applyForRitual, fetchActiveRoadmaps, toggleRoadmapTask, breakOathRoadmap } from "../api/dashboard";
import QuestList from "../components/QuestList";
import CreateQuestModal from "../components/CreateQuestModal";
import RitualModal from "../components/RitualModal";
import { classEmblems } from "../utils/emblems";
import logoImg from "../images/class-emblems/Main-Logo.png";

const RANK_LABELS = {
  E: "E — Initiate",
  D: "D — Apprentice",
  C: "C — Adept",
  B: "B — Expert",
  A: "A — Master",
  S: "S — Sovereign",
};

const AURA_CAPS = {
  E: 900,
  D: 1600,
  C: 2500,
  B: 3200,
  A: 4200,
  S: "MAX"
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
  const [activeRoadmaps, setActiveRoadmaps] = useState([]);
  const [activeRitual, setActiveRitual] = useState({ active: false });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [isQuestModalOpen, setIsQuestModalOpen] = useState(false);
  const [isRitualModalOpen, setIsRitualModalOpen] = useState(false);
  const { logout } = useAuth();
  const navigate = useNavigate();

  const [geminiKeyModalOpen, setGeminiKeyModalOpen] = useState(false);
  const [tempKey, setTempKey] = useState('');

  const loadDashboardData = async () => {
    try {
      const [profileData, questsData, ritualData, roadmapsData] = await Promise.all([
        fetchProfile(),
        fetchQuests(),
        fetchActiveRitual(),
        fetchActiveRoadmaps()
      ]);
      setProfile(profileData);
      setQuests(questsData);
      setActiveRitual(ritualData);
      setActiveRoadmaps(roadmapsData);
      setActiveRitual(ritualData);
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

  const handleCheckIn = async () => {
    try {
      await checkInUser();
      loadDashboardData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleApplyRitual = async () => {
    try {
      await applyForRitual();
      loadDashboardData();
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to apply for ritual');
    }
  };

  const handleToggleRoadmapTask = async (roadmapId, taskIndex) => {
    try {
      const res = await toggleRoadmapTask(roadmapId, taskIndex);
      if (res.completed) {
        alert("Roadmap Completed! Growth Points and Aura Awarded.");
      }
      loadDashboardData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleBreakOath = async (roadmapId) => {
    if (!window.confirm("Are you sure you want to break this oath? You will suffer a severe Aura penalty!")) return;
    try {
      await breakOathRoadmap(roadmapId);
      loadDashboardData();
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to break oath');
    }
  };

  const RITUAL_DAYS_REQUIRED = { E: 7, D: 10, C: 14, B: 21, A: 30 };
  const reqDays = RITUAL_DAYS_REQUIRED[profile?.rank] || 7;
  const isAuraCapped = profile?.aura >= profile?.aura_cap;
  const canApplyRitual = isAuraCapped && profile?.days_at_aura_cap >= reqDays;

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
          <button className="dashboard-nav-btn" onClick={() => navigate("/roadmaps")}>Open Roadmaps</button>
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
          <div className="dashboard-profile-info" style={{ width: '100%' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
              <div>
                <h1 className="dashboard-profile-name">{profile.name}</h1>
                <p className="dashboard-profile-class" style={{ color: accentColor }}>
                  {profile.char_class} <span className="dashboard-profile-archetype">• {profile.archetype}</span>
                </p>
                <p className="dashboard-profile-email">{profile.email}</p>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '0.5rem' }}>
                <div style={{ background: 'rgba(0,0,0,0.3)', padding: '0.5rem 1rem', borderRadius: '8px', border: `1px solid ${accentColor}40`, display: 'flex', gap: '1rem' }}>
                  <span title="Current Streak" style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#f97316' }}>
                    🔥 {profile.streak || 0}
                  </span>
                  <span title="Streak Freezes Available" style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#38bdf8' }}>
                    ❄️ {profile.streak_freezes || 0}/2
                  </span>
                </div>
                <button 
                  onClick={handleCheckIn}
                  disabled={profile.last_checkin === new Date().toLocaleDateString('en-CA')}
                  style={{
                    background: profile.last_checkin === new Date().toLocaleDateString('en-CA') ? 'rgba(255,255,255,0.1)' : accentColor,
                    color: profile.last_checkin === new Date().toLocaleDateString('en-CA') ? 'gray' : '#fff',
                    border: 'none',
                    padding: '0.4rem 1rem',
                    borderRadius: '4px',
                    cursor: profile.last_checkin === new Date().toLocaleDateString('en-CA') ? 'not-allowed' : 'pointer',
                    fontWeight: 'bold',
                    transition: 'all 0.2s',
                    width: '100%'
                  }}
                >
                  {profile.last_checkin === new Date().toLocaleDateString('en-CA') ? 'Checked In Today' : 'Daily Check-In'}
                </button>
              </div>
            </div>
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
            <div className="dashboard-level-row" style={{ marginTop: '1.2rem' }}>
              <span className="dashboard-level-tag" style={{ background: 'transparent', border: '1px solid var(--border)' }}>Aura</span>
              <span className="dashboard-exp-text">
                {profile.aura} {AURA_CAPS[profile.rank] !== "MAX" ? `/ ${AURA_CAPS[profile.rank]}` : ' (MAX)'}
              </span>
            </div>
            {AURA_CAPS[profile.rank] !== "MAX" && (
              <div className="dashboard-exp-track" style={{ height: '4px', marginBottom: '1rem' }}>
                <div 
                  className="dashboard-exp-fill" 
                  style={{ 
                    width: `${Math.min((profile.aura / AURA_CAPS[profile.rank]) * 100, 100)}%`, 
                    background: accentColor, 
                    opacity: 0.8 
                  }}>
                </div>
              </div>
            )}
            
            {activeRitual?.active ? (
              <button 
                onClick={() => setIsRitualModalOpen(true)}
                style={{
                  background: 'transparent',
                  color: accentColor,
                  border: `1px solid ${accentColor}`,
                  padding: '0.5rem 1rem',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontWeight: 'bold',
                  width: '100%',
                  marginTop: '0.5rem'
                }}
              >
                View Active Ritual
              </button>
            ) : (
              isAuraCapped && profile.rank !== 'S' && (
                <div style={{ marginTop: '0.5rem' }}>
                  <p style={{ fontSize: '0.8rem', color: 'gray', marginBottom: '0.5rem', textAlign: 'center' }}>
                    Hold Aura cap for {reqDays} days. ({profile.days_at_aura_cap}/{reqDays})
                  </p>
                  <button 
                    onClick={handleApplyRitual}
                    disabled={!canApplyRitual}
                    style={{
                      background: canApplyRitual ? accentColor : 'rgba(255,255,255,0.1)',
                      color: canApplyRitual ? '#fff' : 'gray',
                      border: 'none',
                      padding: '0.5rem 1rem',
                      borderRadius: '4px',
                      cursor: canApplyRitual ? 'pointer' : 'not-allowed',
                      fontWeight: 'bold',
                      width: '100%'
                    }}
                  >
                    Apply for Ritual
                  </button>
                </div>
              )
            )}
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
              {Object.entries(profile.growth_points).map(([stat, val]) => {
                const getStatRankInfo = (v) => {
                  if (v >= 575) return { rank: 'S', next: 'MAX', progress: 100 };
                  if (v >= 275) return { rank: 'A', next: 575, progress: ((v - 275) / 300) * 100 };
                  if (v >= 125) return { rank: 'B', next: 275, progress: ((v - 125) / 150) * 100 };
                  if (v >= 55)  return { rank: 'C', next: 125, progress: ((v - 55) / 70) * 100 };
                  if (v >= 20)  return { rank: 'D', next: 55,  progress: ((v - 20) / 35) * 100 };
                  if (v >= 5)   return { rank: 'E', next: 20,  progress: ((v - 5) / 15) * 100 };
                  return { rank: 'None', next: 5, progress: (v / 5) * 100 };
                };
                const rankInfo = getStatRankInfo(val);

                return (
                  <div className="dashboard-stat-bar" key={stat} style={{ alignItems: 'center' }}>
                    <span className="dashboard-stat-icon">{STAT_ICONS[stat]}</span>
                    <span className="dashboard-stat-label" style={{ width: '30px' }}>{stat}</span>
                    <span style={{
                      display: 'inline-block',
                      width: '24px',
                      textAlign: 'center',
                      background: 'rgba(255,255,255,0.1)',
                      borderRadius: '4px',
                      fontSize: '0.7rem',
                      fontWeight: 'bold',
                      color: rankInfo.rank === 'None' ? 'gray' : 'var(--primary-light)',
                      marginRight: '0.5rem',
                      padding: '2px 0'
                    }}>{rankInfo.rank !== 'None' ? rankInfo.rank : '-'}</span>
                    
                    <div className="dashboard-stat-track" style={{ flex: 1 }}>
                      <div
                        className="dashboard-stat-fill"
                        style={{
                          width: `${rankInfo.progress}%`,
                          background: `var(--primary-light)`,
                        }}
                      ></div>
                    </div>
                    <span className="dashboard-stat-val" style={{ width: '45px', textAlign: 'right', fontSize: '0.75rem' }}>
                      {val}{rankInfo.next !== 'MAX' ? `/${rankInfo.next}` : ''}
                    </span>
                  </div>
                );
              })}
            </div>
          </section>
        </div>
        {/* ── Active Roadmaps ── */}
        {activeRoadmaps.length > 0 && (
          <section className="dashboard-card dashboard-roadmaps-section" style={{ marginBottom: '2rem' }}>
            <h3 className="dashboard-card-title">Active Roadmaps</h3>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: "1.5rem" }}>
              {activeRoadmaps.map(r => (
                <div key={r.id} style={{ background: "var(--bg-tertiary)", border: "1px solid var(--border)", borderRadius: "8px", padding: "1rem" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "0.5rem" }}>
                    <h4 style={{ color: "var(--text-primary)", margin: 0 }}>{r.title}</h4>
                    <span style={{ fontSize: "0.75rem", color: "#f59e0b", fontWeight: "bold" }}>+{r.reward} GP</span>
                  </div>
                  
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
                    <p style={{ fontSize: "0.8rem", color: "var(--text-tertiary)", margin: 0 }}>
                      Deadline: {new Date(r.deadline).toLocaleDateString()}
                    </p>
                    <button 
                      onClick={() => handleBreakOath(r.id)}
                      className="break-oath-btn"
                      title="Break Oath (Aura Penalty)"
                    >
                      Break Oath
                    </button>
                  </div>

                  {/* Progress Bar */}
                  <div style={{ height: "4px", background: "rgba(255,255,255,0.1)", borderRadius: "2px", marginBottom: "1rem", overflow: "hidden" }}>
                    <div style={{ 
                      height: "100%", 
                      background: accentColor, 
                      width: `${(r.progress.filter(Boolean).length / r.progress.length) * 100}%`,
                      transition: "width 0.3s ease"
                    }} />
                  </div>
                  
                  <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem", maxHeight: "200px", overflowY: "auto", paddingRight: "0.5rem" }}>
                    {r.tasks.map((taskStr, idx) => (
                      <div key={idx} style={{ display: "flex", alignItems: "flex-start", gap: "0.8rem" }}>
                        <input 
                          type="checkbox" 
                          className="custom-checkbox"
                          checked={r.progress[idx]} 
                          onChange={() => handleToggleRoadmapTask(r.id, idx)}
                          style={{ '--chk-color': accentColor, marginTop: "0.1rem" }}
                        />
                        <span style={{ 
                          fontSize: "0.85rem", 
                          color: r.progress[idx] ? "gray" : "var(--text-secondary)",
                          textDecoration: r.progress[idx] ? "line-through" : "none",
                          lineHeight: "1.4"
                        }}>
                          {taskStr}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

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

      {isRitualModalOpen && (
        <RitualModal
          isOpen={isRitualModalOpen}
          onClose={() => setIsRitualModalOpen(false)}
          activeRitual={activeRitual}
          profile={profile}
        />
      )}

    </div>
  );
}
