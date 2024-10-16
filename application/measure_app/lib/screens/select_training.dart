import 'package:flutter/material.dart';
import 'package:measure_app/screens/dialog.dart';

class SelectTraining extends StatelessWidget {
  const SelectTraining({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Balance Ball Training Measure')),
      body: Column(
        children: [
          const Align(
            alignment: Alignment.center,
            child: Padding(
              padding: EdgeInsets.symmetric(vertical: 20),
              child: Text('Select Training', style: TextStyle(fontSize: 24)),
            ),
          ),
          Align(
            alignment: Alignment.center,
            child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 20),
                child: ElevatedButton.icon(
                  icon: const Icon(
                    Icons.tag_faces,
                    color: Colors.white,
                  ),
                  label: const Text('Bounce'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green,
                    foregroundColor: Colors.white,
                  ),
                  onPressed: () {
                    final showDialogInstance = ShowDialog('Bounce');
                    showDialogInstance.showExplainTrainingDialog(context);
                  },
                )),
          ),
          Align(
            alignment: Alignment.center,
            child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 20),
                child: ElevatedButton.icon(
                  icon: const Icon(
                    Icons.tag_faces,
                    color: Colors.white,
                  ),
                  label: const Text('Walking'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green,
                    foregroundColor: Colors.white,
                  ),
                  onPressed: () {
                    final showDialogInstance = ShowDialog('Bounce');
                    showDialogInstance.showExplainTrainingDialog(context);
                  },
                )),
          ),
          Align(
            alignment: Alignment.center,
            child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 20),
                child: ElevatedButton.icon(
                  icon: const Icon(
                    Icons.tag_faces,
                    color: Colors.white,
                  ),
                  label: const Text('Leg Extension'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green,
                    foregroundColor: Colors.white,
                  ),
                  onPressed: () {
                    final showDialogInstance = ShowDialog('Bounce');
                    showDialogInstance.showExplainTrainingDialog(context);
                  },
                )),
          ),
          Align(
            alignment: Alignment.center,
            child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 20),
                child: ElevatedButton.icon(
                  icon: const Icon(
                    Icons.tag_faces,
                    color: Colors.white,
                  ),
                  label: const Text('Knee Up'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green,
                    foregroundColor: Colors.white,
                  ),
                  onPressed: () {
                    final showDialogInstance = ShowDialog('Bounce');
                    showDialogInstance.showExplainTrainingDialog(context);
                  },
                )),
          ),
          Align(
            alignment: Alignment.center,
            child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 20),
                child: ElevatedButton.icon(
                  icon: const Icon(
                    Icons.tag_faces,
                    color: Colors.white,
                  ),
                  label: const Text('Rolling'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green,
                    foregroundColor: Colors.white,
                  ),
                  onPressed: () {
                    final showDialogInstance = ShowDialog('Bounce');
                    showDialogInstance.showExplainTrainingDialog(context);
                  },
                )),
          ),
        ],
      ),
    );
  }
}
