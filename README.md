# 🌤️ Weather App - Applicazione Meteo Moderna

Un'applicazione web moderna e bellissima per consultare le previsioni meteo in tempo reale per qualsiasi città del mondo con **sfondi dinamici ad alta qualità** che cambiano in base alla città cercata.

![Weather App](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)

## ✨ Caratteristiche Principali

- 🌍 **Ricerca globale**: Cerca il meteo per qualsiasi città nel mondo
- 🖼️ **Sfondi dinamici**: Bellissime immagini HD delle città che cambiano con ogni ricerca grazie a LoremFlickr
- 📍 **Geolocalizzazione**: Ottieni il meteo per la tua posizione corrente
- 📅 **Previsioni 5 giorni**: Visualizza le previsioni meteo per i prossimi 5 giorni
- 🎨 **Design moderno**: Interfaccia utente elegante con animazioni fluide e glassmorphism
- 🌈 **Temi dinamici**: Colori adattivi in base alle condizioni meteo
- 🏙️ **Città popolari**: Accesso rapido alle città più cercate
- 📱 **Responsive**: Funziona perfettamente su desktop, tablet e smartphone
- 📚 **Cache intelligente**: Dati meteorologici memorizzati per prestazioni ottimali
- 🌙 **Fasi lunari**: Informazioni complete sulla luna e le maree
- 📊 **Dati completi**: Umidità, velocità vento, precipitazioni, pressione atmosferica
- 📚 **Cronologia ricerche**: Visualizza e ripeti facilmente le ricerche precedenti

## 📁 Struttura del Repository

```
Progetto Generation AI/
├── app.py                    # Applicazione Flask principale
├── requirements.txt          # Dipendenze Python
├── .env.example             # Template per variabili d'ambiente
├── .gitignore               # Configurazione git
├── README.md                # Questo file
├── FINAL_REPORT.md          # Report del progetto
├── TROUBLESHOOTING.md       # Guida alla risoluzione problemi
│
├── templates/               # Template HTML
│   └── index.html          # Interfaccia principale
│
├── static/                  # File statici
│   ├── css/
│   │   └── style.css       # Stili CSS moderni e responsive
│   ├── js/
│   │   └── app.js          # Logica frontend e interazioni
│   └── images/             # Icone e loghi
│
└── test*.py                 # Suite di test automatici
```

## ✨ Caratteristiche

- 🌍 **Ricerca globale**: Cerca il meteo per qualsiasi città nel mondo
- 📍 **Geolocalizzazione**: Ottieni il meteo per la tua posizione corrente
- 📅 **Previsioni 5 giorni**: Visualizza le previsioni meteo per i prossimi 5 giorni
- 🎨 **Design moderno**: Interfaccia utente elegante con animazioni fluide
- 🌈 **Temi dinamici**: Lo sfondo cambia in base alle condizioni meteo
- 🏙️ **Città popolari**: Accesso rapido alle città più cercate
- 📱 **Responsive**: Funziona perfettamente su desktop, tablet e smartphone
- 📚 **Cache intelligente**: Dati meteorologici memorizzati per prestazioni ottimali
- 🌙 **Fasi lunari**: Informazioni complete sulla luna e le maree
- 📊 **Dati completi**: Umidità, velocità vento, precipitazioni, pressione atmosferica
- 📚 **Cronologia ricerche**: Visualizza e ripeti facilmente le ricerche precedenti

## 🚀 Come Eseguire l'Applicazione

### Prerequisiti

- Python 3.8 o superiore
- pip (gestore pacchetti Python)

### Passo 1: Installare le dipendenze

Apri il terminale nella cartella del progetto e installa i pacchetti necessari:

```bash
cd "C:\Progetto Generation AI"
pip install -r requirements.txt
```

### Passo 2: Ottenere la API Key di OpenWeatherMap

Per far funzionare l'applicazione, hai bisogno di una API key gratuita da OpenWeatherMap:

1. Vai su [OpenWeatherMap](https://openweathermap.org/api)
2. Clicca su "Sign Up" e crea un account gratuito
3. **Importante**: Dopo la registrazione, devi verificare il tuo account tramite email
4. Una volta verificato, accedi al tuo account e vai su "My API keys" nel tuo profilo
5. Crea una nuova API key (di default si chiama "Default")
6. Copia la tua API key (dovrebbe essere una stringa di 32 caratteri alfanumerici)

⚠️ **Nota Importante**: La API key fornita nel file `meteo_api.env` potrebbe non essere valida o attiva. Per garantire il funzionamento dell'applicazione, ti consiglio di ottenere la tua API key personale seguendo i passi sopra.

### Passo 3: Configurare la API Key

Crea un file `.env` nella cartella del progetto (puoi copiare `.env.example`):

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Apri il file `.env` con un editor di testo e inserisci la tua API key:

```
OPENWEATHER_API_KEY=la_tua_api_key_qui
FLASK_ENV=development
SECRET_KEY=una_chiave_segreta_a_scelta
```

### Passo 4: Eseguire l'Applicazione

Ora puoi avviare l'applicazione:

```bash
python app.py
```

Vedrai un messaggio simile a questo:

```
🌤️  Weather Application starting...
📍 Access the app at: http://localhost:5000
Press Ctrl+C to stop the server
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### Passo 5: Aprire il Browser

Apri il tuo browser preferito e vai all'indirizzo:

```
http://localhost:5000
```

🎉 **Fatto!** Ora puoi cercare qualsiasi città e vedere le previsioni meteo con bellissimi sfondi dinamici!

## 📖 Come Usare l'App

### Ricerca Singola Città
1. **Cerca una città**: Digita il nome di una città nella barra di ricerca e premi Invio o clicca sul pulsante di ricerca
2. **Usa la geolocalizzazione**: Clicca su "My Location" per ottenere il meteo della tua posizione corrente
3. **Città popolari**: Clicca su una delle città suggerite per vedere rapidamente il meteo

### Ricerca Multipla Città
1. **Inserisci città separate da virgola**: Puoi cercare più città contemporaneamente separandole con virgole (es: "Rome, Milan, Paris")
2. **Visualizzazione affiancata**: I risultati verranno mostrati in card affiancate per un confronto immediato
3. **Cronologia rapida**: Accedi alle ultime 10 città cercate dalla sezione "Recent Searches"

### Navigazione
1. **Cambia tra tab**: Usa "Current" e "Forecast" per cambiare tra meteo attuale e previsioni
2. **Previsioni dettagliate**: Clicca su "Forecast" per vedere le previsioni dei prossimi 5 giorni con dati completi
3. **Informazioni aggiuntive**: Visualizza fasi lunari, dati di umidità, vento, precipitazioni e molto altro

## 📊 Output di Esempio

### Meteo Attuale
```
Rome, IT
🌤️ 22.5°C (Feels like 24.1°C)
Overcast clouds

Dettagli:
- Umidità: 65%
- Vento: 12.3 km/h da NW
- Pressione: 1015 hPa
- Visibilità: 10.0 km
- Alba: 06:32
- Tramonto: 19:45
```

### Previsioni 5 Giorni
```
Lunedì 15 Apr - 24°C / 16°C
🌤️ Partly cloudy

Martedì 16 Apr - 26°C / 18°C
☀️ Clear sky

Mercoledì 17 Apr - 21°C / 14°C
🌧️ Light rain
```

### Fasi Lunari
```
🌙 Fase: Waxing Gibbous
🌕 Illuminazione: 78%
📅 Prossima luna piena: 2026-04-20
🌅 Sorgere luna: 14:30
🌇 Calare luna: 03:15
```

## 🎯 Funzionalità Implementate

### Core Features
- ✅ Ricerca meteo per città singola o multipla
- ✅ Geolocalizzazione automatica
- ✅ Previsioni 5 giorni con dettagli orari
- ✅ Cronologia ricerche (ultime 10 città)
- ✅ Città popolari predefinite

### Advanced Features
- ✅ **Validazione input avanzata** (rifiuta puntini, numeri, nomi troppo corti, pattern invalidi)
- ✅ **Cache intelligente** (memorizzazione temporanea dei dati per prestazioni ottimali)
- ✅ **Fasi lunari** (calcolo automatico della fase lunare e informazioni correlate)
- ✅ **Dati meteorologici completi** (umidità, velocità vento, precipitazioni, pressione, visibilità)
- ✅ **Maree** (informazioni sulle maree basate sulla posizione)
- ✅ **Curiosità meteo** (fatti divertenti basati sulle condizioni atmosferiche)

### UI/UX Features
- ✅ Design moderno con effetti glassmorphism
- ✅ Animazioni fluide e gradienti dinamici
- ✅ Temi basati sulle condizioni meteo
- ✅ Responsive design per tutti i dispositivi
- ✅ Micro-interazioni e transizioni eleganti

## 🛠️ Gestione degli Errori

### Input Non Validi
- **Puntini o caratteri speciali**: "Invalid city name: contains only punctuation"
- **Numeri**: "Invalid city name: contains only numbers"
- **Pattern comuni**: "Invalid city name" (per parole come "test", "asdf", ecc.)
- **Nome troppo corto**: "City name too short" (meno di 2 caratteri)

### Errori API
- **Città non trovata**: "City 'NomeCittà' not found. Please check the spelling and try again."
- **API key non valida**: "API authentication failed. Please check your OpenWeatherMap API key."
- **Connessione fallita**: "Failed to fetch weather data: [dettagli errore]"

### Errori di Sistema
- **Timeout**: "Failed to fetch weather data: [errore di timeout]"
- **Formato risposta**: "Unexpected error: [dettagli tecnici]"

## 🌐 Informazioni API

### OpenWeatherMap API
- **Endpoint principali**:
  - `/weather` - Meteo attuale
  - `/forecast` - Previsioni 5 giorni
- **Limiti gratuiti**: 1000 chiamate/giorno, 60 chiamate/minuto
- **Unità**: Celsius (metric)
- **Formato dati**: JSON

### Nominatim (OpenStreetMap)
- **Utilizzo**: Geocoding e reverse geocoding
- **Endpoint**: API pubblica di OpenStreetMap
- **Limiti**: Rispettare i limiti di rate limiting (1 richiesta/secondo)

### Altre API Integrate
- **Calcolo fasi lunari**: Algoritmo matematico integrato
- **Informazioni maree**: Basato su posizione geografica e ciclo lunare
- **Foto cartolina città**: API Pexels gratuita con fallback locale

## 🔧 Architettura Tecnica

### Backend
- **Framework**: Flask 3.0.0
- **Linguaggio**: Python 3.8+
- **Gestione API**: python-dotenv per variabili d'ambiente
- **HTTP Client**: requests con timeout gestiti
- **Geocoding**: geopy con gestione errori

### Frontend
- **Template Engine**: Jinja2
- **CSS**: Stile moderno con CSS3 avanzato
- **JavaScript**: Vanilla JS per interattività
- **Icone**: Font Awesome 6.4.0
- **Font**: Poppins da Google Fonts

### Sicurezza
- **Variabili d'ambiente**: API keys archiviate in .env
- **Validazione input**: Controllo stringhe e pattern
- **Error handling**: Gestione completa degli errori
- **Logging**: Debug dettagliato per troubleshooting

## 🚀 Miglioramenti Futuri

### Prossimi Sviluppi
- [ ] **Database integrato**: Salvataggio permanente della cronologia e preferiti
- [ ] **Cache avanzata**: Redis o sistema di caching più performante
- [ ] **Mappe interattive**: Selezione città tramite mappa
- [ ] **Notifiche push**: Avvisi per cambiamenti meteo significativi
- [ ] **Supporto multilingua**: Interfaccia in diverse lingue

### Feature Premium
- [ ] **Widget desktop**: Applicazione standalone
- [ ] **Integrazione smart home**: Comandi vocali e automazioni
- [ ] **Dati storici**: Andamento meteo storico per analisi
- [ ] **Allarmi personalizzati**: Soglie personalizzabili per avvisi

### Ottimizzazioni
- [ ] **Performance**: Ottimizzazione caricamento e rendering
- [ ] **Mobile app**: Applicazione nativa iOS/Android
- [ ] **Analytics**: Statistiche di utilizzo e preferenze utente

## 📁 Struttura del Progetto

```
C:\Progetto Generation AI\
├── app.py                 # Applicazione Flask principale
├── requirements.txt       # Dipendenze Python
├── .env.example          # Esempio file di configurazione
├── .env                  # File di configurazione (da creare)
├── README.md             # Questo file
├── TROUBLESHOOTING.md    # Guida risoluzione problemi
├── FINAL_REPORT.md       # Report finale progetto
├── templates/
│   └── index.html        # Template HTML principale
└── static/
    ├── css/
    │   └── style.css     # Fogli di stile CSS
    ├── js/
    │   └── app.js        # JavaScript per l'interattività
    └── images/           # Immagini (se necessarie)
```

## 🛠️ Tecnologie Utilizzate

### Backend
- **Python 3.8+**: Linguaggio principale
- **Flask 3.0.0**: Framework web
- **Requests**: HTTP client
- **python-dotenv**: Gestione variabili d'ambiente
- **geopy**: Geocoding e reverse geocoding
- **datetime**: Gestione date e orari

### Frontend
- **HTML5**: Struttura semantica
- **CSS3**: Stili avanzati con animazioni
- **JavaScript (Vanilla)**: Interattività senza framework
- **Font Awesome**: Icone vettoriali
- **Google Fonts**: Tipografia web

### API Esterne
- **OpenWeatherMap**: Dati meteorologici in tempo reale
- **Nominatim (OpenStreetMap)**: Geocoding e mappe
- **Calcolo fasi lunari**: Algoritmo matematico integrato

## 🎨 Caratteristiche del Design

### Effetti Visivi
- **Glassmorphism**: Effetto vetro moderno per le card
- **Gradienti animati**: Sfondo con orbite colorate in movimento
- **Micro-interazioni**: Effetti hover e transizioni fluide
- **Weather-based themes**: Colori che cambiano in base al meteo
- **Mobile-first**: Design ottimizzato per tutti i dispositivi

### Animazioni
- **Floating icons**: Icone meteo che fluttuano delicatamente
- **Smooth transitions**: Transizioni tra stati e pagine
- **Loading spinners**: Indicatori di caricamento eleganti
- **Particle effects**: Effetto particelle nello sfondo

## ❓ Risoluzione Problemi

### Problemi Comuni

#### L'app non mostra i dati meteo
- Verifica di aver inserito correttamente la API key nel file `.env`
- Assicurati che la API key sia attiva (potrebbe richiedere alcuni minuti dopo la creazione)
- Controlla la connessione internet
- Verifica che l'account OpenWeatherMap sia verificato via email

#### Errore "Module not found"
- Esegui `pip install -r requirements.txt` per installare tutte le dipendenze
- Verifica che Python sia installato correttamente
- Controlla che il virtual environment sia attivo (se usato)

#### La porta 5000 è già in uso
- Chiudi altre applicazioni che usano la porta 5000
- Oppure modifica la porta in `app.py`: `app.run(port=5001)`
- Usa `netstat -ano | findstr :5000` per identificare il processo

#### Cache non funzionante
- Verifica che la cartella `cache/` esista o creala manualmente
- Controlla i permessi di scrittura nella cartella del progetto
- Riavvia l'applicazione per resettare la cache

### Debug Avanzato

#### Log dettagliati
L'applicazione genera log dettagliati per ogni richiesta:
```
🔍 Making API request for: Rome
🔗 Request URL: http://api.openweathermap.org/data/2.5/weather
🔑 API Key: 6d173267a4...
```

#### Test API diretti
Puoi testare le API direttamente dal browser:
- Meteo attuale: `http://localhost:5000/api/weather?city=Rome`
- Previsioni: `http://localhost:5000/api/forecast?city=Rome`
- Fasi lunari: `http://localhost:5000/api/moon?lat=41.9&lon=12.5`

## 📝 Note Tecniche

### Performance
- **Cache duration**: 30 minuti per dati meteorologici
- **API rate limiting**: Rispetta i limiti OpenWeatherMap
- **Timeout gestiti**: 10 secondi per ogni richiesta
- **Error fallback**: Gestione elegante degli errori

### Sicurezza
- **API keys**: Mai hardcodate, sempre in variabili d'ambiente
- **Input validation**: Controllo completo degli input utente
- **Error messages**: Messaggi utente-friendly, dettagli tecnici solo in log
- **CORS**: Gestione limitata per sicurezza

### Scalabilità
- **Architettura modulare**: Facile aggiunta nuove funzionalità
- **API design**: RESTful e ben strutturata
- **Frontend separato**: Facile integrazione con altri framework
- **Database ready**: Struttura pronta per integrazione database

## 🤝 Contributi

Sentiti libero di modificare e migliorare questo progetto per le tue esigenze!

### Come Contribuire
1. Fork del progetto
2. Crea un branch per la tua feature: `git checkout -b feature/nome-feature`
3. Commit delle modifiche: `git commit -m "Aggiunta feature X"`
4. Push sul branch: `git push origin feature/nome-feature`
5. Apri una Pull Request

### Linee Guida
- Mantieni il codice pulito e commentato
- Aggiorna la documentazione per nuove funzionalità
- Testa sempre le modifiche prima del commit
- Segui lo stile di codifica esistente

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT.

### MIT License

Copyright (c) 2024 WeatherApp

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

**Sviluppato con ❤️ usando Python & Flask**
