import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'dart:async';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    Timer(const Duration(seconds: 3), () {
      Navigator.pushReplacementNamed(context, '/login');
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xFF0A0F1F), Color(0xFF05060A)],
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const TeraLogo(),
            const SizedBox(height: 30),
            Text(
              'TERA',
              style: GoogleFonts.orbitron(
                fontSize: 48,
                fontWeight: FontWeight.bold,
                color: Colors.white,
                letterSpacing: 10,
                shadows: [
                  const Shadow(color: Color(0xFFA855F7), blurRadius: 20),
                ],
              ),
            ),
            const SizedBox(height: 10),
            Text(
              'AGENTE PESSOAL DE SERVIÇO',
              style: GoogleFonts.exo2(
                fontSize: 12,
                color: Colors.white70,
                letterSpacing: 2,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class TeraLogo extends StatelessWidget {
  const TeraLogo({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 150,
      height: 150,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        border: Border.all(color: const Color(0xFF3B82F6), width: 2),
        boxShadow: [
          BoxShadow(
            color: const Color(0xFFA855F7).withOpacity(0.3),
            blurRadius: 30,
            spreadRadius: 5,
          ),
        ],
      ),
      child: Center(
        child: CustomPaint(size: const Size(80, 80), painter: LogoPainter()),
      ),
    );
  }
}

class LogoPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..shader = const LinearGradient(
        colors: [Color(0xFFA855F7), Color(0xFF3B82F6)],
      ).createShader(Rect.fromLTWH(0, 0, size.width, size.height))
      ..style = PaintingStyle.fill;

    final path = Path();
    // Simplified futuristic T
    path.moveTo(size.width * 0.1, size.height * 0.2);
    path.lineTo(size.width * 0.9, size.height * 0.2);
    path.lineTo(size.width * 0.9, size.height * 0.35);
    path.lineTo(size.width * 0.6, size.height * 0.35);
    path.lineTo(size.width * 0.6, size.height * 0.9);
    path.lineTo(size.width * 0.4, size.height * 0.9);
    path.lineTo(size.width * 0.4, size.height * 0.35);
    path.lineTo(size.width * 0.1, size.height * 0.35);
    path.close();

    canvas.drawPath(path, paint);

    // Add some "glow" lines
    final glowPaint = Paint()
      ..color = const Color(0xFF22D3EE).withOpacity(0.5)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2;

    canvas.drawCircle(
      Offset(size.width / 2, size.height / 2),
      size.width * 0.7,
      glowPaint,
    );
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
