import 'package:flutter/material.dart';

void main() {
  runApp(const FleetIQDriverApp());
}

class FleetIQDriverApp extends StatelessWidget {
  const FleetIQDriverApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'FleetIQ Driver',
      home: Scaffold(
        appBar: AppBar(title: const Text('FleetIQ Driver App')),
        body: const Padding(
          padding: EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Today\'s Trips', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              SizedBox(height: 8),
              Text('No trips assigned yet. Connect API and sync assignments.'),
            ],
          ),
        ),
      ),
    );
  }
}
