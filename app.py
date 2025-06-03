from flask import Flask, request, jsonify
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import traceback

app = Flask(__name__)

# GPT 初始化（用 LangChain 包裝）
llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# 對話記憶機制
memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(llm=llm, memory=memory, verbose=False)

# Dialogflow webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    user_input = req['queryResult']['queryText']

    try:
        reply = conversation.predict(input=user_input)
        print("🧠 GPT 回應：", reply)
        return jsonify({"fulfillmentText": reply})
    except Exception as e:
        print("❌ 錯誤：", str(e))
        traceback.print_exc()  # ← 印出完整錯誤堆疊
        return jsonify({"fulfillmentText": f"系統錯誤：{str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
