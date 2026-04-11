# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Context Builder
#  File: backend/services/context_manager/context_builder.py
# ============================================================

from typing import List, Dict, Optional


class ContextBuilder:
    """
    Merakit semua bagian konteks menjadi satu list messages
    yang siap dikirim ke Llama API.

    Urutan konteks:
    1. System prompt (instruksi untuk AI)
    2. Ringkasan percakapan sebelumnya (jika ada)
    3. Pesan-pesan terbaru yang dipilih
    """

    # System prompt — instruksi utama untuk AI
    SYSTEM_PROMPT = (
        "Kamu adalah guru bahasa Inggris yang ramah dan sabar, "
        "membantu siswa SMP belajar grammar bahasa Inggris. "
        "Berikan penjelasan yang mudah dipahami, gunakan contoh sederhana, "
        "dan berikan pujian untuk memotivasi siswa. "
        "Selalu jawab dalam bahasa Indonesia yang mudah dimengerti, "
        "tapi tunjukkan contoh kalimat dalam bahasa Inggris. "
        "Fokus pada topik grammar seperti tenses, parts of speech, "
        "sentence structure, dan lainnya yang sesuai level SMP."
    )

    def build(
        self,
        recent_messages: List[Dict[str, str]],
        summary: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        """
        Rakit semua bagian menjadi list messages lengkap.

        Returns:
            List of dict {"role": "system"/"user"/"assistant", "content": ...}
        """
        context: List[Dict[str, str]] = []

        # 1. System prompt selalu ada di awal
        system_content = self.SYSTEM_PROMPT

        # 2. Tambahkan ringkasan jika ada
        if summary:
            system_content += (
                f"\n\nRingkasan percakapan sebelumnya:\n{summary}"
            )

        context.append({
            "role": "system",
            "content": system_content,
        })

        # 3. Tambahkan pesan-pesan terbaru
        context.extend(recent_messages)

        return context