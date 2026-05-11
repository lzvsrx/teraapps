import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../database/db_helper.dart';
import '../widgets/custom_widgets.dart';
import 'splash_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final user =
        ModalRoute.of(context)!.settings.arguments as Map<String, dynamic>;

    return Scaffold(
      drawer: Drawer(
        backgroundColor: const Color(0xFF0A0F1F),
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            DrawerHeader(
              decoration: const BoxDecoration(
                gradient: LinearGradient(
                  colors: [Color(0xFFA855F7), Color(0xFF3B82F6)],
                ),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const TeraLogo(),
                  const SizedBox(height: 10),
                  Text(
                    user['username'],
                    style: GoogleFonts.orbitron(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    user['profession'],
                    style: const TextStyle(color: Colors.white70),
                  ),
                ],
              ),
            ),
            ListTile(
              leading: const Icon(Icons.home, color: Color(0xFF22D3EE)),
              title: const Text('Início'),
              onTap: () => Navigator.pop(context),
            ),
            ListTile(
              leading: const Icon(Icons.exit_to_app, color: Colors.redAccent),
              title: const Text('Sair'),
              onTap: () => Navigator.pushReplacementNamed(context, '/login'),
            ),
          ],
        ),
      ),
      body: Container(
        width: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xFF0A0F1F), Color(0xFF05060A)],
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Builder(
                      builder: (context) => IconButton(
                        icon: const Icon(
                          Icons.menu,
                          color: Colors.white,
                          size: 30,
                        ),
                        onPressed: () => Scaffold.of(context).openDrawer(),
                      ),
                    ),
                    const TeraLogo(),
                  ],
                ),
                const SizedBox(height: 30),
                Text(
                  'Olá, ${user['username']}',
                  style: GoogleFonts.orbitron(
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Text(
                  'Seu assistente pessoal TERA está pronto.',
                  style: TextStyle(
                    color: Colors.white.withOpacity(0.6),
                    fontSize: 16,
                  ),
                ),
                const SizedBox(height: 40),
                Text(
                  'ÁREA DE ATUAÇÃO',
                  style: GoogleFonts.orbitron(
                    fontSize: 18,
                    letterSpacing: 2,
                    color: const Color(0xFF3B82F6),
                  ),
                ),
                const SizedBox(height: 20),
                GestureDetector(
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => ServiceAreaScreen(user: user),
                      ),
                    );
                  },
                  child: GlassCard(
                    child: Container(
                      padding: const EdgeInsets.all(25),
                      width: double.infinity,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              const Icon(
                                Icons.work_outline,
                                color: Color(0xFFA855F7),
                                size: 40,
                              ),
                              const SizedBox(width: 15),
                              Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    user['service_area'],
                                    style: const TextStyle(
                                      fontSize: 22,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                  Text(
                                    user['profession'],
                                    style: const TextStyle(
                                      color: Colors.white70,
                                    ),
                                  ),
                                ],
                              ),
                              const Spacer(),
                              const Icon(
                                Icons.arrow_forward_ios,
                                color: Colors.white24,
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 40),
                Text(
                  'INSIGHTS DIÁRIOS',
                  style: GoogleFonts.orbitron(
                    fontSize: 18,
                    letterSpacing: 2,
                    color: const Color(0xFF22D3EE),
                  ),
                ),
                const SizedBox(height: 20),
                Expanded(
                  child: GridView.count(
                    crossAxisCount: 2,
                    mainAxisSpacing: 15,
                    crossAxisSpacing: 15,
                    children: [
                      _buildInfoCard(Icons.analytics, 'Produtividade', '+12%'),
                      _buildInfoCard(Icons.schedule, 'Agenda', '3 Tarefas'),
                      _buildInfoCard(Icons.cloud_done, 'Sincronizado', '100%'),
                      _buildInfoCard(Icons.security, 'Segurança', 'Máxima'),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildInfoCard(IconData icon, String title, String value) {
    return GlassCard(
      child: Padding(
        padding: const EdgeInsets.all(15),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, color: const Color(0xFF3B82F6), size: 30),
            const SizedBox(height: 10),
            Text(
              title,
              style: const TextStyle(color: Colors.white70, fontSize: 12),
            ),
            Text(
              value,
              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
            ),
          ],
        ),
      ),
    );
  }
}

class ServiceAreaScreen extends StatefulWidget {
  final Map<String, dynamic> user;
  const ServiceAreaScreen({super.key, required this.user});

  @override
  State<ServiceAreaScreen> createState() => _ServiceAreaScreenState();
}

class _ServiceAreaScreenState extends State<ServiceAreaScreen> {
  final _titleController = TextEditingController();
  final _contentController = TextEditingController();
  final _dbHelper = DBHelper();
  List<Map<String, dynamic>> _data = [];

  @override
  void initState() {
    super.initState();
    _refreshData();
  }

  void _refreshData() async {
    final data = await _dbHelper.getServiceData(
      widget.user['id'],
      widget.user['service_area'],
    );
    setState(() => _data = data);
  }

  void _saveData() async {
    if (_titleController.text.isEmpty) return;
    await _dbHelper.saveServiceData(
      widget.user['id'],
      _titleController.text,
      _contentController.text,
      widget.user['service_area'],
    );
    _titleController.clear();
    _contentController.clear();
    if (!mounted) return;
    Navigator.pop(context);
    _refreshData();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          widget.user['service_area'].toUpperCase(),
          style: GoogleFonts.orbitron(fontSize: 16),
        ),
        backgroundColor: const Color(0xFF0A0F1F),
        elevation: 0,
      ),
      body: Container(
        decoration: const BoxDecoration(color: Color(0xFF05060A)),
        child: Column(
          children: [
            Expanded(
              child: ListView.builder(
                padding: const EdgeInsets.all(20),
                itemCount: _data.length,
                itemBuilder: (context, index) {
                  return Card(
                    color: Colors.white.withOpacity(0.05),
                    margin: const EdgeInsets.only(bottom: 15),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(15),
                    ),
                    child: ListTile(
                      title: Text(
                        _data[index]['title'],
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                      subtitle: Text(
                        _data[index]['content'],
                        style: const TextStyle(color: Colors.white70),
                      ),
                      trailing: Text(
                        _data[index]['timestamp'].toString().split(' ')[0],
                        style: const TextStyle(
                          fontSize: 10,
                          color: Colors.white30,
                        ),
                      ),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        backgroundColor: const Color(0xFFA855F7),
        onPressed: () {
          showModalBottomSheet(
            context: context,
            isScrollControlled: true,
            backgroundColor: const Color(0xFF0A0F1F),
            shape: const RoundedRectangleBorder(
              borderRadius: BorderRadius.vertical(top: Radius.circular(25)),
            ),
            builder: (context) => Padding(
              padding: EdgeInsets.only(
                bottom: MediaQuery.of(context).viewInsets.bottom,
                left: 20,
                right: 20,
                top: 20,
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    'NOVO REGISTRO',
                    style: GoogleFonts.orbitron(fontSize: 18),
                  ),
                  const SizedBox(height: 20),
                  TextField(
                    controller: _titleController,
                    decoration: const InputDecoration(labelText: 'Título'),
                  ),
                  TextField(
                    controller: _contentController,
                    decoration: const InputDecoration(
                      labelText: 'Conteúdo / Arquivo',
                    ),
                    maxLines: 3,
                  ),
                  const SizedBox(height: 30),
                  NeonButton(text: 'SALVAR NO BANCO', onPressed: _saveData),
                  const SizedBox(height: 30),
                ],
              ),
            ),
          );
        },
        child: const Icon(Icons.add, color: Colors.white),
      ),
    );
  }
}
