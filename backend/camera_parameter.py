import cv2
import numpy as np

def cameraParameter(square_size, pattern_size, reference_img):
    pattern_points = np.zeros( (np.prod(pattern_size), 3), np.float32 ) #チェスボード（X,Y,Z）座標の指定 (Z=0)
    pattern_points[:,:2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size
    obj_points = []
    img_points = []


    capture = cv2.VideoCapture(0)

    while len(obj_points) < reference_img:
    # 画像の取得
        ret, img = capture.read()
        height = img.shape[0]
        width = img.shape[1]

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # チェスボードのコーナーを検出
        ret, corner = cv2.findChessboardCorners(gray, pattern_size)
        # コーナーがあれば
        if ret == True:
            print("detected coner!")
            print(str(len(obj_points)+1) + "/" + str(reference_img))
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
            cv2.cornerSubPix(gray, corner, (5,5), (-1,-1), term)
            img_points.append(corner.reshape(-1, 2))   #appendメソッド：リストの最後に因数のオブジェクトを追加
            obj_points.append(pattern_points)

        cv2.imshow('image', img)
        # 毎回判定するから 200 ms 待つ．遅延するのはココ
        if cv2.waitKey(200) & 0xFF == ord('q'):
            break

    print("calculating camera parameter...")
    # 内部パラメータを計算
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

    # 計算結果を保存
    np.save("mtx", mtx) # カメラ行列
    np.save("dist", dist.ravel()) # 歪みパラメータ
    # 計算結果を表示
    print("RMS = ", ret)
    print("mtx = \n", mtx)
    print("dist = ", dist.ravel())