<template>
  <div class="scrollable-page">
    <div class="kuesioner-container">

      <!-- Header -->
      <div class="kuesioner-header">
        <h1 class="kuesioner-title">Kuesioner Evaluasi</h1>
        <p class="kuesioner-subtitle">
          Berikan penilaianmu terhadap chatbot belajar grammar ini
        </p>
        <div class="progress-info">
          <span>{{ answeredCount }} / {{ totalQuestions }} dijawab</span>
          <div class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: `${(answeredCount / totalQuestions) * 100}%` }"
            />
          </div>
        </div>
      </div>

      <!-- Form -->
      <div v-if="!showResult" class="kuesioner-form">

        <div class="scale-legend">
          <span>1 = Sangat Tidak Setuju</span>
          <span>5 = Sangat Setuju</span>
        </div>

        <!-- Bagian 1 -->
        <div class="section-group">
          <h2 class="section-title">📚 Kesesuaian Materi & Konteks</h2>
          <p class="section-desc">
            Penilaian apakah chatbot memberikan materi yang sesuai dengan 4 topik grammar SMP.
          </p>
          <div v-for="item in contextQuestions" :key="item.id" class="question-item">
            <p class="q-text">{{ item.id }}. {{ item.question }}</p>
            <div class="scale-buttons">
              <button
                v-for="n in 5" :key="n"
                class="scale-btn"
                :class="{ selected: answers[item.id] === n }"
                @click="answers[item.id] = n"
              >{{ n }}</button>
            </div>
            <div class="scale-labels">
              <span>Sangat Tidak Setuju</span>
              <span>Sangat Setuju</span>
            </div>
          </div>
        </div>

        <!-- Bagian 2 -->
        <div class="section-group">
          <h2 class="section-title">🖥️ Kemudahan Penggunaan</h2>
          <p class="section-desc">
            Penilaian apakah aplikasi mudah digunakan oleh siswa SMP.
          </p>
          <div v-for="item in usabilityQuestions" :key="item.id" class="question-item">
            <p class="q-text">{{ item.id }}. {{ item.question }}</p>
            <div class="scale-buttons">
              <button
                v-for="n in 5" :key="n"
                class="scale-btn"
                :class="{ selected: answers[item.id] === n }"
                @click="answers[item.id] = n"
              >{{ n }}</button>
            </div>
            <div class="scale-labels">
              <span>Sangat Tidak Setuju</span>
              <span>Sangat Setuju</span>
            </div>
          </div>
        </div>

        <!-- Bagian 3 -->
        <div class="section-group">
          <h2 class="section-title">🎯 Manfaat Pembelajaran</h2>
          <p class="section-desc">
            Penilaian apakah chatbot membantu meningkatkan pemahaman grammar.
          </p>
          <div v-for="item in learningQuestions" :key="item.id" class="question-item">
            <p class="q-text">{{ item.id }}. {{ item.question }}</p>
            <div class="scale-buttons">
              <button
                v-for="n in 5" :key="n"
                class="scale-btn"
                :class="{ selected: answers[item.id] === n }"
                @click="answers[item.id] = n"
              >{{ n }}</button>
            </div>
            <div class="scale-labels">
              <span>Sangat Tidak Setuju</span>
              <span>Sangat Setuju</span>
            </div>
          </div>
        </div>

        <!-- Saran -->
        <div class="section-group">
          <h2 class="section-title">💬 Saran & Masukan</h2>
          <textarea
            v-model="saran"
            placeholder="Tuliskan saran atau masukan kamu (opsional)..."
            class="saran-input"
            rows="4"
          />
        </div>

        <p v-if="errorMsg" class="error-message">{{ errorMsg }}</p>

        <button
          class="btn-primary"
          :disabled="!isAllAnswered || submitting"
          @click="submitKuesioner"
        >
          <span v-if="submitting">Menyimpan...</span>
          <span v-else>Kirim Kuesioner ✓</span>
        </button>

      </div>

      <!-- Hasil -->
      <div v-else class="result-area">
        <div class="thank-icon">🎉</div>
        <h2 class="result-title">Terima Kasih!</h2>
        <p class="result-desc">
          Jawabanmu sudah tersimpan. Penilaianmu sangat membantu pengembangan chatbot ini.
        </p>

        <div class="summary-scores">
          <div class="summary-item">
            <span class="summary-label">Kesesuaian Materi</span>
            <span class="summary-value">{{ averageScore(contextQuestions) }}/5</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">Kemudahan Penggunaan</span>
            <span class="summary-value">{{ averageScore(usabilityQuestions) }}/5</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">Manfaat Pembelajaran</span>
            <span class="summary-value">{{ averageScore(learningQuestions) }}/5</span>
          </div>
          <div class="summary-item total">
            <span class="summary-label">Rata-rata Keseluruhan</span>
            <span class="summary-value">{{ averageScoreAll() }}/5</span>
          </div>
        </div>

        <button class="btn-primary" @click="goToChat">
          Kembali ke Chat
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()

const contextQuestions = [
  { id: 1, question: "Chatbot hanya membahas materi grammar yang sesuai dengan topik SMP (Simple Present Tense, Simple Past Tense, Irregular Verbs, Imperative Sentences)." },
  { id: 2, question: "Chatbot tidak membahas topik grammar di luar 4 materi yang ditentukan." },
  { id: 3, question: "Penjelasan yang diberikan chatbot sesuai dengan tingkat pemahaman siswa SMP." },
  { id: 4, question: "Contoh kalimat yang diberikan chatbot mudah dipahami oleh siswa SMP." },
  { id: 5, question: "Chatbot memberikan koreksi yang tepat ketika saya membuat kalimat yang salah." },
  { id: 6, question: "Jawaban chatbot konsisten dan tidak bertentangan satu sama lain." },
]

const usabilityQuestions = [
  { id: 7, question: "Tampilan aplikasi menarik dan nyaman digunakan." },
  { id: 8, question: "Saya mudah memahami cara menggunakan aplikasi ini." },
  { id: 9, question: "Proses login dan daftar akun mudah dilakukan." },
  { id: 10, question: "Fitur riwayat percakapan memudahkan saya mengulang pelajaran." },
  { id: 11, question: "Aplikasi ini berjalan dengan lancar tanpa banyak gangguan." },
]

const learningQuestions = [
  { id: 12, question: "Chatbot ini membantu saya memahami grammar bahasa Inggris dengan lebih baik." },
  { id: 13, question: "Saya merasa lebih percaya diri dalam menggunakan grammar bahasa Inggris setelah menggunakan chatbot ini." },
  { id: 14, question: "Saya ingin terus menggunakan chatbot ini untuk belajar grammar." },
  { id: 15, question: "Saya akan merekomendasikan aplikasi ini kepada teman-teman saya." },
]

const answers = ref({})
const saran = ref('')
const showResult = ref(false)
const submitting = ref(false)
const errorMsg = ref('')

const totalQuestions = contextQuestions.length + usabilityQuestions.length + learningQuestions.length
const answeredCount = computed(() => Object.keys(answers.value).length)
const isAllAnswered = computed(() => answeredCount.value === totalQuestions)

async function submitKuesioner() {
  if (!isAllAnswered.value) {
    errorMsg.value = 'Harap jawab semua pertanyaan terlebih dahulu.'
    return
  }
  submitting.value = true
  errorMsg.value = ''
  try {
    await api.post('/survey/submit', {
      answers: answers.value,
      saran: saran.value,
      avg_context: parseFloat(averageScore(contextQuestions)),
      avg_usability: parseFloat(averageScore(usabilityQuestions)),
      avg_learning: parseFloat(averageScore(learningQuestions)),
      avg_total: parseFloat(averageScoreAll()),
    })
    showResult.value = true
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } catch (err) {
    errorMsg.value = 'Gagal menyimpan kuesioner. Coba lagi.'
  } finally {
    submitting.value = false
  }
}

function averageScore(questionList) {
  const total = questionList.reduce((sum, q) => sum + (answers.value[q.id] || 0), 0)
  return (total / questionList.length).toFixed(1)
}

function averageScoreAll() {
  const all = [...contextQuestions, ...usabilityQuestions, ...learningQuestions]
  const total = all.reduce((sum, q) => sum + (answers.value[q.id] || 0), 0)
  return (total / all.length).toFixed(1)
}

function goToChat() {
  router.push({ name: 'Chat' })
}
</script>

<style scoped>
.page-wrapper {
  width: 100%;
  min-height: 100vh;
  background-color: var(--bg-primary);
  overflow-y: auto;
  overflow-x: hidden;
}

.kuesioner-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px 16px 80px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.kuesioner-header { display: flex; flex-direction: column; gap: 8px; }
.kuesioner-title { font-size: 26px; font-weight: 700; }
.kuesioner-subtitle { font-size: 14px; color: var(--text-secondary); line-height: 1.5; }
.progress-info { display: flex; flex-direction: column; gap: 6px; font-size: 13px; color: var(--text-secondary); }
.progress-bar { width: 100%; height: 8px; background-color: var(--accent-light); border-radius: var(--border-radius-full); overflow: hidden; }
.progress-fill { height: 100%; background-color: var(--accent); transition: width 0.3s ease; }

.kuesioner-form { display: flex; flex-direction: column; gap: 24px; }

.scale-legend {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-secondary);
  padding: 8px 12px;
  background-color: var(--bg-secondary);
  border-radius: var(--border-radius-md);
}

.section-group { display: flex; flex-direction: column; gap: 14px; }
.section-title { font-size: 17px; font-weight: 700; }
.section-desc { font-size: 13px; color: var(--text-secondary); line-height: 1.5; margin-top: -6px; }

.question-item {
  background-color: var(--bg-secondary);
  padding: 16px;
  border-radius: var(--border-radius-md);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.q-text { font-size: 14px; line-height: 1.6; }

.scale-buttons { display: flex; gap: 8px; justify-content: space-between; }

.scale-btn {
  flex: 1;
  aspect-ratio: 1;
  max-width: 52px;
  border-radius: var(--border-radius-md);
  border: 2px solid var(--accent);
  background-color: transparent;
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: var(--transition);
}

.scale-btn:hover { background-color: var(--accent-light); }
.scale-btn.selected { background-color: var(--accent); border-color: var(--accent-hover); transform: scale(1.1); }

.scale-labels { display: flex; justify-content: space-between; font-size: 11px; color: var(--text-secondary); }

.saran-input {
  width: 100%;
  padding: 14px 16px;
  background-color: var(--bg-secondary);
  border: 2px solid var(--accent);
  border-radius: var(--border-radius-md);
  color: var(--text-primary);
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  outline: none;
  transition: var(--transition);
}

.saran-input::placeholder { color: var(--text-secondary); opacity: 0.7; }
.saran-input:focus { border-color: var(--accent-hover); box-shadow: 0 0 0 3px var(--accent-light); }

.error-message {
  color: #7b0000;
  background-color: #ffcccc55;
  padding: 10px 14px;
  border-radius: var(--border-radius-md);
  font-size: 14px;
  text-align: center;
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

.btn-primary:hover:not(:disabled) { background-color: var(--accent-hover); }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }

/* Hasil */
.result-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  text-align: center;
  padding: 20px 0;
}

.thank-icon { font-size: 64px; }
.result-title { font-size: 24px; font-weight: 700; }
.result-desc { font-size: 15px; color: var(--text-secondary); line-height: 1.6; }

.summary-scores { width: 100%; display: flex; flex-direction: column; gap: 8px; }

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: var(--bg-secondary);
  border-radius: var(--border-radius-md);
  font-size: 14px;
}

.summary-item.total { background-color: var(--accent); font-weight: 700; }
.summary-value { font-weight: 700; font-size: 16px; color: var(--accent-hover); }
.summary-item.total .summary-value { color: var(--text-primary); }
</style>