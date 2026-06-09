import React, { useState } from 'react';
import { createQuest } from '../api/dashboard';
import { GoogleGenerativeAI } from '@google/generative-ai';

export default function CreateQuestModal({ isOpen, onClose, onCreated }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [stat, setStat] = useState('');
  const [deadline, setDeadline] = useState('');
  const [subtasks, setSubtasks] = useState([{ description: '' }]);
  const [loading, setLoading] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleAddSubtask = () => {
    setSubtasks([...subtasks, { description: '' }]);
  };

  const handleSubtaskChange = (index, value) => {
    const newSubtasks = [...subtasks];
    newSubtasks[index].description = value;
    setSubtasks(newSubtasks);
  };

  const handleGenerateTasks = async () => {
    const apiKey = localStorage.getItem('geminiApiKey');
    if (!apiKey) {
      setError('Please set your Gemini API Key in the dashboard header first.');
      return;
    }
    if (!title) {
      setError('Please enter a Quest Title first to generate tasks.');
      return;
    }
    
    setIsGenerating(true);
    setError('');
    try {
      const genAI = new GoogleGenerativeAI(apiKey);
      const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });
      
      const prompt = `I have a quest titled "${title}". 
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
        setSubtasks(generatedTasks.map(t => ({ description: t })));
      } else {
        setError('AI returned invalid format.');
      }
    } catch (err) {
      setError('Failed to generate tasks: ' + err.message + '. If the model is overloaded, please try again in a few seconds.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!title || !deadline) {
      setError('Title and Deadline are mandatory.');
      return;
    }

    setLoading(true);
    try {
      const payload = {
        title,
        description,
        stat: stat || null,
        deadline,
        subtasks: subtasks.filter(st => st.description.trim() !== '')
      };
      
      await createQuest(payload);
      onCreated();
      onClose();
      
      // Reset form
      setTitle('');
      setDescription('');
      setStat('');
      setDeadline('');
      setSubtasks([{ description: '' }]);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create quest.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" style={{ zIndex: 1000 }}>
      <div className="modal-content quest-modal">
        <button className="modal-close" onClick={onClose}>×</button>
        <h2>Create a New Quest</h2>
        {error && <p className="auth-error" style={{ color: 'var(--error)' }}>{error}</p>}
        
        <form onSubmit={handleSubmit} className="quest-form">
          <div className="form-group">
            <label>Quest Title*</label>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <input type="text" value={title} onChange={e => setTitle(e.target.value)} required style={{ flex: 1 }} />
              <button 
                type="button" 
                onClick={handleGenerateTasks} 
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
            </div>
          </div>
          
          <div className="form-group">
            <label>Description</label>
            <textarea value={description} onChange={e => setDescription(e.target.value)} rows="2"></textarea>
          </div>
          
          <div className="form-row">
            <div className="form-group flex-1">
              <label>Deadline*</label>
              <input type="datetime-local" value={deadline} onChange={e => setDeadline(e.target.value)} required />
            </div>
            <div className="form-group flex-1">
              <label>Tag Stat (Optional)</label>
              <select value={stat} onChange={e => setStat(e.target.value)}>
                <option value="">None</option>
                <option value="STR">Strength (STR)</option>
                <option value="END">Endurance (END)</option>
                <option value="AGI">Agility (AGI)</option>
                <option value="INT">Intelligence (INT)</option>
                <option value="CHA">Charisma (CHA)</option>
                <option value="WIL">Willpower (WIL)</option>
              </select>
            </div>
          </div>
          
          <div className="form-group subtasks-group">
            <label>Tasks / Subtasks</label>
            <p className="subtask-hint">Difficulty (and XP) scales with the number of tasks!</p>
            {subtasks.map((st, i) => (
              <input 
                key={i}
                type="text" 
                placeholder={`Task ${i + 1}`}
                value={st.description} 
                onChange={e => handleSubtaskChange(i, e.target.value)} 
                className="subtask-input"
              />
            ))}
            <button type="button" className="btn-add-task" onClick={handleAddSubtask}>+ Add Task</button>
          </div>
          
          <button type="submit" className="quest-btn-primary full-width" disabled={loading}>
            {loading ? 'Forging Quest...' : 'Create Quest'}
          </button>
        </form>
      </div>
    </div>
  );
}
