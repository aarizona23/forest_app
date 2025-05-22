import 'package:flutter/material.dart';
import 'models/forest.dart';
import 'forest_item.dart';

class ForestList extends StatelessWidget {
  const ForestList({super.key, required this.forests});

  final List<Forest> forests;

  @override
  Widget build(context) {
    return ListView.builder(
      scrollDirection: Axis.horizontal,
      itemCount: forests.length,
      itemBuilder: (context, index) {
        return ForestItem(forest: forests[index]);
      },
    );
  }
}
