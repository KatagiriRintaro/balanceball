import 'dart:async';
import 'package:flutter/material.dart';
import 'package:measure_app/measure/magnetometer_measure_controller.dart';
import 'package:measure_app/widget/mag_stream_data_graph.dart';

class ShowStreamData extends StatefulWidget {
  const ShowStreamData({super.key});

  @override
  ShowStreamState createState() => ShowStreamState();
}

class ShowStreamState extends State<ShowStreamData> {
  final List<List<double>> _measurementData = []; // 計測データを格納
  late Timer _timer; // タイマー
  late Timer _updateTimer; // グラフ更新用のタイマー
  final MagnetometerMeasureController _magnetometerController =
      MagnetometerMeasureController(); // 磁力センサのコントローラ
  String measurementDataJson = ' ';
  String responseData = ' ';
  double yMax = 0;
  double yMin = 0;

  @override
  void initState() {
    super.initState();
    _startMeasurement();
  }

  @override
  void dispose() {
    _timer.cancel();
    _updateTimer.cancel();
    _magnetometerController.stopMeasurement(); // リソースを解放
    super.dispose();
  }

  // 計測開始
  void _startMeasurement() {
    // 磁力センサの計測を開始
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

          // print('yMax ${yMax}  yMin ${yMin}');
        }
      });
    });
  }

  void _stopMeasurement() {
    setState(() {
      _updateTimer.cancel();
      _magnetometerController.stopShowMeasurement();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('カウントダウン＆計測'),
      ),
      body: Center(
          child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const SizedBox(height: 20),
          // リアルタイムにグラフを更新する部分
          CustomLineChart(
              yMin: yMin, yMax: yMax, measurementData: _measurementData)
        ],
      )),
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
