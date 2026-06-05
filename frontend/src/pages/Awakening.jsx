import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { fetchScenes, submitAwakening } from "../api/awakening";
import { allEmblems } from "../utils/emblems";

const FloatingEmblems = () => {
  return (
    <>
      {allEmblems.map((img, idx) => {
        const top = `${(idx * 23) % 80 + 10}%`;
        const left = `${(idx * 37) % 90 + 5}%`;
        const size = `${(idx % 3) * 20 + 80}px`;
        const delay = `${(idx % 5) * -3}s`;
        const duration = `${15 + (idx % 3) * 5}s`;

        return (
          <img
            key={idx}
            src={img}
            className="floating-emblem"
            style={{
              top,
              left,
              width: size,
              animationDelay: delay,
              animationDuration: duration,
            }}
            alt=""
          />
        );
      })}
    </>
  );
};

export default function Awakening() {
  const [scenes, setScenes]   = useState([]);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState("");
  const navigate = useNavigate();
  const { updateUser } = useAuth();

  useEffect(() => {
    fetchScenes()
      .then((data) => {
        setScenes(data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load The Awakening. Please try again.");
        setLoading(false);
      });
  }, []);

  const handleChoice = async (choiceIdx) => {
    const newAnswers = [...answers, choiceIdx];
    setAnswers(newAnswers);

    if (newAnswers.length < scenes.length) {
      setCurrent(current + 1);
    } else {
      // All answered — submit to server
      try {
        const res = await submitAwakening(newAnswers);
        // Mark awakening as done in auth context
        updateUser({ awakening_done: true, char_class: res.class, archetype: res.archetype });
        navigate("/my-class");
      } catch {
        setError("Failed to submit your answers. Please try again.");
      }
    }
  };

  if (loading) {
    return (
      <div className="awakening-container">
        <FloatingEmblems />
        <div className="awakening-loading">
          <div className="awakening-loading-spinner"></div>
          <p>Preparing The Awakening...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="awakening-container">
        <FloatingEmblems />
        <div className="awakening-error">
          <p>{error}</p>
          <button onClick={() => window.location.reload()}>Retry</button>
        </div>
      </div>
    );
  }



  // ── Scene Screen ──
  const scene = scenes[current];
  const progress = ((current) / scenes.length) * 100;

  return (
    <div className="awakening-container">
      <FloatingEmblems />
      <div className="awakening-scene">
        {/* Progress bar */}
        <div className="awakening-progress-bar">
          <div
            className="awakening-progress-fill"
            style={{ width: `${progress}%` }}
          ></div>
        </div>

        <p className="awakening-step">Scene {current + 1} of {scenes.length}</p>
        <p className="awakening-label">{scene.label}</p>
        <h2 className="awakening-title">{scene.title}</h2>

        <p className="awakening-narrative">{scene.narrative}</p>

        <p className="awakening-question">{scene.question}</p>

        <div className="awakening-choices">
          {scene.choices.map((c, i) => (
            <button
              key={i}
              className="awakening-choice-btn"
              onClick={() => handleChoice(i)}
            >
              {c.text}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
