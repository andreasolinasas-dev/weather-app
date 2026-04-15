"""
Weather Application - Real API Integration Tests
Test che usano l'API OpenWeatherMap reale per validare il funzionamento
"""

import unittest
import requests
import os
from dotenv import load_dotenv
from app import app, get_weather_data, get_weather_by_coordinates, get_forecast_data, format_weather_data, format_forecast_data

class TestRealOpenWeatherMapAPI(unittest.TestCase):
    """Test di integrazione con l'API OpenWeatherMap reale"""
    
    @classmethod
    def setUpClass(cls):
        """Carica le variabili d'ambiente una volta per tutte"""
        load_dotenv()
        cls.api_key = os.getenv('OPENWEATHER_API_KEY')
        cls.base_url = "http://api.openweathermap.org/data/2.5"
        
        # Verifica che l'API key sia configurata
        if not cls.api_key:
            raise unittest.SkipTest("API key non configurata, salto i test API reali")
    
    def test_01_api_key_validity(self):
        """Test che l'API key sia valida"""
        print(f"\n🔑 Testing API Key: {self.api_key[:10]}...")
        self.assertIsNotNone(self.api_key, "API key should not be None")
        self.assertNotEqual(self.api_key, "your_api_key_here", "API key should be set")
        self.assertGreaterEqual(len(self.api_key), 32, "API key should be at least 32 characters")
    
    def test_02_current_weather_london(self):
        """Test meteo attuale per Londra"""
        print("\n🌤️ Testing current weather for London...")
        data = get_weather_data("London")
        
        self.assertIsNotNone(data, "Data should not be None")
        self.assertNotIn('error', data, f"Should not have error: {data.get('error', '')}")
        self.assertEqual(data['name'], 'London', "City should be London")
        self.assertEqual(data['sys']['country'], 'GB', "Country should be GB")
        self.assertIn('main', data, "Should have main weather data")
        self.assertIn('temp', data['main'], "Should have temperature")
        self.assertIsInstance(data['main']['temp'], (int, float), "Temperature should be numeric")
        
        # Verifica che la temperatura sia ragionevole (tra -50 e 60 gradi)
        self.assertGreaterEqual(data['main']['temp'], -50, "Temperature should be >= -50")
        self.assertLessEqual(data['main']['temp'], 60, "Temperature should be <= 60")
        
        print(f"   ✓ London weather: {data['main']['temp']}°C, {data['weather'][0]['description']}")
    
    def test_03_current_weather_rome(self):
        """Test meteo attuale per Roma"""
        print("\n🌤️ Testing current weather for Rome...")
        data = get_weather_data("Rome")
        
        self.assertIsNotNone(data, "Data should not be None")
        self.assertNotIn('error', data, f"Should not have error: {data.get('error', '')}")
        self.assertEqual(data['name'], 'Rome', "City should be Rome")
        self.assertEqual(data['sys']['country'], 'IT', "Country should be IT")
        
        print(f"   ✓ Rome weather: {data['main']['temp']}°C, {data['weather'][0]['description']}")
    
    def test_04_current_weather_with_country_code(self):
        """Test meteo con codice paese specifico"""
        print("\n🌤️ Testing weather with country code...")
        data = get_weather_data("Paris", "FR")
        
        self.assertIsNotNone(data, "Data should not be None")
        self.assertNotIn('error', data, f"Should not have error: {data.get('error', '')}")
        self.assertEqual(data['name'], 'Paris', "City should be Paris")
        self.assertEqual(data['sys']['country'], 'FR', "Country should be FR")
        
        print(f"   ✓ Paris, FR weather: {data['main']['temp']}°C, {data['weather'][0]['description']}")
    
    def test_05_weather_by_coordinates(self):
        """Test meteo per coordinate geografiche"""
        print("\n📍 Testing weather by coordinates (New York)...")
        # Coordinate di New York
        lat, lon = 40.7128, -74.0060
        data = get_weather_by_coordinates(lat, lon)
        
        self.assertIsNotNone(data, "Data should not be None")
        self.assertNotIn('error', data, f"Should not have error: {data.get('error', '')}")
        self.assertIn('name', data, "Should have city name")
        self.assertIn('main', data, "Should have main weather data")
        
        print(f"   ✓ Coordinates ({lat}, {lon}) weather: {data['main']['temp']}°C")
    
    def test_06_forecast_data(self):
        """Test previsioni meteo"""
        print("\n📅 Testing forecast data...")
        data = get_forecast_data("Berlin")
        
        self.assertIsNotNone(data, "Data should not be None")
        self.assertNotIn('error', data, f"Should not have error: {data.get('error', '')}")
        self.assertIn('list', data, "Should have forecast list")
        self.assertGreater(len(data['list']), 0, "Should have at least one forecast")
        
        # Verifica la struttura di una previsione
        forecast_item = data['list'][0]
        self.assertIn('dt_txt', forecast_item, "Should have datetime")
        self.assertIn('main', forecast_item, "Should have main data")
        self.assertIn('weather', forecast_item, "Should have weather data")
        
        print(f"   ✓ Berlin forecast: {len(data['list'])} items, first: {forecast_item['main']['temp']}°C")
    
    def test_07_format_weather_data(self):
        """Test formattazione dati meteo"""
        print("\n📊 Testing weather data formatting...")
        raw_data = get_weather_data("Milan")
        
        self.assertIsNotNone(raw_data, "Raw data should not be None")
        formatted = format_weather_data(raw_data)
        
        self.assertIsNotNone(formatted, "Formatted data should not be None")
        
        # Verifica tutti i campi formattati
        required_fields = [
            'city', 'country', 'temperature', 'feels_like', 
            'temp_min', 'temp_max', 'weather_main', 'weather_description',
            'weather_icon', 'wind_speed', 'humidity', 'pressure',
            'sunrise', 'sunset', 'timestamp'
        ]
        
        for field in required_fields:
            self.assertIn(field, formatted, f"Missing field: {field}")
        
        print(f"   ✓ Formatted data for {formatted['city']}: {formatted['temperature']}°C")
    
    def test_08_format_forecast_data(self):
        """Test formattazione previsioni"""
        print("\n📊 Testing forecast data formatting...")
        raw_data = get_forecast_data("Tokyo")
        
        self.assertIsNotNone(raw_data, "Raw data should not be None")
        formatted = format_forecast_data(raw_data)
        
        self.assertIsNotNone(formatted, "Formatted data should not be None")
        self.assertIsInstance(formatted, list, "Formatted forecast should be a list")
        self.assertGreater(len(formatted), 0, "Should have at least one forecast")
        
        # Verifica la struttura
        forecast = formatted[0]
        self.assertIn('date', forecast, "Should have date")
        self.assertIn('temperature', forecast, "Should have temperature")
        self.assertIn('weather', forecast, "Should have weather")
        
        print(f"   ✓ Formatted {len(formatted)} forecasts for Tokyo")
    
    def test_09_multiple_cities(self):
        """Test meteo per multiple città"""
        print("\n🌍 Testing multiple cities...")
        cities = [
            ("Rome", "IT"),
            ("Milan", "IT"),
            ("Naples", "IT"),
            ("Florence", "IT"),
            ("Venice", "IT"),
            ("London", "GB"),
            ("Paris", "FR"),
            ("Berlin", "DE"),
            ("Madrid", "ES"),
            ("New York", "US")
        ]
        
        successful = 0
        failed = 0
        
        for city, country in cities:
            try:
                data = get_weather_data(city, country)
                if data and 'error' not in data:
                    successful += 1
                    print(f"   ✓ {city}, {country}: {data['main']['temp']}°C")
                else:
                    failed += 1
                    print(f"   ✗ {city}, {country}: {data.get('error', 'Unknown error')}")
            except Exception as e:
                failed += 1
                print(f"   ✗ {city}, {country}: {str(e)}")
        
        print(f"\n   📊 Summary: {successful} successful, {failed} failed out of {len(cities)} cities")
        self.assertGreater(successful, len(cities) * 0.8, "At least 80% of cities should succeed")
    
    def test_10_api_response_time(self):
        """Test tempo di risposta API"""
        print("\n⏱️ Testing API response time...")
        start_time = requests.get.__code__.co_consts  # Just for reference
        
        import time
        start = time.time()
        data = get_weather_data("London")
        elapsed = time.time() - start
        
        self.assertIsNotNone(data, "Data should not be None")
        self.assertLess(elapsed, 10, "API response should be under 10 seconds")
        
        print(f"   ✓ API response time: {elapsed:.2f} seconds")

class TestFlaskAPIEndpoints(unittest.TestCase):
    """Test degli endpoint Flask con API reale"""
    
    @classmethod
    def setUpClass(cls):
        """Configura il client Flask"""
        load_dotenv()
        cls.app = app.test_client()
        cls.app.testing = True
    
    def test_01_weather_endpoint(self):
        """Test endpoint /api/weather"""
        print("\n🔌 Testing /api/weather endpoint...")
        response = self.app.get('/api/weather?city=London')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}")
        self.assertIsNotNone(data, "Response data should not be None")
        self.assertIn('city', data, "Should have city field")
        self.assertIn('temperature', data, "Should have temperature field")
        self.assertEqual(data['city'], 'London', "City should be London")
        
        print(f"   ✓ /api/weather?city=London: {data['temperature']}°C")
    
    def test_02_forecast_endpoint(self):
        """Test endpoint /api/forecast"""
        print("\n🔌 Testing /api/forecast endpoint...")
        response = self.app.get('/api/forecast?city=Rome')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}")
        self.assertIsNotNone(data, "Response data should not be None")
        self.assertIsInstance(data, list, "Forecast should be a list")
        self.assertGreater(len(data), 0, "Should have at least one forecast")
        
        print(f"   ✓ /api/forecast?city=Rome: {len(data)} forecasts")
    
    def test_03_popular_cities_endpoint(self):
        """Test endpoint /api/popular-cities"""
        print("\n🔌 Testing /api/popular-cities endpoint...")
        response = self.app.get('/api/popular-cities')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}")
        self.assertIsNotNone(data, "Response data should not be None")
        self.assertIsInstance(data, list, "Should be a list")
        self.assertGreater(len(data), 0, "Should have at least one city")
        
        # Verifica struttura città
        for city in data:
            self.assertIn('name', city, "Each city should have a name")
            self.assertIn('country', city, "Each city should have a country")
            self.assertIn('display', city, "Each city should have a display name")
        
        print(f"   ✓ /api/popular-cities: {len(data)} cities available")
    
    def test_04_main_page(self):
        """Test pagina principale"""
        print("\n🔌 Testing main page...")
        response = self.app.get('/')
        
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}")
        self.assertIn(b'Weather', response.data, "Page should contain 'Weather'")
        
        print("   ✓ Main page loads successfully")

def run_api_health_check():
    """Esegui un health check completo dell'API"""
    print("\n" + "="*70)
    print("🏥 API HEALTH CHECK")
    print("="*70)
    
    load_dotenv()
    api_key = os.getenv('OPENWEATHER_API_KEY')
    
    if not api_key:
        print("❌ API key non configurata!")
        return False
    
    print(f"✅ API Key trovata: {api_key[:10]}...")
    print(f"📏 Lunghezza API Key: {len(api_key)} caratteri")
    
    # Test connessione API
    try:
        test_url = f"{BASE_URL}/weather?q=London&appid={api_key}&units=metric"
        response = requests.get(test_url, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Connessione API: OK (status {response.status_code})")
            data = response.json()
            print(f"🌡️ Temperatura London: {data['main']['temp']}°C")
            print(f"🌤️ Condizione: {data['weather'][0]['description']}")
            return True
        elif response.status_code == 401:
            print(f"❌ Connessione API: FALLITA (401 Unauthorized)")
            print("   La API key potrebbe non essere attivata o essere invalida")
            return False
        else:
            print(f"❌ Connessione API: FALLITA (status {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Errore connessione API: {e}")
        return False

if __name__ == '__main__':
    # Health check iniziale
    BASE_URL = "http://api.openweathermap.org/data/2.5"
    health_ok = run_api_health_check()
    
    if not health_ok:
        print("\n⚠️ L'API health check è fallito. I test potrebbero non funzionare.")
        print("   Assicurati che la API key sia corretta e attivata.")
    
    # Esegui i test
    print("\n" + "="*70)
    print("🧪 RUNNING REAL API INTEGRATION TESTS")
    print("="*70)
    
    # Crea il test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Aggiungi test API reali
    suite.addTests(loader.loadTestsFromTestCase(TestRealOpenWeatherMapAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestFlaskAPIEndpoints))
    
    # Esegui i test
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary finale
    print("\n" + "="*70)
    if result.wasSuccessful():
        print("✅ TUTTI I TEST SONO PASSATI!")
        print("🎉 L'applicazione è pronta per l'uso!")
    else:
        print("❌ ALCUNI TEST SONO FALLITI")
        print("\nTest falliti:")
        for test, traceback in result.failures + result.errors:
            print(f"  - {test}: {traceback}")
    print("="*70)