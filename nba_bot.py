import asyncio
from playwright.async_api import async_playwright
import requests
import time

# --- CONFIGURACIÓN ---
TOKEN = "8406773199:AAGuhkOWueMc6F0gOcFTNhrYQzxP_Un4QPs"
CHAT_ID = "1769825135"
EQUIPOS_INTERES = ["Celtics", "Heat", "Hawks", "76ers", "Bulls", "Clippers", "Rockets", "Suns", "Nuggets", "Timberwolves"]
META_PUNTOS = 22

async def buscar_puntos():
    async with async_playwright() as p:
        print("🚀 Iniciando navegador invisible...")
        # AJUSTE PARA LA NUBE: Añadimos argumentos de seguridad
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        page = await browser.new_page()
        
        try:
            # Vamos a la página de resultados
            print("🔗 Accediendo a ESPN...")
            await page.goto("https://www.espn.com.mx/basquetbol/nba/resultados", timeout=60000)
            print("🔍 Buscando marcadores de tus equipos...")

            contenido = await page.content()
            
            for equipo in EQUIPOS_INTERES:
                if equipo in contenido:
                    # Buscamos los puntos en el bloque del equipo
                    marcador_texto = await page.locator(f"text={equipo} >> xpath=..").inner_text()
                    numeros = [int(s) for s in marcador_texto.split() if s.isdigit()]
                    if numeros:
                        puntos_actuales = max(numeros)
                        if puntos_actuales >= META_PUNTOS:
                            enviar_telegram(equipo, puntos_actuales)
        except Exception as e:
            print(f"⚠️ Error al acceder a la página: {e}")
        finally:
            await browser.close()
            print("🏁 Navegador cerrado.")

def enviar_telegram(equipo, puntos):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    mensaje = f"🏀 ALERT NBA 🏀\n\n✅ {equipo} ya tiene {puntos} puntos!"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": mensaje})
        print(f"📩 Notificación enviada para {equipo}")
    except Exception as e:
        print(f"❌ Error enviando a Telegram: {e}")

async def loop_infinito():
    while True:
        try:
            print(f"\n{'-'*30}")
            print(f"🕒 Hora: {time.strftime('%H:%M:%S')}")
            print("🔄 Iniciando ronda de vigilancia...")
            await buscar_puntos()
            print("💤 Esperando 5 minutos para la próxima revisión...")
            await asyncio.sleep(300) # Usamos sleep de asyncio para no congelar el servidor
            
        except Exception as e:
            print(f"❌ Ocurrió un error en el bucle: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(loop_infinito())