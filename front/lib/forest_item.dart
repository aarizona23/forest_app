import 'package:flutter/material.dart';
import 'models/forest.dart';
import 'package:forest_hero/screens/forest_screen.dart';

class ForestItem extends StatelessWidget {
  const ForestItem({super.key, required this.forest});

  final Forest forest;

  void _onTap(BuildContext context) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) {
          return ForestScreen(forest: forest);
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 350,
      height: 150,
      child: Card(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20), // Rounded corners
        ),
        clipBehavior: Clip.antiAlias, // Ensures children (image) are clipped
        child: Stack(
          children: [
            // 1) Background image
            Positioned.fill(
              child: Image.asset(
                forest.image[0],
                fit: BoxFit.cover,
              ),
            ),

            // 2) Top-left: Title (forest name)
            Positioned(
              top: 8,
              left: 8,
              child: Text(
                forest.name,
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  shadows: [
                    Shadow(
                      blurRadius: 4,
                      color: Colors.black54,
                      offset: Offset(1, 1),
                    ),
                  ],
                ),
              ),
            ),

            // 3) Top-right: Arrow icon
            Positioned(
              top: 8,
              right: 8,
              child: IconButton(
                onPressed: () => _onTap(context),
                icon: Icon(
                  Icons.arrow_forward,
                  color: Colors.white,
                  size: 32,
                  shadows: const [
                    Shadow(
                      blurRadius: 4,
                      color: Colors.black54,
                      offset: Offset(1, 1),
                    ),
                  ],
                ),
              ),
            ),

            // 4) Bottom-left: Description or extra text
          ],
        ),
      ),
    );
  }
}
