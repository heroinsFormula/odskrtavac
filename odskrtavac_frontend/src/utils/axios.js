import axios from 'axios';

const baseURL = "https://127.0.0.1/"

let authTokens = localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null

const axiosInstance = axios.create({
  baseURL,
  headers:{Authorization: `Bearer ${authTokens.access}`}
});

export default axiosInstance;
