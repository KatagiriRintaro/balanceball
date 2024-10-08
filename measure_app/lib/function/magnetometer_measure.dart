import 'dart:async';
import 'package:flutter/material.dart';
import 'package:dchs_motion_sensors/dchs_motion_sensors.dart';

class MagnetometerMeasure extends StatefulWidget {
  const MagnetometerMeasure({super.key});

  @override
  State<MagnetometerMeasure> createState() => _MagnetometerMeasureState();
}

class _MagnetometerMeasureState extends State<MagnetometerMeasure> {
  List<double>? _magnetometerValues;
  final _streamSubscriptions = <StreamSubscription<dynamic>>[];

  @override
  Widget build(BuildContext context) {
    final magnetometer =
        _magnetometerValues?.map((double v) => v.toStringAsFixed(1)).toList();
    print(magnetometer);

    motionSensors.magnetometerUpdateInterval =
        Duration.microsecondsPerSecond ~/ 100;

    return Scaffold(
      appBar: AppBar(
        title: const Text('下向き検知テスト'),
        elevation: 4,
      ),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: <Widget>[
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: <Widget>[
                Text(
                  magnetometer != null && magnetometer.isNotEmpty
                      ? 'Magnetometer: $magnetometer'
                      : 'ERROR',
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    super.dispose();
    for (final subscription in _streamSubscriptions) {
      subscription.cancel();
    }
  }

  @override
  void initState() {
    DateTime? lastTimestamp;

    super.initState();
    _streamSubscriptions.add(
      // magnetometerEventStream().listen(
      motionSensors.magnetometer.listen(
        (MagnetometerEvent event) {
          if (lastTimestamp != null) {
            final currentTime = DateTime.now();
            final timeDiff =
                currentTime.difference(lastTimestamp!).inMilliseconds;
            print('Interval: $timeDiff ms');
            lastTimestamp = currentTime;
          } else {
            lastTimestamp = DateTime.now();
          }

          setState(() {
            _magnetometerValues = <double>[event.x, event.y, event.z];
            // print('Magnetometer Values: $_magnetometerValues');
          });
        },
        onError: (e) {
          if (!mounted) return;
          showDialog(
              context: context,
              builder: (context) {
                return const AlertDialog(
                  title: Text('センサーが見つかりません'),
                  content: Text('使用中のデバイスではセンサーが搭載されていない可能性があります'),
                );
              });
        },
        cancelOnError: true,
      ),
    );
  }
}
