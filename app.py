from flask import Flask, request, jsonify
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

app = Flask(__name__)

# GPT 初始化（用 LangChain 包裝）
llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-3.5-turbo",
openai_api_key = os.getenv("OPENAI_API_KEY")

# 對話記憶機制：記住過去對話
memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(llm=llm, memory=memory, verbose=False)

# Dialogflow 的 webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    user_input = req['queryResult']['queryText']

    try:
        # 用 GPT 回應，並帶入記憶
        reply = conversation.predict(input=user_input)
        print("🧠 GPT 回應：", reply)
        return jsonify({"fulfillmentText": reply})
    except Exception as e:
        print("❌ 錯誤：", str(e))
        return jsonify({"fulfillmentText": "系統發生錯誤，請稍後再試。"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
