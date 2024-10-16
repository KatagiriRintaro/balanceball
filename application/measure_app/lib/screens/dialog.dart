import 'package:flutter/material.dart';
import 'package:measure_app/screens/explain_training.dart';
import 'package:measure_app/screens/measure_stream.dart';

class ShowDialog {
  final dynamic training;

  ShowDialog(this.training);

  void showExplainTrainingDialog(BuildContext context) {
    showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: const Text('確認'),
            content: Text('$trainingの説明を聞きますか？'),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(
                          builder: (context) =>
                              ShowTraining(training: training)));
                },
                child: const Text('Yes'),
              ),
              TextButton(
                onPressed: () {
                  Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(
                          builder: ((context) => MeasureStreamData())));
                },
                child: const Text('No'),
              ),
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: const Text('Reselect'),
              ),
            ],
          );
        });
  }
}
