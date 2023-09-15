import os

import dotenv
import openai
from flask import Flask, render_template, request

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def explain_code_with_chatgpt(code):
    try:
        # ChatGPTを呼び出して解説を生成
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"ソースコードを解説してください：\n{code}",
            max_tokens=50  # 解説の最大トークン数
        )
        explanation = response.choices[0].text
        return explanation
    except Exception as e:
        return str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    explanation = None
    if request.method == 'POST':
        code = request.form.get('code')
        explanation = explain_code_with_chatgpt(code)
    return render_template('index.html', explanation=explanation)

if __name__ == '__main__':
  port = int(os.getenv('PORT', 5000))
  app.run(host='0.0.0.0', port=port)