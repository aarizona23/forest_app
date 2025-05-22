import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

class LineGraph extends StatelessWidget {
  final List<double> data;

  const LineGraph({Key? key, required this.data}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // Compute min, mean, and max values
    final double computedMin = data.reduce((a, b) => a < b ? a : b);
    final double computedMax = data.reduce((a, b) => a > b ? a : b);
    final double computedMean = data.reduce((a, b) => a + b) / data.length;

    final spots = data
        .asMap()
        .entries
        .map((entry) => FlSpot(entry.key.toDouble(), entry.value))
        .toList();

    return Stack(
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 50),
          child: LineChart(
            LineChartData(
              minY: computedMin,
              maxY: computedMax,
              lineTouchData: LineTouchData(
                enabled: true,
                touchTooltipData: LineTouchTooltipData(
                  getTooltipItems: (touchedSpots) {
                    return touchedSpots.map((LineBarSpot spot) {
                      return LineTooltipItem(
                        'X: ${spot.x}\nY: ${spot.y.toStringAsFixed(2)}',
                        const TextStyle(
                          color: Colors.black,
                        ),
                      );
                    }).toList();
                  },
                ),
              ),
              gridData: FlGridData(
                show: true,
                drawVerticalLine: true,
                verticalInterval: 1,
                horizontalInterval: (computedMax - computedMin) / 5,
                getDrawingHorizontalLine: (value) => FlLine(
                  color: Colors.white.withOpacity(0.2),
                  strokeWidth: 1,
                ),
                getDrawingVerticalLine: (value) => FlLine(
                  color: Colors.white.withOpacity(0.2),
                  strokeWidth: 1,
                ),
              ),
              // Disable default left axis labels
              titlesData: FlTitlesData(
                leftTitles: AxisTitles(
                  sideTitles: SideTitles(showTitles: false),
                ),
                topTitles: AxisTitles(
                  sideTitles: SideTitles(showTitles: false),
                ),
                rightTitles: AxisTitles(
                  sideTitles: SideTitles(showTitles: false),
                ),
                bottomTitles: AxisTitles(
                  sideTitles: SideTitles(
                    showTitles: true,
                    reservedSize: 30,
                    interval: 1,
                  ),
                ),
              ),
              borderData: FlBorderData(
                show: true,
                border: const Border(
                  left: BorderSide(color: Colors.black, width: 1),
                  bottom: BorderSide(color: Colors.black, width: 1),
                ),
              ),
              lineBarsData: [
                LineChartBarData(
                  spots: spots,
                  isCurved: true,
                  barWidth: 3,
                  isStrokeCapRound: true,
                  gradient: const LinearGradient(
                    colors: [Colors.green, Colors.lightGreen],
                  ),
                  dotData: FlDotData(
                    show: true,
                    getDotPainter: (FlSpot spot, double percent,
                        LineChartBarData bar, int index) {
                      return FlDotCirclePainter(
                        radius: 4,
                        color: Colors.green,
                        strokeWidth: 0,
                      );
                    },
                  ),
                  belowBarData: BarAreaData(
                    show: true,
                    gradient: LinearGradient(
                      colors: [
                        Colors.green.withOpacity(0.3),
                        Colors.transparent,
                      ],
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
        // Custom Y-axis labels on the left
        Positioned(
          left: 0,
          top: 0,
          bottom: 0,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(computedMax.toStringAsFixed(2),
                  style: const TextStyle(fontSize: 12)),
              Text(computedMean.toStringAsFixed(2),
                  style: const TextStyle(fontSize: 12)),
              Text(computedMin.toStringAsFixed(2),
                  style: const TextStyle(fontSize: 12)),
            ],
          ),
        ),
      ],
    );
  }
}
