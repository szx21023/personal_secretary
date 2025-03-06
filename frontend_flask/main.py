from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 根路由，顯示 HTML 頁面
@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/submit_form', methods=['POST'])
# def submit_form():
#     try:
#         # 從請求中解析 JSON 資料
#         data = request.get_json()

#         # 在這裡可以對資料進行處理，例如存儲到資料庫、發送電子郵件等
#         name = data.get('name')
#         email = data.get('email')
#         message = data.get('message')

#         # 假設處理成功，返回成功的回應
#         return jsonify({'status': 'success', 'message': 'Form submitted successfully!', 'name': name, 'email': email, 'message': message})

#     except Exception as e:
#         # 如果發生錯誤，返回錯誤訊息
#         return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)