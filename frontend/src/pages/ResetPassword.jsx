import { useState } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import API from "../api/axios";
import logoImg from "../images/class-emblems/Main-Logo.png";

export default function ResetPassword() {
  const navigate = useNavigate();
  const location = useLocation();

  const [form, setForm] = useState({
    email: location.state?.email || "",
    otp: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);
    try {
      const res = await API.post("/reset-password/", form);
      setSuccess(res.data.message || "Password reset successful!");
      setTimeout(() => navigate("/login"), 2000);
    } catch (err) {
      const data = err.response?.data;
      if (data) {
        const messages = Object.values(data).flat().join(" ");
        setError(messages);
      } else {
        setError("Something went wrong. Please try again.");
      }
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
        <h2>Reset Password</h2>
        <p className="auth-subtitle">Enter the OTP and your new password</p>

        {error && <div className="auth-error">{error}</div>}
        {success && <div className="auth-success">{success}</div>}

        <label htmlFor="reset-email">Email</label>
        <input
          id="reset-email"
          name="email"
          type="email"
          placeholder="you@example.com"
          value={form.email}
          onChange={handleChange}
          required
        />

        <label htmlFor="reset-otp">OTP Code</label>
        <input
          id="reset-otp"
          name="otp"
          type="text"
          placeholder="123456"
          maxLength={6}
          value={form.otp}
          onChange={handleChange}
          required
        />

        <label htmlFor="reset-password">New Password</label>
        <input
          id="reset-password"
          name="password"
          type="password"
          placeholder="Min 8 chars, 1 uppercase, 1 special"
          value={form.password}
          onChange={handleChange}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "Resetting…" : "Reset Password"}
        </button>

        <p className="auth-footer">
          <Link to="/login">Back to login</Link>
        </p>
      </form>
    </div>
  );
}
