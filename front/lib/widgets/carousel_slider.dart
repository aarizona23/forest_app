import 'package:flutter/material.dart';

class ImageCarousel extends StatefulWidget {
  final List<String> imagePaths;

  const ImageCarousel({
    super.key,
    required this.imagePaths,
  });

  @override
  State<ImageCarousel> createState() => _ImageCarouselState();
}

class _ImageCarouselState extends State<ImageCarousel> {
  final PageController _pageController = PageController();
  int _currentPage = 0;

  void _onPageChanged(int index) {
    setState(() {
      _currentPage = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    final int pageCount = widget.imagePaths.length;

    return SizedBox(
      // Give a fixed height or use MediaQuery for dynamic sizing
      height: 300,
      child: Stack(
        children: [
          // 1. PageView as the background
          ClipRRect(
            borderRadius: BorderRadius.circular(20),
            child: PageView(
              controller: _pageController,
              onPageChanged: _onPageChanged,
              children: widget.imagePaths.map((path) {
                return Image.asset(
                  path,
                  fit: BoxFit.cover,
                );
              }).toList(),
            ),
          ),

          // 2. Positioned dots at the bottom-center
          Positioned(
            bottom: 16, // Adjust distance from bottom
            left: 0,
            right: 0,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(pageCount, (index) {
                return AnimatedContainer(
                  duration: const Duration(seconds: 3),
                  margin: const EdgeInsets.symmetric(horizontal: 4.0),
                  width: _currentPage == index ? 12.0 : 8.0,
                  height: _currentPage == index ? 12.0 : 8.0,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: _currentPage == index
                        ? Colors.white // Active dot color
                        : Colors.grey, // Inactive dot color
                  ),
                );
              }),
            ),
          ),
        ],
      ),
    );
  }
}
