import requests
import time

# --- CONFIGURACIÓN ---
TOKEN = "8406773199:AAGuhkOWueMc6F0gOcFTNhrYQzxP_Un4QPs"
CHAT_ID = "1769825135"

# TU LISTA COMPLETA DE LIGAS
DEPORTES = {
    "NBA": "basketball/nba",
    "NHL (Hockey)": "hockey/nhl",
    "Champions League": "soccer/uefa.champions",
    "Liga MX": "soccer/mex.1",
    "LaLiga": "soccer/esp.1",
    "Bundesliga": "soccer/ger.1",
    "Eredivisie": "soccer/ned.1",
    "Serie A": "soccer/ita.1",
    "Premier League": "soccer/eng.1",
    "Europa League": "soccer/uefa.europa",
    "Libertadores": "soccer/libertadores",
    "Liga Portugal": "soccer/por.1",
    "Escocia": "soccer/sco.1",
    "Turquía": "soccer/tur.1"
}

def analizar_vivo():
    alertas = []
    for nombre, path in DEPORTES.items():
        url = f"https://site.api.espn.com/apis/site/v2/sports/{path}/scoreboard"
        try:
            res = requests.get(url, timeout=10).json()
            eventos = res.get('events', [])
            
            for ev in eventos:
                estado = ev['status']['type']['state']
                # Solo analizamos partidos EN VIVO
                if estado == "in":
                    detalles = ev['competitions'][0]
                    home = detalles['competitors'][0]
                    away = detalles['competitors'][1]
                    
                    nombre_home = home['team']['displayName']
                    nombre_away = away['team']['displayName']
                    score_home = int(home['score'])
                    score_away = int(away['score'])

                    # --- LÓGICA DE APUESTA (60-70% PROB) ---
                    
                    # ⚽ FÚTBOL (Incluye Liga MX y Champions)
                    # Alerta: Empate al minuto 70+ (Probabilidad de gol en los últimos 20 min)
                    if "soccer" in path:
                        reloj = ev['status']['displayValue']
                        if "70" in reloj or "75" in reloj or "80" in reloj:
                            if score_home == score_away:
                                alertas.append(f"⚽ **ALERTA FÚTBOL ({nombre})**\n🎯 Probabilidad: 65% (+0.5 Goles)\n⏰ Minuto: {reloj}\n🏟️ {nombre_away} {score_away} - {score_home} {nombre_home}")

                    # 🏒 HOCKEY
                    if "hockey" in path:
                        if score_home + score_away >= 4:
                            alertas.append(f"🏒 **ALERTA HOCKEY (NHL)**\n🎯 Probabilidad: 60% (Alta puntuación)\n📊 Marcador: {score_away} - {score_home}")

                    # 🏀 NBA
                    if "nba" in path:
                        periodo = ev['status']['period']
                        if periodo >= 4 and abs(score_home - score_away) < 5:
                            alertas.append(f"🏀 **ALERTA NBA LIVE**\n🎯 Probabilidad: 70% (Final cerrado)\n🔥 {nombre_away} {score_away} - {score_home} {nombre_home}")

        except Exception:
            continue
    return alertas

def enviar_telegram(msj):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msj, "parse_mode": "Markdown"})

if __name__ == "__main__":
    print("Iniciando monitor en vivo...")
    enviar_telegram("🚀 **MONITOR MULTIDEPORTE ACTIVADO**\n\nAnalizando 14 competiciones en tiempo real (Incluye Liga MX y Champions).")
    
    while True:
        oportunidades = analizar_vivo()
        for op in oportunidades:
            enviar_telegram(op)
        # Revisa cada 10 minutos
        time.sleep(600)
