import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import API from "../api/axios";
import logoImg from "../images/class-emblems/Main-Logo.png";

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await API.post("/login/", form);
      // Backend returns { tokens, name, awakening_done }
      login(res.data.tokens, {
        name: res.data.name,
        email: form.email,
        awakening_done: res.data.awakening_done,
      });
      navigate(res.data.awakening_done ? "/dashboard" : "/awakening");
    } catch (err) {
      const data = err.response?.data;
      setError(data?.error || "Login failed. Please try again.");
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
        <h2 class="auth-title">Welcome Back</h2>
        <p className="auth-subtitle">Log in to Crescendo</p>

        {error && <div className="auth-error">{error}</div>}

        <label htmlFor="login-email">Email</label>
        <input
          id="login-email"
          name="email"
          type="email"
          placeholder="you@example.com"
          value={form.email}
          onChange={handleChange}
          required
        />

        <label htmlFor="login-password">Password</label>
        <input
          id="login-password"
          name="password"
          type="password"
          placeholder="Your password"
          value={form.password}
          onChange={handleChange}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "Logging in…" : "Log In"}
        </button>

        <p className="auth-footer">
          <Link to="/forgot-password">Forgot password?</Link>
        </p>
        <p className="auth-footer">
          Don&apos;t have an account? <Link to="/signup">Sign up</Link>
        </p>
      </form>
    </div>
  );
}
