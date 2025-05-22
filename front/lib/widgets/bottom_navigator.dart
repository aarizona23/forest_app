import 'package:flutter/material.dart';

class BottomNavigator extends StatefulWidget {
  const BottomNavigator(
      {super.key, required this.index, required this.onItemTapped});

  final int index;
  final ValueChanged<int> onItemTapped;

  @override
  State<BottomNavigator> createState() => _BottomNavigatorState();
}

class _BottomNavigatorState extends State<BottomNavigator> {
  // void _onItemTapped(int index) {
  //   setState(() {
  //     _selectedIndex = index;
  //   });
  // }

  @override
  Widget build(context) {
    return BottomNavigationBar(
      currentIndex: widget.index,
      onTap: widget.onItemTapped,
      type: BottomNavigationBarType.fixed,
      backgroundColor: Colors.white,
      selectedItemColor: Colors.green,
      unselectedItemColor: Colors.grey,
      items: const <BottomNavigationBarItem>[
        BottomNavigationBarItem(
          icon: Icon(Icons.show_chart),
          label: 'Index',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.forest),
          label: 'Forest',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.map),
          label: 'Deforestation',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.local_fire_department),
          label: 'Burned Area',
        ),
      ],
    );
  }
}
