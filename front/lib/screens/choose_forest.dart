import 'package:flutter/material.dart';
import '../models/forest.dart';
import '../forest_list.dart';
import '../widgets/description.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:forest_hero/models/descriptions.dart';
import '../screens/chat_screen.dart'; // Import your ChatScreen widget

class ChooseForest extends StatelessWidget {
  const ChooseForest({super.key});

  @override
  Widget build(BuildContext context) {
    final String title = 'Forests of Kazakhstan';

    final List<Forest> registeredForests = [
      Forest(
        'Semey Ormany',
        'SemeyOrmany',
        [
          80.5714670950713,
          50.3685743211883,
          81.0227529049287,
          50.6836629049287
        ],
        [
          'assets/forest1/img1.jpg',
          'assets/forest1/img2.jpg',
          'assets/forest1/img3.jpg'
        ],
        semeyOrmanyDesc,
      ),
      Forest(
        'Semey Ormany 2',
        'SemeyOrmany2',
        [79.424667, 50.763611, 79.852944, 51.101222],
        [
          'assets/forest2/img1.jpg',
          'assets/forest2/img2.jpg',
          'assets/forest2/img3.jpg'
        ],
        'The most beautiful forest in KZ',
      ),
      Forest(
        'Borovoe Ormany',
        'NorthKZ',
        [70.120417, 52.938389, 70.403639, 53.097639],
        [
          'assets/forest3/img1.jpg',
          'assets/forest3/img2.jpg',
          'assets/forest3/img3.jpg'
        ],
        borovoeDescription,
      ),
      Forest(
        'East Kazakhstan Forest',
        'EastKZ1',
        [82.757861, 50.6734725, 83.174875, 50.910056],
        [
          'assets/forest4/img1.jpg',
          'assets/forest4/img2.jpg',
          'assets/forest4/img3.jpg'
        ],
        eastKazakhstanDescription,
      ),
    ];

    return Scaffold(
      appBar: AppBar(
        title: Text('Forest analyses',
            style: GoogleFonts.lato(fontSize: 16, fontWeight: FontWeight.bold)),
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.only(
                left: 30,
                top: 8,
              ),
              child: Text(
                'Choose a forest',
                textAlign: TextAlign.start,
                style: GoogleFonts.lato(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            const SizedBox(height: 10),
            SizedBox(
              height: 200,
              width: double.infinity,
              child: Padding(
                padding: const EdgeInsets.only(left: 20),
                child: ForestList(forests: registeredForests),
              ),
            ),
            const SizedBox(height: 10),
            Description(
                title: title, description: forestDescription, image: true),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        backgroundColor: const Color.fromARGB(255, 109, 173, 111),
        onPressed: () {
          // Navigate to ChatScreen when pressed
          Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => const ChatScreen()),
          );
        },
        child: const Icon(
          Icons.chat,
          color: Colors.white,
          size: 30,
        ),
        tooltip: 'Open Chat',
      ),
    );
  }
}
