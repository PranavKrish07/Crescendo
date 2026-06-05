import API from "./axios";

export async function fetchScenes() {
  const res = await API.get("/awakening/scenes/");
  return res.data;
}

export async function submitAwakening(answers) {
  const res = await API.post("/awakening/submit/", { answers });
  return res.data;
}
