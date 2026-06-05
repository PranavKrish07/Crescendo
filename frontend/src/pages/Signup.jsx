import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../api/axios";
import logoImg from "../images/class-emblems/Main-Logo.png";

export default function Signup() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
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
      const response = await API.post("/signup/", form);
      
      // If server responds with 201 Created (even with email warning flags)
      if (response.status === 201) {
        if (response.data?.status === 'warning') {
          // If mail delivery choked, alert the operator but don't halt progression
          alert(`${response.data.message}\nError Details: ${response.data.debug_error || 'Unknown'}`);
        }
        
        // Push user safely to the OTP interface
        navigate("/verify-otp", { state: { email: form.email } });
      }
    } catch (err) {
      const data = err.response?.data;
      
      if (data) {
        if (typeof data === "string") {
          setError(data);
        } else if (data.error || data.message || data.debug_error) {
          setError(data.error || data.message || data.debug_error);
        } else {
          // Flatten standard DRF object structure securely
          try {
            const messages = Object.values(data)
              .map(val => Array.isArray(val) ? val.join(" ") : String(val))
              .join(" ");
            setError(messages || "Field validation failed.");
          } catch (parseError) {
            setError("Failed to compile registration errors.");
          }
        }
      } else {
        setError("Network infrastructure connection timeout. Retry transaction.");
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
        <h2 className="auth-title">Create Account</h2>
        <p className="auth-subtitle">Join Crescendo today</p>

        {error && <div className="auth-error">{error}</div>}

        <label htmlFor="signup-name">Full Name</label>
        <input
          id="signup-name"
          name="name"
          type="text"
          placeholder="Your name"
          value={form.name}
          onChange={handleChange}
          required
        />

        <label htmlFor="signup-email">Email</label>
        <input
          id="signup-email"
          name="email"
          type="email"
          placeholder="you@example.com"
          value={form.email}
          onChange={handleChange}
          required
        />

        <label htmlFor="signup-password">Password</label>
        <input
          id="signup-password"
          name="password"
          type="password"
          placeholder="Min 8 chars, 1 uppercase, 1 special"
          value={form.password}
          onChange={handleChange}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "Signing up…" : "Sign Up"}
        </button>

        <p className="auth-footer">
          Already have an account? <Link to="/login">Log in</Link>
        </p>
      </form>
    </div>
  );
}