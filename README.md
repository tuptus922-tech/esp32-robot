# 🤖 ESP32 Robot Desk Pet

Interaktywny miniaturowy robot biurkowy (Companion Pet) oparty na mikrokontrolerze **ESP32**, wyświetlaczu OLED 0.96" I2C, czujniku ruchu **MPU-6050**, podwójnym czujniku dotyku pojemnościowego do głaskania oraz pasywnym buzzerze.

Projekt zawiera pełną symulację w **Wokwi** (`diagram.json`), dzięki czemu można go uruchamiać i testować zarówno w przeglądarce, jak i na fizycznym sprzęcie.

---

## ✨ Funkcje Robota

- 👀 **Żywe, animowane oczy OLED**:
  - Płynne mruganie, naturalne zerkanie na boki, reakcja na bezczynność.
  - 5 kształtów oczu (*Standard, Cat Eyes, Cyber, Hearts, Anime*).
  - 4 motywy graficzne (*Classic, Invert/Cyber, Neon, Scanlines*).
- 🥰 **Wykrywanie gestu głaskania (Dual Capacitive Touch)**:
  - Dwa paski folii pod obudową (GPIO 32 i GPIO 33) tworzą strefy dotyku.
  - Przejechanie dłonią od czoła do tyłu głowy uruchamia **wieloetapową animację zadowolenia**:
    - Przymrużenie oczek w błogi uśmiech z rzęskami,
    - Bijące serca w oczodołach (*podwójny puls lub-dub*),
    - Uroczy pyszczek kotka `ω` i miękkie rumieńce,
    - Unoszące się serduszka i realistyczny dwufazowy mruk kota (wdech/wydech).
  - Głaskanie pod włos wywołuje zdziwioną minę z uniesioną brwią i spływającą kropelką.
- 📳 **Czujnik ruchu MPU-6050**:
  - Robot zasypia po dłuższym bezruchu i budzi się po podniesieniu lub potrząśnięciu.
- 📋 **Kafelkowe Menu Główne**:
  - Stylizowane na nowoczesne systemy (duże karty z ikonami i animowaną paginacją).
- 🍅 **Stoper Pomodoro**:
  - Wbudowany 25-minutowy czasomierz do pracy/nauki.
- 🦖 **Mini-gra Dino Jump**:
  - Zręcznościowa gra w skakanie przez przeszkody sterowana przyciskiem robota.
- 🔋 **System zasilania i baterii**:
  - Wskaźnik naładowania, animacja podłączenia ładowarki USB oraz powiadomienia o niskim stanie baterii.

---

## 📌 Schemat Połączeń (Pinout)

| Komponent | Pin modułu | Pin ESP32 | Opis |
| :--- | :--- | :--- | :--- |
| **OLED 0.96" (SSD1306)** | SDA | **GPIO 21** | Szyna danych I2C |
| | SCL | **GPIO 22** | Szyna zegara I2C |
| | VCC / GND | 3.3V / GND | Zasilanie ekranu |
| **MPU-6050 (GY-521)** | SDA | **GPIO 21** | Szyna danych I2C (wspólna z OLED) |
| | SCL | **GPIO 22** | Szyna zegara I2C (wspólna z OLED) |
| | VCC / GND | 3.3V / GND | Zasilanie czujnika |
| **Buzzer pasywny** | + (Sygnał) | **GPIO 25** | Generowanie tonów PWM |
| | - | GND | Masa |
| **Przycisk LEWO** | Pin A | **GPIO 18** | Nawigacja / Zerkanie w lewo |
| **Przycisk OK** | Pin A | **GPIO 19** | Zatwierdzenie / Wejście do menu |
| **Przycisk PRAWO** | Pin A | **GPIO 23** | Nawigacja / Zerkanie w prawo |
| **Dotyk PRZÓD (Głowa)** | Folia A | **GPIO 32** (T9) | Dotyk pojemnościowy czoło |
| **Dotyk TYŁ (Głowa)** | Folia B | **GPIO 33** (T8) | Dotyk pojemnościowy tył |

---

## 🚀 Jak uruchomić projekt

### Wymagania:
- [PlatformIO](https://platformio.org/) (jako wtyczka do VS Code lub narzędzie CLI `pio`).

### Kompilacja i wgranie na ESP32:
```bash
# Kompilacja projektu
pio run

# Wgranie kodu na podłączoną płytkę ESP32
pio run -t upload

# Otwarcie monitora portu szeregowego
pio device monitor -b 115200
```

### Uruchomienie w symulatorze Wokwi:
1. Otwórz plik `diagram.json` w edytorze z zainstalowaną wtyczką Wokwi Simulator.
2. Kliknij ikonę **Play** (Uruchom).
3. Sterowanie w symulatorze:
   - **`s`** – Potrząśnięcie (Wake up),
   - **`f`** – Dotknięcie paska dotykowego z przodu głowy,
   - **`b`** – Dotknięcie paska dotykowego z tyłu głowy (wciśnij `f`, a zaraz potem `b`, aby pogłaskać!),
   - **`ArrowLeft` / `ArrowRight` / `Enter`** – Sterowanie przyciskami robota.

---

## 🛠️ Lista części (Hardware BOM)
- 1x ESP32 DevKit v1 (ESP-WROOM-32 z USB-C lub Micro-USB)
- 1x Wyświetlacz OLED 0.96" I2C 128x64 SSD1306
- 1x Akcelerometr / Żyroskop GY-521 (MPU-6050)
- 1x Pasywny przetwornik piezoelektryczny (Passive Buzzer)
- 3x Przyciski Tact Switch (np. 6x6 mm lub 12x12 mm)
- 2x Paski folii aluminiowej / taśmy miedzianej do głaskania
- Kabelki połączeniowe dupont + płytka stykowa
