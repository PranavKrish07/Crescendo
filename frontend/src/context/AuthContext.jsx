import { createContext, useContext, useState, useEffect } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [tokens, setTokens] = useState(null);
  const [loading, setLoading] = useState(true);

  // Rehydrate from localStorage on mount
  useEffect(() => {
    const storedTokens = localStorage.getItem("tokens");
    const storedUser = localStorage.getItem("user");
    if (storedTokens) setTokens(JSON.parse(storedTokens));
    if (storedUser) setUser(JSON.parse(storedUser));
    setLoading(false);
  }, []);

  const login = (tokenData, userData) => {
    localStorage.setItem("tokens", JSON.stringify(tokenData));
    localStorage.setItem("user", JSON.stringify(userData));
    setTokens(tokenData);
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem("tokens");
    localStorage.removeItem("user");
    setTokens(null);
    setUser(null);
  };

  const updateUser = (partial) => {
    setUser((prev) => {
      const updated = { ...prev, ...partial };
      localStorage.setItem("user", JSON.stringify(updated));
      return updated;
    });
  };

  return (
    <AuthContext.Provider value={{ user, tokens, loading, login, logout, updateUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}

export default AuthContext;
