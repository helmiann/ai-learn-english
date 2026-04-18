<template>
  <div class="input-bar">
    <input
      v-model="message"
      type="text"
      placeholder="chat yang mau ditulis"
      class="chat-input"
      :disabled="loading"
      @keyup.enter="handleSend"
    />
    <button
      class="send-btn"
      :disabled="loading || !message.trim()"
      @click="handleSend"
    >
      <!-- Ikon send (panah) -->
      <svg viewBox="0 0 24 24" fill="currentColor" width="22" height="22">
        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  loading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['send'])
const message = ref('')

function handleSend() {
  if (!message.value.trim() || props.loading) return
  emit('send', message.value.trim())
  message.value = ''
}
</script>

<style scoped>
.input-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background-color: var(--accent);
  border-radius: var(--border-radius-lg);
  margin: 0 16px 16px 16px;
}

.chat-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  font-size: 15px;
  color: var(--text-primary);
  caret-color: var(--text-primary);
}

.chat-input::placeholder {
  color: var(--text-secondary);
  opacity: 0.8;
}

.chat-input:disabled {
  opacity: 0.6;
}

.send-btn {
  width: 40px;
  height: 40px;
  border-radius: var(--border-radius-full);
  background-color: var(--bg-primary);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-primary);
  cursor: pointer;
  flex-shrink: 0;
  transition: var(--transition);
}

.send-btn:hover:not(:disabled) {
  background-color: var(--accent-hover);
  color: white;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
