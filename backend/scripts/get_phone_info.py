"""
Get phone number info from Meta API
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
PHONE_ID = "964874743366135"
API_VERSION = "v22.0"


async def get_phone_info():
    """Get phone number information"""
    url = f"https://graph.facebook.com/{API_VERSION}/{PHONE_ID}"

    params = {
        "access_token": META_TOKEN
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

        print(f"📊 Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("\n📱 Informações do número:")
            print(json.dumps(data, indent=2))

            if "display_phone_number" in data:
                print(f"\n✅ Número do bot: {data['display_phone_number']}")
                print(f"✅ Número formatado: {data.get('display_phone_number')}")
        else:
            print(f"\n❌ Erro: {response.text}")


async def main():
    print("=" * 60)
    print("📞 CONSULTAR INFORMAÇÕES DO NÚMERO")
    print("=" * 60)
    print(f"\n📞 Phone ID: {PHONE_ID}")
    print(f"🔑 Token: {META_TOKEN[:30]}...")

    await get_phone_info()

    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
