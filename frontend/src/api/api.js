import axios from "axios";

const API_BASE = "http://localhost:8000"; // backend container'ına göre değişebilir

export const fetchSongs = () => axios.get(`${API_BASE}/songs`);

export const rateSong = (user_id, song_id, rating) =>
  axios.post(`${API_BASE}/rate`, {
    user_id,
    song_id,
    rating,
  });