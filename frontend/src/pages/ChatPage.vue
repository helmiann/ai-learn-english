<template>
  <div class="chat-page">

    <!-- Overlay sidebar -->
    <div
      v-if="sidebarOpen"
      class="sidebar-overlay"
      @click="sidebarOpen = false"
    />

    <!-- Sidebar -->
    <Sidebar
      :is-open="sidebarOpen"
      @close="sidebarOpen = false"
    />

    <!-- Topbar -->
    <div class="topbar">
      <!-- Tombol hamburger (buka sidebar) -->
      <button class="icon-btn hamburger-btn" @click="sidebarOpen = true">
        <svg viewBox="0 0 24 24" fill="currentColor" width="22" height="22">
          <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/>
        </svg>
      </button>

      <!-- Tombol akun -->
      <button class="akun-btn" @click="handleLogout">
        akun
      </button>
    </div>

    <!-- Area konten utama -->
    <div class="chat-main">

      <!-- Tampilan awal — belum ada chat aktif -->
      <div v-if="!chatStore.currentChatId" class="welcome-area">
        <div class="recommendations">
          <RecommendationCard
            v-for="(rec, i) in defaultRecommendations"
            :key="i"
            :topic="rec"
            @select="handleSelectRecommendation"
          />
        </div>
      </div>

      <!-- Area pesan chat -->
      <div v-else class="messages-area" ref="messagesArea">
        <ChatBubble
          v-for="msg in chatStore.messages"
          :key="msg.id_chatmassages"
          :role="msg.role"
          :contents="msg.contents"
        />

        <!-- Loading indicator saat AI sedang menjawab -->
        <div v-if="chatStore.loading" class="bubble-wrapper ai">
          <div class="bubble ai-bubble typing">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>

    </div>

    <!-- Input bar -->
    <ChatInput
      :loading="chatStore.loading"
      @send="handleSendMessage"
    />

  </div>
</template>

<script setup>
import { ref, watch, nextTick, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useChatStore } from '@/stores/chat'
import { useAuthStore } from '@/stores/auth'

import Sidebar from '@/components/Sidebar.vue'
import ChatBubble from '@/components/ChatBubble.vue'
import ChatInput from '@/components/ChatInput.vue'
import RecommendationCard from '@/components/RecommendationCard.vue'

const route = useRoute()
const router = useRouter()
const chatStore = useChatStore()
const authStore = useAuthStore()

const sidebarOpen = ref(false)
const messagesArea = ref(null)

// Rekomendasi topik default
const defaultRecommendations = ref([
  'Belajar Present Tense',
  'Belajar Past Tense',
  'Belajar Future Tense',
  'Parts of Speech',
  'Sentence Structure',
])

// ----------------------------------------------------------
// Load data saat halaman dibuka
// ----------------------------------------------------------
onMounted(async () => {
  await chatStore.fetchChats()

  // Kalau URL punya chat id, buka chat tersebut
  if (route.params.id) {
    await chatStore.openChat(Number(route.params.id))
  }
})

// ----------------------------------------------------------
// Watch perubahan route (pindah chat)
// ----------------------------------------------------------
watch(() => route.params.id, async (newId) => {
  if (newId) {
    await chatStore.openChat(Number(newId))
  }
})

// ----------------------------------------------------------
// Auto scroll ke bawah saat ada pesan baru
// ----------------------------------------------------------
watch(() => chatStore.messages.length, async () => {
  await nextTick()
  if (messagesArea.value) {
    messagesArea.value.scrollTop = messagesArea.value.scrollHeight
  }
})

// ----------------------------------------------------------
// Kirim pesan
// ----------------------------------------------------------
async function handleSendMessage(content) {
  // Kalau belum ada chat aktif, buat dulu
  if (!chatStore.currentChatId) {
    const chat = await chatStore.createChat(
      content.slice(0, 50)  // Judul dari awal pesan
    )
    if (!chat) return
    router.push({ name: 'ChatDetail', params: { id: chat.id_chats } })
  }

  await chatStore.sendMessage(content)
}

// ----------------------------------------------------------
// Pilih rekomendasi → langsung kirim sebagai pesan
// ----------------------------------------------------------
async function handleSelectRecommendation(topic) {
  await handleSendMessage(`Aku ingin belajar tentang ${topic}`)
}

// ----------------------------------------------------------
// Logout
// ----------------------------------------------------------
function handleLogout() {
  authStore.logout()
  chatStore.reset()
  router.push({ name: 'Login' })
}
</script>

<style scoped>
.chat-page {
  width: 100vw;
  height: 100vh;
  background-color: var(--bg-primary);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

/* Overlay gelap saat sidebar terbuka */
.sidebar-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.2);
  z-index: 99;
}

/* Topbar */
.topbar {
  height: var(--topbar-height);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  flex-shrink: 0;
}

.icon-btn {
  width: 44px;
  height: 44px;
  border-radius: var(--border-radius-full);
  background-color: var(--bg-secondary);
  border: none;
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

.akun-btn {
  padding: 8px 20px;
  border-radius: var(--border-radius-full);
  background-color: transparent;
  border: 2px solid var(--accent);
  color: var(--text-primary);
  font-size: 14px;
  cursor: pointer;
  transition: var(--transition);
}

.akun-btn:hover {
  background-color: var(--accent);
}

/* Area konten utama */
.chat-main {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* Area rekomendasi (halaman awal) */
.welcome-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 24px 20px;
}

.recommendations {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 600px;
  width: 100%;
  margin: 0 auto;
}

/* Area pesan */
.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 20px 20px 8px 20px;
  display: flex;
  flex-direction: column;
}

/* Typing indicator */
.bubble-wrapper {
  display: flex;
  width: 100%;
  margin-bottom: 16px;
}

.bubble-wrapper.ai {
  justify-content: flex-start;
}

.bubble {
  padding: 14px 20px;
  border-radius: var(--border-radius-lg);
}

.ai-bubble {
  background-color: transparent;
}

.typing {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 14px 20px;
}

.typing span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: var(--accent);
  animation: bounce 1.2s infinite;
}

.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
  40% { transform: scale(1.2); opacity: 1; }
}
</style>