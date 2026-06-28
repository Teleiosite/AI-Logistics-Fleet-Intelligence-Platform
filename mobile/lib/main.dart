import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

const String _apiBase =
    String.fromEnvironment('API_BASE_URL', defaultValue: 'http://10.0.2.2:8000/api/v1');
const String _tokenKey = 'fleetiq_token';

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
    return HomeScreen(
      token: _token!,
      onLogout: () async {
        final prefs = await SharedPreferences.getInstance();
        await prefs.remove(_tokenKey);
        setState(() => _token = null);
      },
    );
  }
}

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

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

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
      if (mounted) {
        setState(() => _loading = false);
      }
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
                      ),
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
                _InputField(
                  controller: _emailController,
                  label: 'Corporate Email',
                  hint: 'driver@company.com',
                  icon: Icons.email_outlined,
                  keyboardType: TextInputType.emailAddress,
                ),
                const SizedBox(height: 16),
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

class HomeScreen extends StatefulWidget {
  final String token;
  final VoidCallback onLogout;

  const HomeScreen({super.key, required this.token, required this.onLogout});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _currentIndex = 0;
  Map<String, dynamic>? _profile;

  static const _titles = [
    'Shipments',
    'Log Fuel Issuance',
    'Report Delivery Variance',
    'My Performance',
  ];

  @override
  void initState() {
    super.initState();
    _loadProfile();
  }

  Future<void> _loadProfile() async {
    try {
      final response = await http.get(
        Uri.parse('$_apiBase/auth/me'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'Content-Type': 'application/json',
        },
      );
      if (response.statusCode == 200) {
        if (!mounted) {
          return;
        }
        setState(() => _profile = jsonDecode(response.body) as Map<String, dynamic>);
      } else if (response.statusCode == 401) {
        widget.onLogout();
      }
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
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
            Expanded(
              child: Text(
                _titles[_currentIndex],
                style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                overflow: TextOverflow.ellipsis,
              ),
            ),
          ],
        ),
        actions: [
          if ((_profile?['email'] as String?)?.isNotEmpty ?? false)
            Padding(
              padding: const EdgeInsets.only(right: 8),
              child: Center(
                child: Text(
                  _profile!['email'] as String,
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
      body: IndexedStack(
        index: _currentIndex,
        children: [
          ShipmentsScreen(token: widget.token, onLogout: widget.onLogout),
          FuelLogScreen(token: widget.token),
          DVRCreateScreen(token: widget.token),
          DriverPerformanceScreen(token: widget.token),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) => setState(() => _currentIndex = index),
        backgroundColor: const Color(0xFF111111),
        selectedItemColor: const Color(0xFFF59E0B),
        unselectedItemColor: Colors.white38,
        type: BottomNavigationBarType.fixed,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.local_shipping),
            label: 'Shipments',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.local_gas_station),
            label: 'Fuel Log',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.warning_amber),
            label: 'Report Variance',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.bar_chart),
            label: 'My Performance',
          ),
        ],
      ),
    );
  }
}

class ShipmentsScreen extends StatefulWidget {
  final String token;
  final VoidCallback onLogout;

  const ShipmentsScreen({super.key, required this.token, required this.onLogout});

  @override
  State<ShipmentsScreen> createState() => _ShipmentsScreenState();
}

class _ShipmentsScreenState extends State<ShipmentsScreen> {
  List<Map<String, dynamic>> _shipments = [];
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadShipments();
  }

  Future<void> _loadShipments() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final response = await http.get(
        Uri.parse('$_apiBase/shipments'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'Content-Type': 'application/json',
        },
      );
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as List<dynamic>;
        if (!mounted) {
          return;
        }
        setState(() {
          _shipments = data.cast<Map<String, dynamic>>();
        });
      } else if (response.statusCode == 401) {
        widget.onLogout();
        return;
      } else {
        _error = 'Unable to load shipments.';
      }
    } catch (_) {
      _error = 'Unable to load data. Check connection.';
    } finally {
      if (mounted) {
        setState(() => _loading = false);
      }
    }
  }

  Future<void> _showShipmentDetails(Map<String, dynamic> shipment) async {
    await showModalBottomSheet<void>(
      context: context,
      backgroundColor: const Color(0xFF111111),
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (sheetContext) {
        final shipmentId = shipment['id']?.toString() ?? '';
        final shipmentNumber = shipment['shipment_number'] as String? ?? '-';
        final status = shipment['status'] as String? ?? 'unknown';
        final pickup = shipment['pickup_address'] as String? ?? '-';
        final delivery = shipment['delivery_address'] as String? ?? '-';

        return SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Center(
                  child: Container(
                    width: 42,
                    height: 4,
                    decoration: BoxDecoration(
                      color: Colors.white24,
                      borderRadius: BorderRadius.circular(999),
                    ),
                  ),
                ),
                const SizedBox(height: 20),
                Text(
                  shipmentNumber,
                  style: const TextStyle(
                    color: Color(0xFFF59E0B),
                    fontWeight: FontWeight.bold,
                    fontSize: 18,
                  ),
                ),
                const SizedBox(height: 8),
                _DetailRow(label: 'Status', value: _formatLabel(status)),
                _DetailRow(label: 'Pickup', value: pickup),
                _DetailRow(label: 'Delivery', value: delivery),
                const SizedBox(height: 20),
                Row(
                  children: [
                    Expanded(
                      child: OutlinedButton.icon(
                        onPressed: () async {
                          Navigator.of(sheetContext).pop();
                          final updated = await showDialog<bool>(
                            context: context,
                            builder: (_) => StatusUpdateDialog(
                              token: widget.token,
                              shipmentId: shipmentId,
                              initialStatus: status,
                            ),
                          );
                          if (updated == true) {
                            _showMessage('Shipment status updated successfully!');
                            _loadShipments();
                          }
                        },
                        icon: const Icon(Icons.sync_alt),
                        label: const Text('Update Status'),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: FilledButton.icon(
                        onPressed: shipmentId.isEmpty
                            ? null
                            : () async {
                                Navigator.of(sheetContext).pop();
                                await Navigator.of(context).push(
                                  MaterialPageRoute<void>(
                                    builder: (_) => PodCaptureScreen(
                                      shipmentId: shipmentId,
                                      token: widget.token,
                                    ),
                                  ),
                                );
                              },
                        icon: const Icon(Icons.document_scanner_outlined),
                        label: const Text('Capture POD'),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  void _showMessage(String message) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
  }

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      onRefresh: _loadShipments,
      color: const Color(0xFFF59E0B),
      child: _loading
          ? const Center(child: CircularProgressIndicator(color: Color(0xFFF59E0B)))
          : _error != null
              ? Center(child: _ErrorCard(message: _error!))
              : _shipments.isEmpty
                  ? ListView(
                      children: const [
                        SizedBox(height: 140),
                        Icon(Icons.inbox_outlined, size: 64, color: Colors.white12),
                        SizedBox(height: 16),
                        Center(
                          child: Text(
                            'No trips assigned',
                            style: TextStyle(color: Colors.white38, fontSize: 16),
                          ),
                        ),
                        SizedBox(height: 8),
                        Center(
                          child: Text(
                            'Pull to refresh',
                            style: TextStyle(color: Colors.white24, fontSize: 12),
                          ),
                        ),
                      ],
                    )
                  : ListView.separated(
                      padding: const EdgeInsets.all(16),
                      itemCount: _shipments.length,
                      separatorBuilder: (_, __) => const SizedBox(height: 12),
                      itemBuilder: (context, index) => _ShipmentCard(
                        shipment: _shipments[index],
                        onTap: () => _showShipmentDetails(_shipments[index]),
                      ),
                    ),
    );
  }
}

class PodCaptureScreen extends StatefulWidget {
  final String shipmentId;
  final String token;

  const PodCaptureScreen({
    super.key,
    required this.shipmentId,
    required this.token,
  });

  @override
  State<PodCaptureScreen> createState() => _PodCaptureScreenState();
}

class _PodCaptureScreenState extends State<PodCaptureScreen> {
  final _formKey = GlobalKey<FormState>();
  final _podController = TextEditingController();
  final _signatureController = TextEditingController();
  final _notesController = TextEditingController();
  bool _submitting = false;

  @override
  void dispose() {
    _podController.dispose();
    _signatureController.dispose();
    _notesController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    final messenger = ScaffoldMessenger.of(context);
    setState(() => _submitting = true);
    try {
      final response = await http.post(
        Uri.parse('$_apiBase/shipments/${widget.shipmentId}/proof-of-delivery'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'proof_of_delivery_url': _podController.text.trim(),
          'delivery_signature_url': _signatureController.text.trim(),
        }),
      );

      if (response.statusCode >= 200 && response.statusCode < 300) {
        if (!mounted) {
          return;
        }
        messenger.showSnackBar(const SnackBar(content: Text('POD submitted successfully!')));
        Navigator.of(context).pop();
      } else {
        messenger.showSnackBar(
          SnackBar(content: Text('Failed to submit POD (${response.statusCode}).')),
        );
      }
    } catch (_) {
      messenger.showSnackBar(
        const SnackBar(content: Text('Unable to submit POD. Please try again.')),
      );
    } finally {
      if (mounted) {
        setState(() => _submitting = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: const Text('Proof of Delivery'),
        backgroundColor: const Color(0xFF111111),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Form(
            key: _formKey,
            child: Column(
              children: [
                _FormTextField(
                  controller: _podController,
                  label: 'Photo URL or Description',
                  hint: 'Paste a URL or describe the proof captured',
                  icon: Icons.photo_camera_back_outlined,
                  validator: _requiredValidator,
                ),
                const SizedBox(height: 16),
                _FormTextField(
                  controller: _signatureController,
                  label: 'Signature URL',
                  hint: 'Optional signature link',
                  icon: Icons.draw_outlined,
                ),
                const SizedBox(height: 16),
                _FormTextField(
                  controller: _notesController,
                  label: 'Notes',
                  hint: 'Optional delivery notes',
                  icon: Icons.sticky_note_2_outlined,
                  maxLines: 4,
                ),
                const SizedBox(height: 24),
                SizedBox(
                  width: double.infinity,
                  child: FilledButton(
                    onPressed: _submitting ? null : _submit,
                    child: _submitting
                        ? const SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          )
                        : const Text('Submit POD'),
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

class FuelLogScreen extends StatefulWidget {
  final String token;

  const FuelLogScreen({super.key, required this.token});

  @override
  State<FuelLogScreen> createState() => _FuelLogScreenState();
}

class _FuelLogScreenState extends State<FuelLogScreen> {
  final _formKey = GlobalKey<FormState>();
  final _vehicleIdController = TextEditingController();
  final _quantityController = TextEditingController();
  final _priceController = TextEditingController();
  final _odometerController = TextEditingController();
  final _stationController = TextEditingController();
  bool _submitting = false;

  @override
  void dispose() {
    _vehicleIdController.dispose();
    _quantityController.dispose();
    _priceController.dispose();
    _odometerController.dispose();
    _stationController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    final messenger = ScaffoldMessenger.of(context);
    setState(() => _submitting = true);
    try {
      final response = await http.post(
        Uri.parse('$_apiBase/fuel'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'vehicle_id': _vehicleIdController.text.trim(),
          'quantity_liters': num.tryParse(_quantityController.text.trim()),
          'price_per_liter': num.tryParse(_priceController.text.trim()),
          'odometer_reading_km': _odometerController.text.trim().isEmpty
              ? null
              : num.tryParse(_odometerController.text.trim()),
          'station_name': _stationController.text.trim().isEmpty
              ? null
              : _stationController.text.trim(),
        }),
      );

      if (response.statusCode >= 200 && response.statusCode < 300) {
        _formKey.currentState!.reset();
        _vehicleIdController.clear();
        _quantityController.clear();
        _priceController.clear();
        _odometerController.clear();
        _stationController.clear();
        messenger.showSnackBar(
          const SnackBar(content: Text('Fuel log submitted successfully!')),
        );
      } else {
        messenger.showSnackBar(
          SnackBar(content: Text('Failed to submit fuel log (${response.statusCode}).')),
        );
      }
    } catch (_) {
      messenger.showSnackBar(
        const SnackBar(content: Text('Unable to submit fuel log. Please try again.')),
      );
    } finally {
      if (mounted) {
        setState(() => _submitting = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              _FormCard(
                icon: Icons.local_gas_station,
                title: 'Log Fuel Issuance',
                child: Column(
                  children: [
                    _FormTextField(
                      controller: _vehicleIdController,
                      label: 'Vehicle ID',
                      hint: 'Enter assigned vehicle ID',
                      icon: Icons.directions_car_outlined,
                      validator: _requiredValidator,
                    ),
                    const SizedBox(height: 16),
                    _FormTextField(
                      controller: _quantityController,
                      label: 'Quantity (Liters)',
                      hint: '0.0',
                      icon: Icons.water_drop_outlined,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      validator: _requiredNumberValidator,
                    ),
                    const SizedBox(height: 16),
                    _FormTextField(
                      controller: _priceController,
                      label: 'Price per Liter',
                      hint: '0.00',
                      icon: Icons.payments_outlined,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      validator: _requiredNumberValidator,
                    ),
                    const SizedBox(height: 16),
                    _FormTextField(
                      controller: _odometerController,
                      label: 'Odometer Reading (km)',
                      hint: 'Optional odometer reading',
                      icon: Icons.speed_outlined,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      validator: _optionalNumberValidator,
                    ),
                    const SizedBox(height: 16),
                    _FormTextField(
                      controller: _stationController,
                      label: 'Station Name',
                      hint: 'Optional filling station',
                      icon: Icons.store_mall_directory_outlined,
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: FilledButton(
                  onPressed: _submitting ? null : _submit,
                  child: _submitting
                      ? const SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Text('Submit Fuel Log'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class DVRCreateScreen extends StatefulWidget {
  final String token;

  const DVRCreateScreen({super.key, required this.token});

  @override
  State<DVRCreateScreen> createState() => _DVRCreateScreenState();
}

class _DVRCreateScreenState extends State<DVRCreateScreen> {
  final _formKey = GlobalKey<FormState>();
  final _shipmentIdController = TextEditingController();
  final _dvrNumberController = TextEditingController(
    text: 'DVR-${DateTime.now().millisecondsSinceEpoch}',
  );
  final _descriptionController = TextEditingController();
  final _financialImpactController = TextEditingController();
  bool _submitting = false;
  String _varianceType = 'short_delivery';
  String _severity = 'minor';

  static const Map<String, String> _varianceOptions = {
    'short_delivery': 'Short Delivery',
    'damage': 'Physical Damage',
    'late_delivery': 'Late Delivery',
    'wrong_items': 'Wrong Items',
    'refused_delivery': 'Refused Delivery',
    'route_deviation': 'Route Deviation',
  };

  static const List<String> _severityOptions = ['minor', 'moderate', 'major', 'critical'];

  @override
  void dispose() {
    _shipmentIdController.dispose();
    _dvrNumberController.dispose();
    _descriptionController.dispose();
    _financialImpactController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    final messenger = ScaffoldMessenger.of(context);
    setState(() => _submitting = true);
    try {
      final response = await http.post(
        Uri.parse('$_apiBase/dvr'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'shipment_id': _shipmentIdController.text.trim(),
          'dvr_number': _dvrNumberController.text.trim(),
          'variance_type': _varianceType,
          'severity': _severity,
          'description': _descriptionController.text.trim(),
          'financial_impact': _financialImpactController.text.trim().isEmpty
              ? null
              : num.tryParse(_financialImpactController.text.trim()),
        }),
      );

      if (response.statusCode >= 200 && response.statusCode < 300) {
        messenger.showSnackBar(
          const SnackBar(content: Text('Delivery variance reported successfully!')),
        );
      } else {
        messenger.showSnackBar(
          SnackBar(content: Text('Failed to create DVR (${response.statusCode}).')),
        );
      }
    } catch (_) {
      messenger.showSnackBar(
        const SnackBar(content: Text('Unable to create DVR. Please try again.')),
      );
    } finally {
      if (mounted) {
        setState(() => _submitting = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              _FormCard(
                icon: Icons.warning_amber,
                title: 'Report Delivery Variance',
                child: Column(
                  children: [
                    _FormTextField(
                      controller: _shipmentIdController,
                      label: 'Shipment ID',
                      hint: 'Enter shipment ID',
                      icon: Icons.qr_code_2_outlined,
                      validator: _requiredValidator,
                    ),
                    const SizedBox(height: 16),
                    _FormTextField(
                      controller: _dvrNumberController,
                      label: 'DVR Number',
                      hint: 'DVR Number',
                      icon: Icons.confirmation_number_outlined,
                      validator: _requiredValidator,
                    ),
                    const SizedBox(height: 16),
                    _FormDropdown<String>(
                      value: _varianceType,
                      label: 'Variance Type',
                      icon: Icons.report_problem_outlined,
                      items: _varianceOptions.entries
                          .map(
                            (entry) => DropdownMenuItem<String>(
                              value: entry.key,
                              child: Text(entry.value),
                            ),
                          )
                          .toList(),
                      onChanged: (value) {
                        if (value != null) {
                          setState(() => _varianceType = value);
                        }
                      },
                    ),
                    const SizedBox(height: 16),
                    _FormDropdown<String>(
                      value: _severity,
                      label: 'Severity',
                      icon: Icons.priority_high_outlined,
                      items: _severityOptions
                          .map(
                            (item) => DropdownMenuItem<String>(
                              value: item,
                              child: Text(_formatLabel(item)),
                            ),
                          )
                          .toList(),
                      onChanged: (value) {
                        if (value != null) {
                          setState(() => _severity = value);
                        }
                      },
                    ),
                    const SizedBox(height: 16),
                    _FormTextField(
                      controller: _descriptionController,
                      label: 'Description',
                      hint: 'Describe what happened',
                      icon: Icons.notes_outlined,
                      maxLines: 3,
                      validator: _requiredValidator,
                    ),
                    const SizedBox(height: 16),
                    _FormTextField(
                      controller: _financialImpactController,
                      label: 'Financial Impact',
                      hint: 'Optional amount',
                      icon: Icons.attach_money_outlined,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      validator: _optionalNumberValidator,
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: FilledButton(
                  onPressed: _submitting ? null : _submit,
                  child: _submitting
                      ? const SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Text('Submit Variance Report'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class DriverPerformanceScreen extends StatefulWidget {
  final String token;

  const DriverPerformanceScreen({super.key, required this.token});

  @override
  State<DriverPerformanceScreen> createState() => _DriverPerformanceScreenState();
}

class _DriverPerformanceScreenState extends State<DriverPerformanceScreen> {
  Map<String, dynamic>? _profile;
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadProfile();
  }

  Future<void> _loadProfile() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final response = await http.get(
        Uri.parse('$_apiBase/auth/me'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'Content-Type': 'application/json',
        },
      );
      if (response.statusCode == 200) {
        _profile = jsonDecode(response.body) as Map<String, dynamic>;
      } else {
        _error = 'Unable to load your profile.';
      }
    } catch (_) {
      _error = 'Unable to load your performance details.';
    } finally {
      if (mounted) {
        setState(() => _loading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Center(child: CircularProgressIndicator(color: Color(0xFFF59E0B)));
    }

    if (_error != null) {
      return Center(child: _ErrorCard(message: _error!));
    }

    final name = (_profile?['name'] as String?)?.trim();
    final email = _profile?['email'] as String? ?? '-';
    final role = _profile?['role'] as String? ?? 'driver';

    return RefreshIndicator(
      onRefresh: _loadProfile,
      color: const Color(0xFFF59E0B),
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            color: const Color(0xFF111111),
            surfaceTintColor: const Color(0xFFF59E0B),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    name == null || name.isEmpty ? 'FleetIQ Driver' : name,
                    style: const TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    email,
                    style: const TextStyle(color: Colors.white70),
                  ),
                  const SizedBox(height: 14),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    decoration: BoxDecoration(
                      color: const Color(0xFFF59E0B).withOpacity(0.18),
                      borderRadius: BorderRadius.circular(999),
                    ),
                    child: Text(
                      _formatLabel(role),
                      style: const TextStyle(
                        color: Color(0xFFFBBF24),
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          const _PerformanceStatCard(
            title: 'On-Time Rate',
            value: 'N/A',
            icon: Icons.schedule,
          ),
          const SizedBox(height: 12),
          const _PerformanceStatCard(
            title: 'Fuel Efficiency',
            value: 'N/A',
            icon: Icons.local_gas_station,
          ),
          const SizedBox(height: 12),
          const _PerformanceStatCard(
            title: 'DVR Reports',
            value: 'N/A',
            icon: Icons.warning_amber,
          ),
          const SizedBox(height: 16),
          Card(
            color: const Color(0xFF111111),
            surfaceTintColor: const Color(0xFFF59E0B),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
            child: const Padding(
              padding: EdgeInsets.all(18),
              child: Text(
                'Detailed driver analytics coming soon',
                style: TextStyle(color: Colors.white70, fontSize: 15),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class StatusUpdateDialog extends StatefulWidget {
  final String token;
  final String shipmentId;
  final String initialStatus;

  const StatusUpdateDialog({
    super.key,
    required this.token,
    required this.shipmentId,
    required this.initialStatus,
  });

  @override
  State<StatusUpdateDialog> createState() => _StatusUpdateDialogState();
}

class _StatusUpdateDialogState extends State<StatusUpdateDialog> {
  static const List<String> _statusOptions = [
    'assigned',
    'en_route_to_pickup',
    'picked_up',
    'in_transit',
    'delivered',
    'delayed',
    'exception',
  ];

  late String _selectedStatus;
  bool _submitting = false;

  @override
  void initState() {
    super.initState();
    _selectedStatus = _statusOptions.contains(widget.initialStatus)
        ? widget.initialStatus
        : _statusOptions.first;
  }

  Future<void> _submit() async {
    final messenger = ScaffoldMessenger.of(context);
    setState(() => _submitting = true);
    try {
      final response = await http.patch(
        Uri.parse('$_apiBase/shipments/${widget.shipmentId}/status'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'Content-Type': 'application/json',
        },
        body: jsonEncode({'status': _selectedStatus}),
      );

      if (response.statusCode >= 200 && response.statusCode < 300) {
        if (!mounted) {
          return;
        }
        Navigator.of(context).pop(true);
      } else {
        messenger.showSnackBar(
          SnackBar(content: Text('Failed to update status (${response.statusCode}).')),
        );
      }
    } catch (_) {
      messenger.showSnackBar(
        const SnackBar(content: Text('Unable to update shipment status.')),
      );
    } finally {
      if (mounted) {
        setState(() => _submitting = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      backgroundColor: const Color(0xFF111111),
      title: const Text('Update Status'),
      content: _FormDropdown<String>(
        value: _selectedStatus,
        label: 'Shipment Status',
        icon: Icons.local_shipping_outlined,
        items: _statusOptions
            .map(
              (item) => DropdownMenuItem<String>(
                value: item,
                child: Text(_formatLabel(item)),
              ),
            )
            .toList(),
        onChanged: (value) {
          if (value != null) {
            setState(() => _selectedStatus = value);
          }
        },
      ),
      actions: [
        TextButton(
          onPressed: _submitting ? null : () => Navigator.of(context).pop(false),
          child: const Text('Cancel'),
        ),
        FilledButton(
          onPressed: _submitting ? null : _submit,
          child: _submitting
              ? const SizedBox(
                  width: 18,
                  height: 18,
                  child: CircularProgressIndicator(strokeWidth: 2),
                )
              : const Text('Save'),
        ),
      ],
    );
  }
}

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
          decoration: _buildInputDecoration(
            label: label,
            hint: hint,
            icon: icon,
            suffixIcon: suffix,
          ),
        ),
      ],
    );
  }
}

class _FormTextField extends StatelessWidget {
  final TextEditingController controller;
  final String label;
  final String hint;
  final IconData icon;
  final int maxLines;
  final TextInputType keyboardType;
  final String? Function(String?)? validator;

  const _FormTextField({
    required this.controller,
    required this.label,
    required this.hint,
    required this.icon,
    this.maxLines = 1,
    this.keyboardType = TextInputType.text,
    this.validator,
  });

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: controller,
      maxLines: maxLines,
      keyboardType: keyboardType,
      validator: validator,
      style: const TextStyle(color: Colors.white),
      decoration: _buildInputDecoration(label: label, hint: hint, icon: icon),
    );
  }
}

class _FormDropdown<T> extends StatelessWidget {
  final T value;
  final String label;
  final IconData icon;
  final List<DropdownMenuItem<T>> items;
  final ValueChanged<T?> onChanged;

  const _FormDropdown({
    required this.value,
    required this.label,
    required this.icon,
    required this.items,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField<T>(
      value: value,
      items: items,
      onChanged: onChanged,
      decoration: _buildInputDecoration(label: label, icon: icon),
      dropdownColor: const Color(0xFF1A1A1A),
      style: const TextStyle(color: Colors.white),
      iconEnabledColor: const Color(0xFFF59E0B),
    );
  }
}

class _FormCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final Widget child;

  const _FormCard({
    required this.icon,
    required this.title,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      color: const Color(0xFF111111),
      surfaceTintColor: const Color(0xFFF59E0B),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: const Color(0xFFF59E0B)),
                const SizedBox(width: 10),
                Text(
                  title,
                  style: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                    fontSize: 18,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 18),
            child,
          ],
        ),
      ),
    );
  }
}

class _ShipmentCard extends StatelessWidget {
  final Map<String, dynamic> shipment;
  final VoidCallback onTap;

  const _ShipmentCard({required this.shipment, required this.onTap});

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
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Container(
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
                  Row(
                    children: [
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
                      const SizedBox(width: 8),
                      const Icon(Icons.chevron_right, color: Colors.white24),
                    ],
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
        ),
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
              Text(
                pickup,
                style: const TextStyle(color: Colors.white38, fontSize: 11),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 10),
              Text(
                delivery,
                style: const TextStyle(
                  color: Colors.white70,
                  fontSize: 11,
                  fontWeight: FontWeight.w600,
                ),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        ),
      ],
    );
  }
}

class _PerformanceStatCard extends StatelessWidget {
  final String title;
  final String value;
  final IconData icon;

  const _PerformanceStatCard({
    required this.title,
    required this.value,
    required this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      color: const Color(0xFF111111),
      surfaceTintColor: const Color(0xFFF59E0B),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18)),
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Row(
          children: [
            Container(
              width: 44,
              height: 44,
              decoration: BoxDecoration(
                color: const Color(0xFFF59E0B).withOpacity(0.18),
                borderRadius: BorderRadius.circular(14),
              ),
              child: Icon(icon, color: const Color(0xFFFBBF24)),
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: const TextStyle(color: Colors.white70),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    value,
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _DetailRow extends StatelessWidget {
  final String label;
  final String value;

  const _DetailRow({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label.toUpperCase(),
            style: const TextStyle(
              color: Color(0xFFF59E0B),
              fontSize: 10,
              fontWeight: FontWeight.w700,
              letterSpacing: 1.2,
            ),
          ),
          const SizedBox(height: 4),
          Text(value, style: const TextStyle(color: Colors.white70)),
        ],
      ),
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

InputDecoration _buildInputDecoration({
  required String label,
  String? hint,
  required IconData icon,
  Widget? suffixIcon,
}) {
  return InputDecoration(
    labelText: label,
    hintText: hint,
    labelStyle: const TextStyle(color: Color(0xFFF59E0B)),
    hintStyle: const TextStyle(color: Colors.white24),
    prefixIcon: Icon(icon, color: Colors.white38, size: 20),
    suffixIcon: suffixIcon,
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
    errorBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(14),
      borderSide: const BorderSide(color: Colors.redAccent),
    ),
    focusedErrorBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(14),
      borderSide: const BorderSide(color: Colors.redAccent, width: 1.5),
    ),
  );
}

String? _requiredValidator(String? value) {
  if (value == null || value.trim().isEmpty) {
    return 'This field is required.';
  }
  return null;
}

String? _requiredNumberValidator(String? value) {
  if (_requiredValidator(value) != null) {
    return _requiredValidator(value);
  }
  if (num.tryParse(value!.trim()) == null) {
    return 'Enter a valid number.';
  }
  return null;
}

String? _optionalNumberValidator(String? value) {
  if (value == null || value.trim().isEmpty) {
    return null;
  }
  if (num.tryParse(value.trim()) == null) {
    return 'Enter a valid number.';
  }
  return null;
}

String _formatLabel(String value) {
  return value
      .split('_')
      .where((part) => part.isNotEmpty)
      .map((part) => '${part[0].toUpperCase()}${part.substring(1)}')
      .join(' ');
}
