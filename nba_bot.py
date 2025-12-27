import requests
import time
import asyncio

# --- CONFIGURACIÓN ---
TOKEN = "8406773199:AAGuhkOWueMc6F0gOcFTNhrYQzxP_Un4QPs"
CHAT_ID = "1769825135"
EQUIPOS_INTERES = ["Celtics", "Heat", "Hawks", "76ers", "Bulls", "Clippers", "Rockets", "Suns", "Nuggets", "Timberwolves"]
META_PUNTOS = 22

def obtener_puntos_nba():
    # Esta URL es la API de ESPN, permitida en todos lados
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            eventos = data.get('events', [])
            
            encontrado = False
            for evento in eventos:
                for competidor in evento.get('competitions', [])[0].get('competitors', []):
                    nombre_equipo = competidor.get('team', {}).get('shortDisplayName')
                    puntos = int(competidor.get('score', 0))
                    
                    if nombre_equipo in EQUIPOS_INTERES:
                        encontrado = True
                        print(f"🏀 {nombre_equipo}: {puntos} pts")
                        if puntos >= META_PUNTOS:
                            enviar_telegram(nombre_equipo, puntos)
            
            if not encontrado:
                print("No hay partidos en curso de tus equipos en este momento.")
        else:
            print(f"⚠️ Error de servidor: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def enviar_telegram(equipo, puntos):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    mensaje = f"🏀 ALERT NBA 🏀\n\n✅ {equipo} ya tiene {puntos} puntos!"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": mensaje})
    except:
        pass

async def loop_principal():
    while True:
        print(f"\n[{time.strftime('%H:%M:%S')}] 🔄 Vigilando marcadores...")
        obtener_puntos_nba()
        print("💤 Esperando 5 minutos...")
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(loop_principal())
