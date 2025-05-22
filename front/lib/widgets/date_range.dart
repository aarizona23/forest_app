import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

final formatter = DateFormat.yMd();

class DateRange extends StatefulWidget {
  const DateRange({super.key});

  @override
  State<DateRange> createState() => _DateRangeState();
}

class _DateRangeState extends State<DateRange> {
  DateTime? _beginSelectedDate;
  DateTime? _endSelectedDate;

  // These booleans reflect whether the dates have been selected (and should be green)
  bool isBeginSelected = false;
  bool isEndSelected = false;

  // New booleans to indicate the active (tapped) state (should be yellow)
  bool isBeginActive = false;
  bool isEndActive = false;

  void onPickStart() {
    // Set the begin icon as active (will show yellow)
    setState(() {
      isBeginActive = true;
    });
    // Show date picker for the start date
    showDatePicker(
      context: context,
      initialDate: _beginSelectedDate ?? DateTime.now(),
      firstDate: DateTime(2021),
      lastDate: DateTime(2022),
    ).then((date) {
      setState(() {
        // Regardless of selection, the active state is turned off
        isBeginActive = false;
        if (date != null) {
          _beginSelectedDate = date;
          isBeginSelected = true; // Date is selected, so show green
        }
      });
    });
  }

  void onPickEnd() {
    // Set the end icon as active (will show yellow)
    setState(() {
      isEndActive = true;
    });
    // Show date picker for the end date
    showDatePicker(
      context: context,
      initialDate: _endSelectedDate ?? DateTime.now(),
      firstDate: DateTime(2021),
      lastDate: DateTime(2022),
    ).then((date) {
      setState(() {
        // Turn off the active state once the picker is dismissed
        isEndActive = false;
        if (date != null) {
          _endSelectedDate = date;
          isEndSelected = true; // Date is selected, so show green
        }
      });
    });
  }

  @override
  void initState() {
    super.initState();
    // Default both dates to now (optional)
    _beginSelectedDate = DateTime.now();
    _endSelectedDate = DateTime.now();
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 100,
      width: double.infinity,
      child: Card(
        child: Column(children: [
          const Text('Select Date Range'),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  SizedBox(
                    width: 160,
                    height: 50,
                    child: AnimatedContainer(
                      duration: const Duration(milliseconds: 300),
                      width: 160,
                      height: 50,
                      decoration: BoxDecoration(
                        color: isBeginActive
                            ? Colors.yellow
                            : (isBeginSelected ? Colors.green : Colors.white),
                        borderRadius: BorderRadius.circular(4),
                        border: Border.all(color: Colors.black),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.all(5.0),
                        child: Row(
                          children: [
                            Text(
                              _beginSelectedDate == null
                                  ? 'Not selected'
                                  : formatter.format(_beginSelectedDate!),
                              textAlign: TextAlign.center,
                            ),
                            const Spacer(),
                            IconButton(
                              icon: const Icon(Icons.calendar_today, size: 15),
                              onPressed: onPickStart,
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                  const Spacer(),
                  SizedBox(
                    width: 160,
                    height: 50,
                    child: AnimatedContainer(
                      duration: const Duration(milliseconds: 300),
                      width: 160,
                      height: 50,
                      decoration: BoxDecoration(
                        color: isEndActive
                            ? Colors.yellow
                            : (isEndSelected ? Colors.green : Colors.white),
                        borderRadius: BorderRadius.circular(4),
                        border: Border.all(color: Colors.black),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.all(5.0),
                        child: Row(
                          children: [
                            Text(
                              _endSelectedDate == null
                                  ? 'Not selected'
                                  : formatter.format(_endSelectedDate!),
                              textAlign: TextAlign.center,
                            ),
                            const Spacer(),
                            IconButton(
                              icon: const Icon(Icons.calendar_today, size: 15),
                              onPressed: onPickEnd,
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ]),
      ),
    );
  }
}
