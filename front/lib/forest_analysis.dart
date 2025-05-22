import 'package:flutter/material.dart';
import 'package:forest_hero/widgets/bottom_navigator.dart';
import 'package:forest_hero/index_page.dart';
import 'package:forest_hero/models/forest.dart';
import 'package:forest_hero/deforestationMap.dart';
import 'package:forest_hero/forest_map.dart';
import 'package:forest_hero/burned_area_page.dart';

class ForestAnalyses extends StatefulWidget {
  final DateTime? startDate;
  final DateTime? endDate;
  final Forest forest;

  const ForestAnalyses({
    Key? key,
    required this.startDate,
    required this.endDate,
    required this.forest,
  }) : super(key: key);

  @override
  State<ForestAnalyses> createState() => _ForestAnalysesState();
}

class _ForestAnalysesState extends State<ForestAnalyses> {
  int selectedIndex = 0;

  final List<String> _titles = [
    'Index',
    'Forest',
    'Deforestation',
    'Burned Area'
  ];

  void _onItemTapped(int index) {
    setState(() {
      selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    // Make sure this list contains exactly 4 widgets
    final List<Widget> _pages = [
      IndexPage(
        startDate: widget.startDate,
        endDate: widget.endDate,
        forest: widget.forest,
      ),
      ForestScreen(
        forest: widget.forest,
        endDate: widget.endDate,
      ),
      DeforestationPage(
        forest: widget.forest,
        startDate: widget.startDate,
        endDate: widget.endDate,
      ),
      BurnedAreaPage(
        forest: widget.forest,
      ),
    ];

    return Scaffold(
      appBar: AppBar(
        title: Text(_titles[selectedIndex]),
      ),
      body: _pages[selectedIndex],
      bottomNavigationBar: BottomNavigator(
        index: selectedIndex,
        onItemTapped: _onItemTapped,
      ),
    );
  }
}
