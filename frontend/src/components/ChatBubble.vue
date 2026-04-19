<template>
  <!-- Bubble user (kanan) -->
  <div v-if="role === 'user'" class="bubble-wrapper user">
    <div class="bubble user-bubble">{{ contents }}</div>
  </div>

  <!-- Bubble AI (kiri) -->
  <div v-else class="bubble-wrapper ai">
    <div class="bubble ai-bubble">{{ contents }}</div>
  </div>
</template>

<script setup>
defineProps({
  role: {
    type: String,
    required: true,   // 'user' atau 'assistant'
  },
  contents: {
    type: String,
    required: true,
  },
})
</script>

<style scoped>
.bubble-wrapper {
  display: flex;
  width: 100%;
  margin-bottom: 16px;
}

.bubble-wrapper.user {
  justify-content: flex-end;
  padding-left: 20%;
}

.bubble-wrapper.ai {
  justify-content: flex-start;
  padding-right: 20%;
}

.bubble {
  padding: 14px 20px;
  border-radius: var(--border-radius-lg);
  font-size: 15px;
  line-height: 1.6;
  max-width: 100%;
  word-break: break-word;
}

.user-bubble {
  background-color: var(--bubble-user-bg);
  color: var(--text-primary);
  border-bottom-right-radius: 6px;
}

.ai-bubble {
  background-color: transparent;
  color: var(--text-primary);
  border-bottom-left-radius: 6px;
}
</style>
