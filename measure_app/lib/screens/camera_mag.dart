import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:http_parser/http_parser.dart';
import 'dart:io';
import 'dart:async';
import 'dart:convert';
import 'package:measure_app/function/magnetometer_measure_controller.dart';
import 'package:measure_app/widget/operation_button.dart';
// import 'package:path/path.dart';
import 'package:http/http.dart' as http;
import 'package:auto_size_text/auto_size_text.dart';
import 'package:path_provider/path_provider.dart';

class GetMagnetometerAR extends StatefulWidget {
  const GetMagnetometerAR({super.key});

  @override
  GetMagnetometerARState createState() => GetMagnetometerARState();
}

class GetMagnetometerARState extends State<GetMagnetometerAR> {
  bool _isCalibrating = false;
  bool _isMeasuring = false;
  List<CameraDescription>? _cameras;
  List<String> _videoPaths = [];
  // Timer? _timer;
  String magDataJson = "";
  String videoPath = "";
  List<List<dynamic>> _measurementData = [];
  late CameraController _cameraController;
  TextEditingController _textEditController = TextEditingController();
  final MagnetometerMeasureController _magnetometerMeasureController =
      MagnetometerMeasureController();

  @override
  void initState() {
    super.initState();
    _getCamera();
  }

  @override
  void dispose() {
    _cameraController.dispose();
    super.dispose();
  }

  Future<void> _getCamera() async {
    _cameras = await availableCameras();
    if (_cameras != null && _cameras!.isNotEmpty) {
      _cameraController = CameraController(
        _cameras![1],
        ResolutionPreset.max,
      );
      try {
        await _cameraController.initialize();
        setState(() {});
      } catch (e) {
        print("カメラの初期化に失敗しました: $e");
      }
      print(_cameras);
    }
  }

  void _Calibration() {}

  Future<void> _startMeasurement() async {
    if (!_isMeasuring) {
      _isMeasuring = true;

      try {
        final directory = await getTemporaryDirectory();
        videoPath =
            '${directory.path}/${DateTime.now().microsecondsSinceEpoch}.mp4';
        await _cameraController.startVideoRecording();
        _magnetometerMeasureController.startMeasurement();
        print("ビデオ録画を開始しました: $videoPath");
      } catch (e) {
        print('ビデオ録画の開始に失敗しました: $e');
      }
    }
  }

  Future<void> _stopMeasurement() async {
    _isMeasuring = false;

    try {
      final videoFile = await _cameraController.stopVideoRecording();

      // 保存するファイルのパスを作成
      final directory = await getTemporaryDirectory();
      // final videoPath = '${directory.path}/${DateTime.now().microsecondsSinceEpoch}.mp4';
      final videoPath = '${directory.path}/${_textEditController.text}.mp4';

      // ファイルをコピーして、元のファイルを削除
      final newFile = await File(videoFile.path).copy(videoPath);
      await File(videoFile.path).delete(); // 元のファイルを削除

      print("ビデオ録画が終了しました: ${newFile.path}");
      _videoPaths.add(newFile.path); // コピー先の新しいパスをリストに追加
    } catch (e) {
      print("ビデオ録画の停止に失敗しました: $e");
    }

    _sendMagDataToServer();
    _sendVideoToServer();
  }

  Future<void> _sendMagDataToServer() async {
    _measurementData = _magnetometerMeasureController.stopMeasurementAndGet();
    final magDataForSend = _measurementData.map((data) {
      return [
        (data[0] as DateTime)
            .toIso8601String()
            .replaceAll('T', ' '), // DateTimeをISO8601形式の文字列に変換
        data[1], // x
        data[2], // y
        data[3], // z
        data[4],
      ];
    }).toList();

    String fileName = _textEditController.text;

    final requestData = {'file_name': fileName, 'mag_data': magDataForSend};

    // print(magDataJson);
    try {
      final magResponse = await http.post(
        Uri.parse('http://172.16.4.31:5000/upload/mag'),
        headers: {
          "Content-Type": "application/json",
        },
        body: json.encode(requestData),
      );
      if (magResponse.statusCode == 200) {
        print('データ送信成功');
      } else {
        print('データ送信失敗');
      }
    } catch (e) {
      print('磁気センサデータの送信中にエラーが発生しました: $e');
    }
  }

  Future<void> _sendVideoToServer() async {
    if (_videoPaths.isNotEmpty) {
      try {
        String videoPath = _videoPaths.first; // 最初の動画パスを取得
        File videoFile = File(videoPath);

        var request = http.MultipartRequest(
          'POST',
          Uri.parse('http://172.16.4.31:5000/upload/ar'),
        );

        request.files.add(await http.MultipartFile.fromPath(
            'file', videoFile.path,
            contentType: MediaType('video', 'mp4')));

        var streamedResponse = await request.send();
        var response = await http.Response.fromStream(streamedResponse);

        if (response.statusCode == 200) {
          print("Video uploaded successfully: $videoPath");
        } else {
          print("Failed to upload video: Status code ${response.statusCode}");
        }
      } catch (e) {
        print("Error uploading video: $e");
      }
    } else {
      print("No video available to upload.");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("計測"),
      ),
      body: SingleChildScrollView(
          child: Center(
        child: _isCalibrating
            ? const Column(
                mainAxisAlignment: MainAxisAlignment.center,
              )
            : Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  SizedBox(
                    height: 50,
                  ),
                  TextField(
                    controller: _textEditController,
                    decoration: InputDecoration(
                        border: OutlineInputBorder(), labelText: "ファイル名を入力"),
                  ),
                  SizedBox(height: 20),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      OperationButton(
                          onPressed: _startMeasurement,
                          buttonText: "計測開始",
                          buttonWidth: 150),
                      SizedBox(
                        width: 50,
                      ),
                      OperationButton(
                          onPressed: _stopMeasurement,
                          buttonText: "計測終了",
                          buttonWidth: 150),
                    ],
                  )
                ],
              ),
      )),
    );
  }
}
