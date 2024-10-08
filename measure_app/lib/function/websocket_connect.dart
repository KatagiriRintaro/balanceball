import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';

class WebSocketManager {
  WebSocketChannel? _channel;
  final String url;

  WebSocketManager({required this.url});

  // WebSocketサーバに接続する関数
  void connect() {
    try {
      _channel = WebSocketChannel.connect(Uri.parse(url));
      print('WebSocket接続成功');
    } catch (e) {
      print('WebSocket接続エラー: $e');
    }
  }

  // WebSocket接続を閉じる関数
  void disconnect() {
    if (_channel != null) {
      _channel!.sink.close();
      print('WebSocket切断成功');
    }
  }

  // WebSocketを使ってデータを送信する関数
  void sendData(String data) {
    if (_channel != null && data.isNotEmpty) {
      _channel!.sink.add(data);
      print('データ送信中: $data');
    } else {
      print('データ送信失敗: 接続されていないか、データが空です');
    }
  }

  // サーバからのデータを受信するストリーム
  Stream<dynamic>? receiveData() {
    return _channel?.stream;
  }
}
