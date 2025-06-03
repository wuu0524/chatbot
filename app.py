from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# Line Bot 的 Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi('8pabhQTUIrazeSv9wIGUPkok5xp8W/Cf6hMf9E5Rbj5sDUOYxL0uA5riPPvk2Ddhiut39imcJ35B+kMMeRfb519GH23Nd24Wu+Eu2bGiYxXQa5pmCGA0enOXAJ3gG+XElaRz8PANKOnG1nkwoorfuwdB04t89/1O/w1cDnyilFU=')  # 替換為你的 Channel Access Token
handler = WebhookHandler('e6208e0a1f20d88e69368ea6c1a2f276')  # 替換為你的 Channel Secret

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.error("Invalid signature. Check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_message = event.message.text

    app.logger.info(f"Received message from {user_id}: {user_message}")

if __name__ == "__main__":
    app.run(debug=True)
