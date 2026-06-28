import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------
const String _apiBase =
    String.fromEnvironment('API_BASE_URL', defaultValue: 'http://10.0.2.2:8000/api/v1');
const String _tokenKey = 'fleetiq_token';

// ---------------------------------------------------------------------------
// App entry point
// ---------------------------------------------------------------------------

void main() {
  runApp(const FleetIQDriverApp());
}

class FleetIQDriverApp extends StatelessWidget {
  const FleetIQDriverApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'FleetIQ Driver',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFFF59E0B),
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      home: const AuthGateway(),
    );
  }
}

// ---------------------------------------------------------------------------
// Auth gateway – shows Login or Home based on stored token
// ---------------------------------------------------------------------------

class AuthGateway extends StatefulWidget {
  const AuthGateway({super.key});

  @override
  State<AuthGateway> createState() => _AuthGatewayState();
}

class _AuthGatewayState extends State<AuthGateway> {
  bool _loading = true;
  String? _token;

  @override
  void initState() {
    super.initState();
    _checkToken();
  }

  Future<void> _checkToken() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _token = prefs.getString(_tokenKey);
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }
    if (_token == null) {
      return LoginScreen(onLogin: (token) => setState(() => _token = token));
    }
    return TripListScreen(
      token: _token!,
      onLogout: () async {
        final prefs = await SharedPreferences.getInstance();
        await prefs.remove(_tokenKey);
        setState(() => _token = null);
      },
    );
  }
}

// ---------------------------------------------------------------------------
// Login screen
// ---------------------------------------------------------------------------

class LoginScreen extends StatefulWidget {
  final void Function(String token) onLogin;
  const LoginScreen({super.key, required this.onLogin});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _loading = false;
  String? _error;
  bool _obscurePassword = true;

  Future<void> _login() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final resp = await http.post(
        Uri.parse('$_apiBase/auth/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'email': _emailController.text.trim(),
          'password': _passwordController.text,
        }),
      );
      if (resp.statusCode == 200) {
        final data = jsonDecode(resp.body) as Map<String, dynamic>;
        final token = data['access_token'] as String;
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString(_tokenKey, token);
        widget.onLogin(token);
      } else {
        setState(() => _error = 'Invalid credentials. Please try again.');
      }
    } catch (_) {
      setState(() => _error = 'Network error. Check server connection.');
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(32),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  width: 72,
                  height: 72,
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(
                      colors: [Color(0xFFFBBF24), Color(0xFFB45309)],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                    borderRadius: BorderRadius.circular(18),
                    boxShadow: [
                      BoxShadow(
                        color: const Color(0xFFF59E0B).withOpacity(0.4),
                        blurRadius: 20,
                        spreadRadius: 2,
                      )
                    ],
                  ),
                  child: const Icon(Icons.local_shipping, color: Colors.black, size: 40),
                ),
                const SizedBox(height: 24),
                Text(
                  'FleetIQ Driver',
                  style: TextStyle(
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                    color: cs.primary,
                    letterSpacing: -0.5,
                  ),
                ),
                const SizedBox(height: 4),
                const Text(
                  'INTELLIGENCE POWERED LOGISTICS',
                  style: TextStyle(
                    fontSize: 10,
                    color: Colors.white38,
                    letterSpacing: 3,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: 48),
                // Email
                _InputField(
                  controller: _emailController,
                  label: 'Corporate Email',
                  hint: 'driver@company.com',
                  icon: Icons.email_outlined,
                  keyboardType: TextInputType.emailAddress,
                ),
                const SizedBox(height: 16),
                // Password
                _InputField(
                  controller: _passwordController,
                  label: 'Password',
                  hint: '••••••••',
                  icon: Icons.lock_outline,
                  obscureText: _obscurePassword,
                  suffix: IconButton(
                    icon: Icon(
                      _obscurePassword ? Icons.visibility_off : Icons.visibility,
                      color: Colors.white38,
                      size: 20,
                    ),
                    onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
                  ),
                ),
                if (_error != null) ...[
                  const SizedBox(height: 12),
                  Text(_error!, style: const TextStyle(color: Colors.redAccent, fontSize: 13)),
                ],
                const SizedBox(height: 28),
                SizedBox(
                  width: double.infinity,
                  height: 52,
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFFF59E0B),
                      foregroundColor: Colors.black,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                      elevation: 8,
                      shadowColor: const Color(0xFFF59E0B).withOpacity(0.4),
                    ),
                    onPressed: _loading ? null : _login,
                    child: _loading
                        ? const SizedBox(
                            width: 22,
                            height: 22,
                            child: CircularProgressIndicator(strokeWidth: 2, color: Colors.black),
                          )
                        : const Text(
                            'Authorize Access',
                            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                          ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Trip list screen
// ---------------------------------------------------------------------------

class TripListScreen extends StatefulWidget {
  final String token;
  final VoidCallback onLogout;
  const TripListScreen({super.key, required this.token, required this.onLogout});

  @override
  State<TripListScreen> createState() => _TripListScreenState();
}

class _TripListScreenState extends State<TripListScreen> {
  List<Map<String, dynamic>> _shipments = [];
  Map<String, dynamic>? _profile;
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final headers = {
        'Authorization': 'Bearer ${widget.token}',
        'Content-Type': 'application/json',
      };
      final results = await Future.wait([
        http.get(Uri.parse('$_apiBase/shipments'), headers: headers),
        http.get(Uri.parse('$_apiBase/auth/me'), headers: headers),
      ]);

      if (results[0].statusCode == 200) {
        final data = jsonDecode(results[0].body) as List<dynamic>;
        _shipments = data.cast<Map<String, dynamic>>();
      }
      if (results[1].statusCode == 200) {
        _profile = jsonDecode(results[1].body) as Map<String, dynamic>;
      }
      if (results[0].statusCode == 401 || results[1].statusCode == 401) {
        widget.onLogout();
        return;
      }
    } catch (_) {
      _error = 'Unable to load data. Check connection.';
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: const Color(0xFF111111),
        elevation: 0,
        title: Row(
          children: [
            Container(
              width: 32,
              height: 32,
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [Color(0xFFFBBF24), Color(0xFFB45309)],
                ),
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Icon(Icons.local_shipping, color: Colors.black, size: 18),
            ),
            const SizedBox(width: 8),
            const Text('FleetIQ Driver', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
          ],
        ),
        actions: [
          if (_profile != null)
            Padding(
              padding: const EdgeInsets.only(right: 8),
              child: Center(
                child: Text(
                  _profile!['email'] as String? ?? '',
                  style: const TextStyle(color: Colors.white38, fontSize: 11),
                ),
              ),
            ),
          IconButton(
            icon: const Icon(Icons.logout, color: Colors.white38),
            tooltip: 'Sign out',
            onPressed: widget.onLogout,
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: _loadData,
        color: const Color(0xFFF59E0B),
        child: _loading
            ? const Center(child: CircularProgressIndicator(color: Color(0xFFF59E0B)))
            : _error != null
                ? Center(child: _ErrorCard(message: _error!))
                : _shipments.isEmpty
                    ? Center(
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const Icon(Icons.inbox_outlined, size: 64, color: Colors.white12),
                            const SizedBox(height: 16),
                            const Text(
                              'No trips assigned',
                              style: TextStyle(color: Colors.white38, fontSize: 16),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              'Pull to refresh',
                              style: TextStyle(color: Colors.white24, fontSize: 12),
                            ),
                          ],
                        ),
                      )
                    : ListView.separated(
                        padding: const EdgeInsets.all(16),
                        itemCount: _shipments.length,
                        separatorBuilder: (_, __) => const SizedBox(height: 12),
                        itemBuilder: (context, index) => _ShipmentCard(shipment: _shipments[index]),
                      ),
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Widgets
// ---------------------------------------------------------------------------

class _InputField extends StatelessWidget {
  final TextEditingController controller;
  final String label;
  final String hint;
  final IconData icon;
  final bool obscureText;
  final TextInputType keyboardType;
  final Widget? suffix;

  const _InputField({
    required this.controller,
    required this.label,
    required this.hint,
    required this.icon,
    this.obscureText = false,
    this.keyboardType = TextInputType.text,
    this.suffix,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label.toUpperCase(),
          style: const TextStyle(
            fontSize: 10,
            fontWeight: FontWeight.w700,
            color: Color(0xFFF59E0B),
            letterSpacing: 1.5,
          ),
        ),
        const SizedBox(height: 6),
        TextField(
          controller: controller,
          obscureText: obscureText,
          keyboardType: keyboardType,
          style: const TextStyle(color: Colors.white),
          decoration: InputDecoration(
            hintText: hint,
            hintStyle: const TextStyle(color: Colors.white24),
            prefixIcon: Icon(icon, color: Colors.white38, size: 20),
            suffixIcon: suffix,
            filled: true,
            fillColor: Colors.white.withOpacity(0.05),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(14),
              borderSide: BorderSide(color: Colors.white.withOpacity(0.1)),
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(14),
              borderSide: BorderSide(color: Colors.white.withOpacity(0.1)),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(14),
              borderSide: const BorderSide(color: Color(0xFFF59E0B), width: 1.5),
            ),
          ),
        ),
      ],
    );
  }
}

class _ShipmentCard extends StatelessWidget {
  final Map<String, dynamic> shipment;
  const _ShipmentCard({required this.shipment});

  Color _statusColor(String status) {
    switch (status) {
      case 'delivered':
        return const Color(0xFF10B981);
      case 'delayed':
      case 'exception':
        return const Color(0xFFEF4444);
      case 'in_transit':
      case 'en_route_to_pickup':
        return const Color(0xFFF59E0B);
      default:
        return const Color(0xFF6B7280);
    }
  }

  @override
  Widget build(BuildContext context) {
    final status = shipment['status'] as String? ?? 'unknown';
    final statusColor = _statusColor(status);
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF111111),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white.withOpacity(0.08)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                shipment['shipment_number'] as String? ?? '-',
                style: const TextStyle(
                  color: Color(0xFFF59E0B),
                  fontFamily: 'monospace',
                  fontWeight: FontWeight.bold,
                  fontSize: 13,
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: statusColor.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Text(
                  status.toUpperCase().replaceAll('_', ' '),
                  style: TextStyle(
                    color: statusColor,
                    fontSize: 9,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 10),
          Text(
            shipment['customer_name'] as String? ?? '',
            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w600, fontSize: 14),
          ),
          const SizedBox(height: 8),
          _RouteRow(
            pickup: shipment['pickup_address'] as String? ?? '-',
            delivery: shipment['delivery_address'] as String? ?? '-',
          ),
        ],
      ),
    );
  }
}

class _RouteRow extends StatelessWidget {
  final String pickup;
  final String delivery;
  const _RouteRow({required this.pickup, required this.delivery});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Column(
          children: [
            const Icon(Icons.radio_button_checked, color: Colors.white38, size: 12),
            Container(width: 1, height: 20, color: Colors.white12),
            const Icon(Icons.location_on, color: Color(0xFFF59E0B), size: 14),
          ],
        ),
        const SizedBox(width: 10),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(pickup, style: const TextStyle(color: Colors.white38, fontSize: 11), maxLines: 1, overflow: TextOverflow.ellipsis),
              const SizedBox(height: 10),
              Text(delivery, style: const TextStyle(color: Colors.white70, fontSize: 11, fontWeight: FontWeight.w600), maxLines: 1, overflow: TextOverflow.ellipsis),
            ],
          ),
        ),
      ],
    );
  }
}

class _ErrorCard extends StatelessWidget {
  final String message;
  const _ErrorCard({required this.message});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(32),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.cloud_off, size: 48, color: Colors.redAccent),
          const SizedBox(height: 12),
          Text(message, style: const TextStyle(color: Colors.white38), textAlign: TextAlign.center),
        ],
      ),
    );
  }
}

