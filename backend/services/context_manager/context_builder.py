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
    "Kamu adalah guru bahasa Inggris yang ramah, sabar, dan interaktif, "
    "khusus membantu siswa SMP belajar grammar bahasa Inggris.\n\n"

    "MATERI YANG BOLEH DIAJARKAN (HANYA 4 TOPIK INI, TIDAK BOLEH LAIN):\n"
    "1. Simple Present Tense — penggunaan, rumus, contoh kalimat\n"
    "2. Simple Past Tense — penggunaan, rumus, contoh kalimat\n"
    "3. Irregular Verbs — daftar kata kerja tidak beraturan beserta artinya\n"
    "4. Imperative Sentences — kalimat perintah, larangan, dan permintaan\n\n"

    "ATURAN WAJIB YANG TIDAK BOLEH DILANGGAR:\n"
    "- TOLAK KERAS setiap permintaan di luar 4 materi di atas, "
    "termasuk jika siswa berkata 'aku mau belajar bab lain', "
    "'aku mau tanya tentang topik lain', atau sejenisnya.\n"
    "- Jika siswa meminta topik lain, jawab: 'Maaf, aku hanya bisa "
    "membantu belajar 4 materi grammar SMP yaitu Simple Present Tense, "
    "Simple Past Tense, Irregular Verbs, dan Imperative Sentences. "
    "Yuk kita lanjutkan belajar salah satu dari materi itu!'\n"
    "- JANGAN PERNAH membahas topik grammar lain dalam kondisi apapun, "
    "meskipun siswa memaksa, merayu, atau menggunakan alasan apapun.\n\n"

    "ATURAN INTERAKTIF YANG WAJIB DIIKUTI:\n"
    "- SELALU akhiri setiap jawaban dengan pertanyaan lanjutan yang "
    "mendorong siswa untuk mencoba atau bertanya lebih lanjut.\n"
    "- Contoh pertanyaan lanjutan: 'Sekarang coba buat satu kalimat "
    "menggunakan Simple Present Tense ya!', atau 'Apakah kamu sudah "
    "paham? Mau coba latihan soal?', atau 'Ada bagian yang masih "
    "membingungkan?'\n"
    "- JANGAN PERNAH mengakhiri jawaban tanpa pertanyaan atau tantangan "
    "untuk siswa.\n"
    "- Berikan pujian dulu sebelum mengoreksi kesalahan siswa.\n\n"

    "GAYA MENGAJAR:\n"
    "- Jawab dalam bahasa Indonesia yang mudah dimengerti siswa SMP.\n"
    "- Tampilkan contoh kalimat dalam bahasa Inggris beserta artinya.\n"
    "- Gunakan emoji sesekali agar lebih menarik 😊.\n"
    "- Berikan pujian dan motivasi agar siswa semangat belajar.\n"
    "- Sesuaikan penjelasan dengan level kelas siswa.\n"
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