import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to auto-attach Bearer Token from localStorage
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('rag_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth Endpoints
export const signupUser = async (userData) => {
  const response = await api.post('/auth/signup', userData);
  return response.data;
};

export const loginUser = async (credentials) => {
  const response = await api.post('/auth/login', credentials);
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

// Subject Endpoints
export const getSubjects = async () => {
  const response = await api.get('/subjects');
  return response.data;
};

export const createSubject = async (name, code = '') => {
  const response = await api.post('/subjects', { name, code });
  return response.data;
};

// Document & Ingestion Endpoints
export const uploadDocument = async (file, subjectId) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('subject_id', subjectId);

  const response = await api.post('/documents', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

// QA Endpoints
export const askQuestion = async (question, subjectId = null, mode = 'detailed') => {
  const response = await api.post('/ask', {
    question,
    subject_id: subjectId ? parseInt(subjectId, 10) : null,
    mode: mode.toLowerCase(),
  });
  return response.data;
};

// Feedback & Eval Endpoints
export const submitFeedback = async (chatId, rating, feedbackText = '') => {
  const response = await api.post('/feedback', {
    chat_id: chatId,
    helpful: rating >= 3,
    comment: feedbackText,
  });
  return response.data;
};

export const getEvalMetrics = async () => {
  const response = await api.get('/eval');
  return response.data;
};

export default api;
