import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:measure_app/function/magnetometer_measure_controller.dart';
import 'package:measure_app/function/websocketManager.dart';
import 'package:measure_app/widget/operation_button.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:flutter_udid/flutter_udid.dart';
import 'package:auto_size_text/auto_size_text.dart';

class CountGameHomepage extends StatefulWidget {
  const CountGameHomepage({super.key});

  @override
  CountGameHomepageState createState() => CountGameHomepageState();
}

class CountGameHomepageState extends State<CountGameHomepage> {
  bool _isCounting = false;
  bool _isMeasuring = false;
  bool _isRegistering = false;
  bool _isSetting = false;
  bool _isOver = false;
  String _udid = '';
  late Timer _timer;
  late Timer _updateTimer;
  int _countdown = 5;
  final int _countdownseconds = 1;
  final int _measurementTime = 5;
  final int _sendDataUnit = 1;
  final int milliseconds = 10;
  final double _slidingRate = 0.5;
  int _sendCount = 0;
  final MagnetometerMeasureController _magnetometerController =
      MagnetometerMeasureController();
  final WebSocketManager _wsManagerSendData =
      WebSocketManager(url: 'ws://172.16.4.31:8765/');
  final WebSocketManager _wsManagerRegister =
      WebSocketManager(url: 'ws://172.16.4.31:8764/');

  List<List<Object>> _measurementData = [];
  List<List<dynamic>> _dataForSend = [];
  String udidJson = "";
  String measurementDataJson = '';
  Map<String, dynamic> decodedData = {};
  List<dynamic> resultData = [];
  WebSocketChannel? channel;

  @override
  void initState() {
    super.initState();
    _wsManagerRegister.connect();
    getDeviceUDID();
    _listenToMessages();
  }

  @override
  void dispose() {
    // タイマーが実行中ならキャンセル
    _timer.cancel();
    _updateTimer.cancel();
    _magnetometerController.stopMeasurement();
    _wsManagerSendData.disconnect();
    super.dispose();
  }

  // UDIDを取得する非同期メソッド
  Future<void> getDeviceUDID() async {
    try {
      _udid = await FlutterUdid.udid; // デバイスのUDIDを取得
      print("Device UDID: $_udid");

      udidJson = json.encode(_udid);

      _wsManagerRegister.sendUDID(udidJson);
    } catch (e) {
      print("Failed to get UDID: $e");
      setState(() {
        _isRegistering = false;
      });
    }
  }

  // WebSocketメッセージを常にリスンするメソッド
  void _listenToMessages() {
    _wsManagerRegister.receiveData()?.listen((response) {
      String trimmedResponse = json.decode(response).trim();
      print('受信データ: $trimmedResponse');
      if (trimmedResponse.contains("SettingOK")) {
        setState(() {
          _isRegistering = false;
          _isSetting = true;
        });
      } else if (trimmedResponse.contains("SettingNotYet")) {
        setState(() {
          _isRegistering = true;
        });
      } else if (trimmedResponse == "GameStart") {
        _isSetting = false;
        _startCountdown();
      } else if (trimmedResponse == "Over") {
        _isOver = true;
      } else {
        print("Unknown message received: $trimmedResponse");
      }

      setState(() {}); // UIを更新
    }, onError: (error) {
      print('エラーが発生しました: $error');
    });
  }

  void _startCountdown() {
    setState(() {
      _wsManagerSendData.connect();
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
      _countdown = 2;

      _magnetometerController.startMeasurement();

      _updateTimer =
          Timer.periodic(Duration(milliseconds: milliseconds), (timer) {
        // 新しいデータを取得し、グラフを更新
        setState(() {
          // 計測データを追加
          final newData = _magnetometerController.getLatestAllData();
          // print(newData); // 最新データ取得
          if (newData.length == 5) {
            _measurementData.add(newData.cast<Object>());
          }

          if (_sendCount == 0 &&
              _measurementData.length ==
                  (_sendDataUnit * (1000 / milliseconds)).toInt()) {
            final preDataForSend = _measurementData.map((data) {
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
            _dataForSend = preDataForSend
                .map((innerList) => List<dynamic>.from(innerList))
                .toList();
            measurementDataJson = json.encode(_dataForSend);
            _sendMeasureData();
            measurementDataJson = "";
            _sendCount += 1;
          }

          if (_measurementData.length ==
              (_sendDataUnit * (1000 / milliseconds) * (1 + _slidingRate))
                  .toInt()) {
            final preDataForSend = _measurementData.map((data) {
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
            _dataForSend = preDataForSend
                .sublist((_measurementData.length -
                        _sendDataUnit * (1000 / milliseconds))
                    .toInt())
                .map((innerList) => List<dynamic>.from(innerList))
                .toList();
            measurementDataJson = json.encode(_dataForSend);
            _measurementData = _measurementData.sublist(
                (_sendDataUnit * (1000 / milliseconds) * _slidingRate).toInt());
            _sendMeasureData();
            measurementDataJson = "";
            _sendCount += 1;
          }
        });
      });
    });

    Future.delayed(Duration(seconds: _measurementTime), () {
      setState(() {
        _isMeasuring = false; // 計測終了
        _measurementData = [];
      });

      // 計測を終了し、グラフの更新も停止
      _updateTimer.cancel();
      _magnetometerController.stopShowMeasurement();
    });
  }

  void _sendMeasureData() async {
    try {
      var dataWithUdid = {"udid": _udid, "data": measurementDataJson};

      String jsonDataWithUdid = json.encode(dataWithUdid);
      // データ送信
      _wsManagerSendData.sendData(jsonDataWithUdid);

      // サーバからの応答を待機
      // _wsManagerSendData.receiveData()?.listen((response) {
      //   // print('受信データ: $response');

      //   setState(() {}); // UIを更新
      // }, onError: (error) {
      //   print('エラーが発生しました: $error');
      // });
    } catch (e) {
      print('エラーが発生しました: $e');
    } finally {
      measurementDataJson = '';
    }
  }

  void _gameStart() async {
    final String sendData = json.encode("Start$_udid");
    _wsManagerRegister.sendData(sendData);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('カウントゲーム'),
      ),
      body: Center(
        child: _isRegistering
            ? const Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  AutoSizeText(
                    '対戦相手探し中・・・',
                    style: TextStyle(fontSize: 40, fontWeight: FontWeight.bold),
                    maxLines: 1,
                    minFontSize: 20,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
              )
            : _isOver
                ? const Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      AutoSizeText(
                        '定員オーバーです\n後でやり直してください',
                        style: TextStyle(
                            fontSize: 40, fontWeight: FontWeight.bold),
                        maxLines: 2,
                        minFontSize: 20,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ],
                  )
                : _isSetting
                    ? Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Text(
                            "ゲームを開始しますか？",
                            style: TextStyle(
                                fontSize: 30, fontWeight: FontWeight.bold),
                          ),
                          OperationButton(
                            onPressed: _gameStart,
                            buttonText: "はい",
                          ),
                        ],
                      )
                    : _isCounting
                        ? Text(
                            '$_countdown',
                            style: const TextStyle(
                                fontSize: 50, fontWeight: FontWeight.bold),
                          )
                        : _isMeasuring
                            ? const Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Text(
                                    '計測中...',
                                    style: TextStyle(
                                        fontSize: 40,
                                        fontWeight: FontWeight.bold),
                                  ),
                                ],
                              )
                            : const Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  // OperationButton(
                                  //     onPressed: _startCountdown,
                                  //     buttonText: '計測開始'),
                                ],
                              ),
      ),
    );
  }
}
