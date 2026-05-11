class User {
  final int? id;
  final String username;
  final String profession;
  final String serviceArea;

  User({
    this.id,
    required this.username,
    required this.profession,
    required this.serviceArea,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'username': username,
      'profession': profession,
      'service_area': serviceArea,
    };
  }

  factory User.fromMap(Map<String, dynamic> map) {
    return User(
      id: map['id'],
      username: map['username'],
      profession: map['profession'],
      serviceArea: map['service_area'],
    );
  }
}
