# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Grammar Checker Service
#  File: backend/services/grammar_checker/grammar_checker_service.py
#
#  Menggunakan library: language-tool-python
#  Install: pip install language-tool-python
#
#  Catatan: Saat pertama kali dijalankan, library ini akan
#  otomatis mendownload LanguageTool server (~200MB).
#  Pastikan koneksi internet tersedia saat startup pertama.
# ============================================================

from typing import Optional
from dataclasses import dataclass, field

import language_tool_python

from core.logging import logger


# ----------------------------------------------------------
# DATA CLASS — Hasil pengecekan satu kesalahan grammar
# ----------------------------------------------------------
@dataclass
class GrammarError:
    message: str                    # Penjelasan kesalahan
    short_message: str              # Penjelasan singkat
    offset: int                     # Posisi awal kesalahan di teks
    length: int                     # Panjang kata yang salah
    bad_text: str                   # Teks yang salah
    replacements: list[str] = field(default_factory=list)  # Saran koreksi
    rule_id: str = ""               # ID rule LanguageTool
    category: str = ""              # Kategori kesalahan (GRAMMAR, TYPOS, dll)


# ----------------------------------------------------------
# DATA CLASS — Hasil lengkap pengecekan satu kalimat
# ----------------------------------------------------------
@dataclass
class GrammarCheckResult:
    original_text: str              # Teks asli dari siswa
    corrected_text: str             # Teks setelah dikoreksi otomatis
    errors: list[GrammarError]      # Daftar kesalahan yang ditemukan
    error_count: int                # Jumlah kesalahan
    is_correct: bool                # True jika tidak ada kesalahan

    def to_dict(self) -> dict:
        """Konversi ke dict untuk dikirim sebagai JSON response."""
        return {
            "original_text": self.original_text,
            "corrected_text": self.corrected_text,
            "is_correct": self.is_correct,
            "error_count": self.error_count,
            "errors": [
                {
                    "message": e.message,
                    "short_message": e.short_message,
                    "bad_text": e.bad_text,
                    "replacements": e.replacements[:3],  # Maksimal 3 saran
                    "offset": e.offset,
                    "length": e.length,
                    "category": e.category,
                }
                for e in self.errors
            ],
        }


# ----------------------------------------------------------
# GRAMMAR CHECKER SERVICE
# ----------------------------------------------------------
class GrammarCheckerService:
    """
    Service untuk mengecek grammar kalimat bahasa Inggris
    menggunakan LanguageTool.

    Singleton pattern — satu instance dipakai ulang agar
    LanguageTool server tidak perlu distart ulang setiap request.
    """

    _instance: Optional["GrammarCheckerService"] = None
    _tool: Optional[language_tool_python.LanguageTool] = None

    def __new__(cls) -> "GrammarCheckerService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self) -> None:
        """
        Inisialisasi LanguageTool.
        Dipanggil sekali saat startup aplikasi.
        """
        if self._tool is None:
            logger.info("Menginisialisasi LanguageTool...")
            # 'en-US' = American English
            # language_tool_python.utils.getDefaultJarStorage()
            self._tool = language_tool_python.LanguageTool("en-US")
            logger.info("LanguageTool siap digunakan.")

    def _ensure_initialized(self) -> None:
        """Pastikan tool sudah diinisialisasi sebelum dipakai."""
        if self._tool is None:
            self.initialize()

    # ----------------------------------------------------------
    # Cek grammar satu kalimat / teks
    # ----------------------------------------------------------
    def check(self, text: str) -> GrammarCheckResult:
        """
        Cek grammar dari teks yang diberikan.

        Args:
            text: Kalimat bahasa Inggris dari siswa

        Returns:
            GrammarCheckResult berisi kesalahan dan saran koreksi
        """
        self._ensure_initialized()

        if not text or not text.strip():
            return GrammarCheckResult(
                original_text=text,
                corrected_text=text,
                errors=[],
                error_count=0,
                is_correct=True,
            )

        try:
            # Jalankan pengecekan
            matches = self._tool.check(text)

            # Konversi hasil ke GrammarError
            errors = [
                GrammarError(
                    message=match.message,
                    short_message=match.shortMessage,
                    offset=match.offset,
                    length=match.errorLength,
                    bad_text=text[match.offset: match.offset + match.errorLength],
                    replacements=list(match.replacements),
                    rule_id=match.ruleId,
                    category=match.category,
                )
                for match in matches
            ]

            # Koreksi otomatis menggunakan saran pertama tiap kesalahan
            corrected_text = language_tool_python.utils.correct(text, matches)

            result = GrammarCheckResult(
                original_text=text,
                corrected_text=corrected_text,
                errors=errors,
                error_count=len(errors),
                is_correct=len(errors) == 0,
            )

            logger.debug(
                f"Grammar check selesai: "
                f"{len(errors)} kesalahan ditemukan"
            )
            return result

        except Exception as e:
            logger.error(f"Error saat grammar check: {e}")
            # Kembalikan hasil kosong jika ada error
            return GrammarCheckResult(
                original_text=text,
                corrected_text=text,
                errors=[],
                error_count=0,
                is_correct=True,
            )

    # ----------------------------------------------------------
    # Format hasil untuk ditampilkan ke siswa
    # ----------------------------------------------------------
    def format_feedback(self, result: GrammarCheckResult) -> str:
        """
        Format hasil pengecekan menjadi teks feedback
        yang mudah dipahami siswa SMP.
        """
        if result.is_correct:
            return "✅ Kalimatmu sudah benar secara grammar!"

        lines = [
            f"📝 Ditemukan {result.error_count} kesalahan grammar:\n"
        ]

        for i, error in enumerate(result.errors, 1):
            lines.append(f"{i}. Kata salah: \"{error.bad_text}\"")
            lines.append(f"   Penjelasan: {error.message}")

            if error.replacements:
                saran = ", ".join(
                    f'"{r}"' for r in error.replacements[:3]
                )
                lines.append(f"   Saran koreksi: {saran}")
            lines.append("")

        if result.original_text != result.corrected_text:
            lines.append(
                f"✨ Kalimat yang benar:\n\"{result.corrected_text}\""
            )

        return "\n".join(lines)

    def close(self) -> None:
        """Tutup koneksi LanguageTool saat shutdown."""
        if self._tool:
            self._tool.close()
            self._tool = None
            logger.info("LanguageTool ditutup.")


# ----------------------------------------------------------
# Instance tunggal — import ini di file lain
# ----------------------------------------------------------
grammar_checker = GrammarCheckerService()