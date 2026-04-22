# ============================================================
#  ENGLISH GRAMMAR CHATBOT — LangChain Chain
#  File: backend/integration/langchain/chain.py
# ============================================================

import json
from typing import List, Dict, Optional

from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_groq import ChatGroq

from core.config import settings
from core.logging import logger
from integration.langchain.prompt_template import (
    chat_prompt,
    summary_prompt,
    recommendation_prompt,
)


class GrammarChatChain:
    """
    LangChain chain untuk percakapan grammar chatbot.
    Menggunakan Llama API yang kompatibel dengan format OpenAI.
    """

    def __init__(self):
        # Llama API kompatibel dengan format OpenAI
        # sehingga bisa pakai ChatOpenAI dengan base_url custom
        self.llm = ChatGroq(
            model=settings.LLAMA_MODEL,
            groq_api_key=settings.LLAMA_API_KEY,
            max_tokens=settings.LLAMA_MAX_TOKENS,
            temperature=settings.LLAMA_TEMPERATURE,
        )

    # ----------------------------------------------------------
    # Generate respons percakapan
    # ----------------------------------------------------------
    async def generate_response(
        self,
        user_message: str,
        summary_context: str = "",
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """
        Generate respons AI untuk pesan siswa.

        Args:
            user_message    : Pesan terbaru dari siswa
            summary_context : Ringkasan percakapan sebelumnya
            chat_history    : Riwayat pesan terbaru

        Returns:
            Teks respons dari AI
        """
        try:
            # Format system prompt dengan summary
            system_content = chat_prompt.messages[0].prompt.format(
                summary_context=(
                    f"\nRingkasan percakapan sebelumnya:\n{summary_context}"
                    if summary_context else ""
                )
            )

            # Susun messages
            messages = [SystemMessage(content=system_content)]

            # Tambahkan riwayat chat
            if chat_history:
                for msg in chat_history:
                    if msg["role"] == "user":
                        messages.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "assistant":
                        messages.append(AIMessage(content=msg["content"]))

            # Tambahkan pesan user terbaru
            messages.append(HumanMessage(content=user_message))

            # Kirim ke LLM
            response = await self.llm.ainvoke(messages)
            logger.info("LangChain: Respons berhasil di-generate")
            return response.content

        except Exception as e:
            logger.error(f"LangChain generate_response error: {e}")
            raise

    # ----------------------------------------------------------
    # Generate ringkasan percakapan
    # ----------------------------------------------------------
    async def generate_summary(self, conversation_text: str) -> str:
        """
        Generate ringkasan dari teks percakapan.

        Args:
            conversation_text: Percakapan dalam format teks

        Returns:
            Teks ringkasan
        """
        try:
            formatted = summary_prompt.format_messages(
                conversation=conversation_text
            )
            response = await self.llm.ainvoke(formatted)
            logger.info("LangChain: Ringkasan berhasil dibuat")
            return response.content

        except Exception as e:
            logger.error(f"LangChain generate_summary error: {e}")
            raise

    # ----------------------------------------------------------
    # Generate rekomendasi topik
    # ----------------------------------------------------------
    async def generate_recommendations(
        self, learning_history: str
    ) -> List[Dict]:
        """
        Generate rekomendasi topik grammar untuk siswa.

        Args:
            learning_history: Ringkasan topik yang sudah dipelajari

        Returns:
            List rekomendasi topik
        """
        try:
            formatted = recommendation_prompt.format_messages(
                learning_history=learning_history
            )
            response = await self.llm.ainvoke(formatted)

            # Parse JSON dari respons
            raw = response.content.strip()
            # Bersihkan markdown code block jika ada
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]

            data = json.loads(raw)
            recommendations = data.get("recommendations", [])

            logger.info(
                f"LangChain: {len(recommendations)} rekomendasi dibuat"
            )
            return recommendations

        except json.JSONDecodeError as e:
            logger.error(f"LangChain: Gagal parse JSON rekomendasi: {e}")
            return []

        except Exception as e:
            logger.error(f"LangChain generate_recommendations error: {e}")
            raise


# ----------------------------------------------------------
# Instance tunggal
# ----------------------------------------------------------
grammar_chain = GrammarChatChain()