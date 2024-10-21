import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

// カスタムウィジェットを作成
class CustomLineChart extends StatelessWidget {
  final double yMin;
  final double yMax;
  final List<List<double>> measurementData;

  const CustomLineChart({
    super.key,
    required this.yMin,
    required this.yMax,
    required this.measurementData,
  });

  // データから FlSpot のリストを生成する関数
  List<FlSpot> _createSpots(List<List<double>> data, int axisIndex) {
    if (data.isEmpty) return [];
    return List<FlSpot>.generate(data.length, (index) {
      return FlSpot(index.toDouble(), data[index][axisIndex]);
    });
  }

  Widget _buildLegendItem(Color color, String text) {
    return Row(
      children: [
        Container(
          width: 12,
          height: 12,
          color: color, // 凡例の色
        ),
        const SizedBox(width: 4), // アイコンとテキストの間のスペース
        Text(text), // 凡例のラベル
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      // ContainerとPaddingを同じレベルで表示するためにColumnでラップ
      children: [
        Container(
          height: 250,
          width: double.infinity,
          padding: const EdgeInsets.all(16),
          child: LineChart(
            LineChartData(
              minY: yMin,
              maxY: yMax,
              minX: 0,
              maxX: 200,
              lineBarsData: [
                LineChartBarData(
                  spots: _createSpots(measurementData, 0), // x 軸データ
                  isCurved: true,
                  gradient: const LinearGradient(
                    colors: [Colors.blueAccent, Colors.blue],
                  ),
                  dotData: const FlDotData(show: false),
                ),
                LineChartBarData(
                  spots: _createSpots(measurementData, 1), // y 軸データ
                  isCurved: true,
                  gradient: const LinearGradient(
                    colors: [Colors.redAccent, Colors.red],
                  ),
                  dotData: const FlDotData(show: false),
                ),
                LineChartBarData(
                  spots: _createSpots(measurementData, 2), // z 軸データ
                  isCurved: true,
                  gradient: const LinearGradient(
                    colors: [Colors.greenAccent, Colors.green],
                  ),
                  dotData: const FlDotData(show: false),
                ),
              ],
              titlesData: FlTitlesData(
                bottomTitles: AxisTitles(
                  sideTitles: SideTitles(
                    showTitles: true, // 下側にラベルを表示
                    reservedSize: 40,
                    interval: 40,
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
                    interval: 20,
                    getTitlesWidget: (value, meta) {
                      // 20の倍数のみ縦軸に表示する
                      if (value.toInt() % 40 == 0) {
                        return Text(value.toInt().toString());
                      }
                      return Container();
                    },
                  ), // 左側のラベルを表示
                ),
              ),
              borderData: FlBorderData(show: true),
            ),
          ),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(vertical: 8.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              _buildLegendItem(Colors.blue, 'X軸'),
              const SizedBox(width: 16), // 凡例アイテム間のスペース
              _buildLegendItem(Colors.red, 'Y軸'),
              const SizedBox(width: 16),
              _buildLegendItem(Colors.green, 'Z軸'),
            ],
          ),
        ),
      ],
    );
  }
}
