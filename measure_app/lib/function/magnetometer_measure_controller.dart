import 'dart:async';
import 'package:dchs_motion_sensors/dchs_motion_sensors.dart';

class MagnetometerMeasureController {
  List<List<dynamic>> _magnetometerData = [];
  List<double> _magnetometerValue = [];
  final List<StreamSubscription<dynamic>> _streamSubscriptions = [];

  void startMeasurement() {
    DateTime? lastTimestamp;
    motionSensors.magnetometerUpdateInterval =
        Duration.microsecondsPerSecond ~/ 100;

    final startTime = DateTime.now();

    _streamSubscriptions.add(
      motionSensors.magnetometer.listen(
        (MagnetometerEvent event) {
          final currentTime = DateTime.now();
          if (lastTimestamp != null) {
            // final timeDiff =
            //     currentTime.difference(lastTimestamp!).inMilliseconds;
            // print('Interval: $timeDiff ms');
            lastTimestamp = currentTime;
          } else {
            lastTimestamp = DateTime.now();
          }

          final elapsedTime =
              currentTime.difference(startTime).inMilliseconds / 1000;
          // print('ElapsedTime : $elapsedTime');

          final magnetometerValues = <dynamic>[
            currentTime,
            event.x,
            event.y,
            event.z,
            elapsedTime
          ];
          _magnetometerData.add(magnetometerValues);
          // print('Magnetometer Data: $_magnetometerData');
          _magnetometerValue = <double>[event.x, event.y, event.z, elapsedTime];
          // print('Magnetometer Values: $magnetometerValues'); // デバッグ用
        },
        onError: (e) {
          print('エラーが発生しました: $e');
        },
        cancelOnError: true,
      ),
    );
  }

  List<List<dynamic>> stopMeasurement() {
    for (final subscription in _streamSubscriptions) {
      subscription.cancel();
      // print('B$_magnetometerData');
    }
    return _magnetometerData;
  }

  void stopShowMeasurement() {
    for (final subscription in _streamSubscriptions) {
      subscription.cancel();
    }
  }

  List<double>? getLatestData() {
    return _magnetometerValue;
  }
}
