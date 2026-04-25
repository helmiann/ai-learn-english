<template>
  <div class="sidebar" :class="{ open: isOpen }">

    <!-- Header sidebar -->
    <div class="sidebar-header">
      <!-- Avatar user -->
      <div class="user-info">
        <div class="avatar">{{ userInitial }}</div>
        <div class="user-detail">
          <p class="user-name">{{ authStore.username }}</p>
          <p class="user-class">{{ userClass }}</p>
        </div>
      </div>
      <button class="icon-btn close-btn" @click="$emit('close')">
        <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
          <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
        </svg>
      </button>
    </div>

    <!-- Tombol buat chat baru -->
    <button class="new-chat-btn" @click="handleNewChat">
      <span>buat chat baru</span>
      <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
        <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
      </svg>
    </button>

    <!-- Search riwayat -->
    <div class="search-bar">
      <input
        v-model="chatStore.searchQuery"
        type="text"
        placeholder="search riwayat chat"
        class="search-input"
      />
      <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16">
        <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
      </svg>
    </div>

    <!-- Daftar riwayat chat -->
    <div class="chat-list">
      <div
        v-for="chat in chatStore.filteredChats"
        :key="chat.id_chats"
        class="chat-item"
        :class="{ active: chatStore.currentChatId === chat.id_chats }"
        @click="handleOpenChat(chat.id_chats)"
      >
        <span class="chat-item-title">{{ chat.title }}</span>
        <button class="delete-btn" @click.stop="handleDeleteChat(chat.id_chats)">
          <svg viewBox="0 0 24 24" fill="currentColor" width="14" height="14">
            <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
          </svg>
        </button>
      </div>
      <p v-if="chatStore.filteredChats.length === 0" class="empty-text">
        Belum ada percakapan
      </p>
    </div>

    <!-- Divider -->
    <div class="divider" />

    <!-- Menu Evaluasi -->
    <div class="eval-menu">
      <p class="eval-title">Evaluasi</p>

      <button class="eval-btn" @click="goTo('PostTest')">
        <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
          <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-.23c0-.62.28-1.2.76-1.58C7.47 15.82 9.64 15 12 15s4.53.82 6.24 2.19c.48.38.76.97.76 1.58V19z"/>
        </svg>
        <span>Post-Test</span>
      </button>

      <button class="eval-btn" @click="goTo('Kuesioner')">
        <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
          <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-7 12h-2v-2h2v2zm0-4h-2V6h2v4z"/>
        </svg>
        <span>Kuesioner Evaluasi</span>
      </button>
    </div>

    <!-- Footer -->
    <div class="sidebar-footer">
      <button class="logout-btn" @click="handleLogout">
        <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
          <path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/>
        </svg>
        <span>Keluar</span>
      </button>
    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useChatStore } from '@/stores/chat'
import { useAuthStore } from '@/stores/auth'

const chatStore = useChatStore()
const authStore = useAuthStore()
const router = useRouter()

defineProps({
  isOpen: { type: Boolean, default: false },
})

const emit = defineEmits(['close'])

// Huruf awal username
const userInitial = computed(() => {
  const name = authStore.username || ''
  return name.charAt(0).toUpperCase()
})

// Info kelas dari user
const userClass = computed(() => {
  const user = authStore.user
  if (!user) return ''
  const parts = []
  if (user.kelas) parts.push(`Kelas ${user.kelas}`)
  if (user.sekolah) parts.push(user.sekolah)
  return parts.join(' — ')
})

function handleNewChat() {
  chatStore.currentChatId = null
  chatStore.messages = []
  router.push({ name: 'Chat' })
  emit('close')
}

async function handleOpenChat(chatId) {
  await chatStore.openChat(chatId)
  router.push({ name: 'ChatDetail', params: { id: chatId } })
  emit('close')
}

async function handleDeleteChat(chatId) {
  await chatStore.deleteChat(chatId)
}

function goTo(name) {
  router.push({ name })
  emit('close')
}

function handleLogout() {
  authStore.logout()
  chatStore.reset()
  router.push({ name: 'Login' })
  emit('close')
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: var(--sidebar-width);
  height: 100vh;
  background-color: var(--bg-sidebar);
  display: flex;
  flex-direction: column;
  padding: 16px 12px;
  transform: translateX(-100%);
  transition: transform 0.3s ease;
  z-index: 100;
  gap: 10px;
}

.sidebar.open {
  transform: translateX(0);
}

/* Header */
.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  overflow: hidden;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: var(--border-radius-full);
  background-color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  flex-shrink: 0;
}

.user-detail {
  overflow: hidden;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-class {
  font-size: 11px;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.icon-btn {
  width: 36px;
  height: 36px;
  border-radius: var(--border-radius-full);
  background-color: transparent;
  border: 2px solid var(--accent);
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition);
  flex-shrink: 0;
}

.icon-btn:hover {
  background-color: var(--accent);
}

/* Tombol buat chat baru */
.new-chat-btn {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background-color: transparent;
  border: 1px solid var(--accent);
  border-radius: var(--border-radius-md);
  color: var(--text-primary);
  font-size: 14px;
  cursor: pointer;
  transition: var(--transition);
}

.new-chat-btn:hover {
  background-color: var(--accent);
}

/* Search bar */
.search-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border: 1px solid var(--accent);
  border-radius: var(--border-radius-md);
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  font-size: 13px;
  color: var(--text-primary);
}

.search-input::placeholder {
  color: var(--text-secondary);
  opacity: 0.8;
}

/* Daftar chat */
.chat-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.chat-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  background-color: var(--accent);
  border-radius: var(--border-radius-md);
  cursor: pointer;
  transition: var(--transition);
}

.chat-item:hover,
.chat-item.active {
  background-color: var(--accent-hover);
}

.chat-item-title {
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.delete-btn {
  background: transparent;
  border: none;
  color: var(--text-primary);
  cursor: pointer;
  opacity: 0.6;
  transition: var(--transition);
  flex-shrink: 0;
  padding: 2px;
}

.delete-btn:hover {
  opacity: 1;
}

.empty-text {
  font-size: 13px;
  color: var(--text-secondary);
  text-align: center;
  padding: 16px 0;
}

/* Divider */
.divider {
  height: 1px;
  background-color: var(--accent-light);
  margin: 2px 0;
}

/* Menu Evaluasi */
.eval-menu {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.eval-title {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0 4px;
}

.eval-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background-color: transparent;
  border: 1px solid var(--accent);
  border-radius: var(--border-radius-md);
  color: var(--text-primary);
  font-size: 13px;
  cursor: pointer;
  transition: var(--transition);
  text-align: left;
}

.eval-btn:hover {
  background-color: var(--accent);
}

/* Footer logout */
.sidebar-footer {
  padding-top: 4px;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background-color: transparent;
  border: 1px solid var(--accent-light);
  border-radius: var(--border-radius-md);
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: var(--transition);
  width: 100%;
}

.logout-btn:hover {
  background-color: #ff000022;
  border-color: #ff0000;
  color: #ff0000;
}
</style>