"""
Script de teste para enviar mensagem WhatsApp via Meta API
Use este script para testar a integração e descobrir o Phone Number ID
"""

import sys
import httpx
import asyncio
import json

# Fix Windows UTF-8 encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# Configurações
META_TOKEN = "EAALmf481QMUBQKiIai9O2WZCWhY3DfYlF6At6epfyVynmDoYTbSTJG4UJnXtPxVUsIZAN5SrA2OG3nI5DvRkdeej2Y417YPBjf8mH9youQJi2VefEptZBwSyqVa5iT6H4ee1K7Xwmv4ojY0ZBvZB1Jz2TJHo8AhuhqJDiGSYEs91XkOZADNTiwrg88Wq10qa5hlbnkjtsySD8L9qzXVPpMie7qeQ21EcEZA914hEo3cgLMe6Mxf8OE6bDPuAwedvk1SIt2fb3MU9fMJkcAEkaxQPff6"
PHONE_ID = "964874743366135"  # Phone Number ID da Meta
FROM_PHONE = "15551534852"  # Número do bot (sem +)
TO_PHONE = "5511995989872"   # Seu número (sem +)
API_VERSION = "v22.0"  # Versão da API


async def send_test_message():
    """
    Envia uma mensagem de teste para o seu número.
    """
    print(f"\n📤 Enviando mensagem de teste...")

    url = f"https://graph.facebook.com/{API_VERSION}/{PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {META_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": TO_PHONE,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": "🤖 Olá! Esta é uma mensagem de teste do FINAP Bot! Se você recebeu esta mensagem, a integração está funcionando! 🎉"
        }
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            print(f"\n📊 Status: {response.status_code}")
            print(f"📄 Resposta:\n{json.dumps(response.json(), indent=2)}")

            if response.status_code == 200:
                print("\n✅ Mensagem enviada com sucesso!")
                print(f"✅ Verifique seu WhatsApp no número: +{TO_PHONE}")
            else:
                print("\n❌ Erro ao enviar mensagem")

    except Exception as e:
        print(f"\n❌ Erro: {e}")


async def main():
    """Função principal"""
    print("=" * 60)
    print("🤖 TESTE DE INTEGRAÇÃO WHATSAPP - META API")
    print("=" * 60)
    print(f"\n📱 De: +{FROM_PHONE}")
    print(f"📱 Para: +{TO_PHONE}")
    print(f"📞 Phone ID: {PHONE_ID}")
    print(f"🔑 Token: {META_TOKEN[:30]}...")

    # Enviar mensagem de teste
    await send_test_message()

    print("\n" + "=" * 60)
    print("✅ Teste concluído!")
    print("=" * 60)
    print("\n📋 Configurações usadas (já estão no .env):")
    print(f"META_WHATSAPP_TOKEN={META_TOKEN[:30]}...")
    print(f"META_WHATSAPP_PHONE_ID={PHONE_ID}")
    print(f"META_WHATSAPP_API_VERSION={API_VERSION}")
    print(f"META_WHATSAPP_FROM_NUMBER=+{FROM_PHONE}")
    print("\n")


if __name__ == "__main__":
    asyncio.run(main())
