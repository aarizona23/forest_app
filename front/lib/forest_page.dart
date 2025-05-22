import 'package:flutter/material.dart';
import 'models/forest.dart';

class ForestPage extends StatefulWidget {
  const ForestPage({super.key, required this.forest});

  final Forest forest;

  @override
  State<ForestPage> createState() => _ForestPageState();
}

class _ForestPageState extends State<ForestPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold();
  }
}
