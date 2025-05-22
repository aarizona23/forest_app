import 'package:flutter/material.dart';
import 'screens/choose_forest.dart';

var kColorScheme =
    ColorScheme.fromSeed(seedColor: Color.fromARGB(255, 109, 173, 111));

void main() {
  runApp(MaterialApp(
    // theme: ThemeData().copyWith(
    //   elevatedButtonTheme: ElevatedButtonThemeData(
    //     style: ElevatedButton.styleFrom(
    //       backgroundColor: kColorScheme.primary,
    //     ),
    //   ),
    // ),
    home: ChooseForest(),
  ));
}
