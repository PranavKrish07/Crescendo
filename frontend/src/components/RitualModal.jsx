import React, { useState, useEffect } from 'react';

const RITUAL_LORE = {
  'D': {
    title: 'The First Oath',
    duration: 7,
    requirements: [
      'Complete 5 daily quests in a row without missing one',
      'Finish 1 active roadmap fully',
      'Log in for 7 consecutive days',
      "Write a reflection entry: 'Why I am beginning this journey'"
    ]
  },
  'C': {
    title: 'The Trial of Habit',
    duration: 10,
    requirements: [
      'Maintain a 10-day streak with zero breaks',
      'Complete 2 roadmaps back to back',
      'Complete 1 co-op task with a guild member',
      'Reach level 20 within current rank',
      'Aura must not dip below 500 during the ritual window'
    ]
  },
  'B': {
    title: 'The Proving Ground',
    duration: 14,
    requirements: [
      'Complete a full boss event with your guild',
      'Complete 3 roadmaps in the ritual window',
      'Achieve a 14-day streak — no streak shields allowed',
      'Earn at least 500 Aura points during the ritual window'
    ]
  },
  'A': {
    title: 'The Crucible',
    duration: 21,
    requirements: [
      'Complete 5 roadmaps in the ritual window',
      'Maintain Aura above 750 for the entire 21-day window',
      'Win a guild war during the ritual period',
      'Complete 15 daily quests without missing one',
      'Help a guild member complete their own roadmap'
    ]
  },
  'S': {
    title: "The Sovereign's Ascent",
    duration: 30,
    requirements: [
      'Complete 10 roadmaps — at least 3 user-created',
      'Hold Aura at full cap for 30 days — zero dips',
      'Complete 2 boss events with your guild',
      'Win 1 guild war as guild leader',
      'Achieve a 30-day streak — no shields, no breaks',
      'Complete 25 daily quests in the window'
    ]
  }
};

export default function RitualModal({ isOpen, onClose, activeRitual, profile }) {
  const [timeLeft, setTimeLeft] = useState('');

  useEffect(() => {
    if (!activeRitual || !activeRitual.expires_at) return;
    
    const calculateTimeLeft = () => {
      const end = new Date(activeRitual.expires_at).getTime();
      const now = new Date().getTime();
      const diff = end - now;
      
      if (diff <= 0) {
        setTimeLeft('EXPIRED');
        return;
      }
      
      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      setTimeLeft(`${days}d ${hours}h ${mins}m`);
    };

    calculateTimeLeft();
    const interval = setInterval(calculateTimeLeft, 60000);
    return () => clearInterval(interval);
  }, [activeRitual]);

  if (!isOpen || !activeRitual || !activeRitual.active) return null;

  const lore = RITUAL_LORE[activeRitual.target_rank];

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()} style={{ maxWidth: '600px', border: '1px solid var(--primary-light)', boxShadow: '0 0 40px rgba(139, 92, 246, 0.2)' }}>
        
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h2 style={{ color: 'var(--primary-light)', textTransform: 'uppercase', letterSpacing: '2px', fontSize: '1.5rem', margin: '0' }}>
            {lore.title}
          </h2>
          <p style={{ color: 'var(--text-tertiary)', marginTop: '0.5rem', fontSize: '0.9rem' }}>
            Rank Up Ritual to {activeRitual.target_rank}
          </p>
        </div>

        <div style={{ background: 'rgba(0,0,0,0.3)', padding: '1.5rem', borderRadius: '8px', border: '1px solid var(--border)', marginBottom: '2rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', borderBottom: '1px solid var(--border)', paddingBottom: '1rem' }}>
            <span style={{ color: 'var(--text-secondary)' }}>Time Remaining</span>
            <span style={{ color: '#ef4444', fontWeight: 'bold', fontSize: '1.2rem', fontFamily: 'monospace' }}>
              {timeLeft}
            </span>
          </div>
          
          <h3 style={{ fontSize: '1rem', marginBottom: '1rem', color: 'var(--text-primary)' }}>Ritual Requirements</h3>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
            {lore.requirements.map((req, idx) => (
              <div key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.8rem' }}>
                <div style={{ 
                  minWidth: '20px', 
                  height: '20px', 
                  borderRadius: '4px', 
                  border: '1px solid var(--text-tertiary)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  marginTop: '2px'
                }}>
                  {/* Empty checkbox for now since backend states aren't tracked yet */}
                </div>
                <p style={{ margin: 0, color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: '1.4' }}>
                  {req}
                </p>
              </div>
            ))}
          </div>
        </div>

        <p style={{ fontSize: '0.8rem', color: '#ef4444', textAlign: 'center', marginBottom: '1.5rem' }}>
          Warning: Failure to complete all requirements before the deadline will result in an Aura penalty and a 7-day lockout.
        </p>

        <div className="modal-actions" style={{ justifyContent: 'center' }}>
          <button className="modal-btn submit" onClick={onClose} style={{ width: '100%', maxWidth: '200px' }}>
            Continue
          </button>
        </div>

      </div>
    </div>
  );
}
