import requests, os, time
from db import Session, Alert
from telegram import Bot


API_KEY = os.getenv("ODDS_API_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT = Bot(token=BOT_TOKEN)


API_URL = "https://api.the-odds-api.com/v4/sports/soccer/odds"


while True:
session = Session()
alerts = session.query(Alert).all()
for alert in alerts:
params = {
"apiKey": API_KEY,
"regions": "eu",
"markets": "totals", # Over/Under goals
"oddsFormat": "decimal"
}
resp = requests.get(API_URL, params=params)
data = resp.json()
for match in data:
if alert.match.lower() in match["home_team"].lower() or alert.match.lower() in match["away_team"].lower():
for bookmaker in match["bookmakers"]:
for market in bookmaker["markets"]:
if market["key"] == "totals":
for outcome in market["outcomes"]:
if outcome["name"] == "Over 2.5" and float(outcome["price"]) > 1.7:
TELEGRAM_BOT.send_message(
chat_id=alert.user_id,
text=f"⚽ {match['home_team']} vs {match['away_team']}\nOver 2.5 goals now {outcome['price']} at {bookmaker['title']}"
)
session.delete(alert)
session.commit()
time.sleep(60)
