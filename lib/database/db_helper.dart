import 'dart:async';
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';
import 'package:crypto/crypto.dart';
import 'dart:convert';

class DBHelper {
  static Database? _db;

  Future<Database> get db async {
    if (_db != null) return _db!;
    _db = await initDb();
    return _db!;
  }

  initDb() async {
    String path = join(await getDatabasesPath(), 'tera.db');
    var db = await openDatabase(path, version: 1, onCreate: _onCreate);
    return db;
  }

  void _onCreate(Database db, int version) async {
    // Users table
    await db.execute('''
      CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        profession TEXT,
        service_area TEXT
      )
    ''');

    // Files/Data table for service areas
    await db.execute('''
      CREATE TABLE service_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        content TEXT,
        area TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
      )
    ''');
  }

  // Auth functions
  Future<int> registerUser(String username, String password, String profession, String area) async {
    var dbClient = await db;
    var bytes = utf8.encode(password);
    var digest = sha256.convert(bytes);
    
    return await dbClient.insert('users', {
      'username': username,
      'password': digest.toString(),
      'profession': profession,
      'service_area': area
    });
  }

  Future<Map<String, dynamic>?> loginUser(String username, String password) async {
    var dbClient = await db;
    var bytes = utf8.encode(password);
    var digest = sha256.convert(bytes);

    var res = await dbClient.query('users',
        where: 'username = ? AND password = ?',
        whereArgs: [username, digest.toString()]);

    if (res.isNotEmpty) return res.first;
    return null;
  }

  // Service data functions
  Future<int> saveServiceData(int userId, String title, String content, String area) async {
    var dbClient = await db;
    return await dbClient.insert('service_data', {
      'user_id': userId,
      'title': title,
      'content': content,
      'area': area
    });
  }

  Future<List<Map<String, dynamic>>> getServiceData(int userId, String area) async {
    var dbClient = await db;
    return await dbClient.query('service_data',
        where: 'user_id = ? AND area = ?',
        whereArgs: [userId, area],
        orderBy: 'timestamp DESC');
  }
}
