import requests
import time

# --- CONFIGURACIÓN ---
TOKEN = "8406773199:AAGuhkOWueMc6F0gOcFTNhrYQzxP_Un4QPs"
CHAT_ID = "1769825135"

# TU LISTA EXACTA DE JUGADORES Y EQUIPOS
JUGADORES_EQUIPOS = {
    "J. Brunson": "Knicks",
    "D. Mitchell": "Cavaliers", # Cavs
    "J. Clarkson": "Knicks",
    "LaMelo Ball": "Hornets",
    "J. Embiid": "76ers",
    "Nic Claxton": "Nets",
    "James Harden": "Clippers",
    "Dillon Brooks": "Suns",
    "D. Booker": "Suns",
    "Kevin Durant": "Rockets",
    "Luka Doncic": "Lakers",
    "Antony Edwards": "Timberwolves",
    "Nicola Jokic": "Nuggets"
}

EQUIPOS_INTERES = [
    "Celtics", "Heat", "Hawks", "76ers", "Bulls", 
    "Clippers", "Rockets", "Suns", "Nuggets", "Timberwolves"
]

def verificar_agenda():
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
    try:
        response = requests.get(url, timeout=15)
        data = response.json()
        eventos = data.get('events', [])
        
        equipos_hoy = []
        for evento in eventos:
            for competidor in evento['competitions'][0]['competitors']:
                equipos_hoy.append(competidor['team']['displayName'])

        mensajes = []
        
        # 1. Avisar de los EQUIPOS de tu lista que juegan hoy
        for equipo_mio in EQUIPOS_INTERES:
            if any(equipo_mio.lower() in e.lower() for e in equipos_hoy):
                mensajes.append(f"🏀 HOY PARTIDO DE LOS {equipo_mio.upper()}")

        # 2. Avisar de los JUGADORES de tu lista que juegan hoy
        for jugador, equipo_jugador in JUGADORES_EQUIPOS.items():
            if any(equipo_jugador.lower() in e.lower() for e in equipos_hoy):
                mensajes.append(f"⭐ HOY JUEGA TU JUGADOR: {jugador}")

        if mensajes:
            # Eliminar duplicados y ordenar
            final_list = sorted(list(set(mensajes)))
            texto_final = "📅 **AGENDA NBA PARA HOY** 📅\n\n" + "\n".join(final_list)
            enviar_telegram(texto_final)
            print("Notificación enviada con éxito.")
        else:
            print("No hay actividad de tu lista hoy.")
            
    except Exception as e:
        print(f"Error: {e}")

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})

if __name__ == "__main__":
    while True:
        verificar_agenda()
        # Se repite cada 12 horas automáticamente sin entrar a Render
        print("Bot en espera por 12 horas...")
        time.sleep(43200)
