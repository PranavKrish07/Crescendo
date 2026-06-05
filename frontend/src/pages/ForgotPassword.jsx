import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../api/axios";
import logoImg from "../images/class-emblems/Main-Logo.png";

export default function ForgotPassword() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await API.post("/forgot-password/", { email });
      // Navigate to reset-password with the email pre-filled
      navigate("/reset-password", { state: { email } });
    } catch (err) {
      setError(err.response?.data?.error || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <form className="auth-form" autoComplete="off" onSubmit={handleSubmit}>
        <div className="auth-logo-container">
          <img src={logoImg} alt="Crescendo Logo" className="auth-logo" />
        </div>
        <h2 class="auth-title">Forgot Password</h2>
        <p className="auth-subtitle">
          Enter your email and we&apos;ll send a reset OTP
        </p>

        {error && <div className="auth-error">{error}</div>}

        <label htmlFor="forgot-email">Email</label>
        <input
          id="forgot-email"
          type="email"
          placeholder="you@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "Sending…" : "Send Reset OTP"}
        </button>

        <p className="auth-footer">
          <Link to="/login">Back to login</Link>
        </p>
      </form>
    </div>
  );
}
