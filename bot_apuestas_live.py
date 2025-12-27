import requests
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- CONFIGURACIÓN ---
TOKEN = "8406773199:AAGuhkOWueMc6F0gOcFTNhrYQzxP_Un4QPs"
CHAT_ID = "1769825135"

DEPORTES = {
    "NBA": "basketball/nba", "NHL (Hockey)": "hockey/nhl",
    "Champions League": "soccer/uefa.champions", "Liga MX": "soccer/mex.1",
    "LaLiga": "soccer/esp.1", "Bundesliga": "soccer/ger.1",
    "Eredivisie": "soccer/ned.1", "Serie A": "soccer/ita.1",
    "Premier League": "soccer/eng.1", "Europa League": "soccer/uefa.europa",
    "Libertadores": "soccer/libertadores", "Liga Portugal": "soccer/por.1",
    "Escocia": "soccer/sco.1", "Turquía": "soccer/tur.1"
}

# --- SERVIDOR FANTASMA PARA RENDER ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot en linea")

def run_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleHandler)
    server.serve_forever()

# --- LÓGICA DEL BOT ---
def analizar_vivo():
    alertas = []
    for nombre, path in DEPORTES.items():
        url = f"https://site.api.espn.com/apis/site/v2/sports/{path}/scoreboard"
        try:
            res = requests.get(url, timeout=10).json()
            for ev in res.get('events', []):
                if ev['status']['type']['state'] == "in":
                    detalles = ev['competitions'][0]
                    home = detalles['competitors'][0]
                    away = detalles['competitors'][1]
                    reloj = ev['status']['displayValue']
                    # Alerta si es minuto 70+ y van empatados o diferencia de 1
                    if "soccer" in path and ("7" in reloj or "8" in reloj):
                        if abs(int(home['score']) - int(away['score'])) <= 1:
                            alertas.append(f"⚽ **ALERTA ({nombre})**\n🎯 Minuto: {reloj}\n🏟️ {away['team']['displayName']} {away['score']} - {home['score']} {home['team']['displayName']}")
        except: continue
    return alertas

def enviar_telegram(msj):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msj, "parse_mode": "Markdown"})

if __name__ == "__main__":
    # Iniciar servidor en segundo plano para Render
    threading.Thread(target=run_server, daemon=True).start()
    
    enviar_telegram("🚀 **MONITOR MULTIDEPORTE ACTIVADO**\n\nAnalizando 14 competiciones. ¡Listo para las alertas en vivo!")
    
    while True:
        for op in analizar_vivo():
            enviar_telegram(op)
        time.sleep(600)
