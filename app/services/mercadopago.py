import os
import requests
import qrcode
from dotenv import load_dotenv
from typing import Any, Dict
from io import BytesIO

load_dotenv()

class MercadoPagoService:
    """Classe para gerenciar integração com a API do Mercado Pago."""

    BASE_URL = "https://api.mercadopago.com"
    ACCESS_TOKEN = os.getenv("MERCADOPAGO")

    @staticmethod
    def create_preference(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria uma preferência de pagamento.

        Args:
            payload (Dict[str, Any]): Os dados necessários para criar a preferência.

        Returns:
            Dict[str, Any]: A resposta da API sobre a preferência criada.
        """
        url = f"{MercadoPagoService.BASE_URL}/checkout/preferences"
        headers = {
            "Authorization": f"Bearer {MercadoPagoService.ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    @staticmethod
    def generate_qr_code(url: str) -> BytesIO:
        """
        Gera um QR Code a partir de uma URL.

        Args:
            url (str): A URL para a qual o QR Code deve apontar.

        Returns:
            BytesIO: Um stream contendo a imagem do QR Code.
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer)
        buffer.seek(0)
        return buffer
