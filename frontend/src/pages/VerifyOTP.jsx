import { useState } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import API from "../api/axios";
import logoImg from "../images/class-emblems/Main-Logo.png";

export default function VerifyOTP() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const [email, setEmail] = useState(location.state?.email || "");
  const [otp, setOtp] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await API.post("/verify-otp/", { email, otp });
      // Backend returns { message, tokens, name, awakening_done }
      login(res.data.tokens, {
        name: res.data.name,
        email,
        awakening_done: res.data.awakening_done,
      });
      navigate("/awakening");
    } catch (err) {
      const data = err.response?.data;
      setError(data?.error || data?.otp?.join(" ") || "Verification failed.");
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
        <h2 className="auth-title">Verify Your Email</h2>
        <p className="auth-subtitle">Enter the 6-digit OTP sent to your email</p>

        {error && <div className="auth-error">{error}</div>}

        <label htmlFor="verify-email">Email</label>
        <input
          id="verify-email"
          type="email"
          placeholder="you@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <label htmlFor="verify-otp">OTP Code</label>
        <input
          id="verify-otp"
          type="text"
          placeholder="123456"
          maxLength={6}
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "Verifying…" : "Verify"}
        </button>

        <p className="auth-footer">
          <Link to="/signup">Back to Sign Up</Link>
        </p>
      </form>
    </div>
  );
}
