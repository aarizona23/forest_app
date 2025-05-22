import 'package:flutter/material.dart';
import 'package:forest_hero/widgets/carousel_slider.dart';
import 'package:forest_hero/models/forest.dart';
import 'package:forest_hero/widgets/description.dart';
import 'package:forest_hero/widgets/calendar.dart';

class ForestScreen extends StatefulWidget {
  const ForestScreen({super.key, required this.forest});

  final Forest forest;

  @override
  State<ForestScreen> createState() => _ForestScreenState();
}

class _ForestScreenState extends State<ForestScreen> {
  // Track which "tab" or section is currently selected
  String _selectedTab = 'info';

  void _clickInfo() {
    setState(() {
      _selectedTab = 'info';
    });
  }

  void _clickCalendar() {
    setState(() {
      _selectedTab = 'calendar';
    });
  }

  @override
  Widget build(BuildContext context) {
    // Decide which widget to show based on _selectedTab
    Widget mainContent;
    if (_selectedTab == 'info') {
      mainContent = Description(
        title: widget.forest.name,
        description: widget.forest.description,
        image: false,
      );
    } else {
      mainContent = CalendarScreen(forest: widget.forest);
    }

    final Color activeColor = Color.fromARGB(255, 137, 184, 41);
    final Color inactiveColor = Colors.white;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Forest Details'),
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Carousel
            SizedBox(
              height: 350,
              child: ImageCarousel(imagePaths: widget.forest.image),
            ),
            const SizedBox(height: 15),

            // Buttons to switch content
            Padding(
              padding: const EdgeInsets.only(left: 10),
              child: Row(
                children: [
                  TextButton(
                    onPressed: _clickInfo,
                    child: const Text('Info'),
                    style: ButtonStyle(
                      backgroundColor: MaterialStateProperty.all(
                          _selectedTab == 'info' ? activeColor : inactiveColor),
                      foregroundColor: MaterialStateProperty.all(
                          _selectedTab == 'info' ? Colors.white : Colors.grey),
                    ),
                  ),
                  const SizedBox(width: 10),
                  TextButton(
                    onPressed: _clickCalendar,
                    child: const Text('Calendar'),
                    style: ButtonStyle(
                      backgroundColor: MaterialStateProperty.all(
                          _selectedTab == 'calendar'
                              ? activeColor
                              : inactiveColor),
                      foregroundColor: MaterialStateProperty.all(
                          _selectedTab == 'calendar'
                              ? Colors.white
                              : Colors.black),
                    ),
                  ),
                ],
              ),
            ),

            // Info or Calendar, depending on _selectedTab
            mainContent,
          ],
        ),
      ),
    );
  }
}
