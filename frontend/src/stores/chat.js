// ============================================================
//  ENGLISH GRAMMAR CHATBOT — Chat Store (Pinia)
//  File: src/stores/chat.js
// ============================================================

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useChatStore = defineStore('chat', () => {

  // ----------------------------------------------------------
  // STATE
  // ----------------------------------------------------------
  const chats = ref([])               // Daftar semua percakapan
  const currentChatId = ref(null)     // ID chat yang sedang dibuka
  const messages = ref([])            // Pesan di chat yang aktif
  const recommendations = ref([])     // Rekomendasi topik
  const loading = ref(false)          // Loading kirim pesan
  const loadingChats = ref(false)     // Loading daftar chat
  const error = ref(null)
  const searchQuery = ref('')         // Query search riwayat

  // ----------------------------------------------------------
  // GETTERS
  // ----------------------------------------------------------
  const currentChat = computed(() =>
    chats.value.find(c => c.id_chats === currentChatId.value) || null
  )

  const filteredChats = computed(() => {
    if (!searchQuery.value) return chats.value
    return chats.value.filter(c =>
      c.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  })

  // ----------------------------------------------------------
  // ACTIONS
  // ----------------------------------------------------------

  // Ambil semua daftar chat
  async function fetchChats() {
    loadingChats.value = true
    try {
      const response = await api.get('/chat/list')
      chats.value = response.data.chats || []
    } catch (err) {
      error.value = 'Gagal memuat daftar chat'
    } finally {
      loadingChats.value = false
    }
  }

  // Buat chat baru
  async function createChat(title = 'Percakapan Baru') {
    try {
      const response = await api.post('/chat/new', { title })
      const newChat = response.data
      chats.value.unshift(newChat)
      await openChat(newChat.id_chats)
      return newChat
    } catch (err) {
      error.value = 'Gagal membuat chat baru'
      return null
    }
  }

  // Buka chat dan muat pesannya
  async function openChat(chatId) {
    currentChatId.value = chatId
    messages.value = []
    try {
      const response = await api.get(`/history/${chatId}`)
      messages.value = response.data.messages || []
    } catch (err) {
      error.value = 'Gagal memuat riwayat pesan'
    }
  }

  // Kirim pesan
  async function sendMessage(content) {
    if (!currentChatId.value || !content.trim()) return

    // Tambahkan pesan user ke UI dulu (optimistic update)
    const tempMessage = {
      id_chatmassages: Date.now(),
      id_chats: currentChatId.value,
      role: 'user',
      contents: content,
      timestamp: new Date().toISOString(),
      token_used: 0,
    }
    messages.value.push(tempMessage)
    loading.value = true
    error.value = null

    try {
      const response = await api.post(
        `/chat/${currentChatId.value}/message`,
        { content }
      )
      // Tambahkan respons AI
      messages.value.push(response.data)
    } catch (err) {
      error.value = 'Gagal mengirim pesan'
      // Hapus pesan user yang gagal
      messages.value = messages.value.filter(
        m => m.id_chatmassages !== tempMessage.id_chatmassages
      )
    } finally {
      loading.value = false
    }
  }

  // Hapus chat
  async function deleteChat(chatId) {
    try {
      await api.delete(`/chat/${chatId}`)
      chats.value = chats.value.filter(c => c.id_chats !== chatId)
      if (currentChatId.value === chatId) {
        currentChatId.value = null
        messages.value = []
      }
    } catch (err) {
      error.value = 'Gagal menghapus chat'
    }
  }

  // Set rekomendasi
  function setRecommendations(items) {
    recommendations.value = items
  }

  // Reset state
  function reset() {
    chats.value = []
    currentChatId.value = null
    messages.value = []
    recommendations.value = []
    error.value = null
  }

  return {
    chats, currentChatId, messages, recommendations,
    loading, loadingChats, error, searchQuery,
    currentChat, filteredChats,
    fetchChats, createChat, openChat, sendMessage,
    deleteChat, setRecommendations, reset,
  }
})