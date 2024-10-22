from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from predictor import predictor
from dotenv import load_dotenv
import pandas as pd
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
# CORS(app)

load_dotenv()
upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'upload')

if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

ALLOWED_EXTENSIONS = set({'mp4', 'mov', 'avi'})

# ファイルの拡張子をチェックする関数
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["POST"])
def predict_balance_ball_training():
    try:
        # Flutterから送信されたJSONデータを受け取る
        data = request.get_json()

        if not data:
            return jsonify({"message": "データが空です"}), 400

        # print(f"Received data: {data}")
        print(type(data))
        print(f'Data Length: {len(data)}')
        
        # ここでデータ解析を実行
        # predictor.py内の関数などでデータを処理することができます
        result = predictor(data, 100, 3)
        print(type(result))
        result_json = result.to_json(orient = "records", force_ascii=False)
        
        # 解析結果をJSON形式で返す
        return jsonify({"message": "データ受信成功", "data": result_json}), 200
        # return jsonify({"message": "データ受信成功"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "データ受信失敗"}), 400
    
@app.route("/upload/mag", methods=["POST"])
def upload_mag_data():
    try:
        data = request.get_json()
        file_name = data.get('file_name')
        mag_data = data.get('mag_data')
        df = pd.DataFrame(mag_data, columns=['time', 'x', 'y', 'z', 'elapsed time'])
        csv_filename = os.path.join(upload_folder, f"{file_name}.csv")
        df.to_csv(csv_filename, index=False)
        print(f"センサーデータをCSVに保存しました: {csv_filename}")
        return "Success", 200  
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": f"データ受信失敗: {str(e)}"}), 400

@app.route("/upload/ar", methods=["POST"])
def upload_ar_data():

    try:
        if 'file' not in request.files:
            return 'No file part', 400
        
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        
        # ファイルが正しい形式か確認して保存
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            video_save_path = os.path.join(upload_folder, filename)
            file.save(video_save_path)
            print(f"ビデオファイルを保存しました: {video_save_path}")
            return 'File successfully uploaded', 200
        else:
            return 'Unsupported file type', 415
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": f"データ受信失敗: {str(e)}"}), 400

if __name__ == "__main__":
        app.debug = True
        # app.run(host='192.168.10.102', port=5000)
        app.run(host='172.16.4.31', port=5000)