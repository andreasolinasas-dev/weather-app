"""
Test delle nuove funzionalità implementate
"""

from app import app, search_history, validate_city_name, get_moon_info, get_fun_weather_facts
import json

def test_input_validation():
    """Test validazione input città"""
    print("\n" + "="*60)
    print("1. TEST VALIDAZIONE INPUT")
    print("="*60)
    
    # Test puntini
    is_valid, result = validate_city_name("...")
    print(f"   {'✓' if not is_valid else '✗'} Puntini: {result}")
    assert not is_valid, "Puntini dovrebbero essere rifiutati"
    
    # Test numeri
    is_valid, result = validate_city_name("123")
    print(f"   {'✓' if not is_valid else '✗'} Numeri: {result}")
    assert not is_valid, "Numeri dovrebbero essere rifiutati"
    
    # Test pattern invalidi
    is_valid, result = validate_city_name("test")
    print(f"   {'✓' if not is_valid else '✗'} Pattern 'test': {result}")
    assert not is_valid, "'test' dovrebbe essere rifiutato"
    
    # Test troppo corto (1 carattere)
    is_valid, result = validate_city_name("a")
    print(f"   {'✓' if not is_valid else '✗'} Troppo corto (a): {result}")
    assert not is_valid, "Nome troppo corto (1 carattere) dovrebbe essere rifiutato"
    
    # Test lunghezza minima (2 caratteri - accettato)
    is_valid, result = validate_city_name("ab")
    print(f"   {'✓' if is_valid else '✗'} Lunghezza minima (ab): {result}")
    assert is_valid, "Nome di 2 caratteri dovrebbe essere accettato"
    
    # Test nome valido
    is_valid, result = validate_city_name("Rome")
    print(f"   {'✓' if is_valid else '✗'} Nome valido (Rome): {result}")
    assert is_valid, "Rome dovrebbe essere accettato"
    
    # Test nome valido con spazio
    is_valid, result = validate_city_name("New York")
    print(f"   {'✓' if is_valid else '✗'} Nome con spazio (New York): {result}")
    assert is_valid, "New York dovrebbe essere accettato"
    
    print("   ✅ Tutti i test di validazione superati!")

def test_history_management():
    """Test gestione cronologia"""
    print("\n" + "="*60)
    print("2. TEST GESTIONE CRONOLOGIA")
    print("="*60)
    
    with app.test_client() as client:
        # Aggiungi alla cronologia
        response = client.post('/api/history', json={'city': 'Rome', 'country': 'IT'})
        data = response.get_json()
        print(f"   {'✓' if response.status_code == 200 else '✗'} Aggiungi Rome: {response.status_code}")
        assert response.status_code == 200
        
        response = client.post('/api/history', json={'city': 'Milan', 'country': 'IT'})
        data = response.get_json()
        print(f"   {'✓' if response.status_code == 200 else '✗'} Aggiungi Milan: {response.status_code}")
        assert response.status_code == 200
        
        # Ottieni cronologia
        response = client.get('/api/history')
        history = response.get_json()
        print(f"   {'✓' if response.status_code == 200 and len(history) == 2 else '✗'} Ottieni cronologia: {len(history)} elementi")
        assert response.status_code == 200
        assert len(history) == 2
        
        # Cancella cronologia
        response = client.delete('/api/history')
        data = response.get_json()
        print(f"   {'✓' if response.status_code == 200 else '✗'} Cancella cronologia: {response.status_code}")
        assert response.status_code == 200
        
        # Verifica che sia vuota
        response = client.get('/api/history')
        history = response.get_json()
        print(f"   {'✓' if response.status_code == 200 and len(history) == 0 else '✗'} Verifica vuota: {len(history)} elementi")
        assert len(history) == 0
    
    print("   ✅ Tutti i test di cronologia superati!")

def test_moon_phase():
    """Test fase lunare"""
    print("\n" + "="*60)
    print("3. TEST FASE LUNARE")
    print("="*60)
    
    with app.test_client() as client:
        response = client.get('/api/moon')
        data = response.get_json()
        print(f"   {'✓' if response.status_code == 200 else '✗'} Moon API: {response.status_code}")
        print(f"   🌙 Fase: {data.get('phase', 'N/A')}")
        print(f"   🌙 Emoji: {data.get('emoji', 'N/A')}")
        print(f"   🌙 Illuminazione: {data.get('illumination', 'N/A')}%")
        print(f"   🌙 Prossima luna piena: {data.get('next_full_moon', 'N/A')}")
        assert response.status_code == 200
        assert 'phase' in data
        assert 'emoji' in data
    
    print("   ✅ Test fase lunare superato!")

def test_fun_facts():
    """Test curiosità meteo"""
    print("\n" + "="*60)
    print("4. TEST CURIOSITÀ METEO")
    print("="*60)
    
    with app.test_client() as client:
        response = client.get('/api/fun-facts?city=London')
        data = response.get_json()
        print(f"   {'✓' if response.status_code == 200 else '✗'} Fun Facts API: {response.status_code}")
        facts = data.get('facts', [])
        print(f"   📊 Numero di curiosità: {len(facts)}")
        for i, fact in enumerate(facts[:2], 1):
            print(f"   💡 Curiosità {i}: {fact}")
        assert response.status_code == 200
        assert 'facts' in data
    
    print("   ✅ Test curiosità superato!")

def test_weather_with_validation():
    """Test API meteo con validazione"""
    print("\n" + "="*60)
    print("5. TEST API METEO CON VALIDAZIONE")
    print("="*60)
    
    with app.test_client() as client:
        # Test input invalido
        response = client.get('/api/weather?city=...')
        print(f"   {'✓' if response.status_code == 500 else '✗'} Input invalido (...): {response.status_code}")
        assert response.status_code == 500
        
        # Test input valido
        response = client.get('/api/weather?city=London')
        print(f"   {'✓' if response.status_code == 200 else '✗'} Input valido (London): {response.status_code}")
        assert response.status_code == 200
        
        data = response.get_json()
        print(f"   🌤️ Temperatura London: {data.get('temperature', 'N/A')}°C")
        print(f"   🌤️ Condizione: {data.get('weather_description', 'N/A')}")
    
    print("   ✅ Test API meteo con validazione superato!")

def main():
    """Esegui tutti i test"""
    print("\n" + "="*60)
    print("🧪 TEST NUOVE FUNZIONALITÀ WEATHER APP")
    print("="*60)
    
    try:
        test_input_validation()
        test_history_management()
        test_moon_phase()
        test_fun_facts()
        test_weather_with_validation()
        
        print("\n" + "="*60)
        print("✅ TUTTI I TEST SONO STATI SUPERATI!")
        print("="*60)
        print("\n🎉 Le nuove funzionalità sono pronte:")
        print("   ✓ Validazione input città")
        print("   ✓ Cronologia ricerche")
        print("   ✓ Fasi lunari")
        print("   ✓ Curiosità meteo")
        print("="*60 + "\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST FALLITO: {e}")
        print("Controlla l'output per maggiori dettagli.\n")
    except Exception as e:
        print(f"\n❌ ERRORE: {e}")
        print("Si è verificato un errore imprevisto.\n")

if __name__ == '__main__':
    main()