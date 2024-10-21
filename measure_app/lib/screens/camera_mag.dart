import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'dart:io';
import 'dart:async';
import 'package:measure_app/function/magnetometer_measure_controller.dart';
import 'package:measure_app/widget/operation_button.dart';
import 'package:path/path.dart';
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
  int _millSecondsPerFrame = 10;
  List<CameraDescription>? _cameras;
  List<String> _imagePaths = [];
  Timer? _timer;
  List<List<Object>> _measurementData = [];
  late CameraController _controller;
  final MagnetometerMeasureController _magnetometerMeasureController =
      MagnetometerMeasureController();

  @override
  void initState() {
    super.initState();
    _getCamera();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _getCamera() async {
    _cameras = await availableCameras();
    if (_cameras != null && _cameras!.isNotEmpty) {
      _controller = CameraController(
        _cameras![1],
        ResolutionPreset.max,
      );
      try {
        await _controller.initialize();
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
      _magnetometerMeasureController.startMeasurement();
      _isMeasuring = true;

      _timer = Timer.periodic(Duration(milliseconds: _millSecondsPerFrame),
          (timer) async {
        if (!_isMeasuring) {
          _timer?.cancel();
        }

        try {
          final newData = _magnetometerMeasureController.getLatestAllData();
          if (newData.length == 5) {
            _measurementData.add(newData.cast<Object>());
          }
          final image = await _controller.takePicture();
          final directory = await getTemporaryDirectory();
          final imagePath =
              '${directory.path}/${DateTime.now().microsecondsSinceEpoch}.jpg';
          await image.saveTo(imagePath);
          _imagePaths.add(imagePath);
        } catch (e) {
          print('フレームのキャプチャに失敗しました: $e');
        }
      });
    }
  }

  Future<void> _stopMeasurement() async {
    _isMeasuring = false;
  }

  Future<void> _sendImagesToServer() async {
    for (String imagePath in _imagePaths) {
      try {
        File imageFile = File(imagePath);

        var request = http.MultipartRequest(
          'POST',
          Uri.parse('http://your-server-ip:5000/upload'),
        );
        request.files
            .add(await http.MultipartFile.fromPath('file', imageFile.path));
        var response = await request.send();

        if (response.statusCode == 200) {
          print("Image uploaded successfully: $imagePath");
        }
      } catch (e) {
        print("Error uploading image: $imagePath, Error: $e");
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("計測"),
      ),
      body: Center(
          child: _isCalibrating
              ? const Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                )
              : Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    AutoSizeText(
                      '$_cameras',
                      style:
                          TextStyle(fontSize: 40, fontWeight: FontWeight.bold),
                      maxLines: 10,
                      minFontSize: 20,
                      overflow: TextOverflow.ellipsis,
                    ),
                    OperationButton(
                        onPressed: _startMeasurement,
                        buttonText: "キャリブレーション",
                        buttonWidth: 300),
                  ],
                )),
    );
  }
}
