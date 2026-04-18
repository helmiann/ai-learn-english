<template>
  <button class="recommendation-card" @click="$emit('select', topic)">
    {{ topic }}
  </button>
</template>

<script setup>
defineProps({
  topic: {
    type: String,
    required: true,
  },
})

defineEmits(['select'])
</script>

<style scoped>
.recommendation-card {
  width: 100%;
  padding: 16px 20px;
  background-color: transparent;
  border: 2px solid var(--accent);
  border-radius: var(--border-radius-lg);
  color: var(--text-primary);
  font-size: 15px;
  text-align: left;
  cursor: pointer;
  transition: var(--transition);
}

.recommendation-card:hover {
  background-color: var(--accent);
}
</style>
