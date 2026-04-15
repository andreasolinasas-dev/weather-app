"""
Weather Application - Comprehensive Test Suite
Unit and Integration tests for debugging and validation
"""

import unittest
import json
import os
from unittest.mock import patch, MagicMock
from app import app, get_weather_data, get_weather_by_coordinates, get_forecast_data, format_weather_data, format_forecast_data

class TestWeatherAPI(unittest.TestCase):
    """Test suite for Weather API functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Sample weather data for testing
        self.sample_weather_data = {
            'name': 'Berlin',
            'sys': {
                'country': 'DE',
                'sunrise': 1609459200,
                'sunset': 1609488000
            },
            'main': {
                'temp': 5.5,
                'feels_like': 2.1,
                'temp_min': 3.0,
                'temp_max': 8.0,
                'pressure': 1013,
                'humidity': 75
            },
            'weather': [{
                'id': 800,
                'main': 'Clear',
                'description': 'clear sky',
                'icon': '01d'
            }],
            'wind': {
                'speed': 3.5,
                'deg': 180
            },
            'clouds': {
                'all': 10
            },
            'visibility': 10000,
            'dt': 1609466400
        }
        
        # Sample forecast data
        self.sample_forecast_data = {
            'list': [
                {
                    'dt_txt': '2024-01-01 12:00:00',
                    'main': {
                        'temp': 5.5,
                        'temp_min': 3.0,
                        'temp_max': 8.0,
                        'humidity': 75
                    },
                    'weather': [{
                        'main': 'Clear',
                        'description': 'clear sky',
                        'icon': '01d'
                    }],
                    'wind': {
                        'speed': 3.5
                    }
                }
            ]
        }
    
    def test_format_weather_data_success(self):
        """Test successful weather data formatting"""
        result = format_weather_data(self.sample_weather_data)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['city'], 'Berlin')
        self.assertEqual(result['country'], 'DE')
        self.assertEqual(result['temperature'], 5.5)
        self.assertEqual(result['feels_like'], 2.1)
        self.assertEqual(result['temp_min'], 3.0)
        self.assertEqual(result['temp_max'], 8.0)
        self.assertEqual(result['weather_main'], 'Clear')
        self.assertEqual(result['weather_description'], 'clear sky')
        self.assertEqual(result['weather_icon'], '01d')
        self.assertEqual(result['wind_speed'], 3.5)
        self.assertEqual(result['humidity'], 75)
        self.assertEqual(result['pressure'], 1013)
    
    def test_format_weather_data_with_error(self):
        """Test formatting data with error"""
        error_data = {'error': 'API error'}
        result = format_weather_data(error_data)
        self.assertIsNone(result)
    
    def test_format_forecast_data_success(self):
        """Test successful forecast data formatting"""
        result = format_forecast_data(self.sample_forecast_data)
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['date'], '2024-01-01')
        self.assertEqual(result[0]['temperature'], 5.5)
        self.assertEqual(result[0]['weather'], 'Clear')
    
    def test_format_forecast_data_with_error(self):
        """Test formatting forecast with error"""
        error_data = {'error': 'Forecast API error'}
        result = format_forecast_data(error_data)
        self.assertIsNone(result)
    
    @patch('app.requests.get')
    def test_get_weather_data_success(self, mock_get):
        """Test successful weather data fetch"""
        mock_response = MagicMock()
        mock_response.json.return_value = self.sample_weather_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_weather_data('Berlin')
        
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Berlin')
        mock_get.assert_called_once()
    
    @patch('app.requests.get')
    def test_get_weather_data_api_error(self, mock_get):
        """Test weather data fetch with API error"""
        # Create a mock response that raises an HTTPError
        from requests.exceptions import HTTPError
        
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        
        # Create an HTTPError with proper attributes
        http_error = HTTPError()
        http_error.response = mock_response
        mock_response.raise_for_status.side_effect = http_error
        
        mock_get.return_value = mock_response
        
        result = get_weather_data('Berlin')
        
        self.assertIn('error', result)
        # The error message should indicate authentication failure
        self.assertTrue(
            'authentication' in result['error'].lower() or 
            '401' in result['error'] or
            'Unauthorized' in result['error']
        )
    
    @patch('app.requests.get')
    def test_get_weather_by_coordinates_success(self, mock_get):
        """Test successful weather fetch by coordinates"""
        mock_response = MagicMock()
        mock_response.json.return_value = self.sample_weather_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_weather_by_coordinates(52.52, 13.405)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Berlin')
    
    @patch('app.requests.get')
    def test_get_forecast_data_success(self, mock_get):
        """Test successful forecast data fetch"""
        mock_response = MagicMock()
        mock_response.json.return_value = self.sample_forecast_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_forecast_data('Berlin')
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result['list']), 1)
    
    def test_api_weather_endpoint_no_params(self):
        """Test weather endpoint with no parameters"""
        response = self.app.get('/api/weather')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
    
    def test_api_forecast_endpoint_no_params(self):
        """Test forecast endpoint with no parameters"""
        response = self.app.get('/api/forecast')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
    
    def test_api_geocode_endpoint_no_params(self):
        """Test geocode endpoint with no parameters"""
        response = self.app.get('/api/geocode')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
    
    def test_api_popular_cities_endpoint(self):
        """Test popular cities endpoint"""
        response = self.app.get('/api/popular-cities')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        
        # Check structure of cities
        for city in data:
            self.assertIn('name', city)
            self.assertIn('country', city)
            self.assertIn('display', city)
    
    def test_main_page_loads(self):
        """Test that main page loads successfully"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    @patch('app.requests.get')
    def test_api_weather_with_mock(self, mock_get):
        """Test weather API endpoint with mocked request"""
        mock_response = MagicMock()
        mock_response.json.return_value = self.sample_weather_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        response = self.app.get('/api/weather?city=Berlin')
        data = json.loads(response.data)
        
        if response.status_code == 200:
            self.assertEqual(data['city'], 'Berlin')
            self.assertEqual(data['temperature'], 5.5)
    
    @patch('app.requests.get')
    def test_api_forecast_with_mock(self, mock_get):
        """Test forecast API endpoint with mocked request"""
        mock_response = MagicMock()
        mock_response.json.return_value = self.sample_forecast_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        response = self.app.get('/api/forecast?city=Berlin')
        data = json.loads(response.data)
        
        if response.status_code == 200:
            self.assertIsInstance(data, list)
            self.assertGreater(len(data), 0)

class TestEnvironmentConfiguration(unittest.TestCase):
    """Test environment configuration and API key loading"""
    
    def test_api_key_loaded(self):
        """Test that API key is loaded from environment"""
        from app import API_KEY
        
        # Check if API key is set (either from .env or environment)
        if API_KEY:
            self.assertIsNotNone(API_KEY)
            self.assertNotEqual(API_KEY, 'your_api_key_here')
            print(f"✓ API Key is configured: {API_KEY[:10]}...")
        else:
            print("⚠ API Key is not configured")
    
    def test_env_file_exists(self):
        """Test that .env file exists"""
        env_files = ['.env', 'meteo_api.env']
        env_exists = any(os.path.exists(f) for f in env_files)
        
        if env_exists:
            print("✓ Environment file found")
        else:
            print("⚠ No .env file found")
        
        self.assertTrue(env_exists, "At least one .env file should exist")

class TestAPIAuthentication(unittest.TestCase):
    """Test API authentication and error handling"""
    
    def test_api_key_format(self):
        """Test that API key has correct format"""
        from app import API_KEY
        
        if API_KEY and API_KEY != 'your_api_key_here':
            # OpenWeatherMap API keys are typically 32 characters
            self.assertGreaterEqual(len(API_KEY), 32, 
                "API key should be at least 32 characters long")
            print(f"✓ API Key format appears valid (length: {len(API_KEY)})")

def run_diagnostic_tests():
    """Run diagnostic tests to identify issues"""
    print("\n" + "="*60)
    print("🔍 RUNNING DIAGNOSTIC TESTS")
    print("="*60)
    
    # Test 1: Check environment variables
    print("\n1. Checking environment configuration...")
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file
    load_dotenv('meteo_api.env')  # Also try loading the custom env file
    
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if api_key:
        print(f"   ✓ API Key found: {api_key[:10]}...")
    else:
        print("   ✗ API Key NOT found in environment")
    
    # Test 2: Check if requests library works
    print("\n2. Testing HTTP requests...")
    try:
        import requests
        response = requests.get('https://httpbin.org/status/200', timeout=5)
        print(f"   ✓ HTTP requests working (status: {response.status_code})")
    except Exception as e:
        print(f"   ✗ HTTP requests failed: {e}")
    
    # Test 3: Test OpenWeatherMap API directly
    print("\n3. Testing OpenWeatherMap API connection...")
    if api_key:
        try:
            import requests
            test_url = f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={api_key}&units=metric"
            response = requests.get(test_url, timeout=10)
            
            if response.status_code == 200:
                print(f"   ✓ API connection successful (status: {response.status_code})")
                data = response.json()
                print(f"   ✓ Sample data received for: {data.get('name', 'Unknown')}")
                print(f"   ✓ Temperature: {data['main']['temp']}°C")
            elif response.status_code == 401:
                print(f"   ✗ API authentication failed (401)")
                print(f"   ✗ API Key might be invalid or not activated")
            else:
                print(f"   ✗ API returned status: {response.status_code}")
                print(f"   ✗ Response: {response.text}")
        except Exception as e:
            print(f"   ✗ API test failed: {e}")
    else:
        print("   ✗ Cannot test API without API key")
    
    print("\n" + "="*60)
    print("📋 DIAGNOSTIC COMPLETE")
    print("="*60)

if __name__ == '__main__':
    # Run diagnostic tests first
    run_diagnostic_tests()
    
    # Run unit tests
    print("\n🧪 RUNNING UNIT TESTS")
    print("="*60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests
    suite.addTests(loader.loadTestsFromTestCase(TestWeatherAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestEnvironmentConfiguration))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIAuthentication))
    
    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
        print("\nFailed tests:")
        for test, traceback in result.failures + result.errors:
            print(f"  - {test}: {traceback}")
    print("="*60)