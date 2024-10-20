import 'package:flutter/material.dart';
import 'package:measure_app/screens/select_training.dart';
import 'package:measure_app/screens/count_game_homepage.dart';
import 'package:measure_app/screens/show_stream.dart';
import 'package:measure_app/screens/camera_mag.dart';
import 'package:measure_app/widget/select_button.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          // title: const Text('Balance Ball Training Measure')
          ),
      body: const Column(
        children: [
          Align(
            alignment: Alignment.center,
            child: Padding(
              padding: EdgeInsets.symmetric(vertical: 20),
              child: Text('Balance Ball Training Measure',
                  style: TextStyle(fontSize: 24)),
            ),
          ),
          SelectButton(
            nextPage: CountGameHomepage(),
            buttonText: 'カウントゲーム',
            icon: Icons.videogame_asset,
            buttonSize: Size(350, 80),
          ),
          SelectButton(
            nextPage: SelectTraining(),
            buttonText: 'バランスボールトレーニング',
            icon: Icons.accessibility,
            buttonSize: Size(350, 80),
          ),
          SelectButton(
            nextPage: GetMagnetometerAR(),
            buttonText: 'カメラ',
            icon: Icons.camera_alt,
            buttonSize: Size(350, 80),
          ),
          SelectButton(
            nextPage: ShowStreamData(),
            buttonText: '磁力センサデータの確認',
            icon: Icons.timeline,
            buttonSize: Size(350, 80),
          ),
        ],
      ),
    );
  }
}
