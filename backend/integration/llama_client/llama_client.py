# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Llama Client (Orkestrator)
#  File: backend/integration/llama_client/llama_client.py
# ============================================================

from typing import List, Dict, Tuple

import httpx

from core.config import settings
from core.logging import logger
from integration.llama_client.request_formatter import RequestFormatter
from integration.llama_client.response_parser import ResponseParser
from integration.llama_client.error_handler import ErrorHandler, LlamaAPIError
from integration.llama_client.token_counter import TokenCounter
from integration.llama_client.retry_logic import RetryLogic


class LlamaClient:
    """
    Client utama untuk berkomunikasi dengan Llama API.
    Mengkoordinasikan semua komponen integration layer.
    """

    def __init__(self):
        self.formatter = RequestFormatter()
        self.parser = ResponseParser()
        self.error_handler = ErrorHandler()
        self.token_counter = TokenCounter()
        self.retry_logic = RetryLogic()

    async def chat(
        self,
        context: List[Dict[str, str]],
        user_message: str,
    ) -> Tuple[str, int]:
        """
        Kirim pesan ke Llama API dan dapatkan respons.

        Args:
            context      : List pesan konteks dari ContextManager
            user_message : Pesan terbaru dari siswa

        Returns:
            Tuple (teks_respons_ai, jumlah_token_dipakai)
        """
        return await self.retry_logic.execute_with_retry(
            self._send_request,
            context=context,
            user_message=user_message,
        )

    async def _send_request(
        self,
        context: List[Dict[str, str]],
        user_message: str,
    ) -> Tuple[str, int]:
        """Kirim satu request ke Llama API."""

        # 1. Format payload
        payload = self.formatter.format(context, user_message)

        # 2. Cek estimasi token
        token_summary = self.token_counter.get_token_summary(
            payload["messages"]
        )
        logger.debug(
            f"Estimasi token: {token_summary['estimated_tokens']} "
            f"({token_summary['usage_percent']}% dari limit)"
        )

        # 3. Kirim request ke API
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    url=f"{settings.LLAMA_API_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.LLAMA_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )

            # 4. Handle error HTTP
            if response.status_code != 200:
                self.error_handler.handle_http_error(
                    response.status_code,
                    response.text,
                )

            # 5. Parse respons
            response_data = response.json()
            text, token_used = self.parser.parse(response_data)

            logger.info(
                f"Llama API berhasil: token_used={token_used}"
            )
            return text, token_used

        except httpx.TimeoutException:
            self.error_handler.handle_timeout_error()

        except httpx.ConnectError as e:
            self.error_handler.handle_connection_error(e)

        except LlamaAPIError:
            raise

        except Exception as e:
            logger.error(f"Error tidak terduga di LlamaClient: {e}")
            raise LlamaAPIError(f"Error tidak terduga: {str(e)}")