import { useNavigate } from 'react-router-dom'
import logoImg from '../images/class-emblems/Main-Logo.png'

const archetypes = [
  {
    name: 'Grimward',
    tagline: 'Body, Discipline, Endurance',
    description: 'Face every challenge head-on. Show up when the task is ugly.',
    classes: 'Knight, Berserker, Warden, Ronin',
    icon: '⚔️',
    color: '#DC2626',
  },
  {
    name: 'Ashborne',
    tagline: 'Mind, Strategy, Patience',
    description: 'Master what cannot be seen. Operate with precision and insight.',
    classes: 'Ninja, Alchemist, Phantom, Oracle',
    icon: '🌙',
    color: '#7C3AED',
  },
  {
    name: 'Goldveil',
    tagline: 'Spirit, Creation, Connection',
    description: 'Carry light into darkness. Build, inspire, and transform.',
    classes: 'Sage, Bard, Paladin, Mystic',
    icon: '✨',
    color: '#D97706',
  },
]

const statColors = {
  STR: '#D85A30',
  END: '#3B6D11',
  AGI: '#7C3AED',
  INT: '#0D9488',
  CHA: '#D4537E',
  WIL: '#D97706',
}

const features = [
  {
    title: 'Character Classes',
    description: '12 unique classes across 3 archetypes. Find your identity.',
  },
  {
    title: 'RPG Progression',
    description: 'Levels, ranks, stats, and guilds. Real progression that matters.',
  },
  {
    title: 'Social Accountability',
    description: 'Guild system with wars and boss events. Grow together.',
  },
  {
    title: 'Behavioral Integrity',
    description: 'Aura system that rewards consistency and penalizes shortcuts.',
  },
  {
    title: 'Narrative Layer',
    description: 'Lore chapters unlock as you rank up. A story worth telling.',
  },
  {
    title: 'AI-Powered',
    description: 'Smart quest suggestions powered by Gemini API.',
  },
]

export default function Landing() {
  const navigate = useNavigate()

  return (
    <div className="landing">
      {/* Navigation */}
      <nav className="landing-nav">
        <div className="nav-container">
          <div className="nav-logo">
            <img src={logoImg} alt="Crescendo Logo" className="logo-image" />
          </div>
          <div className="nav-links">
            <button onClick={() => navigate('/login')} className="nav-btn nav-login">
              Login
            </button>
            <button onClick={() => navigate('/signup')} className="nav-btn nav-signup">
              Sign Up
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1 className="hero-title">
            Your Self-Improvement Deserves an Epic Story
          </h1>
          <p className="hero-subtitle">
            Crescendo is the AI-powered RPG productivity platform that gamifies your growth.
            Choose your class, build your character, and watch yourself level up in real life.
          </p>
          <div className="hero-cta">
            <button className="cta-primary" onClick={() => navigate('/signup')}>
              Begin Your Awakening
            </button>
            <button className="cta-secondary" onClick={() => navigate('/login')}>
              Already a player? Login
            </button>
          </div>
        </div>
        <div className="hero-visual">
          <div className="hero-glow"></div>
          <div className="hero-card rpg-card">
            <div className="card-shine"></div>
            <div className="rpg-card-inner">
              {/* Rank Badge */}
              <div className="rpg-rank-badge">
                <span className="rpg-rank-letter">B</span>
                <span className="rpg-rank-label">RANK</span>
              </div>
              {/* Character Info */}
              <div className="rpg-char-info">
                <span className="rpg-class-label">Ronin · Grimward</span>
                <span className="rpg-level">Lv. 27</span>
              </div>
              {/* Stat Bars */}
              <div className="rpg-stats">
                {[
                  { name: 'STR', val: 82, fill: '82%' },
                  { name: 'INT', val: 65, fill: '65%' },
                  { name: 'WIL', val: 91, fill: '91%' },
                  { name: 'END', val: 74, fill: '74%' },
                ].map((stat) => (
                  <div 
                    key={stat.name} 
                    className="rpg-stat-row" 
                    style={{ 
                      '--stat-color': statColors[stat.name],
                      '--stat-glow': `${statColors[stat.name]}33`
                    }}
                  >
                    <span className="rpg-stat-name">{stat.name}</span>
                    <div className="rpg-stat-bar">
                      <div className="rpg-stat-fill" style={{ width: stat.fill }}></div>
                    </div>
                    <span className="rpg-stat-val">{stat.val}</span>
                  </div>
                ))}
              </div>
              {/* XP Bar */}
              <div className="rpg-xp-section">
                <div className="rpg-xp-label">
                  <span>XP</span>
                  <span>4,280 / 5,000</span>
                </div>
                <div className="rpg-xp-bar"><div className="rpg-xp-fill"></div></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <h2 className="section-title">Why Crescendo?</h2>
        <div className="features-grid">
          {features.map((feature, idx) => (
            <div key={idx} className="feature-card">
              <div className="feature-icon">{idx + 1}</div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Archetypes Section */}
      <section className="archetypes">
        <h2 className="section-title">Discover Your Archetype</h2>
        <div className="archetypes-grid">
          {archetypes.map((archetype, idx) => (
            <div 
              key={idx} 
              className="archetype-card"
              style={{ 
                '--archetype-color': archetype.color,
                '--archetype-glow': `${archetype.color}26`
              }}
            >
              <div className="archetype-header">
                <span className="archetype-icon">{archetype.icon}</span>
                <h3>{archetype.name}</h3>
              </div>
              <p className="archetype-tagline">{archetype.tagline}</p>
              <p className="archetype-description">{archetype.description}</p>
              <div className="archetype-classes">
                <strong>Classes:</strong> {archetype.classes}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Stats Preview */}
      <section className="stats-preview">
        <h2 className="section-title">Master the Six Stats</h2>
        <div className="stats-container">
          {[
            { name: 'STR', label: 'Strength' },
            { name: 'END', label: 'Endurance' },
            { name: 'AGI', label: 'Agility' },
            { name: 'INT', label: 'Intelligence' },
            { name: 'CHA', label: 'Charisma' },
            { name: 'WIL', label: 'Willpower' },
          ].map((stat, idx) => (
            <div 
              key={idx} 
              className="stat-badge"
              style={{ 
                '--stat-color': statColors[stat.name],
                '--stat-glow': `${statColors[stat.name]}33`
              }}
            >
              <div className="stat-value">{stat.name}</div>
              <div className="stat-label">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Progression Preview */}
      <section className="progression-preview">
        <h2 className="section-title">Two Paths to Mastery</h2>
        <div className="progression-grid">
          <div className="progression-card">
            <h3>Levels</h3>
            <p className="prog-subtitle">Measure of Activity</p>
            <p className="prog-description">
              Increase purely through XP. Every quest completed, every daily, every roadmap finished adds to your pool.
            </p>
            <div className="ranks-display">
              <span>🔵</span> E <span>→</span> D <span>→</span> C <span>→</span> B <span>→</span> A <span>→</span> S
            </div>
          </div>
          <div className="progression-card">
            <h3>Ranks</h3>
            <p className="prog-subtitle">Measure of Character</p>
            <p className="prog-description">
              Fill your Aura bar and hold it full for 14 consecutive days, then conquer the Rank-Up Ritual.
            </p>
            <div className="aura-bar">
              <div className="aura-fill"></div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-final">
        <div className="cta-content">
          <h2>The World Does Not Remember How It Began</h2>
          <p>Only that one day, certain people started hearing it.</p>
          <p className="cta-highlight">They called it the Crescendo.</p>
          <button className="cta-primary cta-large" onClick={() => navigate('/signup')}>
            Now Build It
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <p>&copy; 2026 Crescendo. Where self-improvement feels like an adventure.</p>
      </footer>
    </div>
  )
}
