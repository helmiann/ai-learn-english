// ============================================================
//  ENGLISH GRAMMAR CHATBOT — API Service (Axios)
//  File: src/services/api.js
// ============================================================

import axios from 'axios'

// ----------------------------------------------------------
// INSTANCE
// ----------------------------------------------------------
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL
    ? `${import.meta.env.VITE_API_URL}/api`
    : '/api',
  timeout: 60000,   // 60 detik (lebih lama untuk request AI)
  headers: {
    'Content-Type': 'application/json',
  },
})

// ----------------------------------------------------------
// REQUEST INTERCEPTOR — Tambahkan token ke setiap request
// ----------------------------------------------------------
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// ----------------------------------------------------------
// RESPONSE INTERCEPTOR — Handle error global
// ----------------------------------------------------------
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Token expired atau tidak valid → logout otomatis
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api