import 'package:flutter/material.dart';

class IndexList extends StatefulWidget {
  const IndexList({Key? key}) : super(key: key);

  @override
  State<IndexList> createState() => _IndexListState();
}

class _IndexListState extends State<IndexList> {
  final List<String> _indices = [
    'NDVI',
    'EVI',
    'NBR',
    'NDWI',
    'GNDVI',
    'CI',
    'NIR',
    'VARI',
    'SAVI',
    'MGRVI',
  ];

  // Default to the first index.
  String? _selectedIndex = 'NDVI';

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 50.0),
      child: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: _indices.length,
              itemBuilder: (ctx, index) {
                return RadioListTile<String>(
                  title: Text(_indices[index]),
                  value: _indices[index],
                  groupValue: _selectedIndex,
                  onChanged: (String? value) {
                    setState(() {
                      _selectedIndex = value;
                    });
                  },
                  activeColor: Colors.green,
                );
              },
            ),
          ),
          const SizedBox(height: 20),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop(); // Return nothing if closed
                },
                child: const Text("Close"),
              ),
              TextButton(
                onPressed: () {
                  // Pass the selected index back to the parent.
                  Navigator.of(context).pop(_selectedIndex);
                },
                child: const Text("Submit"),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
