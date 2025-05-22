import 'package:flutter/material.dart';
import 'package:table_calendar/table_calendar.dart';
import 'package:forest_hero/widgets/date_rangecard.dart';
import 'package:forest_hero/forest_analysis.dart';
import 'package:forest_hero/models/forest.dart';

class CalendarScreen extends StatefulWidget {
  const CalendarScreen({super.key, required this.forest});

  final Forest forest;

  @override
  State<CalendarScreen> createState() => _CalendarScreenState();
}

class _CalendarScreenState extends State<CalendarScreen> {
  // We store the two selected dates here in the parent.
  DateTime? _beginSelectedDate;
  DateTime? _endSelectedDate;

  // We also store the table calendar's focused/selected day (for single selection).
  late DateTime _focusedDay;
  DateTime? _selectedDay;

  // Track if we are picking the start date or the end date
  bool _isSelectingStartDate = false;
  bool _isSelectingEndDate = false;

  void _onTap(BuildContext context) {
    setState(() {
      _isSelectingStartDate = false;
      _isSelectingEndDate = false;
    });
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) => ForestAnalyses(
          startDate: _beginSelectedDate,
          endDate: _endSelectedDate,
          forest: widget.forest,
        ),
      ),
    );
  }

  @override
  void initState() {
    super.initState();
    // Default the parent’s date range to now
    _beginSelectedDate = DateTime.now();
    _endSelectedDate = DateTime.now();

    // Initialize the TableCalendar’s “selected day” to today
    _focusedDay = DateTime.now();
    _selectedDay = DateTime.now();
  }

  // This is the method TableCalendar calls when a user picks a day
  void _onDaySelected(DateTime selectedDay, DateTime focusedDay) {
    setState(() {
      _selectedDay = selectedDay;
      _focusedDay = focusedDay;

      // If we are in the process of picking the start date, set it.
      if (_isSelectingStartDate && !_isSelectingEndDate) {
        _beginSelectedDate = selectedDay;
        // done picking
      }
      // If we are picking the end date, set that.
      else if (_isSelectingEndDate) {
        _isSelectingStartDate = false;
        _endSelectedDate = selectedDay;
        // done picking
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20),
      child: Column(
        children: [
          // TABLE CALENDAR
          Card(
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(20),
            ),
            child: TableCalendar(
              firstDay: DateTime.utc(2020, 1, 1),
              lastDay: DateTime.utc(2025, 12, 31),
              focusedDay: _focusedDay,
              selectedDayPredicate: (day) => isSameDay(_selectedDay, day),
              onDaySelected: _onDaySelected,
              onPageChanged: (focusedDay) {
                _focusedDay = focusedDay;
              },

              // Customize style
              calendarStyle: const CalendarStyle(
                todayDecoration: BoxDecoration(
                  color: Color.fromARGB(255, 137, 184, 41),
                  shape: BoxShape.circle,
                ),
                selectedDecoration: BoxDecoration(
                  color: Color.fromARGB(255, 137, 184, 41),
                  shape: BoxShape.rectangle,
                ),
              ),
              headerStyle: const HeaderStyle(
                formatButtonVisible: false,
                titleCentered: true,
              ),
            ),
          ),
          const SizedBox(height: 10),

          // Our custom DateRange widget
          // We pass it the current dates and callbacks
          DateRange(
            beginSelectedDate: _beginSelectedDate,
            endSelectedDate: _endSelectedDate,
            onStartIconPressed: () {
              // The user wants to pick the start date using the table calendar
              setState(() {
                _isSelectingStartDate = true;
                _isSelectingEndDate = false;
              });
            },
            onEndIconPressed: () {
              // The user wants to pick the end date
              setState(() {
                _isSelectingEndDate = true;
                _isSelectingStartDate = false;
              });
            },
          ),
          const SizedBox(height: 10),
          ElevatedButton(
            onPressed: () => _onTap(context),
            style: ButtonStyle(
              backgroundColor:
                  MaterialStateProperty.all(Color.fromARGB(255, 137, 184, 41)),
            ),
            // () {
            //   // Just an example usage of the selected range
            //   _isSelectingEndDate = false;

            //   // debugPrint('Start: $_beginSelectedDate');
            //   // debugPrint('End: $_endSelectedDate');
            // },
            child: const Text('Analyze',
                style: TextStyle(fontSize: 16, color: Colors.white)),
          ),
        ],
      ),
    );
  }
}
