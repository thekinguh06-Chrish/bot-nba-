import requests
import time

# --- TU CONFIGURACIÓN ---
TOKEN = "8406773199:AAGuhkOWueMc6F0gOcFTNhrYQzxP_Un4QPs"
CHAT_ID = "1769825135"

# Listas basadas en tu Excel
EQUIPOS_TOP = ["Lakers", "Heat", "Celtics", "76ers", "Knicks", "Cavs", "Hornets", "Suns","Rockets","Timberwolves","Nuggets"]
JUGADORES_TOP = ["Luka Doncic", "J. Brunson", "J. Embiid", "James Harden", "D.Mitchell", "Kevin Durant","LaMelo Ball","J.Clarkson","Nic Claxton","Dillon Brooks","D.Booker","Antony Edwards","Nicola Jokic"]

def verificar_partidos_hoy():
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            eventos = data.get('events', [])
            
            mensajes = []
            for evento in eventos:
                # Obtenemos nombres de los equipos que juegan
                home_team = evento['competitions'][0]['competitors'][0]['team']['displayName']
                away_team = evento['competitions'][0]['competitors'][1]['team']['displayName']
                
               # 1. Verificar EQUIPOS (Evita duplicados comparando nombres clave)
                for equipo in EQUIPOS_TOP:
                    if equipo.lower() in home_team.lower() or equipo.lower() in away_team.lower():
                        if equipo == "Heat":
                            mensajes.append("🔥 HOY PARTIDO DEL MIAMI HEAT")
                        else:
                            mensajes.append(f"🏀 HOY PARTIDO DE LOS {equipo.upper()}")

                # 2. Verificar JUGADORES (Asociados a sus equipos actuales)
                # Luka / Lakers
                if "Lakers" in home_team or "Lakers" in away_team:
                    mensajes.append("⭐ HOY JUEGA TU JUGADOR: LUKA DONCIC")
                
                # Brunson / Knicks
                if "Knicks" in home_team or "Knicks" in away_team:
                    if "J. Brunson" in JUGADORES_TOP:
                        mensajes.append("⭐ HOY JUEGA TU JUGADOR: J. BRUNSON")

            # --- LIMPIEZA DE DUPLICADOS Y ORDEN ---
            mensajes_finales = sorted(list(set(mensajes)))

            if mensajes_finales:
                texto_final = "📅 **AGENDA NBA PARA HOY** 📅\n\n" + "\n".join(mensajes_finales)
                enviar_telegram(texto_final)
                print("Mensaje enviado con éxito.")
            else:
                print("No hay partidos de tu interés hoy.")
    except Exception as e:
        print(f"Error: {e}")

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Error enviando a Telegram: {e}")

if __name__ == "__main__":
    print("Verificando agenda del día...")
    verificar_partidos_hoy()
