import axios from "axios";

const API = axios.create({
  baseURL: `${import.meta.env.VITE_API_BASE_URL}/api/auth`,
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach JWT access token to every outgoing request if available
API.interceptors.request.use((config) => {
  const tokens = JSON.parse(localStorage.getItem("tokens"));
  if (tokens?.access) {
    config.headers.Authorization = `Bearer ${tokens.access}`;
  }
  return config;
});

export default API;
