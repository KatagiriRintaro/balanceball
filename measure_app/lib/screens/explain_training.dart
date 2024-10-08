import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';
import 'package:measure_app/screens/measure_stream.dart';

const explainText = {
  'Bounce': 'バランスボールの上で跳ねる',
  'Walking': 'バランスボールの上で跳ねながら腕を振る',
  'Leg Extension': 'バランスボールに座った状態で足を前に上げる(右限定)',
  'Knee Up': 'バランスボールに座った状態で足を上に上げる(右限定)',
  'Rolling': 'バランスボールに座った状態で腰を反時計回りまわす'
};

class ShowTraining extends StatefulWidget {
  final String training;

  const ShowTraining({Key? key, required this.training}) : super(key: key);

  @override
  _ShowTrainingState createState() => _ShowTrainingState();
}

class _ShowTrainingState extends State<ShowTraining> {
  late VideoPlayerController _controller;

  @override
  void initState() {
    super.initState();
    _controller =
        VideoPlayerController.asset('assets/videos/${widget.training}.mp4')
          ..initialize().then((_) {
            setState(() {}); // 動画が初期化されたら画面を更新
          });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          // title: Text('Training: ${widget.training}'),
          ),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          Column(
            children: [
              Align(
                alignment: Alignment.center,
                child: Padding(
                  padding: const EdgeInsets.symmetric(vertical: 20),
                  child: Column(children: [
                    Text('Training: ${widget.training}',
                        style: const TextStyle(fontSize: 24)),
                    Text(explainText[widget.training] ?? '説明がありません',
                        style: const TextStyle(fontSize: 24)),
                  ]),
                ),
              ),
            ],
          ),
          AspectRatio(
            aspectRatio: _controller.value.aspectRatio,
            // 動画を表示
            child: VideoPlayer(_controller),
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              IconButton(
                onPressed: () {
                  // 動画を最初から再生
                  _controller
                      .seekTo(Duration.zero)
                      .then((_) => _controller.play());
                },
                icon: const Icon(Icons.refresh),
              ),
              IconButton(
                onPressed: () {
                  // 動画を再生
                  _controller.play();
                },
                icon: const Icon(Icons.play_arrow),
              ),
              IconButton(
                onPressed: () {
                  // 動画を一時停止
                  _controller.pause();
                },
                icon: const Icon(Icons.pause),
              ),
            ],
          ),
          Column(children: [
            Align(
              alignment: Alignment.center,
              child: Padding(
                  padding: const EdgeInsets.symmetric(vertical: 20),
                  child: ElevatedButton.icon(
                    icon: const Icon(
                      Icons.tag_faces,
                      color: Colors.white,
                    ),
                    label: const Text('Measure'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.green,
                      foregroundColor: Colors.white,
                    ),
                    onPressed: () {
                      Navigator.of(context).push(MaterialPageRoute(
                          builder: (context) => MeasureStreamData()));
                    },
                  )),
            ),
          ]),
        ],
      ),
    );
  }
}
