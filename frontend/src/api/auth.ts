import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/v1/auth";

export const loginUser = async (email: string, password: string) => {
  const res = await axios.post(`${API_URL}/jwt/create/`, { email, password });
  return res.data;
};

export const fetchProfile = async (token: string) => {
  const res = await axios.get(`${API_URL}/me/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
};