# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Context Builder
#  File: backend/services/context_manager/context_builder.py
# ============================================================

from typing import List, Dict, Optional


class ContextBuilder:
    """
    Merakit semua bagian konteks menjadi satu list messages
    yang siap dikirim ke Llama API.
    """

    SYSTEM_PROMPT = (
        "Kamu adalah guru bahasa Inggris yang ramah dan sabar, "
        "khusus membantu siswa SMP belajar grammar bahasa Inggris. \n\n"
        "MATERI YANG BOLEH DIAJARKAN (hanya 4 topik ini):\n"
        "1. Simple Present Tense — penggunaan, rumus, contoh kalimat\n"
        "2. Simple Past Tense — penggunaan, rumus, contoh kalimat\n"
        "3. Irregular Verbs — daftar kata kerja tidak beraturan beserta artinya\n"
        "4. Imperative Sentences — kalimat perintah, larangan, dan permintaan\n\n"
        "ATURAN PENTING:\n"
        "- Jika siswa bertanya di luar 4 materi di atas, tolak dengan sopan "
        "dan arahkan kembali ke salah satu dari 4 materi tersebut.\n"
        "- Sesuaikan penjelasan dengan level SMP (mudah dipahami, tidak terlalu teknis).\n"
        "- Selalu jawab dalam bahasa Indonesia yang mudah dimengerti.\n"
        "- Tampilkan contoh kalimat dalam bahasa Inggris beserta artinya.\n"
        "- Berikan pujian dan motivasi agar siswa semangat belajar.\n"
        "- Jika siswa membuat kalimat yang salah, koreksi dengan sopan.\n"
    )

    def build(
        self,
        recent_messages: List[Dict[str, str]],
        summary: Optional[str] = None,
        user_info: Optional[Dict] = None,
    ) -> List[Dict[str, str]]:
        """
        Rakit semua bagian menjadi list messages lengkap.
        """
        context: List[Dict[str, str]] = []

        system_content = self.SYSTEM_PROMPT

        # Tambahkan info siswa jika ada
        if user_info:
            kelas = user_info.get("kelas", "")
            sekolah = user_info.get("sekolah", "")
            if kelas or sekolah:
                system_content += (
                    f"\nInfo siswa: Kelas {kelas}"
                    f"{f' dari {sekolah}' if sekolah else ''}. "
                    "Sesuaikan penjelasan dengan level kelasnya.\n"
                )

        # Tambahkan ringkasan jika ada
        if summary:
            system_content += (
                f"\nRingkasan percakapan sebelumnya:\n{summary}\n"
            )

        context.append({"role": "system", "content": system_content})
        context.extend(recent_messages)

        return context