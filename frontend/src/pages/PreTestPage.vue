<template>
  <div class="test-container">

    <!-- Header -->
    <div class="test-header">
      <h1 class="test-title">Pre-Test</h1>
      <p class="test-subtitle">Grammar Bahasa Inggris — SMP</p>
      <div class="test-info">
        <span>{{ currentIndex + 1 }} / {{ questions.length }} soal</span>
        <span class="section-badge">{{ currentQuestion.section }}</span>
      </div>
      <!-- Progress bar -->
      <div class="progress-bar">
        <div
          class="progress-fill"
          :style="{ width: `${((currentIndex + 1) / questions.length) * 100}%` }"
        />
      </div>
    </div>

    <!-- Soal -->
    <div v-if="!showResult" class="question-area">
      <p class="question-text">{{ currentQuestion.question }}</p>

      <div class="options-list">
        <button
          v-for="(option, i) in currentQuestion.options"
          :key="i"
          class="option-btn"
          :class="{
            selected: answers[currentQuestion.id] === option,
          }"
          @click="selectAnswer(option)"
        >
          <span class="option-label">{{ ['A', 'B', 'C', 'D'][i] }}</span>
          <span class="option-text">{{ option }}</span>
        </button>
      </div>

      <!-- Navigasi -->
      <div class="nav-buttons">
        <button
          class="nav-btn prev-btn"
          :disabled="currentIndex === 0"
          @click="prevQuestion"
        >
          ← Sebelumnya
        </button>

        <button
          v-if="currentIndex < questions.length - 1"
          class="nav-btn next-btn"
          :disabled="!answers[currentQuestion.id]"
          @click="nextQuestion"
        >
          Selanjutnya →
        </button>

        <button
          v-else
          class="nav-btn submit-btn"
          :disabled="!isAllAnswered"
          @click="submitTest"
        >
          Selesai ✓
        </button>
      </div>

      <!-- Indikator soal -->
      <div class="question-dots">
        <span
          v-for="(q, i) in questions"
          :key="q.id"
          class="dot"
          :class="{
            answered: answers[q.id],
            current: i === currentIndex,
          }"
          @click="goToQuestion(i)"
        />
      </div>
    </div>

    <!-- Hasil -->
    <div v-else class="result-area">
      <div class="result-card">
        <div class="score-circle">
          <span class="score-number">{{ result.score }}</span>
          <span class="score-label">/ 100</span>
        </div>

        <h2 class="result-title">Pre-Test Selesai!</h2>
        <p class="result-desc">
          Kamu menjawab <strong>{{ result.correct }}</strong> dari
          <strong>{{ result.total }}</strong> soal dengan benar.
        </p>

        <!-- Nilai per section -->
        <div class="section-scores">
          <div
            v-for="(val, section) in sectionScores"
            :key="section"
            class="section-score-item"
          >
            <span class="section-name">{{ section }}</span>
            <span class="section-val">{{ val.correct }}/{{ val.total }}</span>
          </div>
        </div>

        <p class="result-note">
          Nilai pre-test kamu sudah tersimpan. Sekarang kamu bisa mulai
          belajar dengan chatbot!
        </p>

        <button class="btn-primary" @click="goToChat">
          Mulai Belajar →
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { questions, calculateScore, calculateScoreBySection } from '@/data/questions'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

const currentIndex = ref(0)
const answers = ref({})
const showResult = ref(false)
const result = ref(null)
const sectionScores = ref(null)
const saving = ref(false)

const currentQuestion = computed(() => questions[currentIndex.value])

const isAllAnswered = computed(() =>
  questions.every(q => answers.value[q.id])
)

// Cek apakah sudah pernah pre-test
onMounted(async () => {
  try {
    const response = await api.get('/test/pre-test/check')
    if (response.data.already_taken) {
      router.push({ name: 'Chat' })
    }
  } catch {
    // Belum ada API test, lanjut saja
  }
})

function selectAnswer(option) {
  answers.value[currentQuestion.value.id] = option
}

function nextQuestion() {
  if (currentIndex.value < questions.length - 1) {
    currentIndex.value++
  }
}

function prevQuestion() {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}

function goToQuestion(index) {
  currentIndex.value = index
}

async function submitTest() {
  saving.value = true

  result.value = calculateScore(answers.value)
  sectionScores.value = calculateScoreBySection(answers.value)

  // Simpan ke backend
  try {
    await api.post('/test/pre-test', {
      answers: answers.value,
      score: result.value.score,
      correct: result.value.correct,
      total: result.value.total,
    })
  } catch (err) {
    console.error('Gagal simpan hasil pre-test:', err)
  } finally {
    saving.value = false
  }

  showResult.value = true
}

function goToChat() {
  router.push({ name: 'Chat' })
}
</script>

<style scoped>
.test-container {
  width: 100vw;
  min-height: 100vh;
  background-color: var(--bg-primary);
  display: flex;
  flex-direction: column;
  padding: 20px 16px;
  overflow-y: auto;
}

/* Header */
.test-header {
  margin-bottom: 24px;
}

.test-title {
  font-size: 26px;
  font-weight: 700;
  color: var(--text-primary);
}

.test-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 12px;
}

.test-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 14px;
  color: var(--text-primary);
}

.section-badge {
  background-color: var(--accent);
  padding: 4px 12px;
  border-radius: var(--border-radius-full);
  font-size: 12px;
  font-weight: 600;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: var(--accent-light);
  border-radius: var(--border-radius-full);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: var(--accent);
  border-radius: var(--border-radius-full);
  transition: width 0.3s ease;
}

/* Soal */
.question-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.question-text {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.6;
  background-color: var(--bg-secondary);
  padding: 16px 20px;
  border-radius: var(--border-radius-md);
}

/* Pilihan jawaban */
.options-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-btn {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  background-color: transparent;
  border: 2px solid var(--accent);
  border-radius: var(--border-radius-md);
  color: var(--text-primary);
  font-size: 15px;
  cursor: pointer;
  transition: var(--transition);
  text-align: left;
}

.option-btn:hover {
  background-color: var(--accent-light);
}

.option-btn.selected {
  background-color: var(--accent);
  border-color: var(--accent-hover);
}

.option-label {
  width: 32px;
  height: 32px;
  border-radius: var(--border-radius-full);
  background-color: var(--accent-light);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}

.option-btn.selected .option-label {
  background-color: var(--accent-hover);
  color: white;
}

/* Navigasi */
.nav-buttons {
  display: flex;
  gap: 10px;
  margin-top: 8px;
}

.nav-btn {
  flex: 1;
  padding: 14px;
  border-radius: var(--border-radius-lg);
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
  border: 2px solid var(--accent);
  background-color: transparent;
  color: var(--text-primary);
}

.nav-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.next-btn,
.submit-btn {
  background-color: var(--accent);
  border-color: var(--accent);
}

.next-btn:hover:not(:disabled),
.submit-btn:hover:not(:disabled) {
  background-color: var(--accent-hover);
}

/* Indikator dot soal */
.question-dots {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  padding: 8px 0;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: var(--accent-light);
  border: 2px solid var(--accent);
  cursor: pointer;
  transition: var(--transition);
}

.dot.answered {
  background-color: var(--accent);
}

.dot.current {
  background-color: var(--accent-hover);
  transform: scale(1.3);
}

/* Hasil */
.result-area {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px 0;
}

.result-card {
  width: 100%;
  max-width: 480px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  text-align: center;
}

.score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background-color: var(--accent);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 30px var(--accent-light);
}

.score-number {
  font-size: 36px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
}

.score-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.result-title {
  font-size: 22px;
  font-weight: 700;
}

.result-desc {
  font-size: 15px;
  color: var(--text-secondary);
}

.section-scores {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.section-score-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 16px;
  background-color: var(--bg-secondary);
  border-radius: var(--border-radius-md);
  font-size: 14px;
}

.section-val {
  font-weight: 700;
  color: var(--accent-hover);
}

.result-note {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.btn-primary {
  width: 100%;
  padding: 16px;
  background-color: var(--accent);
  color: var(--text-primary);
  border: none;
  border-radius: var(--border-radius-lg);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
}

.btn-primary:hover {
  background-color: var(--accent-hover);
}
</style>