import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/axios";
import logoImg from "../images/class-emblems/Main-Logo.png";
import { classEmblems } from "../utils/emblems";
import { archetypes, classes } from "../utils/classData";

export default function MyClass() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await API.get("/me/");
        setProfile(res.data);
      } catch (err) {
        setError("Failed to load your class data.");
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  if (loading) {
    return (
      <div className="awakening-container">
        <div className="awakening-loading">
          <div className="awakening-loading-spinner"></div>
          <p>Loading your profile...</p>
        </div>
      </div>
    );
  }

  if (error || !profile?.awakening_done) {
    return (
      <div className="awakening-container">
        <div className="awakening-error">
          <p>{error || "You haven't completed The Awakening yet."}</p>
          <button onClick={() => navigate("/awakening")}>Go to Awakening</button>
        </div>
      </div>
    );
  }

  const archetypeColors = {
    Grimward: "#DC2626",
    Ashborne: "#7C3AED",
    Goldveil: "#F59E0B",
  };
  const glowColor = archetypeColors[profile.archetype] || "#0D9488";
  const emblemSrc = classEmblems[profile.char_class] || logoImg;
  
  const archetypeData = archetypes[profile.archetype];
  const classData = classes[profile.char_class];

  return (
    <div className="awakening-container" style={{ padding: '40px 20px', alignItems: 'flex-start' }}>
      <div className="result-screen dossier-layout">
        
        <div className="dossier-header">
          <div className="result-emblem-frame" style={{ "--result-color": glowColor }}>
            <img src={emblemSrc} alt={profile.char_class} className="result-emblem" />
          </div>
          <div className="dossier-title-block">
            <p className="result-label">Your Class</p>
            <h1 className="result-class" style={{ color: glowColor }}>
              {profile.char_class}
            </h1>
            <p className="result-archetype">
              House of <span style={{ color: glowColor }}>{profile.archetype}</span>
            </p>
          </div>
        </div>

        <div className="result-scores dossier-scores">
          {Object.entries(profile.scores).map(([stat, val]) => (
            <div className="result-score-bar" key={stat}>
              <span className="result-score-label">{stat}</span>
              <div className="result-score-track">
                <div
                  className="result-score-fill"
                  style={{
                    width: `${Math.min((val / 15) * 100, 100)}%`,
                    background: glowColor,
                  }}
                ></div>
              </div>
              <span className="result-score-val">{val}</span>
            </div>
          ))}
        </div>

        {archetypeData && (
          <div className="lore-section" style={{ borderLeftColor: glowColor }}>
            <h3 style={{ color: glowColor }}>The Archetype</h3>
            <p className="lore-text">{archetypeData.description}</p>
          </div>
        )}

        {classData && (
          <div className="lore-section" style={{ borderLeftColor: glowColor }}>
            <h3 style={{ color: glowColor }}>Class Lore</h3>
            <p className="lore-text">{classData.lore}</p>
            
            <h3 style={{ color: glowColor, marginTop: '2rem' }}>Path to Mastery</h3>
            <ul className="tips-list">
              {classData.tips.map((tip, idx) => {
                const parts = tip.split(': ');
                const boldPart = parts[0];
                const rest = parts.slice(1).join(': ');
                return (
                  <li key={idx}>
                    <strong style={{ color: glowColor }}>{boldPart}:</strong> {rest || boldPart}
                  </li>
                );
              })}
            </ul>
          </div>
        )}

        <button className="result-enter-btn" onClick={() => navigate("/dashboard")} style={{ marginTop: '2rem' }}>
          Go to Dashboard
        </button>
      </div>
    </div>
  );
}
