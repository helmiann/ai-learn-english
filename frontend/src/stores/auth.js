// ============================================================
//  ENGLISH GRAMMAR CHATBOT — Auth Store (Pinia)
//  File: src/stores/auth.js
// ============================================================

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {

  // ----------------------------------------------------------
  // STATE
  // ----------------------------------------------------------
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const loading = ref(false)
  const error = ref(null)

  // ----------------------------------------------------------
  // GETTERS
  // ----------------------------------------------------------
  const isLoggedIn = computed(() => !!token.value)
  const username = computed(() => user.value?.username || '')

  // ----------------------------------------------------------
  // ACTIONS
  // ----------------------------------------------------------

  // Login
  async function login(username, password) {
    loading.value = true
    error.value = null

    try {
      // Kirim sebagai form data (sesuai OAuth2PasswordRequestForm)
      const formData = new FormData()
      formData.append('username', username)
      formData.append('password', password)

      const response = await api.post('/auth/login', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })

      // Simpan token
      token.value = response.data.access_token
      localStorage.setItem('token', token.value)

      // Ambil data user
      await fetchMe()

      return true
    } catch (err) {
      error.value = err.response?.data?.detail || 'Login gagal'
      return false
    } finally {
      loading.value = false
    }
  }

  // Register
  async function register(username, password, kelas, sekolah) {
    loading.value = true
    error.value = null

    try {
      await api.post('/auth/register', { username, password, kelas, sekolah })
      return true
    } catch (err) {
      error.value = err.response?.data?.detail || 'Registrasi gagal'
      return false
    } finally {
      loading.value = false
    }
  }

  // Ambil data user yang sedang login
  async function fetchMe() {
    try {
      const response = await api.get('/auth/me')
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(user.value))
    } catch {
      logout()
    }
  }

  // Logout
  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return {
    token, user, loading, error,
    isLoggedIn, username,
    login, register, fetchMe, logout,
  }
})
