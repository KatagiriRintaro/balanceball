import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:measure_app/measure/magnetometer_measure_controller.dart';
import 'package:measure_app/widget/operation_button.dart';

class CountGameHomepage extends StatefulWidget {
  const CountGameHomepage({super.key});

  @override
  CountGameHomepageState createState() => CountGameHomepageState();
}

class CountGameHomepageState extends State<CountGameHomepage> {
  bool _isCounting = false;
  bool _isMeasuring = false;
  late Timer _timer;
  late Timer _updateTimer;
  int _countdown = 5;
  final int _countdownseconds = 1;
  final int _measurementTime = 300;
  final int _sendInterval = 3;
  final MagnetometerMeasureController _magnetometerController =
      MagnetometerMeasureController();
  final List<List<double>> _measurementData = [];
  String measurementDataJson = ' ';
  Map<String, dynamic> decodedData = {};
  List<dynamic> resultData = [];

  @override
  void dispose() {
    // タイマーが実行中ならキャンセル
    _timer.cancel();
    _updateTimer.cancel();
    _magnetometerController.stopMeasurement();
    super.dispose();
  }

  void _startCountdown() {
    setState(() {
      _isCounting = true;
    });

    _timer = Timer.periodic(Duration(seconds: _countdownseconds), (timer) {
      setState(() {
        if (_countdown > 1) {
          _countdown--;
        } else {
          _timer.cancel();
          _startMeasurement();
        }
      });
    });
  }

  void _startMeasurement() {
    setState(() {
      _isCounting = false;
      _isMeasuring = true;
      _countdown = 5;

      _magnetometerController.startMeasurement();

      int milliseconds = 10;
      _updateTimer =
          Timer.periodic(Duration(milliseconds: milliseconds), (timer) {
        // 新しいデータを取得し、グラフを更新
        setState(() {
          // 計測データを追加
          final newData = _magnetometerController.getLatestData();
          // print(newData); // 最新データ取得
          if (newData != null && newData.length == 4) {
            _measurementData.add(newData);
          }
        });
      });

      Timer.periodic(Duration(seconds: _sendInterval), (timer) {
        if (!_isMeasuring) {
          timer.cancel();
        } else {
          _sendMeasureData();
        }
      });
    });

    Future.delayed(Duration(seconds: _measurementTime), () {
      setState(() {
        _isMeasuring = false; // 計測終了
      });

      // 計測を終了し、グラフの更新も停止
      _updateTimer.cancel();
      final measurementData = _magnetometerController.stopMeasurement();
      // print('A$measurementData');

      final measurementDataForJson = measurementData.map((data) {
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

      measurementDataJson = json.encode(measurementDataForJson);
    });
  }

  void _sendMeasureData() async {
    try {
      final response = await http.post(
        Uri.parse('http://172.16.4.31:5000/'),
        headers: {
          "Content-Type": "application/json",
        },
        body: measurementDataJson,
      );
      if (response.statusCode == 200) {
        // print('データ送信成功');
        decodedData = json.decode(response.body);

        final strData = decodedData['data'];
        resultData = json.decode(strData);

        setState(() {});
      } else {
        print('データ送信失敗: ${response.statusCode}');
      }
    } catch (e) {
      print('エラーが発生しました: $e');
    } finally {
      measurementDataJson = '';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('カウントゲーム'),
      ),
      body: Center(
        child: _isCounting
            ? Text(
                '$_countdown',
                style:
                    const TextStyle(fontSize: 50, fontWeight: FontWeight.bold),
              )
            : (_isMeasuring
                ? const Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        '計測中...',
                        style: TextStyle(
                            fontSize: 40, fontWeight: FontWeight.bold),
                      ),
                    ],
                  )
                : Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      OperationButton(
                          onPressed: _startCountdown, buttonText: '計測開始'),
                    ],
                  )),
      ),
    );
  }
}
