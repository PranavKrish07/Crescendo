import React, { useState } from 'react';
import { setQuestAsDaily, toggleSubtask, addSubtask, deleteSubtask, deleteQuest } from '../api/dashboard';
import { GoogleGenerativeAI } from '@google/generative-ai';

export default function QuestList({ quests, onQuestUpdate, accentColor }) {
  const [activeQuest, setActiveQuest] = useState(null);
  const [newTaskInput, setNewTaskInput] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const handleToggleSubtask = async (subtaskId) => {
    try {
      const res = await toggleSubtask(subtaskId);
      if (res.quest_completed) {
        // Automatically handled by updating the quest list
      }
      onQuestUpdate();
      
      // Update local modal state optimistically
      if (activeQuest) {
        const updatedTasks = activeQuest.subtasks.map(st => 
          st.id === subtaskId ? { ...st, is_completed: res.is_completed } : st
        );
        const updatedQuest = { ...activeQuest, subtasks: updatedTasks };
        if (res.quest_completed) {
          updatedQuest.status = 'COMPLETED';
        }
        setActiveQuest(updatedQuest);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleSetDaily = async (e, questId) => {
    e.stopPropagation();
    try {
      await setQuestAsDaily(questId);
      onQuestUpdate();
      if (activeQuest && activeQuest.id === questId) {
        setActiveQuest({ ...activeQuest, is_daily: true });
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddTask = async (questId) => {
    if (!newTaskInput || newTaskInput.trim() === '') return;
    
    try {
      await addSubtask(questId, newTaskInput);
      setNewTaskInput('');
      onQuestUpdate();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteTask = async (subtaskId) => {
    try {
      await deleteSubtask(subtaskId);
      onQuestUpdate();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteQuest = async (questId) => {
    if (window.confirm("Are you sure you want to delete this quest? If deleted before completion, you won't receive any rewards! (Completed quest rewards remain intact).")) {
      try {
        await deleteQuest(questId);
        setActiveQuest(null);
        onQuestUpdate();
      } catch (err) {
        console.error(err);
      }
    }
  };

  const handleGenerateTasksForExisting = async () => {
    const apiKey = localStorage.getItem('geminiApiKey');
    if (!apiKey) {
      alert('Please set your Gemini API Key in the dashboard header first.');
      return;
    }
    
    setIsGenerating(true);
    try {
      const genAI = new GoogleGenerativeAI(apiKey);
      const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });
      
      const prompt = `I have a quest titled "${activeQuest.title}". 
Generate a list of tasks needed to complete this quest. 
Predict its difficulty and add that many tasks (Easy: 1-6 tasks, Medium: 7-12 tasks, Hard: 13+ tasks). 
Return ONLY a valid JSON array of strings representing the task descriptions, without any markdown formatting.`;

      let result;
      let retries = 3;
      while (retries > 0) {
        try {
          result = await model.generateContent(prompt);
          break;
        } catch (err) {
          if (retries === 1) throw err;
          if (err?.status === 503 || err?.status === 429 || err?.message?.toLowerCase().includes('demand') || err?.message?.toLowerCase().includes('overloaded')) {
            retries--;
            await new Promise(r => setTimeout(r, 2000));
          } else {
            throw err;
          }
        }
      }

      const response = await result.response;
      let text = response.text();
      text = text.replace(/```json/g, '').replace(/```/g, '').trim();
      const generatedTasks = JSON.parse(text);
      
      if (Array.isArray(generatedTasks)) {
        for (const taskDesc of generatedTasks) {
          await addSubtask(activeQuest.id, taskDesc);
        }
        onQuestUpdate();
      } else {
        alert('AI returned invalid format.');
      }
    } catch (err) {
      alert('Failed to generate tasks: ' + err.message + '. If the model is overloaded, please try again in a few seconds.');
    } finally {
      setIsGenerating(false);
    }
  };

  // Sync active quest when quests prop changes
  React.useEffect(() => {
    if (activeQuest) {
      const updated = quests.find(q => q.id === activeQuest.id);
      if (updated) {
        setActiveQuest(updated);
      } else {
        setActiveQuest(null);
      }
    }
  }, [quests]);

  if (!quests || quests.length === 0) {
    return <p className="quest-empty">No active quests. Create one to begin your journey!</p>;
  }

  return (
    <div className="quest-list">
      {quests.map(quest => {
        const totalTasks = quest.subtasks ? quest.subtasks.length : 0;
        const completedTasks = quest.subtasks ? quest.subtasks.filter(t => t.is_completed).length : 0;
        const progressPercent = totalTasks === 0 ? 0 : (completedTasks / totalTasks) * 100;

        return (
          <div 
            key={quest.id} 
            className={`quest-card ${quest.status === 'COMPLETED' ? 'quest-completed' : ''} ${quest.status === 'FAILED' ? 'quest-failed' : ''}`}
            onClick={() => setActiveQuest(quest)}
            style={{ cursor: 'pointer' }}
          >
            <div className="quest-card-header">
              <div>
                <h4 className="quest-title">{quest.title} {quest.is_daily && <span className="quest-daily-badge">DAILY</span>}</h4>
                <p className="quest-meta">
                  Difficulty: <span className={`quest-diff-${quest.difficulty.toLowerCase()}`}>{quest.difficulty}</span> | 
                  Deadline: {new Date(quest.deadline).toLocaleDateString()}
                  {quest.stat && ` | Tagged: ${quest.stat}`}
                </p>
              </div>
              {quest.status === 'PENDING' && (
                <div className="quest-actions">
                  {!quest.is_daily && (
                    <button className="quest-btn-secondary" onClick={(e) => handleSetDaily(e, quest.id)}>Make Daily</button>
                  )}
                </div>
              )}
              {quest.status !== 'PENDING' && (
                <div className="quest-status-badge">{quest.status}</div>
              )}
            </div>
            
            {/* Progress Bar Preview */}
            <div style={{ marginTop: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>
                <span>Progress</span>
                <span>{completedTasks} / {totalTasks} Tasks</span>
              </div>
              <div style={{ height: '6px', background: 'rgba(0,0,0,0.3)', borderRadius: '3px', overflow: 'hidden' }}>
                <div style={{ width: `${progressPercent}%`, height: '100%', background: accentColor, transition: 'width 0.3s ease' }}></div>
              </div>
            </div>
          </div>
        );
      })}

      {/* ── Quest Details Modal ── */}
      {activeQuest && (
        <div className="modal-overlay" onClick={() => setActiveQuest(null)}>
          <div 
            className="modal-content quest-modal" 
            onClick={e => e.stopPropagation()}
            style={{ 
              borderTop: `4px solid ${accentColor}`,
              boxShadow: `0 10px 40px ${accentColor}25, 0 0 20px ${accentColor}15 inset` 
            }}
          >
            <button className="modal-close" onClick={() => setActiveQuest(null)}>×</button>
            
            <h2 style={{ marginBottom: '0.5rem', color: accentColor, textShadow: `0 0 10px ${accentColor}40` }}>{activeQuest.title}</h2>
            {activeQuest.description && <p className="quest-desc" style={{ marginBottom: '1.5rem' }}>{activeQuest.description}</p>}
            
            <div className="quest-subtasks" style={{ borderTop: 'none', paddingTop: 0, marginTop: 0 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h4 style={{ color: 'var(--text-secondary)', margin: 0 }}>Tasks</h4>
                {activeQuest.status === 'PENDING' && (
                  <button 
                    type="button" 
                    onClick={handleGenerateTasksForExisting} 
                    disabled={isGenerating}
                    style={{ 
                      background: 'transparent', 
                      color: 'var(--text-primary)', 
                      border: 'none', 
                      padding: '0 0.5rem', 
                      cursor: isGenerating ? 'wait' : 'pointer',
                      fontSize: '1.25rem',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      transition: 'transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
                      filter: 'invert(0.6) sepia(1) saturate(5) hue-rotate(130deg)'
                    }}
                    onMouseOver={(e) => !isGenerating && (e.currentTarget.style.transform = 'scale(1.2)')}
                    onMouseOut={(e) => !isGenerating && (e.currentTarget.style.transform = 'scale(1)')}
                    title="Auto-Generate Tasks"
                  >
                    {isGenerating ? '⏳' : '✨'}
                  </button>
                )}
              </div>
              
              {(() => {
                const incomplete = activeQuest.subtasks ? activeQuest.subtasks.filter(t => !t.is_completed) : [];
                const completed = activeQuest.subtasks ? activeQuest.subtasks.filter(t => t.is_completed) : [];

                const renderTask = (st) => (
                  <div key={st.id} className="subtask-item-wrapper" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                    <label className="subtask-item" style={{ flex: 1, margin: 0 }}>
                      <input 
                        type="checkbox" 
                        className="custom-checkbox"
                        checked={st.is_completed} 
                        onChange={() => handleToggleSubtask(st.id)} 
                        disabled={activeQuest.status !== 'PENDING'}
                        style={{ '--chk-color': accentColor }}
                      />
                      <span className={st.is_completed ? 'subtask-done' : ''} style={{ fontSize: '1rem' }}>{st.description}</span>
                    </label>
                    {activeQuest.status === 'PENDING' && (
                      <button 
                        className="quest-btn-secondary" 
                        style={{ padding: '0.2rem 0.5rem', fontSize: '0.8rem', borderColor: 'transparent', color: 'var(--text-tertiary)' }}
                        onClick={() => handleDeleteTask(st.id)}
                        title="Delete task"
                      >
                        ✖
                      </button>
                    )}
                  </div>
                );

                return (
                  <>
                    {incomplete.map(renderTask)}
                    
                    {completed.length > 0 && (
                      <div style={{ marginTop: '1.5rem' }}>
                        <h5 style={{ fontSize: '0.85rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.5rem', borderBottom: '1px solid rgba(255,255,255,0.05)', paddingBottom: '0.25rem' }}>Completed</h5>
                        {completed.map(renderTask)}
                      </div>
                    )}
                  </>
                );
              })()}
              
              {activeQuest.status === 'PENDING' && (
                <div className="add-task-row" style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid rgba(255,255,255,0.05)' }}>
                  <input 
                    type="text" 
                    value={newTaskInput}
                    onChange={(e) => setNewTaskInput(e.target.value)}
                    placeholder="Add a new task..."
                    style={{ flex: 1, background: 'rgba(0,0,0,0.2)', border: '1px solid var(--border)', padding: '0.6rem 1rem', borderRadius: '4px', color: 'var(--text-primary)', fontSize: '0.9rem' }}
                    onKeyDown={(e) => e.key === 'Enter' && handleAddTask(activeQuest.id)}
                  />
                  <button 
                    className="quest-btn-primary" 
                    style={{ padding: '0.6rem 1rem', fontSize: '0.9rem' }}
                    onClick={() => handleAddTask(activeQuest.id)}
                  >
                    Add Task
                  </button>
                </div>
              )}
            </div>
            
            <div style={{ marginTop: '2.5rem', display: 'flex', justifyContent: 'flex-end' }}>
              <button 
                onClick={() => handleDeleteQuest(activeQuest.id)}
                style={{ 
                  background: 'rgba(239, 68, 68, 0.05)', 
                  color: '#EF4444', 
                  border: '1px solid rgba(239, 68, 68, 0.3)', 
                  padding: '0.5rem 1rem', 
                  borderRadius: '4px', 
                  cursor: 'pointer', 
                  fontSize: '0.85rem',
                  fontWeight: '600',
                  transition: 'all 0.2s'
                }}
                className="quest-btn-secondary"
                onMouseOver={(e) => { e.currentTarget.style.borderColor = '#EF4444'; e.currentTarget.style.background = 'rgba(239, 68, 68, 0.15)' }}
                onMouseOut={(e) => { e.currentTarget.style.borderColor = 'rgba(239, 68, 68, 0.3)'; e.currentTarget.style.background = 'rgba(239, 68, 68, 0.05)' }}
              >
                Delete Quest
              </button>
            </div>
            
          </div>
        </div>
      )}
    </div>
  );
}
