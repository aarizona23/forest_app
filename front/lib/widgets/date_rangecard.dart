import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

final formatter = DateFormat.yMd();

class DateRange extends StatelessWidget {
  // These come from the parent
  final DateTime? beginSelectedDate;
  final DateTime? endSelectedDate;
  final VoidCallback onStartIconPressed;
  final VoidCallback onEndIconPressed;

  const DateRange({
    super.key,
    required this.beginSelectedDate,
    required this.endSelectedDate,
    required this.onStartIconPressed,
    required this.onEndIconPressed,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 100,
      width: double.infinity,
      child: Card(
        child: Column(
          children: [
            const Text('Select Date Range'),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: Row(
                  children: [
                    // Start date
                    SizedBox(
                      width: 160,
                      height: 50,
                      child: Card(
                        child: Padding(
                          padding: const EdgeInsets.all(5.0),
                          child: Row(
                            children: [
                              Text(
                                beginSelectedDate == null
                                    ? 'Not selected'
                                    : formatter.format(beginSelectedDate!),
                                textAlign: TextAlign.center,
                              ),
                              const Spacer(),
                              IconButton(
                                icon: const Icon(
                                  Icons.calendar_today,
                                  size: 15,
                                ),
                                onPressed: onStartIconPressed,
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                    const Spacer(),
                    // End date
                    SizedBox(
                      width: 160,
                      height: 50,
                      child: Card(
                        child: Padding(
                          padding: const EdgeInsets.all(5.0),
                          child: Row(
                            children: [
                              Text(
                                endSelectedDate == null
                                    ? 'Not selected'
                                    : formatter.format(endSelectedDate!),
                                textAlign: TextAlign.center,
                              ),
                              const Spacer(),
                              IconButton(
                                icon: const Icon(
                                  Icons.calendar_today,
                                  size: 15,
                                ),
                                onPressed: onEndIconPressed,
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
          ],
        ),
      ),
    );
  }
}
