import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:http/http.dart' as http;
import 'package:forest_hero/models/forest.dart';

class ForestScreen extends StatefulWidget {
  const ForestScreen({super.key, required this.forest, required this.endDate});
  final Forest forest;
  final DateTime? endDate;

  @override
  State<ForestScreen> createState() => _ForestScreenState();
}

class _ForestScreenState extends State<ForestScreen> {
  String? maskImageUrl;

  @override
  void initState() {
    super.initState();
    _fetchMask();
  }

  Future<void> _fetchMask() async {
    // Use appropriate URL: If using an Android emulator, consider using 10.0.2.2.
    const String url = 'http://10.0.2.2:8000/forest/get_forest_mask/';
    final String endDate =
        widget.endDate?.toIso8601String().split('T')[0] ?? '';
    print('endDate: $endDate');
    print('forestId: ${widget.forest.forestId}');
    final body = jsonEncode({
      "forest_unique_id": widget
          .forest.forestId, // or use a hardcoded string like "SemeyOrmany"
      "end_date": endDate
    });

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {"Content-Type": "application/json"},
        body: body,
      );

      if (response.statusCode == 200) {
        // Assume the response is a JSON-encoded string.
        final result = jsonDecode(response.body);
        setState(() {
          maskImageUrl = result;
          print(result);
        });
      } else {
        // Handle error response here if needed.
        debugPrint('Error: ${response.statusCode}');
      }
    } catch (e) {
      debugPrint('Exception: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    final LatLngBounds overlayBounds = LatLngBounds(
      LatLng(widget.forest.bbox[1], widget.forest.bbox[0]),
      LatLng(widget.forest.bbox[3], widget.forest.bbox[2]),
    );

    // Calculate center from bbox:
    final double centerLat =
        (widget.forest.bbox[1] + widget.forest.bbox[3]) / 2;
    final double centerLon =
        (widget.forest.bbox[0] + widget.forest.bbox[2]) / 2;

    String? correctedPath;
    String? fullImageUrl;
    // if (maskImageUrl != null) {
    //   if (maskImageUrl!.startsWith('/files')) {
    //     // Remove the leading '/files' from the response.
    //     final correctedPath = maskImageUrl!.substring('/files'.length);
    //     fullImageUrl = "http://10.0.2.2:8000/files" + correctedPath;
    //   } else {
    //     fullImageUrl = "http://10.0.2.2:8000" + maskImageUrl!;
    //   }
    // }
    if (maskImageUrl != null) {
      // Replace '/files/files' with a single '/files'
      // correctedPath = maskImageUrl!.replaceFirst('/files/files', '/files');
      fullImageUrl = "http://10.0.2.2:8000" + maskImageUrl!;
      print(fullImageUrl);
    }

    return Scaffold(
      body: FlutterMap(
        options: MapOptions(
          initialCenter: LatLng(centerLat, centerLon),
          initialZoom: 10.0,
        ),
        children: [
          TileLayer(
            urlTemplate: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
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

            // userAgentPackageName: 'com.example.your_app',
          ),
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
    );
  }
}
