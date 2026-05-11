import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../database/db_helper.dart';
import '../widgets/custom_widgets.dart';
import 'splash_screen.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  final _professionController = TextEditingController();
  String _selectedArea = 'Tecnologia';
  final _dbHelper = DBHelper();

  final List<String> _areas = [
    'Tecnologia',
    'Saúde',
    'Educação',
    'Engenharia',
    'Artes',
    'Serviços Gerais',
    'Comércio',
    'Outros'
  ];

  void _register() async {
    if (_usernameController.text.isEmpty || _passwordController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Preencha todos os campos!')),
      );
      return;
    }

    try {
      await _dbHelper.registerUser(
        _usernameController.text,
        _passwordController.text,
        _professionController.text,
        _selectedArea,
      );
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Cadastro realizado com sucesso!')),
      );
      Navigator.pop(context);
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Erro ao cadastrar. Usuário já existe?')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Container(
          height: MediaQuery.of(context).size.height,
          padding: const EdgeInsets.all(30),
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [Color(0xFF0A0F1F), Color(0xFF05060A)],
            ),
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const TeraLogo(),
              const SizedBox(height: 20),
              Text(
                'CADASTRO',
                style: GoogleFonts.orbitron(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 4,
                ),
              ),
              const SizedBox(height: 20),
              GlassCard(
                child: Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    children: [
                      TextField(
                        controller: _usernameController,
                        decoration: const InputDecoration(
                          labelText: 'Usuário',
                          prefixIcon: Icon(Icons.person, color: Color(0xFF3B82F6)),
                        ),
                      ),
                      TextField(
                        controller: _passwordController,
                        obscureText: true,
                        decoration: const InputDecoration(
                          labelText: 'Senha',
                          prefixIcon: Icon(Icons.lock, color: Color(0xFFA855F7)),
                        ),
                      ),
                      TextField(
                        controller: _professionController,
                        decoration: const InputDecoration(
                          labelText: 'Profissão',
                          prefixIcon: Icon(Icons.work, color: Color(0xFF22D3EE)),
                        ),
                      ),
                      const SizedBox(height: 15),
                      DropdownButtonFormField<String>(
                        value: _selectedArea,
                        dropdownColor: const Color(0xFF0A0F1F),
                        decoration: const InputDecoration(
                          labelText: 'Área de Serviço',
                          prefixIcon: Icon(Icons.category, color: Colors.white70),
                        ),
                        items: _areas.map((area) {
                          return DropdownMenuItem(value: area, child: Text(area));
                        }).toList(),
                        onChanged: (val) => setState(() => _selectedArea = val!),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 30),
              NeonButton(
                text: 'CADASTRAR',
                onPressed: _register,
              ),
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('Já tem uma conta? Login', style: TextStyle(color: Colors.white70)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
