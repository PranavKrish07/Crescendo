import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000/api/auth",
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
