<template>
  <!-- Wrapper luar untuk scroll -->
  <div class="scrollable-page">
    <div class="test-container">

      <!-- Header -->
      <div class="test-header">
        <h1 class="test-title">Pre-Test</h1>
        <p class="test-subtitle">Grammar Bahasa Inggris — SMP</p>
        <div class="test-info">
          <span>{{ currentIndex + 1 }} / {{ questions.length }} soal</span>
          <span class="section-badge">{{ currentQuestion.section }}</span>
        </div>
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
            :class="{ selected: answers[currentQuestion.id] === option }"
            @click="selectAnswer(option)"
          >
            <span class="option-label">{{ ['A', 'B', 'C', 'D'][i] }}</span>
            <span class="option-text">{{ option }}</span>
          </button>
        </div>

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

        <div class="question-dots">
          <span
            v-for="(q, i) in questions"
            :key="q.id"
            class="dot"
            :class="{ answered: answers[q.id], current: i === currentIndex }"
            @click="goToQuestion(i)"
          />
        </div>
      </div>

      <!-- Hasil -->
      <div v-else class="result-area">
        <div class="score-circle">
          <span class="score-number">{{ result.score }}</span>
          <span class="score-label">/ 100</span>
        </div>

        <h2 class="result-title">Pre-Test Selesai!</h2>
        <p class="result-desc">
          Kamu menjawab <strong>{{ result.correct }}</strong> dari
          <strong>{{ result.total }}</strong> soal dengan benar.
        </p>

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
          Nilai pre-test kamu sudah tersimpan. Sekarang kamu bisa mulai belajar!
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
import { questions, calculateScore, calculateScoreBySection, calculateSectionScores } from '@/data/questions'
import api from '@/services/api'

const router = useRouter()

const currentIndex = ref(0)
const answers = ref({})
const showResult = ref(false)
const result = ref(null)
const sectionScores = ref(null)

const currentQuestion = computed(() => questions[currentIndex.value])
const isAllAnswered = computed(() => questions.every(q => answers.value[q.id]))

onMounted(async () => {
  try {
    const response = await api.get('/test/pre-test/check')
    if (response.data.already_taken) {
      router.push({ name: 'Chat' })
    }
  } catch { /* lanjut */ }
})

function selectAnswer(option) {
  answers.value[currentQuestion.value.id] = option
}

function nextQuestion() {
  if (currentIndex.value < questions.length - 1) currentIndex.value++
}

function prevQuestion() {
  if (currentIndex.value > 0) currentIndex.value--
}

function goToQuestion(index) {
  currentIndex.value = index
}

async function submitTest() {
  result.value = calculateScore(answers.value)
  sectionScores.value = calculateScoreBySection(answers.value)
  try {
    await api.post('/test/pre-test', {
      answers: answers.value,
      score: result.value.score,
      correct: result.value.correct,
      total: result.value.total,
      section_scores: calculateSectionScores(answers.value),  // ← tambahkan
    })
  } catch (err) {
    console.error('Gagal simpan pre-test:', err)
  }
  showResult.value = true
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function goToChat() {
  router.push({ name: 'Chat' })
}
</script>

<style scoped>
/* Wrapper luar — ini yang handle scroll */
.page-wrapper {
  width: 100%;
  min-height: 100vh;
  background-color: var(--bg-primary);
  overflow-y: auto;
  overflow-x: hidden;
}

.test-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px 16px 80px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.test-header { display: flex; flex-direction: column; gap: 8px; }

.test-title {
  font-size: 26px;
  font-weight: 700;
  color: var(--text-primary);
}

.test-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
}

.test-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
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

.question-area {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.question-text {
  font-size: 17px;
  font-weight: 600;
  line-height: 1.6;
  background-color: var(--bg-secondary);
  padding: 16px 20px;
  border-radius: var(--border-radius-md);
}

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
  width: 100%;
}

.option-btn:hover { background-color: var(--accent-light); }
.option-btn.selected { background-color: var(--accent); border-color: var(--accent-hover); }

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

.option-btn.selected .option-label { background-color: var(--accent-hover); color: white; }

.nav-buttons { display: flex; gap: 10px; }

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

.nav-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.next-btn, .submit-btn { background-color: var(--accent); }
.next-btn:hover:not(:disabled), .submit-btn:hover:not(:disabled) { background-color: var(--accent-hover); }

.question-dots {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
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

.dot.answered { background-color: var(--accent); }
.dot.current { background-color: var(--accent-hover); transform: scale(1.3); }

/* Hasil */
.result-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  text-align: center;
  padding-bottom: 20px;
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

.score-number { font-size: 36px; font-weight: 700; line-height: 1; }
.score-label { font-size: 14px; color: var(--text-secondary); }
.result-title { font-size: 22px; font-weight: 700; }
.result-desc { font-size: 15px; color: var(--text-secondary); }

.section-scores {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.section-score-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 16px;
  background-color: var(--bg-secondary);
  border-radius: var(--border-radius-md);
  font-size: 14px;
}

.section-val { font-weight: 700; color: var(--accent-hover); }

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

.btn-primary:hover { background-color: var(--accent-hover); }
</style>