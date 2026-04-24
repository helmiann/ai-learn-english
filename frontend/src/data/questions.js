// ============================================================
//  ENGLISH GRAMMAR CHATBOT — Soal Pre-test & Post-test
//  File: frontend/src/data/questions.js
//
//  20 soal pilihan ganda, 5 soal per materi:
//  1. Simple Present Tense (soal 1-5)
//  2. Simple Past Tense (soal 6-10)
//  3. Irregular Verbs (soal 11-15)
//  4. Imperative Sentences (soal 16-20)
// ============================================================

export const questions = [

  // ----------------------------------------------------------
  // BAGIAN 1 — Simple Present Tense
  // ----------------------------------------------------------
  {
    id: 1,
    section: "Simple Present Tense",
    question: "She ___ to school every day.",
    options: ["go", "goes", "went", "going"],
    answer: "goes",
    explanation: "Subjek 'She' (orang ketiga tunggal) menggunakan kata kerja + 's/es' dalam Simple Present Tense.",
  },
  {
    id: 2,
    section: "Simple Present Tense",
    question: "They ___ football every weekend.",
    options: ["plays", "play", "played", "playing"],
    answer: "play",
    explanation: "Subjek 'They' (jamak) menggunakan kata kerja tanpa tambahan 's/es'.",
  },
  {
    id: 3,
    section: "Simple Present Tense",
    question: "My father ___ coffee every morning.",
    options: ["drink", "drinks", "drank", "drinking"],
    answer: "drinks",
    explanation: "Subjek 'My father' (orang ketiga tunggal) menggunakan kata kerja + 's'.",
  },
  {
    id: 4,
    section: "Simple Present Tense",
    question: "Dina and Rini ___ in the same class.",
    options: ["is", "am", "are", "was"],
    answer: "are",
    explanation: "Subjek jamak (dua orang) menggunakan 'are' dalam Simple Present Tense.",
  },
  {
    id: 5,
    section: "Simple Present Tense",
    question: "He ___ not like spicy food.",
    options: ["do", "does", "did", "is"],
    answer: "does",
    explanation: "Kalimat negatif Simple Present Tense untuk orang ketiga tunggal menggunakan 'does not'.",
  },

  // ----------------------------------------------------------
  // BAGIAN 2 — Simple Past Tense
  // ----------------------------------------------------------
  {
    id: 6,
    section: "Simple Past Tense",
    question: "Yesterday, I ___ to the market with my mother.",
    options: ["go", "goes", "went", "going"],
    answer: "went",
    explanation: "'Go' adalah irregular verb. Bentuk past tense-nya adalah 'went'.",
  },
  {
    id: 7,
    section: "Simple Past Tense",
    question: "She ___ a delicious cake last Sunday.",
    options: ["make", "makes", "made", "making"],
    answer: "made",
    explanation: "'Make' adalah irregular verb. Bentuk past tense-nya adalah 'made'.",
  },
  {
    id: 8,
    section: "Simple Past Tense",
    question: "They ___ football in the field this morning.",
    options: ["play", "plays", "played", "playing"],
    answer: "played",
    explanation: "'Play' adalah regular verb. Bentuk past tense-nya ditambah '-ed' menjadi 'played'.",
  },
  {
    id: 9,
    section: "Simple Past Tense",
    question: "He ___ not come to school yesterday because he was sick.",
    options: ["do", "does", "did", "was"],
    answer: "did",
    explanation: "Kalimat negatif Simple Past Tense menggunakan 'did not' untuk semua subjek.",
  },
  {
    id: 10,
    section: "Simple Past Tense",
    question: "___ you finish your homework last night?",
    options: ["Do", "Does", "Did", "Was"],
    answer: "Did",
    explanation: "Kalimat tanya Simple Past Tense menggunakan 'Did' di awal kalimat.",
  },

  // ----------------------------------------------------------
  // BAGIAN 3 — Irregular Verbs
  // ----------------------------------------------------------
  {
    id: 11,
    section: "Irregular Verbs",
    question: "What is the past tense of 'buy'?",
    options: ["buyed", "buys", "bought", "buying"],
    answer: "bought",
    explanation: "'Buy' adalah irregular verb. Bentuk past tense-nya adalah 'bought', bukan 'buyed'.",
  },
  {
    id: 12,
    section: "Irregular Verbs",
    question: "What is the past tense of 'see'?",
    options: ["seed", "sees", "saw", "seen"],
    answer: "saw",
    explanation: "'See' adalah irregular verb. Bentuk past tense-nya adalah 'saw'.",
  },
  {
    id: 13,
    section: "Irregular Verbs",
    question: "What is the past tense of 'write'?",
    options: ["writed", "writes", "written", "wrote"],
    answer: "wrote",
    explanation: "'Write' adalah irregular verb. Bentuk past tense-nya adalah 'wrote'.",
  },
  {
    id: 14,
    section: "Irregular Verbs",
    question: "I ___ a letter to my friend last week. (send)",
    options: ["sended", "sends", "sent", "sending"],
    answer: "sent",
    explanation: "'Send' adalah irregular verb. Bentuk past tense-nya adalah 'sent', bukan 'sended'.",
  },
  {
    id: 15,
    section: "Irregular Verbs",
    question: "She ___ her bag at home yesterday. (leave)",
    options: ["leaved", "leaves", "left", "leaving"],
    answer: "left",
    explanation: "'Leave' adalah irregular verb. Bentuk past tense-nya adalah 'left', bukan 'leaved'.",
  },

  // ----------------------------------------------------------
  // BAGIAN 4 — Imperative Sentences
  // ----------------------------------------------------------
  {
    id: 16,
    section: "Imperative Sentences",
    question: "Which sentence is a correct imperative sentence?",
    options: [
      "You should open the door.",
      "Open the door, please.",
      "He opens the door.",
      "The door is opened.",
    ],
    answer: "Open the door, please.",
    explanation: "Kalimat imperatif dimulai langsung dengan kata kerja (verb) tanpa subjek. 'Open the door, please' adalah contoh yang benar.",
  },
  {
    id: 17,
    section: "Imperative Sentences",
    question: "How do you make the sentence 'Close the window' into a negative imperative?",
    options: [
      "Not close the window.",
      "Don't close the window.",
      "Doesn't close the window.",
      "No close the window.",
    ],
    answer: "Don't close the window.",
    explanation: "Kalimat imperatif negatif dibentuk dengan menambahkan 'Don't' (Do not) di depan kata kerja.",
  },
  {
    id: 18,
    section: "Imperative Sentences",
    question: "___ quiet in the library!",
    options: ["Be", "Is", "Are", "Am"],
    answer: "Be",
    explanation: "Imperatif dengan kata sifat atau kata benda menggunakan 'Be' di awal kalimat.",
  },
  {
    id: 19,
    section: "Imperative Sentences",
    question: "Which sentence is a correct negative imperative?",
    options: [
      "Not run in the hallway.",
      "Don't running in the hallway.",
      "Don't run in the hallway.",
      "Doesn't run in the hallway.",
    ],
    answer: "Don't run in the hallway.",
    explanation: "Kalimat negatif imperatif yang benar adalah 'Don't + verb (base form)'. Jadi 'Don't run' bukan 'Don't running'.",
  },
  {
    id: 20,
    section: "Imperative Sentences",
    question: "Your teacher says: '___ your book to page 10.' What is the correct word?",
    options: ["Opens", "Opened", "Open", "Opening"],
    answer: "Open",
    explanation: "Kalimat imperatif menggunakan kata kerja bentuk dasar (base form) tanpa tambahan apapun.",
  },
]

// ----------------------------------------------------------
// HELPER — Hitung skor dari jawaban
// ----------------------------------------------------------
export function calculateScore(answers) {
  // answers: { [question_id]: "jawaban_siswa" }
  let correct = 0
  questions.forEach(q => {
    if (answers[q.id] === q.answer) correct++
  })
  return {
    correct,
    total: questions.length,
    score: Math.round((correct / questions.length) * 100),
    percentage: `${Math.round((correct / questions.length) * 100)}%`,
  }
}

// ----------------------------------------------------------
// HELPER — Nilai per section
// ----------------------------------------------------------
export function calculateScoreBySection(answers) {
  const sections = {}
  questions.forEach(q => {
    if (!sections[q.section]) {
      sections[q.section] = { correct: 0, total: 0 }
    }
    sections[q.section].total++
    if (answers[q.id] === q.answer) {
      sections[q.section].correct++
    }
  })
  return sections
}