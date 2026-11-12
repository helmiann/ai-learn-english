<template>
  <div class="chat-page">

    <!-- Overlay sidebar -->
    <div
      v-if="sidebarOpen"
      class="sidebar-overlay"
      @click="sidebarOpen = false"
    />

    <!-- Sidebar -->
    <Sidebar :is-open="sidebarOpen" @close="sidebarOpen = false" />

    <!-- Topbar -->
    <div class="topbar">
      <button class="icon-btn hamburger-btn" @click="sidebarOpen = true">
        <svg viewBox="0 0 24 24" fill="currentColor" width="22" height="22">
          <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/>
        </svg>
      </button>

      <!-- Avatar huruf awal username -->
      <div class="user-avatar" @click="sidebarOpen = true">
        {{ userInitial }}
      </div>
    </div>

    <!-- Area konten utama -->
    <div class="chat-main">

      <!-- Tampilan awal — belum ada chat aktif -->
      <div v-if="!chatStore.currentChatId" class="welcome-area">

        <!-- Petunjuk penggunaan -->
        <div class="guide-box">
          <p class="guide-title">💡 Cara menggunakan chatbot:</p>
          <ol class="guide-list">
            <li>Pilih salah satu topik di bawah untuk mulai belajar</li>
            <li>Baca penjelasan dari AI dengan seksama</li>
            <li>Ketik jawaban atau pertanyaanmu di <strong>kolom chat di bawah</strong> 👇</li>
            <li>Tekan Enter atau tombol kirim untuk mengirim</li>
          </ol>
        </div>

        <p class="welcome-text">Pilih topik untuk mulai belajar:</p>

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

        <!-- Typing indicator -->
        <div v-if="chatStore.loading" class="bubble-wrapper ai">
          <div class="typing">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>

    </div>

    <!-- Input bar -->
    <ChatInput
      :loading="chatStore.loading"
      :placeholder="inputPlaceholder"
      @send="handleSendMessage"
    />

  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted } from 'vue'
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

// Huruf awal username untuk avatar
const userInitial = computed(() => {
  const name = authStore.username || '?'
  return name.charAt(0).toUpperCase()
})

// Placeholder input berubah sesuai kondisi
const inputPlaceholder = computed(() => {
  if (!chatStore.currentChatId) {
    return 'Pilih topik dulu atau ketik pertanyaanmu...'
  }
  if (chatStore.loading) {
    return 'AI sedang menjawab...'
  }
  return 'Tulis jawabanmu atau pertanyaanmu di sini...'
})

const defaultRecommendations = ref([
  'Simple Present Tense',
  'Simple Past Tense',
  'Irregular Verbs',
  'Imperative Sentences',
])

onMounted(async () => {
  await chatStore.fetchChats()
  if (route.params.id) {
    await chatStore.openChat(Number(route.params.id))
  }
})

watch(() => route.params.id, async (newId) => {
  if (newId) {
    await chatStore.openChat(Number(newId))
  }
})

// Auto scroll ke bawah saat ada pesan baru
watch(() => chatStore.messages.length, async () => {
  await nextTick()
  if (messagesArea.value) {
    messagesArea.value.scrollTop = messagesArea.value.scrollHeight
  }
})

async function handleSendMessage(content) {
  if (!chatStore.currentChatId) {
    const chat = await chatStore.createChat(content.slice(0, 50))
    if (!chat) return
    router.push({ name: 'ChatDetail', params: { id: chat.id_chats } })
  }
  await chatStore.sendMessage(content)
}

async function handleSelectRecommendation(topic) {
  const messages = {
    'Simple Present Tense': 'Halo! Aku ingin belajar Simple Present Tense. Bisa jelaskan rumus dan contohnya?',
    'Simple Past Tense': 'Halo! Aku ingin belajar Simple Past Tense. Bisa jelaskan rumus dan contohnya?',
    'Irregular Verbs': 'Halo! Aku ingin belajar Irregular Verbs. Bisa tunjukkan daftarnya dan cara penggunaannya?',
    'Imperative Sentences': 'Halo! Aku ingin belajar Imperative Sentences. Bisa jelaskan cara membuatnya?',
  }
  await handleSendMessage(messages[topic] || `Aku ingin belajar ${topic}`)
}
</script>

<style scoped>
.chat-page {
  width: 100vw;
  height: 100vh;
  height: 100dvh;
  background-color: var(--bg-primary);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

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

.icon-btn:hover { background-color: var(--accent); }

.user-avatar {
  width: 44px;
  height: 44px;
  border-radius: var(--border-radius-full);
  background-color: var(--accent);
  border: 2px solid var(--accent-hover);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  cursor: pointer;
  transition: var(--transition);
  user-select: none;
}

.user-avatar:hover {
  background-color: var(--accent-hover);
  transform: scale(1.05);
}

/* Area konten */
.chat-main {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

/* Welcome area */
.welcome-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 16px 20px;
  gap: 14px;
  overflow-y: auto;
}

/* Kotak petunjuk */
.guide-box {
  background-color: var(--bg-secondary);
  border-radius: var(--border-radius-md);
  padding: 18px 20px;
  max-width: 600px;
  width: 100%;
  margin: 0 auto;
}

.guide-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.guide-list {
  padding-left: 15px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.guide-list li {
  font-size: 13px;
  color: var(--text-primary);
  line-height: 1.5;
}

.welcome-text {
  font-size: 14px;
  color: var(--text-secondary);
  text-align: center;
  font-weight: 600; 
}

.recommendations {
  display: flex;
  flex-direction: column;
  gap: 11px;
  max-width: 600px;
  width: 100%;
  margin: 0 auto;
}

/* Area pesan */
.messages-area {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 20px 20px 8px 20px;
  display: flex;
  flex-direction: column;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior: contain;
}

/* Typing indicator */
.bubble-wrapper {
  display: flex;
  width: 100%;
  margin-bottom: 16px;
}

.bubble-wrapper.ai { justify-content: flex-start; }

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