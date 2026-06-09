import axios from "axios";

const dashboardAPI = axios.create({
  baseURL: "http://localhost:8000/api/dashboard",
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach JWT access token to every outgoing request if available
dashboardAPI.interceptors.request.use((config) => {
  const tokens = JSON.parse(localStorage.getItem("tokens"));
  if (tokens?.access) {
    config.headers.Authorization = `Bearer ${tokens.access}`;
  }
  return config;
});

export const fetchProfile = async () => {
  const res = await dashboardAPI.get("/profile/");
  return res.data;
};

export const fetchQuests = async () => {
  const res = await dashboardAPI.get("/quests/");
  return res.data;
};

export const createQuest = async (data) => {
  const res = await dashboardAPI.post("/quests/", data);
  return res.data;
};

export const completeQuest = async (id) => {
  const res = await dashboardAPI.post(`/quests/${id}/complete/`);
  return res.data;
};

export const setQuestAsDaily = async (id) => {
  const res = await dashboardAPI.post(`/quests/${id}/set_daily/`);
  return res.data;
};

export const toggleSubtask = async (id) => {
  const res = await dashboardAPI.post(`/quests/subtask/${id}/toggle/`);
  return res.data;
};

export const addSubtask = async (questId, description) => {
  const res = await dashboardAPI.post(`/quests/${questId}/add_subtask/`, { description });
  return res.data;
};

export const deleteSubtask = async (id) => {
  const res = await dashboardAPI.delete(`/quests/subtask/${id}/`);
  return res.data;
};

export const deleteQuest = async (id) => {
  const res = await dashboardAPI.delete(`/quests/${id}/`);
  return res.data;
};

export default dashboardAPI;
