import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:http/http.dart' as http;
import 'package:forest_hero/models/forest.dart';

class DeforestationPage extends StatefulWidget {
  const DeforestationPage({
    super.key,
    required this.forest,
    required this.startDate,
    required this.endDate,
  });
  final Forest forest;
  final DateTime? startDate;
  final DateTime? endDate;

  @override
  State<DeforestationPage> createState() => _DeforestationPageState();
}

class _DeforestationPageState extends State<DeforestationPage> {
  String? maskImageUrl;

  @override
  void initState() {
    super.initState();
    _fetchMask();
  }

  Future<void> _fetchMask() async {
    const String url = 'http://10.0.2.2:8000/forest/get_deforestation_mask/';
    final String endDate =
        widget.endDate?.toIso8601String().split('T')[0] ?? '';
    final String startDate =
        widget.startDate?.toIso8601String().split('T')[0] ?? '';
    print('endDate: $endDate');
    print('forestId: ${widget.forest.forestId}');
    final body = jsonEncode({
      "forest_unique_id": widget.forest.forestId,
      "start_date": startDate,
      "end_date": endDate
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
          print(result);
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
    // Get bounds for overlay from the forest's bounding box.
    final LatLngBounds overlayBounds = LatLngBounds(
      LatLng(widget.forest.bbox[1], widget.forest.bbox[0]),
      LatLng(widget.forest.bbox[3], widget.forest.bbox[2]),
    );

    // Calculate center from bbox.
    final double centerLat =
        (widget.forest.bbox[1] + widget.forest.bbox[3]) / 2;
    final double centerLon =
        (widget.forest.bbox[0] + widget.forest.bbox[2]) / 2;

    String? fullImageUrl;
    if (maskImageUrl != null) {
      fullImageUrl = "http://10.0.2.2:8000" + maskImageUrl!;
      print(fullImageUrl);
    }

    return Scaffold(
      body: Stack(
        children: [
          FlutterMap(
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
          // Display a loading indicator if the mask data hasn't loaded yet.
          if (maskImageUrl == null)
            Container(
              color: Colors.black.withOpacity(0.3),
              child: const Center(
                child: CircularProgressIndicator(),
              ),
            ),
        ],
      ),
    );
  }
}
