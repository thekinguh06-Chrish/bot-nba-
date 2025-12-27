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
                
                # 1. Verificar si juega un EQUIPO de tu lista
                for equipo in EQUIPOS_TOP:
                    if equipo in home_team or equipo in away_team:
                        mensajes.append(f"🏀 HOY PARTIDO DE LOS {equipo.upper()}")

                # 2. Verificar si juega un JUGADOR de tu lista (basado en su equipo)
                # Nota: Aquí asociamos al jugador con su equipo para saber si juega
                if "Mavericks" in home_team or "Mavericks" in away_team:
                    if "Luka Doncic" in JUGADORES_TOP:
                        mensajes.append(f"⭐ HOY JUEGA TU JUGADOR: LUKA DONCIC")
                
                if "Heat" in home_team or "Heat" in away_team:
                    mensajes.append(f"🔥 HOY PARTIDO DEL MIAMI HEAT")

            # Eliminar duplicados y enviar
            final_list = list(set(mensajes))
            if final_list:
                texto_final = "📅 **AGENDA NBA PARA HOY** 📅\n\n" + "\n".join(final_list)
                enviar_telegram(texto_final)
            else:
                print("No hay partidos de tu interés hoy.")
    except Exception as e:
        print(f"Error: {e}")

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})

if __name__ == "__main__":
    print("Verificando agenda del día...")
    verificar_partidos_hoy()
