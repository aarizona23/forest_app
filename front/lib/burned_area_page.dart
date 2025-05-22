import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:http/http.dart' as http;
import 'package:forest_hero/models/forest.dart';

class BurnedAreaPage extends StatefulWidget {
  const BurnedAreaPage({super.key, required this.forest});
  final Forest forest;

  @override
  State<BurnedAreaPage> createState() => _BurnedAreaPageState();
}

class _BurnedAreaPageState extends State<BurnedAreaPage> {
  String? maskImageUrl;

  @override
  void initState() {
    super.initState();
    // Fetch a default burned mask for one of the dates, e.g., "2023-03-16"
    _fetchBurnedMask("2023-06-09");
  }

  Future<void> _fetchBurnedMask(String date) async {
    // Use the burned mask endpoint.
    const String url = 'http://10.0.2.2:8000/forest/get_burned_mask/';
    final body = jsonEncode({
      "forest_unique_id": widget.forest.forestId, // e.g., "SemeyOrmany"
      "end_date": date,
    });

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {"Content-Type": "application/json"},
        body: body,
      );

      if (response.statusCode == 200) {
        final result = jsonDecode(response.body);
        setState(() {
          maskImageUrl = result;
          print("Mask for $date: $result");
        });
      } else {
        debugPrint('Error: ${response.statusCode}');
      }
    } catch (e) {
      debugPrint('Exception: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    // Define the overlay bounds using the forest's bbox.
    final LatLngBounds overlayBounds = LatLngBounds(
      LatLng(widget.forest.bbox[1], widget.forest.bbox[0]),
      LatLng(widget.forest.bbox[3], widget.forest.bbox[2]),
    );

    // Calculate the center of the bounding box.
    final double centerLat =
        (widget.forest.bbox[1] + widget.forest.bbox[3]) / 2;
    final double centerLon =
        (widget.forest.bbox[0] + widget.forest.bbox[2]) / 2;

    String? fullImageUrl;
    if (maskImageUrl != null) {
      // Prepend the base URL to the returned relative path.
      fullImageUrl = "http://10.0.2.2:8000" + maskImageUrl!;
      print("Full Image URL: $fullImageUrl");
    }

    return Scaffold(
      body: Column(
        children: [
          // The map area
          Expanded(
            child: FlutterMap(
              options: MapOptions(
                initialCenter: LatLng(centerLat, centerLon),
                initialZoom: 10.0,
              ),
              children: [
                TileLayer(
                  urlTemplate:
                      "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                  subdomains: ['a', 'b', 'c'],
                  tileBuilder: (
                    BuildContext context,
                    Widget tileWidget,
                    TileImage tile,
                  ) {
                    return ColorFiltered(
                      colorFilter: const ColorFilter.matrix(<double>[
                        -0.2126, -0.7152, -0.0722, 0, 255, // Red channel
                        -0.2126, -0.7152, -0.0722, 0, 255, // Green channel
                        -0.2126, -0.7152, -0.0722, 0, 255, // Blue channel
                        0, 0, 0, 1, 0, // Alpha channel
                      ]),
                      child: tileWidget,
                    );
                  },
                ),
                // Overlay the burned mask image if available.
                if (maskImageUrl != null)
                  OverlayImageLayer(
                    overlayImages: [
                      OverlayImage(
                        bounds: overlayBounds,
                        opacity: 0.4,
                        imageProvider: NetworkImage(fullImageUrl!),
                      ),
                    ],
                  ),
              ],
            ),
          ),
          // A row of three buttons to select different dates
          Padding(
              padding: const EdgeInsets.all(8.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Expanded(
                    child: ElevatedButton(
                      onPressed: () => _fetchBurnedMask("2023-06-09"),
                      child: const Text("Jun 09, 2023"),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: ElevatedButton(
                      onPressed: () => _fetchBurnedMask("2023-06-11"),
                      child: const Text("Jun 11, 2023"),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: ElevatedButton(
                      onPressed: () => _fetchBurnedMask("2023-06-16"),
                      child: const Text("Jun 16, 2023"),
                    ),
                  ),
                ],
              )),
        ],
      ),
    );
  }
}
