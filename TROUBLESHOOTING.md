# 🔧 Troubleshooting Guide - Weather App

## Problema: Errore 401 Unauthorized

### Diagnosi Completata ✅

Abbiamo eseguito test completi e identificato il problema:

```
🔍 Making API request for: Berlin
🔗 Request URL: http://api.openweathermap.org/data/2.5/weather
🔑 API Key: 6d173267a4...
✗ API authentication failed (401)
✗ API Key might be invalid or not activated
```

### Causa del Problema

La API key presente nel file `meteo_api.env` (`6d173267a45beef15be3b470e5751d95`) **non è valida** o **non è stata attivata** da OpenWeatherMap.

### Soluzione

#### Passo 1: Ottenere una Nuova API Key

1. Vai su [OpenWeatherMap](https://openweathermap.org/api)
2. Clicca su "Sign Up" e crea un account gratuito
3. **Importante**: Verifica il tuo account tramite l'email che riceverai
4. Accedi al tuo account e vai su "My API keys"
5. Crea una nuova API key (di solito si chiama "Default")
6. Copia la tua nuova API key (32 caratteri alfanumerici)

#### Passo 2: Configurare la API Key

1. Crea un file `.env` nella cartella del progetto:
   ```bash
   copy .env.example .env
   ```

2. Apri il file `.env` e sostituisci `la_tua_api_key_qui` con la tua nuova API key:
   ```
   OPENWEATHER_API_KEY=la_tua_nuova_api_key_qui
   FLASK_ENV=development
   SECRET_KEY=AndreaDevelope
   ```

#### Passo 3: Riavviare l'Applicazione

1. Ferma il server Flask (Ctrl+C)
2. Riavvia l'applicazione:
   ```bash
   python app.py
   ```

3. Apri il browser su `http://localhost:5000`

#### Passo 4: Verificare il Funzionamento

1. Cerca una città (es. "Rome" o "Milan")
2. Dovresti vedere i dati meteo correttamente

### Test di Verifica

Abbiamo creato un suite di test completo per verificare il funzionamento:

```bash
python test_app.py
```

Questo eseguirà:
- ✅ Test di formattazione dati
- ✅ Test delle API endpoints
- ✅ Test di configurazione ambiente
- ✅ Test diagnostici della connessione API

### Messaggi di Errore Comuni

#### "API authentication failed"
- **Causa**: API key non valida o non attivata
- **Soluzione**: Ottieni una nuova API key da OpenWeatherMap

#### "City not found"
- **Causa**: Nome della città scritto male
- **Soluzione**: Controlla l'ortografia o usa il nome in inglese

#### "Failed to fetch weather data"
- **Causa**: Problemi di connessione internet
- **Soluzione**: Controlla la tua connessione

### Note Importanti

1. **Attivazione API Key**: Dopo aver creato una nuova API key, potrebbero essere necessari alcuni minuti (a volte fino a 2 ore) prima che sia completamente attiva.

2. **Limiti API Gratuita**: 
   - 1000 chiamate al giorno
   - 60 chiamate al minuto
   - Aggiornamenti ogni 10 minuti

3. **Formato API Key**: Le API key di OpenWeatherMap sono tipicamente stringhe di 32 caratteri alfanumerici.

### Struttura del Progetto

```
C:\Progetto Generation AI\
├── app.py                 # Applicazione Flask principale
├── test_app.py            # Suite di test completa
├── requirements.txt       # Dipendenze Python
├── .env.example          # Esempio configurazione
├── .env                  # Configurazione (da creare)
├── meteo_api.env         # Vecchia configurazione (API key non valida)
├── README.md             # Documentazione principale
├── TROUBLESHOOTING.md    # Questa guida
├── templates/
│   └── index.html        # Template HTML
└── static/
    ├── css/
    │   └── style.css     # Stili CSS moderni
    ├── js/
    │   └── app.js        # JavaScript per interattività
    └── images/           # Immagini (se necessarie)
```

### Debug Avanzato

Se hai ancora problemi dopo aver seguito questi passi:

1. **Verifica la API Key**:
   ```bash
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENWEATHER_API_KEY'))"
   ```

2. **Testa la connessione API manualmente**:
   ```python
   import requests
   api_key = "la_tua_api_key"
   url = f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={api_key}&units=metric"
   response = requests.get(url)
   print(response.status_code)
   print(response.json())
   ```

3. **Controlla i log dell'applicazione**:
   - Quando avvii `python app.py`, vedrai i log delle richieste API
   - Cerca messaggi che iniziano con `🔍` per vedere i dettagli delle richieste

### Contatti e Supporto

Se il problema persiste:
- Controlla la documentazione ufficiale di [OpenWeatherMap](https://openweathermap.org/faq)
- Verifica che il tuo account OpenWeatherMap sia verificato
- Prova a rigenerare una nuova API key dal tuo account

---

**Aggiornato**: 9 Aprile 2026
**Stato**: Problema identificato e soluzione documentata ✅