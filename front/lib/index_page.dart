import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'index_list.dart';
import 'package:forest_hero/widgets/line_graph.dart';
import 'package:forest_hero/models/forest.dart';

class IndexPage extends StatefulWidget {
  final DateTime? startDate;
  final DateTime? endDate;
  final Forest forest;

  const IndexPage({
    Key? key,
    required this.startDate,
    required this.endDate,
    required this.forest,
  }) : super(key: key);

  @override
  State<IndexPage> createState() => _IndexPageState();
}

class _IndexPageState extends State<IndexPage> {
  String? _selectedIndex;
  // This will store the list of indices returned by the endpoint.
  List<double> _forestIndices = [];

  // Show the bottom sheet and await the returned selected index.
  void _showIndices() async {
    final result = await showModalBottomSheet(
      isScrollControlled: true,
      context: context,
      builder: (ctx) => const IndexList(),
    );

    if (result != null && result is String) {
      setState(() {
        _selectedIndex = result;
      });
    }
  }

  // Call the endpoint to get forest indices.
  Future<void> _fetchForestIndices() async {
    const url = 'http://10.0.2.2:8000/forest/get_forest_indices/';
    // Format dates to 'YYYY-MM-DD'
    final String startDate =
        widget.startDate?.toIso8601String().split('T')[0] ?? '';
    print('startDate: $startDate');
    final String endDate =
        widget.endDate?.toIso8601String().split('T')[0] ?? '';
    print('endDate: $endDate');
    print('forestId: ${widget.forest.forestId}');

    final body = jsonEncode({
      "forest_unique_id": widget.forest.forestId,
      "start_date": startDate,
      "end_date": endDate,
      "indice_name": _selectedIndex ?? 'NDVI',
    });

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {"Content-Type": "application/json"},
        body: body,
      );

      if (response.statusCode == 200) {
        // The API returns a JSON array of numbers.
        final data = jsonDecode(response.body);
        setState(() {
          _forestIndices = List<double>.from(data);
          print(_forestIndices);
        });
      } else {
        // Handle non-200 responses.
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
              content: Text('Error: ${response.statusCode} ${response.body}')),
        );
      }
    } catch (e) {
      // Handle connection errors or exceptions.
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Exception: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(10.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Select needed index', style: TextStyle(fontSize: 20)),
          const SizedBox(height: 15),
          Card(
            child: ListTile(
              // Display the selected index or a default text.
              title: Text(_selectedIndex ?? 'Indices'),
              trailing: const Icon(Icons.arrow_forward_ios),
              onTap: _showIndices,
            ),
          ),
          const SizedBox(height: 15),
          ElevatedButton(
            onPressed: _fetchForestIndices,
            child: const Text("Fetch Indices"),
          ),
          const SizedBox(height: 30),
          // Display the line chart if data is available.
          if (_forestIndices.isNotEmpty)
            // Expanded(child: LineGraph(data: _forestIndices))
            SizedBox(
              height: 400, // set your desired height here
              child: LineGraph(data: _forestIndices),
            )
          else
            const Expanded(
              child: Center(child: Text("No data available")),
            ),
        ],
      ),
    );
  }
}
