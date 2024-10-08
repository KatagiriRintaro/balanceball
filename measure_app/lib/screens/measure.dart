import 'dart:async';
import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:measure_app/measure/magnetometer_measure_controller.dart'; // パスは適宜修正

class CountDownTimer extends StatefulWidget {
  @override
  _CountDownTimerState createState() => _CountDownTimerState();
}

class _CountDownTimerState extends State<CountDownTimer> {
  int _countdown = 3; // カウントダウン秒数
  bool _isCounting = false; // カウントダウン中かどうか
  bool _isMeasuring = false; // 計測中かどうか
  late Timer _timer; // タイマー
  final MagnetometerMeasureController _magnetometerController =
      MagnetometerMeasureController(); // 磁力センサのコントローラ

  @override
  void dispose() {
    _timer.cancel();
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

    // 計測処理（ここでは5秒後に計測を終了）
    Future.delayed(Duration(seconds: 5), () {
      setState(() {
        _isMeasuring = false; // 計測終了
      });

      // 計測結果を取得
      final measurementData = _magnetometerController.stopMeasurement();

      // 計測結果を次の画面に渡す
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => MeasurementResultScreen(measurementData),
        ),
      );
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
                style: TextStyle(fontSize: 50, fontWeight: FontWeight.bold),
              )
            : _isMeasuring
                ? const Text(
                    '計測中...',
                    style: TextStyle(fontSize: 40, fontWeight: FontWeight.bold),
                  )
                : ElevatedButton(
                    onPressed: _startCountdown,
                    child: const Text('計測開始'),
                  ),
      ),
    );
  }
}

// 計測結果画面
class MeasurementResultScreen extends StatelessWidget {
  final List<List<dynamic>> measurementData;

  MeasurementResultScreen(this.measurementData);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('計測結果'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          children: [
            // グラフ描画部分
            Container(
              height: 250,
              width: double.infinity,
              padding: const EdgeInsets.all(16),
              child: LineChart(
                LineChartData(
                  minY: -70,
                  maxY: 100,
                  minX: 0,
                  maxX: measurementData.length.toDouble(),
                  lineBarsData: [
                    LineChartBarData(
                      spots: _createSpots(measurementData, 0), // x 軸データ
                      isCurved: true,
                      gradient: const LinearGradient(
                        // colors の代わりに gradient を使用
                        colors: [Colors.blueAccent, Colors.blue],
                      ),
                      dotData: const FlDotData(show: false),
                    ),
                    LineChartBarData(
                      spots: _createSpots(measurementData, 1), // y 軸データ
                      isCurved: true,
                      gradient: const LinearGradient(
                        // y 軸データの色設定
                        colors: [Colors.redAccent, Colors.red],
                      ),
                      dotData: const FlDotData(show: false),
                    ),
                    LineChartBarData(
                      spots: _createSpots(measurementData, 2), // z 軸データ
                      isCurved: true,
                      gradient: const LinearGradient(
                        // z 軸データの色設定
                        colors: [Colors.greenAccent, Colors.green],
                      ),
                      dotData: const FlDotData(show: false),
                    ),
                  ],
                  titlesData: FlTitlesData(
                    bottomTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true, // 下側にラベルを表示
                        reservedSize: 22,
                        interval: 50,
                        getTitlesWidget: (value, meta) {
                          return Text(value.toInt().toString()); // 横軸の値を表示
                        },
                      ),
                    ),
                    topTitles: const AxisTitles(
                      sideTitles: SideTitles(showTitles: false), // 上側のラベルを非表示
                    ),
                    rightTitles: const AxisTitles(
                      sideTitles: SideTitles(showTitles: false), // 右側のラベルを非表示
                    ),
                    leftTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        reservedSize: 30,
                        interval: 10,
                        getTitlesWidget: (value, meta) {
                          return Text(value.toInt().toString());
                        },
                      ), // 左側のラベルを表示
                    ),
                  ),
                  borderData: FlBorderData(show: true),
                ),
              ),
            ),
            // 計測データのリスト表示部分
            // Expanded(
            //   child: ListView.builder(
            //     itemCount: measurementData.length,
            //     itemBuilder: (context, index) {
            //       final dataPoint = measurementData[index];
            //       return ListTile(
            //         title: Text(
            //           'x: ${dataPoint[0]}, y: ${dataPoint[1]}, z: ${dataPoint[2]}',
            //         ),
            //         subtitle: Text(
            //           'Time: ${dataPoint[3]}',
            //         ),
            //       );
            //     },
            //   ),
            // ),
          ],
        ),
      ),
    );
  }

  // グラフ用のスポットデータを生成するメソッド
  List<FlSpot> _createSpots(List<List<dynamic>> data, int axisIndex) {
    return List<FlSpot>.generate(data.length, (index) {
      return FlSpot(index.toDouble(), data[index][axisIndex].toDouble());
    });
  }
}
