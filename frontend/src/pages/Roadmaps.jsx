import { useEffect, useState } from "react";
import { fetchRoadmapTemplates, registerRoadmap, fetchProfile, fetchActiveRoadmaps } from "../api/dashboard";
import { useNavigate } from "react-router-dom";

export default function Roadmaps() {
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [deadline, setDeadline] = useState("");
  const navigate = useNavigate();

  const [profile, setProfile] = useState(null);
  const [activeIds, setActiveIds] = useState([]);

  useEffect(() => {
    Promise.all([
      fetchRoadmapTemplates(),
      fetchProfile(),
      fetchActiveRoadmaps()
    ])
      .then(([templatesData, profileData, activeData]) => {
        setTemplates(templatesData);
        setProfile(profileData);
        setActiveIds(activeData.map(r => r.template_id));
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const handleRegister = async () => {
    if (!deadline) {
      alert("Please select a deadline.");
      return;
    }
    try {
      await registerRoadmap(selectedTemplate.id, deadline);
      setSelectedTemplate(null);
      setDeadline("");
      navigate("/"); // Redirect to dashboard to see active roadmap
    } catch (err) {
      alert(err.response?.data?.error || "Failed to register roadmap");
    }
  };

  if (loading) {
    return <div style={{ padding: "2rem", color: "var(--text-secondary)" }}>Loading Roadmaps...</div>;
  }

  const getDifficultyColor = (diff) => {
    switch(diff) {
      case 'EASY': return '#10b981';
      case 'MEDIUM': return '#f59e0b';
      case 'HARD': return '#ef4444';
      default: return '#3b82f6';
    }
  };

  const archetypeColors = {
    Grimward: "#DC2626",
    Ashborne: "#7C3AED",
    Goldveil: "#F59E0B",
  };
  const accentColor = profile ? (archetypeColors[profile.archetype] || "#0D9488") : "#0D9488";

  return (
    <div style={{ padding: "2rem", maxWidth: "1200px", margin: "0 auto" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "2rem" }}>
        <h1 style={{ color: "var(--text-primary)", fontSize: "2rem" }}>Grand Roadmaps</h1>
        <button 
          className="roadmap-back-btn"
          onClick={() => navigate("/")}
        >
          Back to Dashboard
        </button>
      </div>

      <p style={{ color: "var(--text-secondary)", marginBottom: "2rem" }}>
        Commit to a Grand Roadmap to massively boost your Growth Points. Roadmaps are grueling marathons. Choose wisely.
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))", gap: "2rem" }}>
        {templates.map(t => (
          <div key={t.id} className="roadmap-card">
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "1.2rem" }}>
              <span style={{ 
                background: "rgba(13, 148, 136, 0.15)", 
                color: "var(--primary-light)", 
                padding: "0.3rem 0.8rem", 
                borderRadius: "6px", 
                fontSize: "0.85rem", 
                fontWeight: "800",
                letterSpacing: "0.05em",
                border: "1px solid rgba(13, 148, 136, 0.3)"
              }}>
                {t.stat}
              </span>
              <span style={{ 
                color: getDifficultyColor(t.difficulty), 
                fontSize: "0.85rem", 
                fontWeight: "800",
                letterSpacing: "0.05em",
                textShadow: `0 0 10px ${getDifficultyColor(t.difficulty)}40`
              }}>
                {t.difficulty}
              </span>
            </div>
            
            <h3 style={{ color: "var(--text-primary)", fontSize: "1.3rem", marginBottom: "0.8rem", letterSpacing: "0.02em" }}>{t.title}</h3>
            <p style={{ color: "var(--text-secondary)", fontSize: "0.95rem", lineHeight: "1.5", flexGrow: 1, marginBottom: "1.5rem" }}>
              {t.description}
            </p>

            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderTop: "1px solid var(--border)", paddingTop: "1.2rem", marginBottom: "1.5rem" }}>
              <span style={{ color: "var(--text-tertiary)", fontSize: "0.9rem" }}>
                Tasks: <strong style={{ color: "var(--text-primary)" }}>{t.tasks.length}</strong>
              </span>
              <span style={{ color: "#f59e0b", fontSize: "0.9rem", fontWeight: "800", textShadow: "0 0 10px rgba(245, 158, 11, 0.3)" }}>
                +{t.reward} Growth Points
              </span>
            </div>

            <button 
              className="roadmap-btn"
              onClick={() => setSelectedTemplate(t)}
              disabled={activeIds.includes(t.id)}
              style={activeIds.includes(t.id) ? { filter: 'grayscale(1)', opacity: 0.5, cursor: 'not-allowed' } : {}}
            >
              {activeIds.includes(t.id) ? 'Active' : 'Take the Oath'}
            </button>
          </div>
        ))}
      </div>

      {selectedTemplate && (
        <div 
          className="modal-overlay" 
          onClick={(e) => {
            if (e.target === e.currentTarget) setSelectedTemplate(null);
          }}
        >
          <div className="modal-content quest-modal" style={{ border: `1px solid ${accentColor}`, boxShadow: `0 0 20px ${accentColor}30` }}>
            <button className="modal-close" onClick={() => setSelectedTemplate(null)}>×</button>
            <h2 style={{ textShadow: `0 0 10px ${accentColor}50` }}>Register Roadmap</h2>
            <p style={{ color: "var(--text-secondary)", marginBottom: "1.5rem", fontSize: "0.9rem", lineHeight: "1.5" }}>
              You are about to commit to <strong style={{ color: accentColor }}>{selectedTemplate.title}</strong>. When do you vow to complete this by?
            </p>
            <div className="quest-form">
              <div className="form-group" style={{ marginBottom: "2rem" }}>
                <label style={{ color: accentColor }}>Deadline</label>
                <input 
                  type="date" 
                  value={deadline}
                  onChange={e => setDeadline(e.target.value)}
                  style={{ borderColor: accentColor }}
                />
              </div>
              <div style={{ display: "flex", gap: "1rem", marginTop: "1rem" }}>
                <button className="quest-btn-secondary flex-1" onClick={() => setSelectedTemplate(null)}>Cancel</button>
                <button 
                  className="quest-btn-primary flex-1" 
                  onClick={handleRegister}
                  style={{ background: accentColor, borderColor: accentColor, boxShadow: `0 4px 15px ${accentColor}40` }}
                >
                  Confirm Registration
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
