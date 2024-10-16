import 'package:flutter/material.dart';

// 新しいクラスを定義
class OperationButton extends StatelessWidget {
  final VoidCallback onPressed; // ボタンが押されたときのコールバック
  final String buttonText; // ボタンのテキスト

  // コンストラクタ
  const OperationButton({
    Key? key,
    required this.onPressed,
    this.buttonText = '計測をやり直す', // デフォルトテキスト
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ElevatedButton(
          onPressed: onPressed,
          style: ElevatedButton.styleFrom(fixedSize: const Size(200, 80)),
          child: Text(buttonText,
              style: const TextStyle(
                  fontFamily: 'NotoSansJP',
                  fontSize: 20,
                  fontWeight: FontWeight.w300)),
        ),
      ],
    );
  }
}
