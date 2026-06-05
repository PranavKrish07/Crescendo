import { useEffect, useRef } from "react";
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Landing from "./pages/Landing";
import Signup from "./pages/Signup";
import VerifyOTP from "./pages/VerifyOTP";
import Login from "./pages/Login";
import ForgotPassword from "./pages/ForgotPassword";
import ResetPassword from "./pages/ResetPassword";
import Awakening from "./pages/Awakening";
import MyClass from "./pages/MyClass";

function Home() {
  const { user, logout } = useAuth();
  return (
    <div className="home-container">
      <div className="home-card">
        <h1>🎵 Crescendo</h1>
        <p>Welcome{user?.name ? `, ${user.name}` : ""}!</p>
        <p className="home-subtitle">You are logged in.</p>
        <button onClick={logout}>Log Out</button>
      </div>
    </div>
  );
}

function PrivateRoute({ children }) {
  const { tokens, user, loading } = useAuth();
  if (loading) return null;
  if (!tokens) return <Navigate to="/login" />;
  if (!user?.awakening_done) return <Navigate to="/awakening" />;
  return children;
}

function GuestRoute({ children }) {
  const { tokens, user, loading } = useAuth();
  if (loading) return null;
  if (!tokens) return children;
  // Authenticated — redirect based on awakening status
  return user?.awakening_done ? <Navigate to="/dashboard" /> : <Navigate to="/awakening" />;
}

function RequiresAwakening({ children }) {
  const { tokens, user, loading } = useAuth();
  if (loading) return null;
  if (!tokens) return <Navigate to="/login" />;
  if (user?.awakening_done) return <Navigate to="/my-class" />;
  return children;
}

export default function App() {
  return (
    <AuthProvider>
      <CursorTrail />
      <BrowserRouter>
        <Routes>
          {/* Landing — public root */}
          <Route
            path="/"
            element={
              <GuestRoute>
                <Landing />
              </GuestRoute>
            }
          />

          {/* Awakening — required before dashboard */}
          <Route
            path="/awakening"
            element={
              <RequiresAwakening>
                <Awakening />
              </RequiresAwakening>
            }
          />

          {/* Dashboard — protected, requires awakening done */}
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Home />
              </PrivateRoute>
            }
          />
          <Route
            path="/my-class"
            element={
              <PrivateRoute>
                <MyClass />
              </PrivateRoute>
            }
          />
          <Route
            path="/signup"
            element={
              <GuestRoute>
                <Signup />
              </GuestRoute>
            }
          />
          <Route
            path="/verify-otp"
            element={<VerifyOTP />}
          />
          <Route
            path="/login"
            element={
              <GuestRoute>
                <Login />
              </GuestRoute>
            }
          />
          <Route
            path="/forgot-password"
            element={
              <GuestRoute>
                <ForgotPassword />
              </GuestRoute>
            }
          />
          <Route
            path="/reset-password"
            element={<ResetPassword />}
          />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

function CursorTrail() {
  const canvasRef = useRef(null);

  useEffect(() => {
    // Disable on coarse pointer devices (e.g. touchscreens)
    if (window.matchMedia("(pointer: coarse)").matches) return;

    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    let animationFrameId;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const mouse = { x: 0, y: 0, active: false };
    const cursorCircle = { x: 0, y: 0 };
    const points = [];
    const maxPoints = 12; // Length of the trailing dot stream

    const handleMouseMove = (e) => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
      if (!mouse.active) {
        // Snap smooth follower to cursor initially to avoid sliding in from (0,0)
        cursorCircle.x = e.clientX;
        cursorCircle.y = e.clientY;
        mouse.active = true;
      }
    };

    const handleMouseLeave = () => {
      mouse.active = false;
    };

    const handleResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };

    window.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseleave", handleMouseLeave);
    window.addEventListener("resize", handleResize);

    const render = () => {
      ctx.clearRect(0, 0, width, height);

      if (mouse.active) {
        // Easing for the leading circle follower
        const dx = mouse.x - cursorCircle.x;
        const dy = mouse.y - cursorCircle.y;
        cursorCircle.x += dx * 0.15;
        cursorCircle.y += dy * 0.15;

        points.push({ x: cursorCircle.x, y: cursorCircle.y });
      }

      // Shrink trail if inactive
      if (points.length > maxPoints || (!mouse.active && points.length > 0)) {
        points.shift();
      }

      // Draw trailing particle stream
      for (let i = 0; i < points.length; i++) {
        const pt = points[i];
        const ratio = (i + 1) / points.length;
        const opacity = ratio * 0.35; // Faint, elegant opacity
        const size = ratio * 4.5;     // Tapered trail size

        ctx.beginPath();
        ctx.arc(pt.x, pt.y, size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(13, 148, 136, ${opacity})`; // Teal (#0D9488) matching the theme
        ctx.fill();
      }

      // Draw the main following circle with subtle glow
      if (mouse.active) {
        ctx.beginPath();
        ctx.arc(cursorCircle.x, cursorCircle.y, 6.5, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(20, 184, 166, 0.75)"; // Light teal/mana highlight
        ctx.shadowBlur = 8;
        ctx.shadowColor = "rgba(20, 184, 166, 0.8)";
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseleave", handleMouseLeave);
      window.removeEventListener("resize", handleResize);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        pointerEvents: "none",
        zIndex: 99999,
        width: "100%",
        height: "100%",
      }}
    />
  );
}
