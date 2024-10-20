import 'package:flutter/material.dart';

class RecognitionResultTable extends StatefulWidget {
  final List<dynamic> resultData; // Map<String, dynamic> 型を受け取る

  const RecognitionResultTable({super.key, required this.resultData});

  @override
  RecognitionResultTableState createState() => RecognitionResultTableState();
}

class RecognitionResultTableState extends State<RecognitionResultTable> {
  @override
  Widget build(BuildContext context) {
    return widget.resultData.isEmpty
        ? const Center(child: CircularProgressIndicator()) // データがない場合はロード中
        : SizedBox(
            width: MediaQuery.of(context).size.width * 0.8,
            height: 300,
            child: SingleChildScrollView(
              scrollDirection: Axis.vertical,
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: DataTable(
                  columns: const <DataColumn>[
                    DataColumn(label: Text('Label')),
                    DataColumn(label: Text('Duration (seconds)')),
                  ],
                  rows: widget.resultData
                      .map((item) => DataRow(cells: <DataCell>[
                            DataCell(Text(
                                item['Label'] ?? 'N/A')), // Labelがない場合は'N/A'を表示
                            DataCell(Text(
                                item['Duration (seconds)']?.toString() ??
                                    '0')), // Durationがない場合は'0'を表示
                          ]))
                      .toList(),
                ),
              ),
            ),
          );
  }
}
