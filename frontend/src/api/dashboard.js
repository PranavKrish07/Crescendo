import axios from "axios";

const dashboardAPI = axios.create({
  baseURL: `${import.meta.env.VITE_API_BASE_URL}/api/dashboard`,
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

export const checkInUser = async () => {
  const res = await dashboardAPI.post(`/checkin/`);
  return res.data;
};

export const fetchActiveRitual = async () => {
  const res = await dashboardAPI.get(`/rituals/active/`);
  return res.data;
};

export const applyForRitual = async () => {
  const res = await dashboardAPI.post(`/rituals/apply/`);
  return res.data;
};

export const fetchRoadmapTemplates = async () => {
  const res = await dashboardAPI.get("/roadmaps/templates/");
  return res.data;
};

export const fetchActiveRoadmaps = async () => {
  const res = await dashboardAPI.get("/roadmaps/user/active/");
  return res.data;
};

export const registerRoadmap = async (template_id, deadline) => {
  const res = await dashboardAPI.post("/roadmaps/user/register/", { template_id, deadline });
  return res.data;
};

export const toggleRoadmapTask = async (id, task_index) => {
  const res = await dashboardAPI.post(`/roadmaps/user/${id}/toggle_task/`, { task_index });
  return res.data;
};

export const breakOathRoadmap = async (id) => {
  const res = await dashboardAPI.post(`/roadmaps/user/${id}/break_oath/`);
  return res.data;
};

export default dashboardAPI;
