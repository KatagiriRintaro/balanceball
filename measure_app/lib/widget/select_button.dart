import 'package:flutter/material.dart';

// 新しいクラスを定義
class SelectButton extends StatelessWidget {
  final String buttonText; // ボタンのテキスト
  final IconData? icon;
  final Widget? nextPage;
  final Size? buttonSize;

  // コンストラクタ
  const SelectButton(
      {super.key,
      required this.nextPage,
      this.buttonText = '計測をやり直す',
      this.icon = Icons.tag_faces,
      this.buttonSize});

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: Alignment.center,
      child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 20),
          child: ElevatedButton.icon(
            icon: Icon(icon, color: Colors.white),
            label: Text(buttonText,
                style: const TextStyle(
                    fontFamily: 'NotoSansJP',
                    fontSize: 20,
                    fontWeight: FontWeight.w300)),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.green,
              foregroundColor: Colors.white,
              minimumSize: buttonSize ?? const Size(200, 50),
            ),
            onPressed: () {
              if (nextPage != null) {
                Navigator.of(context)
                    .push(MaterialPageRoute(builder: ((context) => nextPage!)));
              }
            },
          )),
    );
  }
}
