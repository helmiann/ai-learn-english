// ============================================================
//  ENGLISH GRAMMAR CHATBOT — Vue Router
//  File: src/router/index.js
// ============================================================

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const routes = [
  { path: '/', redirect: '/chat' },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/LoginPage.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/pages/RegisterPage.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/pre-test',
    name: 'PreTest',
    component: () => import('@/pages/PreTestPage.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/post-test',
    name: 'PostTest',
    component: () => import('@/pages/PostTestPage.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/kuesioner',
    name: 'Kuesioner',
    component: () => import('@/pages/KuesionerPage.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/chat',
    name: 'Chat',
    component: () => import('@/pages/ChatPage.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/chat/:id',
    name: 'ChatDetail',
    component: () => import('@/pages/ChatPage.vue'),
    meta: { requiresAuth: true },
  },
  { path: '/:pathMatch(.*)*', redirect: '/chat' },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  const isLoggedIn = authStore.isLoggedIn

  if (to.meta.requiresAuth && !isLoggedIn) {
    return next({ name: 'Login' })
  }

  if (to.meta.requiresGuest && isLoggedIn) {
    return next({ name: 'Chat' })
  }

  // Cek pre-test sebelum masuk chat
  if (isLoggedIn && (to.name === 'Chat' || to.name === 'ChatDetail')) {
    try {
      const response = await api.get('/test/pre-test/check')
      if (!response.data.already_taken) {
        return next({ name: 'PreTest' })
      }
    } catch {
      // API error → biarkan masuk chat
    }
  }

  next()
})

export default router