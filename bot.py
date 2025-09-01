from telegram.ext import Updater, CommandHandler
from db import Session, Alert
import os


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def start(update, context):
update.message.reply_text("⚽ Welcome! This bot sends alerts when Over 2.5 goals odds go above 1.7.")


def addalert(update, context):
session = Session()
match = " ".join(context.args)
if not match:
update.message.reply_text("Usage: /addalert <team or match>")
return
alert = Alert(user_id=update.message.chat_id, match=match)
session.add(alert)
session.commit()
update.message.reply_text(f"✅ Alert created for {match}: Over 2.5 goals > 1.7")


def myalerts(update, context):
session = Session()
alerts = session.query(Alert).filter_by(user_id=update.message.chat_id).all()
if not alerts:
update.message.reply_text("You have no active alerts.")
else:
msg = "\n".join([f"{a.id}: {a.match}" for a in alerts])
update.message.reply_text("📋 Your alerts:\n" + msg)


def removealert(update, context):
session = Session()
try:
alert_id = int(context.args[0])
session.query(Alert).filter_by(id=alert_id, user_id=update.message.chat_id).delete()
session.commit()
update.message.reply_text("❌ Alert removed")
except:
update.message.reply_text("Usage: /removealert <id>")


def main():
updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("addalert", addalert))
dp.add_handler(CommandHandler("myalerts", myalerts))
dp.add_handler(CommandHandler("removealert", removealert))
updater.start_polling()
updater.idle()


if __name__ == "__main__":
main()
