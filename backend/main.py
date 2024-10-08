from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
<<<<<<< HEAD
from predictor import predictor
=======
import predictor 
>>>>>>> c77b0830baa7108ec8cbb14edce9792e4a122857

app = Flask(__name__)
# CORS(app)

@app.route("/", methods=["POST"])
def predict_balance_ball_training():
    try:
        # Flutterから送信されたJSONデータを受け取る
        data = request.get_json()

        if not data:
            return jsonify({"message": "データが空です"}), 400

<<<<<<< HEAD
        # print(f"Received data: {data}")
        print(type(data))
=======
        print(f"Received data: {data}")
>>>>>>> c77b0830baa7108ec8cbb14edce9792e4a122857
        print(f'Data Length: {len(data)}')
        
        # ここでデータ解析を実行
        # predictor.py内の関数などでデータを処理することができます
<<<<<<< HEAD
        result = predictor(data, 100, 3)
        print(type(result))
        result_json = result.to_json(orient = "records", force_ascii=False)
        
        # 解析結果をJSON形式で返す
        return jsonify({"message": "データ受信成功", "data": result_json}), 200
        # return jsonify({"message": "データ受信成功"}), 200
=======
        result = predictor.analyze_data(data, 100, 3)
        print(f'CCC {result}')
        # result_json = result.to_json(orient = "records", force_ascii=False)
        
        # 解析結果をJSON形式で返す
        # return jsonify({"message": "データ受信成功", "data": result_json}), 200
        return jsonify({"message": "データ受信成功"}), 200
>>>>>>> c77b0830baa7108ec8cbb14edce9792e4a122857
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "データ受信失敗"}), 400
    

if __name__ == "__main__":
    app.debug = True
    # app.run(host='192.168.10.102', port=5000)
    app.run(host='172.16.4.31', port=5000)