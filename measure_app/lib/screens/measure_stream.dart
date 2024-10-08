import 'dart:async';
import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:measure_app/function/magnetometer_measure_controller.dart';
import 'package:measure_app/widget/mag_stream_data_graph.dart';
import 'package:measure_app/widget/operation_button.dart';
import 'package:measure_app/widget/recognition_result_table.dart';

class MeasureStreamData extends StatefulWidget {
  const MeasureStreamData({super.key});

  @override
  MeasureStreamDataState createState() => MeasureStreamDataState();
}

class MeasureStreamDataState extends State<MeasureStreamData> {
  int _countdown = 3; // カウントダウン秒数
  bool _isCounting = false; // カウントダウン中かどうか
  bool _isMeasuring = false; // 計測中かどうか
  bool _showButtons = false;
  bool _showResult = false;
  final List<List<double>> _measurementData = []; // 計測データを格納
  late Timer _timer; // タイマー
  late Timer _updateTimer; // グラフ更新用のタイマー
  final MagnetometerMeasureController _magnetometerController =
      MagnetometerMeasureController(); // 磁力センサのコントローラ
  String measurementDataJson = ' ';
  Map<String, dynamic> decodedData = {};
  List<dynamic> resultData = [];
  double yMax = 0;
  double yMin = 0;

  @override
  void dispose() {
    _timer.cancel();
    _updateTimer.cancel();
    _magnetometerController.stopMeasurement(); // リソースを解放
    super.dispose();
  }

  // カウントダウン開始
  void _startCountdown() {
    setState(() {
      _isCounting = true;
    });

    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
      setState(() {
        if (_countdown > 1) {
          _countdown--;
        } else {
          _timer.cancel(); // カウントダウン終了
          _startMeasurement(); // 計測開始
        }
      });
    });
  }

  // 計測開始
  void _startMeasurement() {
    setState(() {
      _isCounting = false;
      _isMeasuring = true;
      _countdown = 3; // 次回のカウントダウンに備えてリセット
    });

    // 磁力センサの計測を開始
    _magnetometerController.startMeasurement();

    // 計測処理とグラフ更新を5秒間行う
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
          if (_measurementData.length > 200) {
            _measurementData.removeAt(0);
          }

          double maxValue = _measurementData
              .map((row) => row.sublist(0, 3)) // X, Y, Z のみ取り出し
              .expand((values) => values)
              .reduce((a, b) => a > b ? a : b);

          double minValue = _measurementData
              .map((row) => row.sublist(0, 3)) // X, Y, Z のみ取り出し
              .expand((values) => values)
              .reduce((a, b) => a < b ? a : b);

          yMax = ((maxValue / 10).floor() * 10 + 10);
          yMin = ((minValue / 10).floor() * 10 - 10);
        }
      });
    });

    // 計測終了処理（5秒後にタイマー停止）
    Future.delayed(Duration(seconds: 30), () {
      setState(() {
        _isMeasuring = false; // 計測終了
        _showButtons = true;
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

      // print('Measurement Data in JSON: $measurementDataJson');
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

        setState(() {
          // responseData = decodedData["data"];
          _showButtons = false;
          _showResult = true;
        });
      } else {
        print('データ送信失敗: ${response.statusCode}');
      }
    } catch (e) {
      print('エラーが発生しました: $e');
    } finally {
      measurementDataJson = '';
    }
  }

  void _resetState() {
    setState(() {
      _measurementData.clear();
      _countdown = 3;
      _isCounting = false;
      _isMeasuring = false;
      _showButtons = false;
      _showResult = false;
      decodedData = {};
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('カウントダウン＆計測'),
      ),
      body: Center(
        child: _isCounting
            ? Text(
                '$_countdown',
                style:
                    const TextStyle(fontSize: 50, fontWeight: FontWeight.bold),
              )
            : _isMeasuring
                ? Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text(
                        '計測中...',
                        style: TextStyle(
                            fontSize: 40, fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 20),
                      // リアルタイムにグラフを更新する部分
                      CustomLineChart(
                          yMin: yMin,
                          yMax: yMax,
                          measurementData: _measurementData)
                    ],
                  )
                : _showButtons
                    ? Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          OperationButton(
                              onPressed: _sendMeasureData,
                              buttonText: 'データを送信'),
                          const SizedBox(height: 20),
                          OperationButton(
                              onPressed: _resetState, buttonText: '計測をやり直す'),
                        ],
                      )
                    : _showResult
                        ? Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              if (decodedData.isNotEmpty) ...[
                                const Text('識別結果',
                                    style: TextStyle(
                                        fontFamily: 'NotoSansJP',
                                        fontSize: 20,
                                        fontWeight: FontWeight.w300)),
                                RecognitionResultTable(resultData: resultData),
                                const SizedBox(height: 20),
                                OperationButton(
                                    onPressed: _resetState, buttonText: 'やり直す'),
                              ] else ...[
                                const Text('識別に失敗しました',
                                    style: TextStyle(
                                        fontFamily: 'NotoSansJP',
                                        fontSize: 20,
                                        fontWeight: FontWeight.w300)),
                              ],
                            ],
                          )
                        : Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              OperationButton(
                                  onPressed: _startCountdown,
                                  buttonText: '計測開始'),
                            ],
                          ),
      ),
    );
  }
}

// 仮のセンサーデータ取得メソッド
extension on MagnetometerMeasureController {
  List<double>? getLatestData() {
    // 最新の計測データを取得し、[x, y, z] のリストとして返す
    // 実装はセンサーの取得ロジックに基づいて変更してください
    // 例: [x, y, z] データを返す
    return [10.0, 20.0, 30.0]; // ダミーデータ、実際にはセンサーの値を返す
  }
}
