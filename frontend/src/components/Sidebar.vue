<template>
  <div class="sidebar" :class="{ open: isOpen }">

    <!-- Tombol tutup sidebar -->
    <div class="sidebar-header">
      <button class="icon-btn close-btn" @click="$emit('close')">
        <!-- Ikon X -->
        <svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
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
      <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
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
        <button
          class="delete-btn"
          @click.stop="handleDeleteChat(chat.id_chats)"
        >
          <!-- Ikon hapus -->
          <svg viewBox="0 0 24 24" fill="currentColor" width="14" height="14">
            <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
          </svg>
        </button>
      </div>

      <!-- Kosong -->
      <p v-if="chatStore.filteredChats.length === 0" class="empty-text">
        Belum ada percakapan
      </p>
    </div>

    <!-- Settings -->
    <div class="sidebar-footer">
      <button class="icon-btn settings-btn">
        <svg viewBox="0 0 24 24" fill="currentColor" width="22" height="22">
          <path d="M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.07-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.29L5.24,5.33c-0.22-0.08-0.47,0-0.59,0.22L2.74,8.87 C2.62,9.08,2.66,9.34,2.86,9.48l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.07,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54 c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.44-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.47-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z"/>
        </svg>
      </button>
    </div>

  </div>
</template>

<script setup>
import { useChatStore } from '@/stores/chat'
import { useRouter } from 'vue-router'

const chatStore = useChatStore()
const router = useRouter()

defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['close'])

async function handleNewChat() {
  // Reset ke halaman chat tanpa membuka chat tertentu
  // agar rekomendasi muncul dulu sebelum mulai percakapan
  chatStore.currentChatId = null
  chatStore.messages = []
  router.push({ name: 'Chat' })
  emit('close')
}

async function handleOpenChat(chatId) {
  await chatStore.openChat(chatId)
  router.push({ name: 'ChatDetail', params: { id: chatId } })
}

async function handleDeleteChat(chatId) {
  await chatStore.deleteChat(chatId)
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

.sidebar-header {
  display: flex;
  justify-content: flex-end;
}

.icon-btn {
  width: 40px;
  height: 40px;
  border-radius: var(--border-radius-full);
  background-color: transparent;
  border: 2px solid var(--accent);
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition);
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
  background-color: transparent;
  border: 1px solid var(--accent);
  border-radius: var(--border-radius-md);
  color: var(--text-primary);
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
  gap: 8px;
}

.chat-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
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
  font-size: 14px;
  color: var(--text-primary);
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
  padding: 2px;
  opacity: 0.6;
  transition: var(--transition);
  flex-shrink: 0;
}

.delete-btn:hover {
  opacity: 1;
}

.empty-text {
  font-size: 13px;
  color: var(--text-secondary);
  text-align: center;
  padding: 20px 0;
}

/* Footer settings */
.sidebar-footer {
  padding-top: 8px;
  border-top: 1px solid var(--accent-light);
}
</style>
