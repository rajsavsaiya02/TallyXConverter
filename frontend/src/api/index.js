// frontend/src/api/index.js
import axios from 'axios';

const api = axios.create({
  baseURL: '/api', // Vite proxy will handle this
});

export const getFileColumns = (formData) => {
  return api.post('/preview-columns', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const convertAndDownload = (formData) => {
  return api.post('/convert', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    responseType: 'blob',
  });
};

export const getLogs = (password) => {
  return api.get('/admin/log', {
    headers: { Authorization: `Bearer ${password}` },
  });
};

export const addLog = (logData, password) => {
  return api.post('/admin/log', logData, {
    headers: { Authorization: `Bearer ${password}` },
  });
};