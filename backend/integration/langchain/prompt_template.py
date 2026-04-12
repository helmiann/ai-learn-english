# ============================================================
#  ENGLISH GRAMMAR CHATBOT — LangChain Prompt Templates
#  File: backend/integration/langchain/prompt_template.py
# ============================================================

from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


# ----------------------------------------------------------
# SYSTEM PROMPT — Instruksi utama untuk AI
# ----------------------------------------------------------
SYSTEM_TEMPLATE = """Kamu adalah guru bahasa Inggris yang ramah dan sabar, \
membantu siswa SMP belajar grammar bahasa Inggris.

Panduan mengajar:
- Berikan penjelasan yang mudah dipahami oleh siswa SMP
- Gunakan contoh kalimat sederhana dan relevan
- Berikan pujian untuk memotivasi siswa
- Jawab dalam bahasa Indonesia, tapi tampilkan contoh dalam bahasa Inggris
- Fokus pada topik: tenses, parts of speech, sentence structure

{summary_context}"""

# ----------------------------------------------------------
# PROMPT UNTUK PERCAKAPAN BIASA
# ----------------------------------------------------------
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(SYSTEM_TEMPLATE),
    HumanMessagePromptTemplate.from_template("{user_message}"),
])

# ----------------------------------------------------------
# PROMPT UNTUK MEMBUAT RINGKASAN
# ----------------------------------------------------------
SUMMARY_TEMPLATE = """Buatkan ringkasan singkat dari percakapan belajar \
bahasa Inggris berikut. Fokus pada:
1. Topik grammar yang sudah dibahas
2. Kemajuan dan pemahaman siswa
3. Poin penting yang perlu diingat

Percakapan:
{conversation}

Ringkasan (maksimal 3 paragraf):"""

summary_prompt = ChatPromptTemplate.from_messages([
    HumanMessagePromptTemplate.from_template(SUMMARY_TEMPLATE),
])

# ----------------------------------------------------------
# PROMPT UNTUK REKOMENDASI TOPIK
# ----------------------------------------------------------
RECOMMENDATION_TEMPLATE = """Berdasarkan riwayat belajar siswa berikut, \
rekomendasikan 3 topik grammar bahasa Inggris yang cocok dipelajari selanjutnya.

Riwayat belajar:
{learning_history}

Berikan rekomendasi dalam format JSON:
{{
    "recommendations": [
        {{"topic": "nama topik", "reason": "alasan rekomendasi", "difficulty": "mudah/sedang/sulit"}},
        ...
    ]
}}"""

recommendation_prompt = ChatPromptTemplate.from_messages([
    HumanMessagePromptTemplate.from_template(RECOMMENDATION_TEMPLATE),
])