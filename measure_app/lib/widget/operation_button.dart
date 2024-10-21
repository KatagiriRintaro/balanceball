import 'package:flutter/material.dart';

// 新しいクラスを定義
class OperationButton extends StatelessWidget {
  final VoidCallback onPressed; // ボタンが押されたときのコールバック
  final String buttonText; // ボタンのテキスト
  final double buttonWidth;

  // コンストラクタ
  const OperationButton(
      {super.key,
      required this.onPressed,
      this.buttonText = '計測をやり直す', // デフォルトテキスト
      required this.buttonWidth});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ElevatedButton(
          onPressed: onPressed,
          style: ElevatedButton.styleFrom(fixedSize: Size(buttonWidth, 80)),
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
