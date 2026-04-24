// ============================================================
//  ENGLISH GRAMMAR CHATBOT — Vue Router
//  File: src/router/index.js
// ============================================================

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// ----------------------------------------------------------
// ROUTE DEFINITIONS
// ----------------------------------------------------------
const routes = [
  {
    path: '/',
    redirect: '/chat',
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/LoginPage.vue'),
    meta: { requiresGuest: true },   // Hanya untuk yang belum login
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/pages/RegisterPage.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/chat',
    name: 'Chat',
    component: () => import('@/pages/ChatPage.vue'),
    meta: { requiresAuth: true },    // Harus login dulu
  },
  {
    path: '/chat/:id',
    name: 'ChatDetail',
    component: () => import('@/pages/ChatPage.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/chat',
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

  ]

  // ----------------------------------------------------------
  // ROUTER INSTANCE
  // ----------------------------------------------------------
  const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
})

// ----------------------------------------------------------
// NAVIGATION GUARD — Cek auth sebelum pindah halaman
// ----------------------------------------------------------
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isLoggedIn = authStore.isLoggedIn

  // Halaman yang butuh login
  if (to.meta.requiresAuth && !isLoggedIn) {
    return next({ name: 'Login' })
  }

  // Halaman yang hanya untuk guest (belum login)
  if (to.meta.requiresGuest && isLoggedIn) {
    return next({ name: 'Chat' })
  }

  next()
})

export default router