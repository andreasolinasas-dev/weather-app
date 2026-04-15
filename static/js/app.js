/**
 * Weather App - Frontend JavaScript
 * Handles all user interactions and API calls
 */

// Global variables
let currentCity = null;
let currentCountry = null;
let lastSearchQuery = '';
let currentLanguage = 'it';
let currentWeatherData = null;
let localClockTimer = null;

const SUPPORTED_LANGUAGES = ['it', 'en', 'fr', 'es'];
const SCENE_CLASSES = ['scene-sunny', 'scene-clouds', 'scene-rain', 'scene-snow', 'scene-night', 'scene-storm', 'scene-mist'];
const BACKGROUND_CACHE_KEY = 'weatherapp-background-cache-v7';
const BACKGROUND_VARIANT_SEEDS = ['dawn', 'midday', 'golden', 'harbor'];
let backgroundPhotoRequestToken = 0;
function buildPostcardUrls(queries) {
    return (Array.isArray(queries) ? queries : []).map((query, index) => (
        `https://source.unsplash.com/featured/1600x900/?${encodeURIComponent(query)}&sig=${index + 1}`
    ));
}

const CITY_BACKGROUND_PROFILES = {
    'Moscow,RU': {
        images: [
            'https://images.unsplash.com/photo-1512040236537-7cb4f5a3f0b7?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1513326738677-b964603b136d?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1541845157-a6d2d100c931?auto=format&fit=crop&w=1600&q=85'
        ]
    },
    'Dubai,AE': {
        images: [
            'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1518684079-3c830dcef090?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1600&q=85'
        ]
    },
    'Sydney,AU': {
        queries: ['sydney opera house', 'sydney harbour bridge', 'sydney harbour skyline', 'sydney australia skyline']
    },
    'Beijing,CN': {
        queries: ['beijing skyline', 'forbidden city beijing', 'beijing china landmark', 'beijing city lights']
    },
    'Berlin,DE': {
        queries: ['berlin brandenburg gate', 'berlin tv tower', 'berlin skyline', 'berlin germany architecture']
    },
    'London,GB': {
        queries: ['london tower bridge', 'london big ben', 'london thames skyline', 'london uk cityscape']
    },
    'Nuuk,GL': {
        queries: ['nuuk greenland harbor', 'nuuk greenland colorful houses', 'nuuk greenland fjord', 'nuuk greenland skyline']
    },
    'Cagliari,IT': {
        queries: ['cagliari harbor', 'cagliari italy coastline', 'cagliari bastion', 'cagliari sardinia skyline']
    },
    'Madrid,ES': {
        queries: ['madrid plaza mayor', 'madrid royal palace', 'madrid gran via', 'madrid skyline']
    },
    'Florence,IT': {
        queries: ['florence duomo', 'florence ponte vecchio', 'florence skyline', 'florence italy old town']
    },
    'Venice,IT': {
        queries: ['venice canal gondola', 'venice rialto bridge', 'venice st mark square', 'venice lagoon']
    },
    'Turin,IT': {
        queries: ['turin mole antonelliana', 'turin piazza castello', 'turin italy skyline', 'turin city center']
    },
    'Rome,IT': {
        queries: ['rome colosseum', 'rome vatican', 'rome pantheon', 'rome skyline']
    },
    'Milan,IT': {
        queries: ['milan duomo', 'milan galleria vittorio emanuele', 'milan skyline', 'milan city center']
    },
    'Naples,IT': {
        queries: ['naples vesuvius', 'naples bay', 'naples historic center', 'naples waterfront']
    },
    'Paris,FR': {
        queries: ['paris eiffel tower', 'paris seine', 'paris louvre', 'paris skyline']
    },
    'Tokyo,JP': {
        queries: ['tokyo skyline', 'shibuya crossing tokyo', 'tokyo tower', 'tokyo japan city lights']
    },
    'New York,US': {
        queries: ['new york skyline', 'statue of liberty', 'brooklyn bridge', 'central park new york']
    },
    'Kaski,NP': {
        images: [
            'https://images.unsplash.com/photo-1512273222628-4f3be6b821d4?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1464822759844-d150baec0497?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1600&q=85'
        ]
    },
    'Nyul,HU': {
        queries: ['hungary countryside', 'hungarian village landscape', 'hungary scenic view', 'rural hungary']
    },
    'Sisimiut,GL': { queries: ['sisimiut greenland harbor', 'sisimiut colorful houses', 'sisimiut greenland coast', 'sisimiut fjord'] },
    'Ilulissat,GL': { queries: ['ilulissat greenland icefjord', 'ilulissat iceberg', 'ilulissat greenland coast', 'ilulissat arctic landscape'] },
    'Aasiaat,GL': { queries: ['aasiaat greenland harbor', 'aasiaat colorful houses', 'aasiaat arctic coast', 'aasiaat greenland town'] },
    'Qaqortoq,GL': { queries: ['qaqortoq greenland colorful houses', 'qaqortoq harbor', 'qaqortoq greenland coast', 'qaqortoq arctic town'] },
    'Maniitsoq,GL': { queries: ['maniitsoq greenland harbor', 'maniitsoq fjord', 'maniitsoq arctic coast', 'maniitsoq colorful houses'] },
    'Tasiilaq,GL': { queries: ['tasiilaq greenland mountains', 'tasiilaq harbor', 'tasiilaq fjord', 'tasiilaq arctic town'] },
    'Paamiut,GL': { queries: ['paamiut greenland coast', 'paamiut harbor', 'paamiut colorful houses', 'paamiut fjord'] },
    'Narsaq,GL': { queries: ['narsaq greenland fjord', 'narsaq greenland village', 'narsaq harbor', 'narsaq arctic landscape'] },
    'Uummannaq,GL': { queries: ['uummannaq greenland iceberg', 'uummannaq harbor', 'uummannaq fjord', 'uummannaq arctic town'] }
};

const TRANSLATIONS = {
    it: {
        brandTagline: 'La tua app meteo più affidabile',
        navCurrent: 'Oggi',
        navForecast: 'Previsioni',
        searchPlaceholder: 'Cerca una citta...',
        myLocation: 'La mia posizione',
        recentSearches: 'Ricerche recenti',
        popularCities: 'Citta popolari',
        welcomeTitle: 'Benvenuto in WeatherApp',
        welcomeText: 'Cerca una citta o usa la tua posizione per vedere il meteo in tempo reale.',
        currentWeatherLabel: 'Meteo attuale',
        feelsLikePrefix: 'Percepita',
        windLabel: 'Vento',
        humidityLabel: 'Umidita',
        visibilityLabel: 'Visibilita',
        pressureLabel: 'Pressione',
        cloudsLabel: 'Nuvole',
        sunriseLabel: 'Alba',
        sunsetLabel: 'Tramonto',
        forecastTitle: 'Previsioni a piu giorni',
        forecastSubtitle: 'Ogni giornata mostra temperatura minima e massima, oltre al meteo principale.',
        loadingText: 'Caricamento dei dati meteo...',
        errorTitle: 'Ops, qualcosa non ha funzionato',
        errorText: 'Impossibile recuperare i dati meteo. Riprova.',
        retryButton: 'Riprova',
        footerData: 'I dati meteo sono forniti da OpenWeatherMap.',
        footerBuild: 'WeatherApp. Creata con Python e Flask.',
        photoCredit: 'Foto fornite da',
        heroText: 'Orari corretti per alba e tramonto, previsioni con minime e massime, e un tema che segue il meteo.'
    },
    en: {
        brandTagline: 'Your most reliable weather app',
        navCurrent: 'Today',
        navForecast: 'Forecast',
        searchPlaceholder: 'Search for a city...',
        myLocation: 'My location',
        recentSearches: 'Recent searches',
        popularCities: 'Popular cities',
        welcomeTitle: 'Welcome to WeatherApp',
        welcomeText: 'Search for a city or use your location to get real-time weather updates.',
        currentWeatherLabel: 'Current weather',
        feelsLikePrefix: 'Feels like',
        windLabel: 'Wind',
        humidityLabel: 'Humidity',
        visibilityLabel: 'Visibility',
        pressureLabel: 'Pressure',
        cloudsLabel: 'Clouds',
        sunriseLabel: 'Sunrise',
        sunsetLabel: 'Sunset',
        forecastTitle: 'Multi-day forecast',
        forecastSubtitle: 'Each day includes minimum and maximum temperature, plus the main condition.',
        loadingText: 'Loading weather data...',
        errorTitle: 'Oops, something went wrong',
        errorText: 'Unable to fetch weather data. Please try again.',
        retryButton: 'Retry',
        footerData: 'Weather data provided by OpenWeatherMap.',
        footerBuild: 'WeatherApp. Built with Python and Flask.',
        photoCredit: 'Photos provided by',
        heroText: 'Accurate sunrise and sunset times, min and max forecasts, and a weather-aware theme.'
    },
    fr: {
        brandTagline: 'Votre application meteo la plus fiable',
        navCurrent: 'Aujourd hui',
        navForecast: 'Previsions',
        searchPlaceholder: 'Rechercher une ville...',
        myLocation: 'Ma position',
        recentSearches: 'Recherches recentes',
        popularCities: 'Villes populaires',
        welcomeTitle: 'Bienvenue sur WeatherApp',
        welcomeText: 'Recherchez une ville ou utilisez votre position pour obtenir la meteo en temps reel.',
        currentWeatherLabel: 'Meteo actuelle',
        feelsLikePrefix: 'Ressenti',
        windLabel: 'Vent',
        humidityLabel: 'Humidite',
        visibilityLabel: 'Visibilite',
        pressureLabel: 'Pression',
        cloudsLabel: 'Nuages',
        sunriseLabel: 'Lever du soleil',
        sunsetLabel: 'Coucher du soleil',
        forecastTitle: 'Previsions sur plusieurs jours',
        forecastSubtitle: 'Chaque jour affiche la temperature minimale et maximale, ainsi que l etat principal.',
        loadingText: 'Chargement des donnees meteo...',
        errorTitle: 'Oups, quelque chose a mal tourne',
        errorText: 'Impossible de recuperer les donnees meteo. Reessayez.',
        retryButton: 'Reessayer',
        footerData: 'Les donnees meteo sont fournies par OpenWeatherMap.',
        footerBuild: 'WeatherApp. Creee avec Python et Flask.',
        photoCredit: 'Photos fournies par',
        heroText: 'Heures exactes du lever et du coucher du soleil, previsions avec minima et maxima, et un theme adapte au meteo.'
    },
    es: {
        brandTagline: 'Tu app del tiempo mas fiable',
        navCurrent: 'Hoy',
        navForecast: 'Pronostico',
        searchPlaceholder: 'Busca una ciudad...',
        myLocation: 'Mi ubicacion',
        recentSearches: 'Busquedas recientes',
        popularCities: 'Ciudades populares',
        welcomeTitle: 'Bienvenido a WeatherApp',
        welcomeText: 'Busca una ciudad o usa tu ubicacion para ver el tiempo en tiempo real.',
        currentWeatherLabel: 'Tiempo actual',
        feelsLikePrefix: 'Sensacion termica',
        windLabel: 'Viento',
        humidityLabel: 'Humedad',
        visibilityLabel: 'Visibilidad',
        pressureLabel: 'Presion',
        cloudsLabel: 'Nubes',
        sunriseLabel: 'Amanecer',
        sunsetLabel: 'Atardecer',
        forecastTitle: 'Prevision de varios dias',
        forecastSubtitle: 'Cada dia incluye temperatura minima y maxima, ademas del estado principal.',
        loadingText: 'Cargando datos meteorologicos...',
        errorTitle: 'Vaya, algo salio mal',
        errorText: 'No se pudieron obtener los datos meteorologicos. Intentalo de nuevo.',
        retryButton: 'Reintentar',
        footerData: 'Los datos meteorologicos son proporcionados por OpenWeatherMap.',
        footerBuild: 'WeatherApp. Creada con Python y Flask.',
        photoCredit: 'Fotos proporcionadas por',
        heroText: 'Horas correctas de amanecer y atardecer, previsiones con minimas y maximas, y un tema que sigue el clima.'
    }
};

// DOM Elements
const cityInput = document.getElementById('cityInput');
const searchBtn = document.getElementById('searchBtn');
const locationBtn = document.getElementById('locationBtn');
const searchSuggestions = document.getElementById('searchSuggestions');
const popularCitiesContainer = document.getElementById('popularCities');
const welcomeState = document.getElementById('welcomeState');
const weatherContent = document.getElementById('weatherContent');
const loadingState = document.getElementById('loadingState');
const errorState = document.getElementById('errorState');
const navLinks = document.querySelectorAll('.nav-link');
const mainContainer = document.querySelector('.container');

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    initializeLanguage();
    injectHeaderLanguageSwitcher();
    applyTranslations();
    loadPopularCities();
    setupEventListeners();
    loadHistory();
});

function initializeLanguage() {
    const savedLanguage = localStorage.getItem('weatherapp-language');
    const browserLanguage = (navigator.language || 'it').slice(0, 2).toLowerCase();
    currentLanguage = SUPPORTED_LANGUAGES.includes(savedLanguage)
        ? savedLanguage
        : (SUPPORTED_LANGUAGES.includes(browserLanguage) ? browserLanguage : 'it');
}

function injectHeaderLanguageSwitcher() {
    const header = document.querySelector('.header');
    if (!header || document.getElementById('languageSelect')) {
        return;
    }

    const actions = document.createElement('div');
    actions.className = 'header-actions';
    actions.innerHTML = `
        <label class="language-switcher" aria-label="Language selector">
            <i class="fas fa-globe"></i>
            <select id="languageSelect">
                <option value="it">Italiano</option>
                <option value="en">English</option>
                <option value="fr">Français</option>
                <option value="es">Español</option>
            </select>
        </label>
    `;

    const nav = header.querySelector('.nav');
    if (nav) {
        nav.insertAdjacentElement('afterend', actions);
    } else {
        header.appendChild(actions);
    }

    const languageSelect = document.getElementById('languageSelect');
    if (languageSelect) {
        languageSelect.value = currentLanguage;
    }
}

function t(key) {
    return (TRANSLATIONS[currentLanguage] && TRANSLATIONS[currentLanguage][key]) || TRANSLATIONS.it[key] || key;
}

function applyTranslations() {
    const brandSpan = document.querySelector('.logo span');
    if (brandSpan) {
        brandSpan.textContent = `WeatherApp - ${t('brandTagline')}`;
    }

    const brandTagline = document.querySelector('.brand-tagline');
    if (brandTagline) {
        brandTagline.remove();
    }

    document.title = `WeatherApp - ${t('brandTagline')}`;
    document.documentElement.lang = currentLanguage;

    const navCurrent = document.querySelector('.nav-link[data-tab="current"] span');
    const navForecast = document.querySelector('.nav-link[data-tab="forecast"] span');
    if (navCurrent) navCurrent.textContent = t('navCurrent');
    if (navForecast) navForecast.textContent = t('navForecast');

    const placeholder = document.getElementById('cityInput');
    if (placeholder) placeholder.placeholder = t('searchPlaceholder');

    const locationText = document.querySelector('#locationBtn span');
    if (locationText) locationText.textContent = t('myLocation');

    const recentTitle = document.querySelector('.search-history .history-header h3');
    if (recentTitle) recentTitle.innerHTML = `<i class="fas fa-history"></i> ${t('recentSearches')}`;

    const popularTitle = document.querySelector('.popular-cities h3');
    if (popularTitle) popularTitle.textContent = t('popularCities');

    const welcomeTitle = document.querySelector('.welcome-state h2');
    const welcomeText = document.querySelector('.welcome-state p');
    if (welcomeTitle) welcomeTitle.textContent = t('welcomeTitle');
    if (welcomeText) welcomeText.textContent = t('welcomeText');

    const feelsLikeBox = document.querySelector('.feels-like');
    if (feelsLikeBox) {
        feelsLikeBox.innerHTML = `${t('feelsLikePrefix')} <span id="feelsLike">--</span>&deg;C`;
    }

    const detailLabels = document.querySelectorAll('.detail-label');
    const detailKeys = ['windLabel', 'humidityLabel', 'visibilityLabel', 'pressureLabel', 'cloudsLabel', 'sunriseLabel', 'sunsetLabel'];
    detailLabels.forEach((label, index) => {
        const key = detailKeys[index];
        if (key) {
            label.textContent = t(key);
        }
    });

    const loadingText = document.querySelector('.loading-state p');
    if (loadingText) loadingText.textContent = t('loadingText');

    const errorTitle = document.querySelector('.error-state h2');
    const errorMessage = document.getElementById('errorMessage');
    const retryButton = document.querySelector('.retry-btn');
    if (errorTitle) errorTitle.textContent = t('errorTitle');
    if (errorMessage) errorMessage.textContent = t('errorText');
    if (retryButton) retryButton.innerHTML = `<i class="fas fa-redo"></i> ${t('retryButton')}`;

    const footerBuild = document.querySelector('.footer p:last-child');
    if (footerBuild) footerBuild.textContent = t('footerBuild');

    const footerData = document.querySelector('.footer p a')?.parentElement;
    if (footerData) {
        footerData.innerHTML = `${t('footerData')} <a href="https://openweathermap.org/" target="_blank" rel="noreferrer">OpenWeatherMap</a>`;
    }

    const photoCredit = document.getElementById('photoCredit');
    if (photoCredit && photoCredit.classList.contains('visible')) {
        const photoUrl = photoCredit.dataset.photoUrl || 'https://www.pexels.com/';
        const photographer = photoCredit.dataset.photographer || '';
        photoCredit.innerHTML = `${t('photoCredit')} <a href="${photoUrl}" target="_blank" rel="noreferrer">Pexels</a>${photographer ? ` by ${photographer}` : ''}`;
    }

    const languageSelect = document.getElementById('languageSelect');
    if (languageSelect) {
        languageSelect.value = currentLanguage;
    }
}

// Setup Event Listeners
function setupEventListeners() {
    // Search button click
    searchBtn.addEventListener('click', () => searchWeather());
    
    // Enter key in search input
    cityInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchWeather();
        }
    });
    
    // Location button click
    locationBtn.addEventListener('click', () => getLocationWeather());
    
    // Input focus/blur for suggestions
    cityInput.addEventListener('focus', () => {
        if (cityInput.value.length > 0) {
            showSuggestions();
        }
    });
    
    cityInput.addEventListener('input', () => {
        if (cityInput.value.length > 0) {
            showSuggestions();
        } else {
            hideSuggestions();
        }
    });
    
    // Click outside to close suggestions
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-container')) {
            hideSuggestions();
        }
    });
    
    // Tab navigation
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const tab = link.dataset.tab;
            switchTab(tab);
        });
    });

    const languageSelect = document.getElementById('languageSelect');
    if (languageSelect) {
        languageSelect.addEventListener('change', () => {
            currentLanguage = languageSelect.value;
            localStorage.setItem('weatherapp-language', currentLanguage);
            applyTranslations();

            if (currentCity) {
                searchWeather(currentCity, currentCountry, true);
            }
        });
    }
    
    // Clear history button
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');
    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener('click', () => {
            if (confirm('Are you sure you want to clear your search history?')) {
                clearHistory();
            }
        });
    }
    
    // Load initial history
    loadHistory();
}

// Load Popular Cities
async function loadPopularCities() {
    try {
        const response = await fetch('/api/popular-cities');
        const cities = await response.json();
        warmBackgroundVariantsForCities(cities);
        
        popularCitiesContainer.innerHTML = cities.map(city => `
            <div class="city-chip" data-city="${city.name}" data-country="${city.country}">
                ${city.display}
            </div>
        `).join('');
        
        // Add click listeners to city chips
        document.querySelectorAll('.city-chip').forEach(chip => {
            chip.addEventListener('click', () => {
                const city = chip.dataset.city;
                const country = chip.dataset.country;
                cityInput.value = city;
                searchWeather(city, country);
            });
        });
    } catch (error) {
        console.error('Error loading popular cities:', error);
    }
}

// Search Weather
async function searchWeather(city = null, country = null, silent = false) {
    const query = city || cityInput.value.trim();
    
    if (!query) {
        cityInput.focus();
        return;
    }
    
    lastSearchQuery = query;
    currentCity = query;
    currentCountry = country || null;
    showLoading();
    hideSuggestions();
    
    try {
        let url = `/api/weather?city=${encodeURIComponent(query)}&lang=${encodeURIComponent(currentLanguage)}`;
        if (country) {
            url += `&country=${encodeURIComponent(country)}`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (response.ok && data) {
            currentWeatherData = data;
            displayWeather(data);
            
            // Add to history
            addToHistory(query, country);
            
            // Load forecast as well
            loadForecast(query);
            
            // Load moon phase and fun facts
            loadMoonPhase();
            loadFunFacts(query, country);
            
            if (!silent) {
                switchTab('current');
            }
        } else {
            showError(data.error || t('errorText'));
        }
    } catch (error) {
        showError(t('errorText'));
    }
}

async function searchWeatherByCoordinates(lat, lon, label = null, silent = false) {
    lastSearchQuery = label || `${lat},${lon}`;
    showLoading();
    hideSuggestions();

    try {
        const response = await fetch(`/api/weather?lat=${encodeURIComponent(lat)}&lon=${encodeURIComponent(lon)}&lang=${encodeURIComponent(currentLanguage)}`);
        const data = await response.json();

        if (response.ok && data) {
            currentCity = data.city;
            currentCountry = data.country;
            currentWeatherData = data;
            cityInput.value = label || data.city;
            displayWeather(data);
            addToHistory(data.city, data.country);
            loadForecast(data.city);
            loadFunFacts(data.city, data.country);
            loadMoonPhase();

            if (!silent) {
                switchTab('current');
            }
        } else {
            showError(data.error || t('errorText'));
        }
    } catch (error) {
        showError(t('errorText'));
    }
}

// History Management
async function addToHistory(city, country = null) {
    try {
        const response = await fetch('/api/history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ city, country })
        });
        
        if (response.ok) {
            loadHistory();
        }
    } catch (error) {
        console.error('Error adding to history:', error);
    }
}

async function loadHistory() {
    try {
        const response = await fetch('/api/history');
        const history = await response.json();
        warmBackgroundVariantsForCities(history.map((item) => ({
            name: item.city,
            country: item.country || ''
        })));
        
        const historySection = document.getElementById('searchHistorySection');
        const historyGrid = document.getElementById('searchHistory');
        
        if (history.length > 0) {
            historySection.style.display = 'block';
            historyGrid.innerHTML = history.map(item => `
                <div class="history-item" data-city="${item.city}" data-country="${item.country || ''}">
                    <i class="fas fa-map-marker-alt"></i>
                    <span>${item.display}</span>
                    <small>${new Date(item.timestamp).toLocaleTimeString()}</small>
                </div>
            `).join('');
            
            // Add click listeners to history items
            document.querySelectorAll('.history-item').forEach(item => {
                item.addEventListener('click', () => {
                    const city = item.dataset.city;
                    const country = item.dataset.country;
                    cityInput.value = city;
                    searchWeather(city, country || null);
                });
            });
        } else {
            historySection.style.display = 'none';
        }
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

async function clearHistory() {
    try {
        const response = await fetch('/api/history', {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadHistory();
        }
    } catch (error) {
        console.error('Error clearing history:', error);
    }
}

// Moon Phase
async function loadMoonPhase() {
    try {
        const response = await fetch('/api/moon');
        const moonData = await response.json();
        
        // You could add a moon phase display section here
        console.log('Moon phase:', moonData.phase);
    } catch (error) {
        console.error('Error loading moon phase:', error);
    }
}

// Fun Facts
async function loadFunFacts(city, country) {
    try {
        let url = `/api/fun-facts?city=${encodeURIComponent(city)}&lang=${encodeURIComponent(currentLanguage)}`;
        if (country) {
            url += `&country=${encodeURIComponent(country)}`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (response.ok && data.facts && data.facts.length > 0) {
            // You could add a fun facts section here
            console.log('Fun facts:', data.facts);
        }
    } catch (error) {
        console.error('Error loading fun facts:', error);
    }
}

// Display Weather Data
function displayWeather(data) {
    // Update main weather card
    document.getElementById('cityName').textContent = data.city;
    document.getElementById('countryName').textContent = getCountryFlag(data.country) + ' ' + data.country;
    document.getElementById('timestamp').textContent = formatCityDateTime(data.timestamp_unix, data.timezone_offset);
    document.getElementById('temperature').textContent = data.temperature;
    document.getElementById('weatherDescription').textContent = capitalizeText(data.weather_description);
    document.getElementById('tempMax').textContent = data.temp_max;
    document.getElementById('tempMin').textContent = data.temp_min;
    document.getElementById('feelsLike').textContent = data.feels_like;
    
    // Weather icon
    const iconUrl = `https://openweathermap.org/img/wn/${data.weather_icon}@4x.png`;
    document.getElementById('weatherIcon').innerHTML = `<img src="${iconUrl}" alt="${data.weather_description}">`;
    
    // Weather details
    document.getElementById('windSpeed').textContent = `${data.wind_speed} m/s`;
    document.getElementById('humidity').textContent = `${data.humidity}%`;
    document.getElementById('visibility').textContent = `${data.visibility} km`;
    document.getElementById('pressure').textContent = `${data.pressure} hPa`;
    document.getElementById('clouds').textContent = `${data.clouds}%`;
    document.getElementById('sunrise').textContent = data.sunrise;
    document.getElementById('sunset').textContent = data.sunset;

    ensureLocalClockElement();
    startLocalClock(data.timezone_offset);
    
    // Update body class for weather-based background
    updateWeatherBackground(data.weather_main, data.weather_icon, data.sunrise_unix, data.sunset_unix, data.timestamp_unix, data.timezone_offset, data.city, data.country);
    
    // Show weather content
    showWeatherContent();
}

// Load Forecast
async function loadForecast(city) {
    try {
        const response = await fetch(`/api/forecast?city=${encodeURIComponent(city)}&lang=${encodeURIComponent(currentLanguage)}`);
        const data = await response.json();
        
        if (response.ok && data) {
            displayForecast(data);
        }
    } catch (error) {
        console.error('Error loading forecast:', error);
    }
}

// Display Forecast Data
function displayForecast(forecasts) {
    const container = document.getElementById('forecastContainer');
    
    container.innerHTML = forecasts.map(forecast => {
        const iconUrl = `https://openweathermap.org/img/wn/${forecast.icon}@2x.png`;
        
        return `
            <div class="forecast-card">
                <div class="forecast-date">${formatForecastDate(forecast.date)}</div>
                <div class="forecast-icon">
                    <img src="${iconUrl}" alt="${forecast.description}">
                </div>
                <div class="forecast-temp">${forecast.temp_max}&deg; / ${forecast.temp_min}&deg;</div>
                <div class="forecast-desc">${capitalizeText(forecast.description)}</div>
                <div class="forecast-details">
                    <span><i class="fas fa-temperature-high"></i> ${forecast.temperature}&deg;</span>
                    <span><i class="fas fa-tint"></i> ${forecast.humidity}%</span>
                </div>
            </div>
        `;
    }).join('');
}

// Get Location Weather
function getLocationWeather() {
    if ('geolocation' in navigator) {
        locationBtn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> <span>${t('myLocation')}</span>`;
        locationBtn.disabled = true;
        
        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const { latitude, longitude } = position.coords;
                
                try {
                    // First, get weather by coordinates
                    const response = await fetch(`/api/weather?lat=${latitude}&lon=${longitude}&lang=${encodeURIComponent(currentLanguage)}`);
                    const data = await response.json();
                    
                    if (response.ok && data) {
                        currentCity = data.city;
                        currentCountry = data.country;
                        cityInput.value = data.city;
                        displayWeather(data);
                        addToHistory(data.city, data.country);
                        loadForecast(data.city);
                        loadFunFacts(data.city, data.country);
                    } else {
                        showError(t('errorText'));
                    }
                } catch (error) {
                    showError(t('errorText'));
                } finally {
                    locationBtn.innerHTML = `<i class="fas fa-location-arrow"></i> <span>${t('myLocation')}</span>`;
                    locationBtn.disabled = false;
                }
            },
            (error) => {
                showError(t('errorText'));
                locationBtn.innerHTML = `<i class="fas fa-location-arrow"></i> <span>${t('myLocation')}</span>`;
                locationBtn.disabled = false;
            }
        );
    } else {
        showError(t('errorText'));
    }
}

// Show Suggestions
async function showSuggestions() {
    const query = cityInput.value.trim();
    
    if (query.length < 2) {
        hideSuggestions();
        return;
    }
    
    try {
        const response = await fetch(`/api/geocode?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (response.ok && data) {
            searchSuggestions.innerHTML = `
                <button type="button" class="suggestion-item" data-city="${query}" data-lat="${data.lat}" data-lon="${data.lon}">
                    <i class="fas fa-map-marker-alt"></i>
                    <span>${data.address}</span>
                </button>
            `;
            searchSuggestions.classList.add('active');
            
            const suggestion = document.querySelector('.suggestion-item');
            if (suggestion) {
                suggestion.addEventListener('pointerdown', (event) => {
                    event.preventDefault();
                    const lat = suggestion.dataset.lat;
                    const lon = suggestion.dataset.lon;
                    if (lat && lon) {
                        searchWeatherByCoordinates(lat, lon, query);
                    } else {
                        cityInput.value = query;
                        searchWeather();
                    }
                });
            }
        } else {
            hideSuggestions();
        }
    } catch (error) {
        hideSuggestions();
    }
}

// Hide Suggestions
function hideSuggestions() {
    searchSuggestions.classList.remove('active');
}

function ensureLocalClockElement() {
    const cityInfo = document.querySelector('.city-info');
    if (!cityInfo || document.getElementById('localClock')) {
        return;
    }

    const timestamp = document.getElementById('timestamp');
    const localClock = document.createElement('p');
    localClock.className = 'local-clock';
    localClock.id = 'localClock';

    if (timestamp && timestamp.parentNode) {
        timestamp.insertAdjacentElement('afterend', localClock);
    } else {
        cityInfo.appendChild(localClock);
    }
}

function formatLocalClock(offsetSeconds) {
    const now = new Date(Date.now() + Number(offsetSeconds || 0) * 1000);
    return new Intl.DateTimeFormat(currentLanguage, {
        weekday: 'short',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZone: 'UTC'
    }).format(now);
}

function startLocalClock(offsetSeconds) {
    const localClock = document.getElementById('localClock');
    if (!localClock) {
        return;
    }

    if (localClockTimer) {
        clearInterval(localClockTimer);
    }

    const prefixes = {
        it: 'Ora locale',
        en: 'Local time',
        fr: 'Heure locale',
        es: 'Hora local'
    };

    const update = () => {
        localClock.textContent = `${prefixes[currentLanguage] || prefixes.it}: ${formatLocalClock(offsetSeconds)}`;
    };

    update();
    localClockTimer = setInterval(update, 1000);
}

function formatCityDateTime(timestamp, offsetSeconds) {
    if (timestamp === null || timestamp === undefined) {
        return '--';
    }

    const localDate = new Date((Number(timestamp) + Number(offsetSeconds || 0)) * 1000);
    return new Intl.DateTimeFormat(currentLanguage, {
        dateStyle: 'medium',
        timeStyle: 'short',
        timeZone: 'UTC'
    }).format(localDate);
}

function formatForecastDate(dateString) {
    const date = new Date(`${dateString}T12:00:00Z`);
    return new Intl.DateTimeFormat(currentLanguage, {
        weekday: 'long',
        month: 'short',
        day: 'numeric',
        timeZone: 'UTC'
    }).format(date);
}

function capitalizeText(value) {
    if (!value) {
        return '--';
    }

    return value.charAt(0).toUpperCase() + value.slice(1);
}

function getLocalMinutes(timestampUnix, offsetSeconds) {
    if (timestampUnix === null || timestampUnix === undefined) {
        return null;
    }

    const localDate = new Date((Number(timestampUnix) + Number(offsetSeconds || 0)) * 1000);
    return localDate.getUTCHours() * 60 + localDate.getUTCMinutes();
}

function hashString(input) {
    return String(input || '')
        .split('')
        .reduce((hash, char) => ((hash * 31) + char.charCodeAt(0)) >>> 0, 0);
}

function normalizeBackgroundKey(value) {
    const prefixStripped = String(value || '')
        .replace(/^comune di\s+/i, '')
        .replace(/^city of\s+/i, '')
        .replace(/^municipality of\s+/i, '');
    return prefixStripped
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/\s+/g, ' ')
        .trim()
        .toLowerCase();
}

const CITY_BACKGROUND_PROFILE_LOOKUP = (() => {
    const lookup = {};

    Object.entries(CITY_BACKGROUND_PROFILES).forEach(([key, profile]) => {
        const exactKey = normalizeBackgroundKey(key);
        lookup[exactKey] = profile;

        const cityPart = normalizeBackgroundKey(String(key).split(',')[0]);
        if (cityPart && !lookup[cityPart]) {
            lookup[cityPart] = profile;
        }
    });

    return lookup;
})();

function getExistingCityBackground(city, country) {
    const key = normalizeBackgroundKey(`${city},${country}`) || normalizeBackgroundKey(city);
    const profile = CITY_BACKGROUND_PROFILE_LOOKUP[key];
    if (!profile) {
        return null;
    }

    if (profile.images && profile.images.length > 0) {
        // Return a random image from the array
        const index = Math.floor(Math.random() * profile.images.length);
        return profile.images[index];
    }

    if (profile.queries && profile.queries.length > 0) {
        // Build Unsplash URL from queries
        const urls = buildPostcardUrls(profile.queries);
        const index = Math.floor(Math.random() * urls.length);
        return urls[index];
    }

    return null;
}

function readBackgroundCache() {
    try {
        return JSON.parse(localStorage.getItem(BACKGROUND_CACHE_KEY) || '{}');
    } catch (error) {
        return {};
    }
}

function writeBackgroundCache(cache) {
    try {
        localStorage.setItem(BACKGROUND_CACHE_KEY, JSON.stringify(cache));
    } catch (error) {
        console.error('Error saving background cache:', error);
    }
}

function buildBackgroundCacheKey(scene, salt) {
    return `${scene}:${salt || 'default'}`;
}

function getCachedBackground(scene, salt) {
    const cache = readBackgroundCache();
    const key = buildBackgroundCacheKey(scene, salt);
    return cache[key] || null;
}

function setCachedBackground(scene, salt, url) {
    const cache = readBackgroundCache();
    const key = buildBackgroundCacheKey(scene, salt);
    cache[key] = url;
    writeBackgroundCache(cache);
}

function prefetchBackground(url) {
    if (!url) {
        return;
    }

    const img = new Image();
    img.decoding = 'async';
    img.loading = 'eager';
    img.src = url;
}

function warmBackgroundVariantsForCities(cities) {
    if (!Array.isArray(cities) || cities.length === 0) {
        return;
    }

    cities.forEach((city) => {
        const cityKey = getCityBackgroundKey(city.name || city.city || city.display || '', city.country || '');
        const profile = getCityBackgroundProfile(city.name || city.city || city.display || '', city.country || '');
        if (profile) {
            const profileScenes = getProfileScenePools(profile);
            Object.entries(profileScenes).forEach(([scene, images]) => {
                images.forEach((imageUrl, index) => {
                    const salt = `${cityKey}:profile:${scene}:${index}`;
                    const cached = getCachedBackground(scene, salt);
                    if (cached) {
                        prefetchBackground(cached);
                        return;
                    }
                    setCachedBackground(scene, salt, imageUrl);
                    prefetchBackground(imageUrl);
                });
            });
            return;
        }

        const scenes = ['sunny', 'clouds', 'rain', 'snow', 'night', 'storm', 'mist'];
        const saltBase = `${cityKey}`;
        scenes.forEach((scene) => {
            const salt = `${saltBase}:${scene}`;
            const cached = getCachedBackground(scene, salt);
            if (cached) {
                prefetchBackground(cached);
                return;
            }

            const imageUrl = getSceneImageUrl(scene, salt);
            setCachedBackground(scene, salt, imageUrl);
            prefetchBackground(imageUrl);
        });
    });
}

function getCityBackgroundKey(city, country) {
    return `${String(city || '').trim()},${String(country || '').trim()}`.replace(/\s+/g, ' ');
}

function getCityBackgroundProfile(city, country) {
    const exactKey = normalizeBackgroundKey(getCityBackgroundKey(city, country));
    const exactProfile = CITY_BACKGROUND_PROFILE_LOOKUP[exactKey];
    if (exactProfile) {
        return exactProfile;
    }

    const cityKey = normalizeBackgroundKey(city);
    return CITY_BACKGROUND_PROFILE_LOOKUP[cityKey] || null;
}

function getProfileScenePools(profile) {
    if (!profile || typeof profile !== 'object') {
        return {};
    }

    if (profile.scenes && typeof profile.scenes === 'object') {
        return profile.scenes;
    }

    if (Array.isArray(profile.queries) && profile.queries.length > 0) {
        return {
            sunny: buildPostcardUrls(profile.queries)
        };
    }

    if (Array.isArray(profile.images) && profile.images.length > 0) {
        return {
            sunny: profile.images
        };
    }

    return {};
}

function getSceneImageUrl(scene, salt = '', city = '', country = '') {
    const cityKey = getCityBackgroundKey(city, country);
    const profile = getCityBackgroundProfile(city, country);
    if (profile) {
        const scenePools = getProfileScenePools(profile);
        const profileImages = scenePools[scene] && scenePools[scene].length > 0
            ? scenePools[scene]
            : (scenePools.sunny && scenePools.sunny.length > 0
                ? scenePools.sunny
                : Object.values(scenePools).flat().filter(Boolean));

        if (Array.isArray(profileImages) && profileImages.length > 0) {
            const profileSalt = `${cityKey}:${scene}`;
            const cached = getCachedBackground(scene, profileSalt);
            if (cached) {
                return cached;
            }

            const index = hashString(`${cityKey}:${scene}:${salt}`) % profileImages.length;
            const selected = profileImages[index];
            setCachedBackground(scene, profileSalt, selected);
            return selected;
        }
    }

    const urls = {
        sunny: [
            'https://images.unsplash.com/photo-1500375592092-40eb2168fd21?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1493246507139-91e8fad9978e?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1473448912268-2022ce9509d8?auto=format&fit=crop&w=1600&q=85'
        ],
        clouds: [
            'https://images.unsplash.com/photo-1513151233558-d860c5398176?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1525921151707-4f14a1c8f8df?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1500740516770-92bd004b996e?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1493246318656-5bfd4cfb29b0?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1534088568595-a066f410bcda?auto=format&fit=crop&w=1600&q=85'
        ],
        rain: [
            'https://images.unsplash.com/photo-1501691223387-dd0500403073?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1455203763265-6d96f3b1f8d4?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1493314894560-5c412a56c17c?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1525920980995-f8f2e3f8f7ec?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1448317971285-3f5c1e33cb9e?auto=format&fit=crop&w=1600&q=85'
        ],
        snow: [
            'https://images.unsplash.com/photo-1489515217757-5fd1be406fef?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1515263487990-61b07816b324?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1516715094483-75da7dee9758?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1461695008884-244cb4543d74?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1516594915697-87eb3b1c14ea?auto=format&fit=crop&w=1600&q=85'
        ],
        night: [
            'https://images.unsplash.com/photo-1519608487953-e999c86e7455?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1522120693417-2b6e48c9c0d0?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=1600&q=85'
        ],
        storm: [
            'https://images.unsplash.com/photo-1500674425229-f692875b0ab7?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1506973035872-a4f23a086d50?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1534088568595-a066f410bcda?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1561484930-998b6a7b22e8?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1605727216801-e27ce1d0cc4b?auto=format&fit=crop&w=1600&q=85'
        ],
        mist: [
            'https://images.unsplash.com/photo-1505142468610-359e7d316be0?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1485236715568-ddc5ee6ca227?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1511497584788-876760111969?auto=format&fit=crop&w=1600&q=85',
            'https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1600&q=85'
        ]
    };

    const cached = getCachedBackground(scene, salt);
    if (cached) {
        return cached;
    }

    const list = urls[scene] || urls.sunny;
    const index = hashString(`${scene}:${salt}`) % list.length;
    const selected = list[index];
    setCachedBackground(scene, salt, selected);
    return selected;
}

// Switch Tab
function switchTab(tab) {
    // Update nav links
    navLinks.forEach(link => {
        link.classList.toggle('active', link.dataset.tab === tab);
    });
    
    // Update tab content
    document.getElementById('currentTab').style.display = tab === 'current' ? 'block' : 'none';
    document.getElementById('forecastTab').style.display = tab === 'forecast' ? 'block' : 'none';
}

// Show Loading State
function showLoading() {
    welcomeState.style.display = 'none';
    weatherContent.style.display = 'none';
    errorState.style.display = 'none';
    loadingState.style.display = 'block';
}

// Show Weather Content
function showWeatherContent() {
    welcomeState.style.display = 'none';
    loadingState.style.display = 'none';
    errorState.style.display = 'none';
    weatherContent.style.display = 'block';
}

// Show Error State
function showError(message) {
    welcomeState.style.display = 'none';
    loadingState.style.display = 'none';
    weatherContent.style.display = 'none';
    errorState.style.display = 'block';
    document.getElementById('errorMessage').textContent = message;
}

function updatePhotoCredit(photoData) {
    const photoCredit = document.getElementById('photoCredit');
    if (!photoCredit) {
        return;
    }

    if (photoData && photoData.source === 'pexels') {
        photoCredit.dataset.photoUrl = photoData.photo_url || '';
        photoCredit.dataset.photographer = photoData.photographer || '';
        const photographer = photoData.photographer ? ` by ${photoData.photographer}` : '';
        const link = photoData.photo_url
            ? `<a href="${photoData.photo_url}" target="_blank" rel="noreferrer">Pexels</a>`
            : `<a href="https://www.pexels.com/" target="_blank" rel="noreferrer">Pexels</a>`;
        photoCredit.innerHTML = `${t('photoCredit')} ${link}${photographer}`;
        photoCredit.classList.add('visible');
        return;
    }

    if (photoData && photoData.source === 'unsplash') {
        photoCredit.dataset.photoUrl = photoData.photo_url || '';
        photoCredit.dataset.photographer = photoData.photographer || '';
        const photographer = photoData.photographer ? ` by ${photoData.photographer}` : '';
        const link = photoData.photo_url
            ? `<a href="${photoData.photo_url}" target="_blank" rel="noreferrer">Unsplash</a>`
            : `<a href="https://unsplash.com/" target="_blank" rel="noreferrer">Unsplash</a>`;
        photoCredit.innerHTML = `${t('photoCredit')} ${link}${photographer}`;
        photoCredit.classList.add('visible');
        return;
    }

    if (photoData && photoData.source === 'loremflickr') {
        photoCredit.dataset.photoUrl = photoData.photo_url || '';
        photoCredit.dataset.photographer = photoData.photographer || '';
        const photographer = photoData.photographer ? ` by ${photoData.photographer}` : '';
        const link = photoData.photo_url
            ? `<a href="${photoData.photo_url}" target="_blank" rel="noreferrer">LoremFlickr</a>`
            : `<a href="https://loremflickr.com/" target="_blank" rel="noreferrer">LoremFlickr</a>`;
        photoCredit.innerHTML = `${t('photoCredit')} ${link}${photographer}`;
        photoCredit.classList.add('visible');
        return;
    }

    if (photoData && photoData.source === 'existing') {
        photoCredit.dataset.photographer = photoData.photographer || '';
        const photographer = photoData.photographer ? ` by ${photoData.photographer}` : '';
        photoCredit.innerHTML = `${t('photoCredit')} Existing Photos${photographer}`;
        photoCredit.classList.add('visible');
        return;
    }

    photoCredit.removeAttribute('data-photo-url');
    photoCredit.removeAttribute('data-photographer');
    photoCredit.classList.remove('visible');
    photoCredit.textContent = '';
}

async function loadPexelsBackground(city, country, fallbackUrl) {
    const token = ++backgroundPhotoRequestToken;
    const queryCity = String(city || currentCity || '').trim();
    const queryCountry = String(country || currentCountry || '').trim();

    console.log('loadPexelsBackground called with city:', queryCity, 'country:', queryCountry);

    if (!queryCity) {
        console.log('No city, returning');
        return;
    }

    try {
        const response = await fetch(
            `/api/background-photo?city=${encodeURIComponent(queryCity)}&country=${encodeURIComponent(queryCountry)}&lang=${encodeURIComponent(currentLanguage)}`
        );
        const data = await response.json();

        console.log('API response:', response.ok, data);

        if (token !== backgroundPhotoRequestToken) {
            return;
        }

        if (response.ok && data && data.image_url) {
            console.log('Setting scene image to:', data.image_url);
            prefetchBackground(data.image_url);
            document.documentElement.style.setProperty('--scene-image', `url("${data.image_url}")`);
            updatePhotoCredit(data);
            return;
        }
    } catch (error) {
        console.debug('API background unavailable, using existing photos.', error);
    }

    // Fallback to existing photos
    const existingImage = getExistingCityBackground(queryCity, queryCountry);
    console.log('Existing image:', existingImage);
    if (existingImage) {
        console.log('Setting scene image to existing:', existingImage);
        prefetchBackground(existingImage);
        document.documentElement.style.setProperty('--scene-image', `url("${existingImage}")`);
        updatePhotoCredit({ source: 'existing', photographer: 'Various', photographer_url: '#' });
        return;
    }

    if (fallbackUrl) {
        console.log('Using fallback:', fallbackUrl);
        document.documentElement.style.setProperty('--scene-image', `url("${fallbackUrl}")`);
    }
    updatePhotoCredit(null);
}

// Update Weather Background
function updateWeatherBackground(weatherMain, weatherIcon, sunriseUnix, sunsetUnix, timestampUnix, timezoneOffset, city = '', country = '') {
    // Removed weather-based scene classes to keep background dynamic based on city only
    loadPexelsBackground(city || currentCity || '', country || currentCountry || '', null);
}

// Get Country Flag Emoji
function getCountryFlag(countryCode) {
    const codePoints = countryCode
        .toUpperCase()
        .split('')
        .map(char => 127397 + char.charCodeAt(0));
    return String.fromCodePoint(...codePoints);
}

// Retry Search
function retrySearch() {
    if (lastSearchQuery) {
        cityInput.value = lastSearchQuery;
        searchWeather();
    }
}

// Make retrySearch available globally
window.retrySearch = retrySearch;
