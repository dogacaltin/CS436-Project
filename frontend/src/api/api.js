import axios from "axios";

export const API_BASE = "http://35.188.156.109"; 

export const fetchSongs = () => axios.get(`${API_BASE}/songs`);

export const rateSong = (proID, songID, rate) =>
  axios.post(`${API_BASE}/rate`, {
    proID,
    songID,
    rate,
  });

export const login = (nick, password) =>
  axios.post(`${API_BASE}/login`, { nick, password });

export const signup = (nick, password) =>
  axios.post(`${API_BASE}/signup`, { nick, password });
