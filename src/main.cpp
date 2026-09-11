#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

#define BUZZER_PIN 25
#define CHARGER_PIN 34   // Podłączone do przełącznika USB-C (lub potencjometru)
#define SHAKE_BTN_PIN 13 // Przycisk SHAKE w Wokwi (klikasz myszką!)
#define BTN_LEFT_PIN 18  // Przycisk LEWO (niebieski)
#define BTN_OK_PIN 19    // Przycisk OK (żółty)
#define BTN_RIGHT_PIN 23 // Przycisk PRAWO (czerwony)
#define TOUCH_FRONT_PIN 32 // Pasek dotykowy A: Przód głowy (ESP32 Touch 9)
#define TOUCH_BACK_PIN  33 // Pasek dotykowy B: Tył głowy (ESP32 Touch 8)
#define TOUCH_THRESHOLD 40 // Próg detekcji zbliżenia dłoni (< 40 = dotyk)
#include <esp_system.h>

// Flagi automatycznego wykrywania środowiska i sprzętu
bool isWokwiEnvironment = false;
bool hasMpuSensor = false;

// Dynamiczna autokalibracja dotyku pojemnościowego na fizycznym ESP32
int touchBaselineFront = 75;
int touchBaselineBack = 75;
int touchThresholdFront = 40;
int touchThresholdBack = 40;

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
Adafruit_MPU6050 mpu;

// --- STANY ROBOTA ---
enum RobotState {
  STATE_SLEEP,            // Robot śpi, zamknięte oczka
  STATE_AWAKE,            // Wybudzony, mruga, reaguje na potrząsanie (po 2s)
  STATE_HAPPY_PET,        // Pogłaskany po głowie: mruczenie, serduszka, szczęśliwe oczka
  STATE_LOW_BATTERY_SAD,  // Smutne, zmęczone oczka + smutny dźwięk
  STATE_LOW_BATTERY_ICON, // Duża ikona pustej baterii z wykrzyknikiem
  STATE_DEAD_SLEEP,       // Całkowicie rozładowany (brak reakcji na potrząsanie)
  STATE_CHARGING,         // Podłączony do kabla USB-C, animacja ładowania
  STATE_MENU,             // Menu główne
  STATE_SUB_EYES,         // Wybór stylu i koloru oczu
  STATE_SUB_PC_MONITOR,   // Monitor podzespołów PC
  STATE_SUB_POMODORO,     // Czasomierz Pomodoro
  STATE_SUB_GAME          // Mini-gra Dino-Robot Jump
};

RobotState currentState = STATE_SLEEP;

// --- MOTYWY I KSZTAŁTY OCZÓW ---
enum EyeTheme {
  THEME_CLASSIC = 0,   // Białe oczy na czarnym tle
  THEME_INVERT,        // Negatyw / Cyber: Czarne oczy na białym tle
  THEME_NEON,          // Obwódka neonowa (kontur)
  THEME_SCANLINES      // Paski skanera CRT
};
const int THEME_COUNT = 4;
const char* const themeNames[] = {"Classic", "Invert", "Neon", "Scanlines"};

enum EyeShape {
  SHAPE_DEFAULT = 0,   // Standard rounded
  SHAPE_CAT,           // Cat slit eyes
  SHAPE_CYBER,         // Cyber angular
  SHAPE_HEARTS,        // Heart eyes
  SHAPE_ANIME          // Anime sparkle
};
const int SHAPE_COUNT = 5;
const char* const shapeNames[] = {"Standard", "Cat Eyes", "Cyber", "Hearts", "Anime"};

int currentTheme = THEME_CLASSIC;
int currentShape = SHAPE_DEFAULT;

// --- MAIN MENU ---
const char* const menuItems[] = {
  "1. Eye Style",
  "2. Pomodoro",
  "3. Dino Jump",
  "4. Exit Menu"
};
const int MENU_ITEMS_COUNT = 4;
int currentMenuIndex = 0;

// --- STATYSTYKI MONITOROWANIA PC ---
float pcCpu = 45.0f;
float pcRam = 58.0f;
float pcGpu = 62.0f;
float pcTemp = 56.0f;
unsigned long lastPcPacketTime = 0;

// --- CZASOMIERZ POMODORO ---
unsigned long pomodoroSecondsLeft = 25 * 60; // 25 minut
bool pomodoroRunning = false;
unsigned long lastPomodoroTick = 0;

// --- MINI-GRA DINO JUMP ---
float gamePlayerY = 44.0f;
float gamePlayerVy = 0.0f;
bool gameIsJumping = false;
int gameObstacleX = 128;
int gameObstacleW = 8;
int gameObstacleH = 12;
int gameScore = 0;
bool isGameOver = false;
unsigned long lastGameTick = 0;

// --- OBSŁUGA PRZYCISKÓW ---
bool lastBtnLeft = false, lastBtnOk = false, lastBtnRight = false;
unsigned long timeBtnLeft = 0, timeBtnOk = 0, timeBtnRight = 0;

// --- PROTOTYPY FUNKCJI ---
void soundWakeUp();
void soundSleep();
void soundSadBattery();
void soundChargerPlugged();
void soundFullyCharged();
void soundNavClick();
void soundConfirm();
void soundBack();
void soundPurr();
void soundSurprised();
void drawEyes(int eyeHeight, int offsetX = 0, int offsetY = 0);
void drawSingleEye(int x, int y, int w, int h, int shape, int theme);
void drawSleepEyes(int sleepPhase = 2);
void drawSadTiredEyes();
void drawBigEmptyBattery(bool blink);
void drawBigChargingBattery(int percent, int frame);
void drawMiniHeart(int x, int y);
void drawSmilingEye(int cx, int cy, int w, int h, int theme);
void drawHappyPetEyes(unsigned long elapsed, bool reverse = false);
void triggerHappyPet(bool reverse = false);
bool isPadTouched(int pin);
void handleTouchGestures();
void playWakeUpAnimation();
void playSleepAnimation();
void triggerShake();
void handleSerialCommands();
void turnScreenOff();
void turnScreenOn();
void drawMenuScreen();
void drawEyesSubMenu();
void drawPcMonitorScreen();
void drawPomodoroScreen();
void drawGameScreen();
void updatePcStats();
void updateGame();
void handleIdleEyes(unsigned long now);
bool isLeftPressed();
bool isOkPressed();
bool isRightPressed();

// --- CZASY I COOLDOWNY ---
unsigned long wakeUpTimestamp = 0;       // Czas ostatniego wybudzenia
unsigned long stateChangeTimestamp = 0;  // Czas wejścia w bieżący stan
unsigned long lastBlinkTime = 0;
unsigned long nextIdleActionTime = 0;    // Czas do kolejnego spojrzenia/mrugnięcia w bezczynności
unsigned long lastBatteryTick = 0;
unsigned long lastAnimTick = 0;
unsigned long lastSleepAnimTick = 0;
unsigned long lastShakeTime = 0;
unsigned long fullChargeTimestamp = 0;
int sleepAnimPhase = 2;
bool isScreenTurnedOff = false;          // Flaga całkowitego wyłączenia ekranu po 5s snu
const unsigned long WAKE_IGNORE_DURATION = 2000; // 2 sekundy ignorowania potrząsania po obudzeniu
const unsigned long SHAKE_DEBOUNCE = 600;

// --- GEST GŁASKANIA (TOUCH 32 / 33) ---
unsigned long lastTouchFrontTime = 0;
unsigned long lastTouchBackTime = 0;
unsigned long touchCooldownUntil = 0;
unsigned long happyPetStartTime = 0;
unsigned long lastPurrTick = 0;
bool isHappySurprised = false;
bool lastPadF = false;
bool lastPadB = false;

// --- BATERIA I SYMULACJA ŁADOWANIA ---
float batteryPercent = 100.0f;          // Pełna bateria (100%) - nie rozładuje się natychmiast podczas testów!
bool isUsbConnected = false;
bool wasUsbConnected = false;
int virtualUsb = -1;                    // -1: tryb automatyczny (przełącznik w Wokwi), 1: wymuszone USB ON, 0: wymuszone USB OFF
int animFrame = 0;


// ==========================================
// DŹWIĘKI (BUZZER)
// ==========================================
void soundWakeUp() {
  tone(BUZZER_PIN, 600, 80);
  delay(90);
  tone(BUZZER_PIN, 900, 80);
  delay(90);
  tone(BUZZER_PIN, 1300, 150);
}

void soundSleep() {
  tone(BUZZER_PIN, 1000, 100);
  delay(120);
  tone(BUZZER_PIN, 500, 220);
}

void soundSadBattery() {
  tone(BUZZER_PIN, 850, 180);
  delay(200);
  tone(BUZZER_PIN, 650, 180);
  delay(200);
  tone(BUZZER_PIN, 480, 220);
  delay(240);
  tone(BUZZER_PIN, 300, 400);
}

void soundChargerPlugged() {
  // Radosny dwuton jak podłączenie iPhone'a / Switcha
  tone(BUZZER_PIN, 523, 100); // C5
  delay(110);
  tone(BUZZER_PIN, 659, 100); // E5
  delay(110);
  tone(BUZZER_PIN, 784, 200); // G5
}

void soundFullyCharged() {
  tone(BUZZER_PIN, 659, 90);
  delay(100);
  tone(BUZZER_PIN, 784, 90);
  delay(100);
  tone(BUZZER_PIN, 1046, 250);
}

void soundNavClick() {
  tone(BUZZER_PIN, 1500, 20);
}

void soundConfirm() {
  tone(BUZZER_PIN, 1800, 35);
  delay(40);
  tone(BUZZER_PIN, 2400, 55);
}

void soundBack() {
  tone(BUZZER_PIN, 900, 30);
  delay(35);
  tone(BUZZER_PIN, 650, 40);
}

// Przyjemne mruczenie zadowolonego robota
void soundPurr() {
  for (int i = 0; i < 3; i++) {
    tone(BUZZER_PIN, 320, 25);
    delay(35);
    tone(BUZZER_PIN, 280, 25);
    delay(35);
  }
}

// Zaskoczony, wysoki dźwięk "bip-bip?!" przy głaskaniu pod włos
void soundSurprised() {
  tone(BUZZER_PIN, 750, 60);
  delay(70);
  tone(BUZZER_PIN, 1500, 110);
}

// ==========================================
// OBSŁUGA 3 PRZYCISKÓW (LEWO, OK, PRAWO)
// ==========================================
bool checkBtn(uint8_t pin, bool &lastState, unsigned long &lastTime) {
  unsigned long now = millis();
  bool current = (digitalRead(pin) == LOW);
  bool triggered = false;
  if (current && !lastState && (now - lastTime > 160)) {
    triggered = true;
    lastTime = now;
  }
  lastState = current;
  return triggered;
}

bool isLeftPressed()  { return checkBtn(BTN_LEFT_PIN, lastBtnLeft, timeBtnLeft); }
bool isOkPressed()    { return checkBtn(BTN_OK_PIN, lastBtnOk, timeBtnOk); }
bool isRightPressed() { return checkBtn(BTN_RIGHT_PIN, lastBtnRight, timeBtnRight); }

// ==========================================
// GRAFIKA EKRANU (OLED SSD1306)
// ==========================================

void turnScreenOff() {
  if (!isScreenTurnedOff) {
    isScreenTurnedOff = true;
    display.clearDisplay();
    display.display();
    display.ssd1306_command(SSD1306_DISPLAYOFF);
    Serial.println("[EKRAN] --> 5 sekund minelo: Ekran calkowicie zgaszony (tryb uspienia OLED).");
  }
}

void turnScreenOn() {
  if (isScreenTurnedOff) {
    isScreenTurnedOff = false;
    display.ssd1306_command(SSD1306_DISPLAYON);
    Serial.println("[EKRAN] --> Wlaczenie ekranu (OLED ON).");
  }
}

// Rysowanie pojedynczego oka z płynną animacją otwierania i zamykania powiek
void drawSingleEye(int x, int y, int w, int h, int shape, int theme) {
  uint16_t color = (theme == THEME_INVERT) ? SSD1306_BLACK : SSD1306_WHITE;
  uint16_t invColor = (theme == THEME_INVERT) ? SSD1306_WHITE : SSD1306_BLACK;

  // 1. Gdy oko jest całkowicie lub niemal całkowicie zamknięte (h <= 3)
  if (h <= 3) {
    if (shape == SHAPE_CYBER) {
      display.drawFastHLine(x, y + 1, w, color);
      display.drawFastHLine(x + 1, y, w - 2, color);
    } else if (shape == SHAPE_CAT) {
      display.drawFastHLine(x + 3, y + 1, w - 6, color);
      display.drawPixel(x + 1, y, color);
      display.drawPixel(x + 2, y + 1, color);
      display.drawPixel(x + w - 3, y + 1, color);
      display.drawPixel(x + w - 2, y, color);
    } else if (shape == SHAPE_HEARTS) {
      display.drawFastHLine(x + 2, y + 1, w / 2 - 4, color);
      display.drawFastHLine(x + w / 2 + 2, y + 1, w / 2 - 4, color);
      display.drawPixel(x + 1, y, color);
      display.drawPixel(x + w / 2 + 1, y, color);
    } else {
      display.fillRoundRect(x, y, w, max(2, h), 1, color);
    }
    return;
  }

  // 2. Kształt: STANDARD
  if (shape == SHAPE_DEFAULT) {
    int r = min(8, h / 2);
    if (theme == THEME_NEON) {
      display.drawRoundRect(x, y, w, h, r, color);
      if (w > 4 && h > 4) display.drawRoundRect(x + 1, y + 1, w - 2, h - 2, max(1, r - 1), color);
    } else {
      display.fillRoundRect(x, y, w, h, r, color);
    }
  }

  // 3. Kształt: KOCIE OCZY (CAT EYES)
  else if (shape == SHAPE_CAT) {
    int r = min(12, h / 2);
    if (theme == THEME_NEON) {
      display.drawRoundRect(x, y, w, h, r, color);
    } else {
      display.fillRoundRect(x, y, w, h, r, color);
    }
    // Źrenica zwęża się płynnie wraz ze zmianą wysokości oka
    if (h > 6) {
      int slitW = max(2, (int)(w * 0.12f));
      int slitH = max(3, h - 5);
      int slitX = x + (w - slitW) / 2;
      int slitY = y + (h - slitH) / 2;
      display.fillRoundRect(slitX, slitY, slitW, slitH, 1, invColor);
    }
  }

  // 4. Kształt: CYBER ROBOT
  else if (shape == SHAPE_CYBER) {
    if (theme == THEME_NEON) {
      display.drawRect(x, y, w, h, color);
      if (w > 4 && h > 4) display.drawRect(x + 1, y + 1, w - 2, h - 2, color);
    } else {
      display.fillRect(x, y, w, h, color);
      if (h > 8) {
        int cut = min(4, h / 4);
        display.fillTriangle(x, y, x + cut, y, x, y + cut, invColor);
        display.fillTriangle(x + w - 1, y, x + w - 1 - cut, y, x + w - 1, y + cut, invColor);
        display.fillTriangle(x, y + h - 1, x + cut, y + h - 1, x, y + h - 1 - cut, invColor);
        display.fillTriangle(x + w - 1, y + h - 1, x + w - 1 - cut, y + h - 1, x + w - 1, y + h - 1 - cut, invColor);
      }
    }
  }

  // 5. Kształt: SERDUSZKA (HEARTS)
  else if (shape == SHAPE_HEARTS) {
    if (h < 10) {
      display.fillRoundRect(x, y, w, h, 2, color);
    } else {
      int r = min(w / 4, h / 3);
      int cx1 = x + w / 4;
      int cx2 = x + 3 * w / 4;
      int cy = y + r;
      display.fillCircle(cx1, cy, r, color);
      display.fillCircle(cx2, cy, r, color);
      display.fillTriangle(x, cy + r / 2, x + w - 1, cy + r / 2, x + w / 2, y + h - 1, color);
    }
  }

  // 6. Kształt: ANIME (Z gwiazdkami i blaskiem)
  else if (shape == SHAPE_ANIME) {
    int r = min(8, h / 2);
    display.fillRoundRect(x, y, w, h, r, color);
    if (h > 10) {
      int sparkleR = max(1, min(4, h / 7));
      display.fillCircle(x + w - 8, y + (h * 0.28f), sparkleR, invColor);
      if (h > 18) {
        display.fillCircle(x + 8, y + (h * 0.72f), max(1, sparkleR - 2), invColor);
      }
    }
  }

  // Efekt Scanlines (linie skanera CRT)
  if (theme == THEME_SCANLINES && h > 5) {
    for (int line = y + 2; line < y + h; line += 3) {
      display.drawFastHLine(x, line, w, invColor);
    }
  }
}

// Oczy z regulowaną wysokością i pozycją (do patrzenia w lewo/prawo)
void drawEyes(int eyeHeight, int offsetX, int offsetY) {
  display.clearDisplay();
  if (currentTheme == THEME_INVERT) {
    display.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, SSD1306_WHITE);
  }
  int eyeY = 32 - (eyeHeight / 2) + offsetY;
  int leftX = constrain(24 + offsetX, 0, 96);
  int rightX = constrain(72 + offsetX, 32, 96);

  drawSingleEye(leftX, eyeY, 32, eyeHeight, currentShape, currentTheme);
  drawSingleEye(rightX, eyeY, 32, eyeHeight, currentShape, currentTheme);
  display.display();
}

// Sekwencja wybudzania: powolne otwieranie -> lewo -> prawo -> mruganie -> środek
void playWakeUpAnimation() {
  // 1. Zaspany początek - cichy niski ton
  tone(BUZZER_PIN, 450, 90);

  // Powolne otwieranie oczu
  int openSteps[] = {4, 8, 14, 22, 30, 36};
  for (int h : openSteps) {
    drawEyes(h, 0, 0);
    delay(80);
  }
  delay(120);

  // Przetarcie oczek / zaspany blink
  drawEyes(16, 0, 0);
  tone(BUZZER_PIN, 700, 80);
  delay(100);
  drawEyes(36, 0, 0);
  delay(250);

  // 2. Ogląda się w LEWO
  tone(BUZZER_PIN, 900, 70);
  drawEyes(36, -14, 0); // Spojrzenie w lewo
  delay(450);

  // Krótkie spojrzenie przez środek
  drawEyes(36, 0, 0);
  delay(100);

  // 3. Ogląda się w PRAWO
  tone(BUZZER_PIN, 1100, 70);
  drawEyes(36, 14, 0); // Spojrzenie w prawo
  delay(450);

  // Powrót na środek
  drawEyes(36, 0, 0);
  delay(180);

  // 4. Mruga kilka razy
  // Mrugnięcie 1
  drawEyes(6, 0, 0);
  delay(60);
  drawEyes(36, 0, 0);
  delay(120);

  // Mrugnięcie 2
  drawEyes(2, 0, 0);
  delay(60);
  drawEyes(36, 0, 0);
  delay(100);

  // Mrugnięcie 3 (szybkie)
  drawEyes(8, 0, 0);
  delay(50);
  drawEyes(36, 0, 0);

  // 5. Radosny finałowy dźwięk pełnego wybudzenia (oczka na środku)
  tone(BUZZER_PIN, 1200, 80);
  delay(90);
  tone(BUZZER_PIN, 1500, 160);
  delay(160);
}

// Organiczne rozglądanie się w lewo i prawo oraz mruganie w stanie bezczynności
void handleIdleEyes(unsigned long now) {
  if (now < nextIdleActionTime) return;

  // Kolejna losowa akcja za 2.4 do 4.8 sekundy
  nextIdleActionTime = now + random(2400, 4800);

  int action = random(0, 5);

  if (action == 0) {
    // 1. Zwykłe pojedyncze mrugnięcie
    drawEyes(14, 0, 0);
    delay(50);
    drawEyes(2, 0, 0);
    delay(60);
    drawEyes(14, 0, 0);
    delay(50);
    drawEyes(36, 0, 0);
  } else if (action == 1) {
    // 2. Słodkie podwójne mrugnięcie
    drawEyes(4, 0, 0);
    delay(50);
    drawEyes(36, 0, 0);
    delay(80);
    drawEyes(6, 0, 0);
    delay(50);
    drawEyes(36, 0, 0);
  } else if (action == 2) {
    // 3. Spojrzenie z zaciekawieniem w LEWO
    drawEyes(36, -8, 0);
    delay(40);
    drawEyes(36, -15, 0);
    delay(600);
    // Mały blink z okiem w lewo
    drawEyes(8, -15, 0);
    delay(50);
    drawEyes(36, -15, 0);
    delay(300);
    // Płynny powrót na środek
    drawEyes(36, -7, 0);
    delay(40);
    drawEyes(36, 0, 0);
  } else if (action == 3) {
    // 4. Spojrzenie z zaciekawieniem w PRAWO
    drawEyes(36, 8, 0);
    delay(40);
    drawEyes(36, 15, 0);
    delay(600);
    // Mały blink z okiem w prawo
    drawEyes(8, 15, 0);
    delay(50);
    drawEyes(36, 15, 0);
    delay(300);
    // Płynny powrót na środek
    drawEyes(36, 7, 0);
    delay(40);
    drawEyes(36, 0, 0);
  } else if (action == 4) {
    // 5. Rozglądnięcie się w obie strony: lewo -> środek -> prawo -> powrót
    drawEyes(36, -14, 0);
    delay(420);
    drawEyes(36, 0, 0);
    delay(80);
    drawEyes(36, 14, 0);
    delay(420);
    drawEyes(36, 0, 0);
  }
}

// Zamknięte oczka (sen) z animowanymi literkami snu
void drawSleepEyes(int sleepPhase) {
  display.clearDisplay();
  if (currentTheme == THEME_INVERT) {
    display.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, SSD1306_WHITE);
  }
  uint16_t textColor = (currentTheme == THEME_INVERT) ? SSD1306_BLACK : SSD1306_WHITE;

  // Rysowanie zamkniętych oczu zgodnie z wybranym kształtem i motywem
  drawSingleEye(24, 32, 32, 2, currentShape, currentTheme);
  drawSingleEye(72, 32, 32, 2, currentShape, currentTheme);

  display.setTextSize(1);
  display.setTextColor(textColor);

  // Animowane literki snu "z Z Z"
  if (sleepPhase >= 0) {
    display.setCursor(102, 18);
    display.print("z");
  }
  if (sleepPhase >= 1) {
    display.setCursor(110, 10);
    display.print("Z");
  }
  if (sleepPhase >= 2) {
    display.setCursor(118, 3);
    display.print("Z");
  }

  display.display();
}

// Piękna, urocza sekwencja zasypiania
void playSleepAnimation() {
  // 1. Ziewnięcie - miękki, opadający ton
  tone(BUZZER_PIN, 750, 140);
  delay(150);
  tone(BUZZER_PIN, 520, 240);

  // Stopniowe opadanie powiek (ciężkie powieki)
  int droopSteps[] = {32, 26, 20, 14, 8};
  for (int h : droopSteps) {
    drawEyes(h, 0, 0);
    delay(90);
  }
  delay(160);

  // 2. Próba walki ze snem - lekkie otwarcie oczu z westchnieniem
  tone(BUZZER_PIN, 580, 80);
  drawEyes(18, 0, 0);
  delay(220);

  // Ostateczne powolne opadnięcie do wąskich kresek
  int closeSteps[] = {14, 10, 6, 3};
  for (int h : closeSteps) {
    drawEyes(h, 0, 0);
    delay(110);
  }
  delay(120);

  // 3. Spokojne zamknięcie oczu (same powieki)
  drawSleepEyes(-1);

  // Cichy, kołysankowy ton zasypiania
  tone(BUZZER_PIN, 380, 300);
  delay(350);

  // 4. Krok po kroku pojawiają się unoszące literki "z", "Z", "Z"
  drawSleepEyes(0);
  delay(350);
  drawSleepEyes(1);
  delay(350);
  drawSleepEyes(2);
  delay(300);
}

// Rysowanie małego serduszka 5x5 px
void drawMiniHeart(int x, int y) {
  display.fillCircle(x - 1, y - 1, 1, SSD1306_WHITE);
  display.fillCircle(x + 1, y - 1, 1, SSD1306_WHITE);
  display.drawPixel(x, y - 1, SSD1306_WHITE);
  display.fillTriangle(x - 2, y, x + 2, y, x, y + 3, SSD1306_WHITE);
}

// Rysowanie uroczych, uśmiechniętych oczek łukowych (Happy Squint Eyes)
void drawSmilingEye(int cx, int cy, int w, int h, int theme) {
  uint16_t color = (theme == THEME_INVERT) ? SSD1306_BLACK : SSD1306_WHITE;
  uint16_t invColor = (theme == THEME_INVERT) ? SSD1306_WHITE : SSD1306_BLACK;

  int r = min(12, h / 2);
  display.fillRoundRect(cx - w / 2, cy - h / 2, w, h, r, color);
  display.fillRoundRect(cx - w / 2 + 2, cy - h / 2 + 4, w - 4, h, r, invColor);

  // Słodkie rzęski w kącikach
  if (cx < 64) {
    display.drawLine(cx - w / 2, cy, cx - w / 2 - 2, cy - 3, color);
  } else {
    display.drawLine(cx + w / 2 - 1, cy, cx + w / 2 + 1, cy - 3, color);
  }
}

// Piękna, organiczna i ekspresyjna animacja zadowolenia po pogłaskaniu robota
void drawHappyPetEyes(unsigned long elapsed, bool reverse) {
  display.clearDisplay();

  // Obsługa tła dla motywu Invert
  if (currentTheme == THEME_INVERT) {
    display.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, SSD1306_WHITE);
  }

  uint16_t fgColor = (currentTheme == THEME_INVERT) ? SSD1306_BLACK : SSD1306_WHITE;
  uint16_t bgColor = (currentTheme == THEME_INVERT) ? SSD1306_WHITE : SSD1306_BLACK;

  if (reverse) {
    // ==========================================
    // GEST POD WŁOS: ZDZIWIENIE I ZAKŁOPOTANIE
    // ==========================================
    int pupilOffset = (int)(sin(elapsed / 45.0f) * 3.5f);
    int eyeY = 14;

    // Wielkie, szeroko otwarte, zdziwione oczy robota
    drawSingleEye(18, eyeY, 34, 38, SHAPE_DEFAULT, currentTheme);
    drawSingleEye(76, eyeY, 34, 38, SHAPE_DEFAULT, currentTheme);

    // Drgające ze zdziwienia źrenice
    display.fillCircle(35 + pupilOffset, eyeY + 19, 5, bgColor);
    display.fillCircle(93 + pupilOffset, eyeY + 19, 5, bgColor);

    // Uniesione brwi zdziwienia nad oczami
    display.drawLine(20, eyeY - 4, 48, eyeY - 8, fgColor);
    display.drawLine(20, eyeY - 5, 48, eyeY - 9, fgColor);
    display.drawLine(108, eyeY - 4, 80, eyeY - 8, fgColor);
    display.drawLine(108, eyeY - 5, 80, eyeY - 9, fgColor);

    // Znak zapytania nad środkiem głowy
    display.setTextSize(1);
    display.setTextColor(fgColor);
    display.setCursor(62, 4);
    display.print("?");

    // Animowana spływająca kropla potu / zakłopotania z boku
    int dropY = 18 + ((elapsed / 60) % 20);
    display.fillCircle(116, dropY, 2, fgColor);
    display.fillTriangle(116, dropY - 3, 114, dropY, 118, dropY, fgColor);

  } else {
    // ==========================================
    // GEST W PRZÓD: BŁOGOŚĆ, MRUCZENIE, SERDUSZKA
    // ==========================================

    // Delikatne, organiczne kołysanie główki (oddychanie szczęściem)
    int bounce = (int)(sin(elapsed / 130.0f) * 2.5f);
    int eyeCenterY = 28 + bounce;

    // FAZA 1 (0 - 900 ms): Błogie zmrużenie oczu w urocze łuki uśmiechu
    if (elapsed < 900) {
      int squintW = 32;
      int squintH = map(elapsed, 0, 900, 26, 16);
      drawSmilingEye(36, eyeCenterY, squintW, squintH, currentTheme);
      drawSmilingEye(92, eyeCenterY, squintW, squintH, currentTheme);
    }
    // FAZA 2 (900 - 2700 ms): Czysta miłość - pulsujące serca w oczach (bicie serca: lub-dub)
    else if (elapsed < 2700) {
      int beatCycle = elapsed % 650;
      float pulseScale = 0.0f;
      if (beatCycle < 140) {
        pulseScale = sin((beatCycle / 140.0f) * 3.14159f) * 5.5f;
      } else if (beatCycle >= 200 && beatCycle < 340) {
        pulseScale = sin(((beatCycle - 200) / 140.0f) * 3.14159f) * 3.5f;
      }

      int hw = 28 + (int)pulseScale;
      int hh = 28 + (int)pulseScale;

      drawSingleEye(36 - hw / 2, eyeCenterY - hh / 2, hw, hh, SHAPE_HEARTS, currentTheme);
      drawSingleEye(92 - hw / 2, eyeCenterY - hh / 2, hw, hh, SHAPE_HEARTS, currentTheme);
    }
    // FAZA 3 (2700 - 3300 ms): Łagodne otwieranie oczu i powrót do wybranego kształtu
    else {
      int openH = map(elapsed, 2700, 3300, 16, 36);
      drawSingleEye(20, eyeCenterY - openH / 2, 32, openH, currentShape, currentTheme);
      drawSingleEye(76, eyeCenterY - openH / 2, 32, openH, currentShape, currentTheme);
    }

    // UROCZY PYSZCZEK KOTKA / ANIME "ω" POD OCZKAMI:
    int mouthY = 46 + bounce;
    display.drawCircle(61, mouthY, 3, fgColor);
    display.drawCircle(67, mouthY, 3, fgColor);
    display.fillRect(57, mouthY - 4, 15, 4, bgColor); // obcięcie góry by powstało "w"

    // RUMIEŃCE (BLUSH) NA POLICZKACH - 3 miękkie skośne kreseczki z każdej strony:
    display.drawLine(14, 43 + bounce, 17, 39 + bounce, fgColor);
    display.drawLine(19, 43 + bounce, 22, 39 + bounce, fgColor);
    display.drawLine(24, 43 + bounce, 27, 39 + bounce, fgColor);

    display.drawLine(101, 43 + bounce, 104, 39 + bounce, fgColor);
    display.drawLine(106, 43 + bounce, 109, 39 + bounce, fgColor);
    display.drawLine(111, 43 + bounce, 114, 39 + bounce, fgColor);

    // UNOSZĄCE SIĘ MINI-SERDUSZKA WOKÓŁ GŁOWY (Pływająca trajektoria):
    int h1Prog = (elapsed / 38) % 36;
    int h2Prog = ((elapsed + 450) / 38) % 36;
    int h1Y = 32 - h1Prog;
    int h2Y = 32 - h2Prog;
    int h1X = 14 + (int)(sin(h1Prog / 3.0f) * 4.0f);
    int h2X = 114 - (int)(sin(h2Prog / 3.0f) * 4.0f);
    if (h1Y > 2 && h1Y < 46) drawMiniHeart(h1X, h1Y);
    if (h2Y > 2 && h2Y < 46) drawMiniHeart(h2X, h2Y);
  }

  display.display();
}

// Smutne, zmęczone oczka (opadnięte powieki)
void drawSadTiredEyes() {
  display.clearDisplay();
  // Lewe oko ze ściętym górnym zewnętrznym rogiem
  display.fillRoundRect(24, 26, 32, 18, 4, SSD1306_WHITE);
  display.fillTriangle(24, 26, 46, 26, 24, 38, SSD1306_BLACK);

  // Prawe oko ze ściętym górnym zewnętrznym rogiem
  display.fillRoundRect(72, 26, 32, 18, 4, SSD1306_WHITE);
  display.fillTriangle(82, 26, 104, 26, 104, 38, SSD1306_BLACK);

  // Mała łezka zmęczenia
  display.fillCircle(112, 46, 2, SSD1306_WHITE);
  display.fillTriangle(112, 42, 110, 46, 114, 46, SSD1306_WHITE);
  
  display.display();
}

// Duża ikona pustej baterii z wykrzyknikiem zamiast oczu
void drawBigEmptyBattery(bool blink) {
  display.clearDisplay();
  
  // Obrys dużej baterii (wyśrodkowana)
  display.drawRoundRect(28, 8, 64, 30, 4, SSD1306_WHITE);
  display.drawRoundRect(29, 9, 62, 28, 3, SSD1306_WHITE);
  
  // Cypelek bieguna dodatniego (+)
  display.fillRoundRect(92, 16, 5, 14, 2, SSD1306_WHITE);

  if (blink) {
    // Duży wykrzyknik na środku baterii
    display.fillRect(58, 14, 4, 11, SSD1306_WHITE);
    display.fillRect(58, 28, 4, 4, SSD1306_WHITE);

    // Cienki migający pasek 3px z lewej
    display.fillRect(34, 13, 3, 20, SSD1306_WHITE);
  }

  // Czysty, wyśrodkowany napis "LOW BATTERY"
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(31, 46);
  display.print("LOW BATTERY");
  
  display.display();
}

// Ikona ostrego, wyrazistego pioruna 16x24 px w pamięci PROGMEM
const unsigned char PROGMEM lightning_bolt_16x24[] = {
  0x00, 0x30, 0x00, 0x70, 0x00, 0xF0, 0x01, 0xF0,
  0x03, 0xF0, 0x07, 0xF0, 0x0F, 0xF0, 0x1F, 0xF0,
  0x3F, 0xF0, 0x7F, 0xFF, 0x01, 0xFF, 0x03, 0xFE,
  0x07, 0xFC, 0x0F, 0xF8, 0x1F, 0xF0, 0x3F, 0xE0,
  0x7F, 0xC0, 0xFF, 0x00, 0xFE, 0x00, 0xFC, 0x00,
  0xF8, 0x00, 0xF0, 0x00, 0xE0, 0x00, 0xC0, 0x00
};

// Nowoczesna, dynamiczna animacja ładowania przez USB-C
void drawBigChargingBattery(int percent, int frame) {
  display.clearDisplay();

  // 1. Obrys dużej baterii (szerokość 74, wysokość 32, zaokrąglona)
  display.drawRoundRect(22, 6, 74, 32, 4, SSD1306_WHITE);
  display.drawRoundRect(23, 7, 72, 30, 3, SSD1306_WHITE);
  display.fillRoundRect(96, 14, 5, 16, 2, SSD1306_WHITE); // cypelek (+)

  // 2. Pięć dynamicznych segmentów energii wewnątrz baterii
  int filledSegments = percent / 20; // 0 do 5
  int waveStep = frame % 6;          // fala energii 0..5

  for (int i = 0; i < 5; i++) {
    int segX = 26 + (i * 13);
    int segY = 10;
    int segW = 10;
    int segH = 24;

    // Segment świeci jeśli osiągnięto dany poziom lub płynie przez niego fala
    bool isLit = (i < filledSegments) || (i <= waveStep && percent < 100);

    if (isLit) {
      display.fillRoundRect(segX, segY, segW, segH, 2, SSD1306_WHITE);
    }
  }

  // 3. Piorun ładowania ⚡ - wyrazisty, ostry, z czarną obwódką (halo)
  int boltX = 51;
  int boltY = 10;

  // Czarna obwódka (1px maska dookoła), by piorun idealnie odcinał się od białych słupków
  display.drawBitmap(boltX - 1, boltY, lightning_bolt_16x24, 16, 24, SSD1306_BLACK);
  display.drawBitmap(boltX + 1, boltY, lightning_bolt_16x24, 16, 24, SSD1306_BLACK);
  display.drawBitmap(boltX, boltY - 1, lightning_bolt_16x24, 16, 24, SSD1306_BLACK);
  display.drawBitmap(boltX, boltY + 1, lightning_bolt_16x24, 16, 24, SSD1306_BLACK);
  display.drawBitmap(boltX - 1, boltY - 1, lightning_bolt_16x24, 16, 24, SSD1306_BLACK);
  display.drawBitmap(boltX + 1, boltY - 1, lightning_bolt_16x24, 16, 24, SSD1306_BLACK);
  display.drawBitmap(boltX - 1, boltY + 1, lightning_bolt_16x24, 16, 24, SSD1306_BLACK);
  display.drawBitmap(boltX + 1, boltY + 1, lightning_bolt_16x24, 16, 24, SSD1306_BLACK);

  // Świecący, ostry biały piorun
  display.drawBitmap(boltX, boltY, lightning_bolt_16x24, 16, 24, SSD1306_WHITE);

  // Animowane iskry energii wokół pioruna
  if (frame % 2 == 0) {
    display.drawPixel(boltX - 3, boltY + 8, SSD1306_WHITE);
    display.drawPixel(boltX + 18, boltY + 15, SSD1306_WHITE);
  } else {
    display.drawPixel(boltX - 2, boltY + 16, SSD1306_WHITE);
    display.drawPixel(boltX + 17, boltY + 7, SSD1306_WHITE);
  }

  // 4. Pasek postępu pod baterią
  display.drawRoundRect(22, 42, 74, 6, 2, SSD1306_WHITE);
  int progressW = map(percent, 0, 100, 0, 70);
  if (progressW > 0) {
    display.fillRect(24, 44, progressW, 2, SSD1306_WHITE);
  }

  // 5. Tekst statusu na dole ekranu
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  if (percent >= 100) {
    display.setCursor(20, 53);
    display.print("100% FULL CHARGED!");
  } else {
    display.setCursor(24, 53);
    const char* dots[] = {"   ", ".  ", ".. ", "..."};
    display.printf("CHARGING %d%% %s", percent, dots[frame % 4]);
  }

  display.display();
}

// ==========================================
// EKRANY MENU I PODSYSTEMÓW
// ==========================================

// Ekran Menu Głównego - Styl kafelkowy Bruce Firmware (jeden duży kafelek, karuzela)
void drawMenuScreen() {
  display.clearDisplay();

  // 1. Górny wskaźnik strony: np. [1 / 5]
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(49, 0);
  display.printf("[%d/%d]", currentMenuIndex + 1, MENU_ITEMS_COUNT);

  // Boczne strzałki przełączania kafelków (◄ i ►)
  display.fillTriangle(3, 31, 7, 27, 7, 35, SSD1306_WHITE);
  display.fillTriangle(124, 31, 120, 27, 120, 35, SSD1306_WHITE);

  // 2. Duży centralny Kafelek (Card) z zaokrąglonymi rogami
  display.drawRoundRect(11, 9, 106, 44, 5, SSD1306_WHITE);
  display.drawRoundRect(12, 10, 104, 42, 4, SSD1306_WHITE);

  // 3. Ikona, Tytuł i Podtytuł dla bieżącego kafelka
  int cx = 64;

  if (currentMenuIndex == 0) {
    // KAFELEK 1: EYE STYLE & THEMES
    display.drawRoundRect(cx - 13, 13, 11, 13, 3, SSD1306_WHITE);
    display.fillRoundRect(cx - 11, 15, 7, 9, 2, SSD1306_WHITE);
    display.drawRoundRect(cx + 3, 13, 11, 13, 3, SSD1306_WHITE);
    display.fillRoundRect(cx + 5, 15, 7, 9, 2, SSD1306_WHITE);

    display.setTextSize(1);
    display.setCursor(cx - 27, 29);
    display.print("EYE STYLE");

    display.setCursor(cx - 45, 40);
    display.print("Shapes & Themes");
  } else if (currentMenuIndex == 1) {
    // KAFELEK 2: POMODORO TIMER
    display.drawCircle(cx, 18, 7, SSD1306_WHITE);
    display.drawFastHLine(cx - 2, 10, 5, SSD1306_WHITE);
    display.drawFastVLine(cx, 10, 2, SSD1306_WHITE);
    display.drawLine(cx, 18, cx, 14, SSD1306_WHITE);
    display.drawLine(cx, 18, cx + 4, 18, SSD1306_WHITE);

    display.setTextSize(1);
    display.setCursor(cx - 24, 29);
    display.print("POMODORO");

    display.setCursor(cx - 45, 40);
    display.print("25m Focus Timer");
  } else if (currentMenuIndex == 2) {
    // KAFELEK 3: MINI GAME DINO ROBOT
    display.drawRoundRect(cx - 12, 13, 24, 11, 3, SSD1306_WHITE);
    display.drawFastHLine(cx - 9, 18, 5, SSD1306_WHITE);
    display.drawFastVLine(cx - 7, 16, 5, SSD1306_WHITE);
    display.drawPixel(cx + 5, 16, SSD1306_WHITE);
    display.drawPixel(cx + 8, 19, SSD1306_WHITE);

    display.setTextSize(1);
    display.setCursor(cx - 27, 29);
    display.print("DINO JUMP");

    display.setCursor(cx - 48, 40);
    display.print("Mini Arcade Game");
  } else if (currentMenuIndex == 3) {
    // KAFELEK 4: EXIT TO FACE
    display.drawRoundRect(cx - 10, 13, 20, 12, 3, SSD1306_WHITE);
    display.drawPixel(cx - 5, 17, SSD1306_WHITE);
    display.drawPixel(cx + 4, 17, SSD1306_WHITE);
    display.drawLine(cx - 4, 21, cx + 3, 21, SSD1306_WHITE);

    display.setTextSize(1);
    display.setCursor(cx - 12, 29);
    display.print("EXIT");

    display.setCursor(cx - 42, 40);
    display.print("Return to Face");
  }

  // 4. Kropki nawigacyjne paginacji na dole ekranu (styl Bruce firmware)
  int startDotX = 64 - ((MENU_ITEMS_COUNT - 1) * 8) / 2;
  for (int i = 0; i < MENU_ITEMS_COUNT; i++) {
    int dotX = startDotX + (i * 8);
    if (i == currentMenuIndex) {
      display.fillCircle(dotX, 58, 2, SSD1306_WHITE);
    } else {
      display.drawCircle(dotX, 58, 2, SSD1306_WHITE);
    }
  }

  display.display();
}

// Ekran wyboru stylu i motywu oczek
void drawEyesSubMenu() {
  display.clearDisplay();

  // Nagłówek
  display.fillRect(0, 0, 128, 11, SSD1306_WHITE);
  display.setTextColor(SSD1306_BLACK, SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(13, 2);
  display.print("EYE STYLE & THEME");

  // Podgląd obu oczek w wybranym stylu i motywie na środku
  drawSingleEye(36, 14, 24, 20, currentShape, currentTheme);
  drawSingleEye(68, 14, 24, 20, currentShape, currentTheme);

  // Etykiety wyboru
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(2, 38);
  display.printf("[<]Theme: %s", themeNames[currentTheme]);

  display.setCursor(2, 47);
  display.printf("[>]Shape: %s", shapeNames[currentShape]);

  // Stopka
  display.drawFastHLine(0, 56, 128, SSD1306_WHITE);
  display.setCursor(16, 57);
  display.print("[OK] Save & Exit");
  display.display();
}

// Aktualizacja danych monitora PC (symulacja lub dane z USB)
void updatePcStats() {
  unsigned long now = millis();
  if (now - lastPcPacketTime > 2500) {
    pcCpu = 40.0f + 25.0f * sin(now / 1800.0f) + 12.0f * cos(now / 600.0f);
    pcCpu = constrain(pcCpu, 8.0f, 98.0f);
    pcRam = 54.0f + 6.0f * sin(now / 4500.0f);
    pcGpu = 45.0f + 32.0f * sin(now / 2200.0f);
    pcGpu = constrain(pcGpu, 12.0f, 99.0f);
    pcTemp = 48.0f + (pcGpu * 0.22f);
  }
}

// Ekran monitora parametrów PC
void drawPcMonitorScreen() {
  display.clearDisplay();

  // Nagłówek
  display.fillRect(0, 0, 128, 11, SSD1306_WHITE);
  display.setTextColor(SSD1306_BLACK, SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(4, 2);
  display.print("PC MONITOR");
  display.setCursor(76, 2);
  display.print("[OK:Back]");

  display.setTextColor(SSD1306_WHITE);

  // 1. CPU Bar
  display.setCursor(2, 14);
  display.print("CPU");
  display.drawRoundRect(24, 14, 66, 8, 2, SSD1306_WHITE);
  int cpuW = map((int)pcCpu, 0, 100, 0, 62);
  if (cpuW > 0) display.fillRect(26, 16, cpuW, 4, SSD1306_WHITE);
  display.setCursor(94, 14);
  display.printf("%2.0f%%", pcCpu);

  // 2. RAM Bar
  display.setCursor(2, 26);
  display.print("RAM");
  display.drawRoundRect(24, 26, 66, 8, 2, SSD1306_WHITE);
  int ramW = map((int)pcRam, 0, 100, 0, 62);
  if (ramW > 0) display.fillRect(26, 28, ramW, 4, SSD1306_WHITE);
  display.setCursor(94, 26);
  display.printf("%2.0f%%", pcRam);

  // 3. GPU Bar
  display.setCursor(2, 38);
  display.print("GPU");
  display.drawRoundRect(24, 38, 66, 8, 2, SSD1306_WHITE);
  int gpuW = map((int)pcGpu, 0, 100, 0, 62);
  if (gpuW > 0) display.fillRect(26, 40, gpuW, 4, SSD1306_WHITE);
  display.setCursor(94, 38);
  display.printf("%2.0f%%", pcGpu);

  // 4. Stopka
  display.drawFastHLine(0, 49, 128, SSD1306_WHITE);
  display.setCursor(10, 53);
  display.printf("Temp:%.0fC  RAM:%.1fG", pcTemp, (pcRam / 100.0f) * 16.0f);

  display.display();
}

// Ekran czasomierza Pomodoro
void drawPomodoroScreen() {
  display.clearDisplay();

  // Nagłówek
  display.fillRect(0, 0, 128, 11, SSD1306_WHITE);
  display.setTextColor(SSD1306_BLACK, SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(22, 2);
  display.print("POMODORO TIMER");

  // Zegar cyfrowy
  int mins = pomodoroSecondsLeft / 60;
  int secs = pomodoroSecondsLeft % 60;
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(34, 18);
  display.printf("%02d:%02d", mins, secs);

  // Status
  display.setTextSize(1);
  if (pomodoroSecondsLeft == 0) {
    display.setCursor(22, 38);
    display.print("* TIME'S UP! *");
  } else if (pomodoroRunning) {
    display.setCursor(31, 38);
    display.print("[ RUNNING ]");
  } else {
    display.setCursor(34, 38);
    display.print("[ PAUSED ]");
  }

  // Stopka
  display.drawFastHLine(0, 50, 128, SSD1306_WHITE);
  display.setCursor(2, 54);
  display.print(pomodoroRunning ? "<Pause" : "<Start");
  display.setCursor(44, 54);
  display.print("[OK:Back]");
  display.setCursor(102, 54);
  display.print(">Rst");
  display.display();
}

// Aktualizacja logiki mini-gry
void updateGame() {
  unsigned long now = millis();
  if (now - lastGameTick < 35) return;
  lastGameTick = now;

  if (!isGameOver) {
    // Fizyka skoku
    if (gameIsJumping) {
      gamePlayerVy += 0.65f;
      gamePlayerY += gamePlayerVy;
      if (gamePlayerY >= 44.0f) {
        gamePlayerY = 44.0f;
        gamePlayerVy = 0.0f;
        gameIsJumping = false;
      }
    }

    // Przeszkoda
    gameObstacleX -= 3;
    if (gameObstacleX < -10) {
      gameObstacleX = 130 + random(0, 30);
      gameScore++;
      tone(BUZZER_PIN, 1800, 15);
    }

    // Kolizja
    int obsY = 54 - gameObstacleH;
    if (gameObstacleX < 26 && (gameObstacleX + gameObstacleW) > 16) {
      if ((gamePlayerY + 10) > obsY) {
        isGameOver = true;
        tone(BUZZER_PIN, 300, 300);
      }
    }
  }
}

// Rysowanie mini-gry
void drawGameScreen() {
  display.clearDisplay();

  // Linia ziemi
  display.drawFastHLine(0, 54, 128, SSD1306_WHITE);

  if (isGameOver) {
    display.setTextSize(2);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(12, 6);
    display.print("GAME OVER");

    display.setTextSize(1);
    display.setCursor(26, 25);
    display.printf("SCORE: %d PTS", gameScore);

    display.setCursor(19, 36);
    display.print("[OK] Play Again");
    display.setCursor(16, 46);
    display.print("[<] Back to Menu");
  } else {
    // Wynik
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(2, 2);
    display.print("[<] Exit");
    display.setCursor(76, 2);
    display.printf("PTS: %d", gameScore);

    // Gracz: mini robot z oczkami i antenką
    int px = 16;
    int py = (int)gamePlayerY;
    display.drawRoundRect(px, py, 10, 10, 2, SSD1306_WHITE);
    display.drawPixel(px + 2, py + 3, SSD1306_WHITE);
    display.drawPixel(px + 7, py + 3, SSD1306_WHITE);
    display.drawLine(px + 2, py + 10, px + 2, py + 11, SSD1306_WHITE);
    display.drawLine(px + 7, py + 10, px + 7, py + 11, SSD1306_WHITE);

    // Przeszkoda
    int obsY = 54 - gameObstacleH;
    display.fillRect(gameObstacleX, obsY, gameObstacleW, gameObstacleH, SSD1306_WHITE);
    display.drawPixel(gameObstacleX + 1, obsY - 1, SSD1306_WHITE);
    display.drawPixel(gameObstacleX + gameObstacleW - 2, obsY - 1, SSD1306_WHITE);
  }

  display.display();
}


// ==========================================
// OBSŁUGA POLECEŃ SERIAL (WOKWI TERMINAL)
// ==========================================
String inputBuffer = "";

void processCommand(String cmd) {
  cmd.trim();
  cmd.toLowerCase();
  if (cmd.length() == 0) return;

  if (cmd == "shake") {
    Serial.println("[KONSOLA] Symulacja potrzasniecia robota!");
    triggerShake();
  } else if (cmd.startsWith("bat ")) {
    int val = cmd.substring(4).toInt();
    val = constrain(val, 0, 100);
    batteryPercent = val;
    Serial.printf("[KONSOLA] Ustawiono poziom baterii na: %d%%\n", val);
  } else if (cmd == "usb on" || cmd == "charge") {
    virtualUsb = 1;
    Serial.println("[KONSOLA] Wymuszono podlaczenie USB-C (ON)!");
  } else if (cmd == "usb off" || cmd == "discharge") {
    virtualUsb = 0;
    Serial.println("[KONSOLA] Wymuszono odlaczenie USB-C (OFF)!");
  } else if (cmd == "usb auto") {
    virtualUsb = -1;
    Serial.println("[KONSOLA] Sterowanie USB z powrotem przelacznikiem Wokwi!");
  } else if (cmd == "menu") {
    turnScreenOn();
    currentState = STATE_MENU;
    currentMenuIndex = 0;
    drawMenuScreen();
    Serial.println("[KONSOLA] Otwarto Menu główne!");
  } else if (cmd.startsWith("pc")) {
    // np: pc cpu=45 ram=60 gpu=70 temp=52
    int cPos = cmd.indexOf("cpu=");
    if (cPos != -1) pcCpu = constrain(cmd.substring(cPos + 4).toFloat(), 0.0f, 100.0f);
    int rPos = cmd.indexOf("ram=");
    if (rPos != -1) pcRam = constrain(cmd.substring(rPos + 4).toFloat(), 0.0f, 100.0f);
    int gPos = cmd.indexOf("gpu=");
    if (gPos != -1) pcGpu = constrain(cmd.substring(gPos + 4).toFloat(), 0.0f, 100.0f);
    int tPos = cmd.indexOf("temp=");
    if (tPos != -1) pcTemp = constrain(cmd.substring(tPos + 5).toFloat(), 0.0f, 120.0f);
    lastPcPacketTime = millis();
    Serial.printf("[PC] Zaktualizowano parametry: CPU=%.0f%% RAM=%.0f%% GPU=%.0f%% TEMP=%.0fC\n", pcCpu, pcRam, pcGpu, pcTemp);
  } else if (cmd == "pet" || cmd == "glaskaj") {
    Serial.println("[KONSOLA] Symulacja poglaskania robota (Przod -> Tyl)!");
    triggerHappyPet(false);
  } else if (cmd == "pet rev" || cmd == "pet_rev") {
    Serial.println("[KONSOLA] Symulacja poglaskania pod wlos (Tyl -> Przod)!");
    triggerHappyPet(true);
  } else if (cmd == "touch") {
    int df = digitalRead(TOUCH_FRONT_PIN);
    int db = digitalRead(TOUCH_BACK_PIN);
    Serial.println("--- ODCZYT CZUJNIKOW DOTYKU (TOUCH) ---");
    if (!isWokwiEnvironment) {
      int tf = touchRead(TOUCH_FRONT_PIN);
      int tb = touchRead(TOUCH_BACK_PIN);
      Serial.printf("Pasek A (Przod - GPIO %d): Odczyt=%d | Prog=%d | Baza=%d -> %s\n",
                    TOUCH_FRONT_PIN, tf, touchThresholdFront, touchBaselineFront,
                    (tf < touchThresholdFront || df == LOW) ? "[DOTKNIETY!]" : "wolny");
      Serial.printf("Pasek B (Tyl   - GPIO %d): Odczyt=%d | Prog=%d | Baza=%d -> %s\n",
                    TOUCH_BACK_PIN, tb, touchThresholdBack, touchBaselineBack,
                    (tb < touchThresholdBack || db == LOW) ? "[DOTKNIETY!]" : "wolny");
    } else {
      Serial.printf("Pasek A (Przod - GPIO %d): Stan=%s (klawisz 'f')\n", TOUCH_FRONT_PIN, (df == LOW) ? "[DOTKNIETY!]" : "wolny");
      Serial.printf("Pasek B (Tyl   - GPIO %d): Stan=%s (klawisz 'b')\n", TOUCH_BACK_PIN, (db == LOW) ? "[DOTKNIETY!]" : "wolny");
      Serial.println("(Tryb Wokwi: bezpieczna symulacja cyfrowa bez crashujacego touchRead)");
    }
  } else if (cmd == "calib") {
    if (!isWokwiEnvironment) {
      Serial.println("[KALIBRACJA] Kalibrowanie czujnikow dotykowych...");
      long sumF = 0, sumB = 0;
      for (int i = 0; i < 20; i++) {
        sumF += touchRead(TOUCH_FRONT_PIN);
        sumB += touchRead(TOUCH_BACK_PIN);
        delay(10);
      }
      touchBaselineFront = sumF / 20;
      touchBaselineBack = sumB / 20;
      if (touchBaselineFront > 15) touchThresholdFront = (int)(touchBaselineFront * 0.65f);
      else touchThresholdFront = 40;
      if (touchBaselineBack > 15) touchThresholdBack = (int)(touchBaselineBack * 0.65f);
      else touchThresholdBack = 40;
      Serial.printf("[KALIBRACJA] Gotowe! Przod: prog=%d, baza=%d | Tyl: prog=%d, baza=%d\n",
                    touchThresholdFront, touchBaselineFront, touchThresholdBack, touchBaselineBack);
    } else {
      Serial.println("[KALIBRACJA] Niedostepne w symulatorze Wokwi.");
    }
  } else if (cmd == "status") {
    Serial.println("--- STATUS ROBOTA ---");
    Serial.printf("Bateria: %.1f%%\n", batteryPercent);
    Serial.printf("USB-C: %s\n", isUsbConnected ? "PODLACZONE" : "ODLACZONE");
    Serial.printf("Ekran OLED: %s\n", isScreenTurnedOff ? "WYLACZONY (USPIONY)" : "WLACZONY");
    Serial.printf("Motyw oczu: %s | Ksztalt: %s\n", themeNames[currentTheme], shapeNames[currentShape]);
    Serial.print("Stan: ");
    switch (currentState) {
      case STATE_SLEEP: Serial.println("SLEEP (spi)"); break;
      case STATE_AWAKE: Serial.println("AWAKE (wybudzony)"); break;
      case STATE_HAPPY_PET: Serial.println("HAPPY_PET (glaskany / mruczy)"); break;
      case STATE_LOW_BATTERY_SAD: Serial.println("LOW_BATTERY_SAD (smutne oczy)"); break;
      case STATE_LOW_BATTERY_ICON: Serial.println("LOW_BATTERY_ICON (ikona pustej baterii)"); break;
      case STATE_DEAD_SLEEP: Serial.println("DEAD_SLEEP (rozladowany)"); break;
      case STATE_CHARGING: Serial.println("CHARGING (ladowanie)"); break;
      case STATE_MENU: Serial.println("MENU (menu glowne)"); break;
      case STATE_SUB_EYES: Serial.println("SUB_EYES (wybor oczu)"); break;
      case STATE_SUB_PC_MONITOR: Serial.println("SUB_PC_MONITOR (monitor PC)"); break;
      case STATE_SUB_POMODORO: Serial.println("SUB_POMODORO (stoper pomodoro)"); break;
      case STATE_SUB_GAME: Serial.println("SUB_GAME (gra dino robot)"); break;
    }
  } else if (cmd == "help") {
    Serial.println("Dostepne polecenia:");
    Serial.println("  pet        - poglaskaj robota (animacja zadowolenia + mruczenie)");
    Serial.println("  pet rev    - poglaskaj robota pod wlos (zdziwienie)");
    Serial.println("  touch      - sprawdz odczyty pinow dotykowych GPIO 32 i 33");
    Serial.println("  calib      - skalibruj czujniki dotyku (tylko fizyczny ESP32)");
    Serial.println("  menu       - otwiera menu na ekranie");
    Serial.println("  shake      - potrzasnij robotem (budzi lub usypia)");
    Serial.println("  bat <0-100>- zmien poziom baterii (np. bat 15)");
    Serial.println("  usb on/off - podlacz / odlacz kabel USB-C");
    Serial.println("  status     - wyswietl aktualne parametry");
  } else {
    Serial.printf("Nieznane polecenie: '%s'. Wpisz 'help'.\n", cmd.c_str());
  }
}

void handleSerialCommands() {
  while (Serial.available() > 0) {
    char c = (char)Serial.read();

    if (c == '\r' || c == '\n') {
      if (inputBuffer.length() > 0) {
        Serial.println();
        processCommand(inputBuffer);
        inputBuffer = "";
        Serial.print("robot> ");
      }
    } else if (c == '\b' || (uint8_t)c == 127) {
      if (inputBuffer.length() > 0) {
        inputBuffer.remove(inputBuffer.length() - 1);
        Serial.print("\b \b");
      }
    } else if (c >= 32 && c <= 126) {
      inputBuffer += c;
      Serial.print(c); // Natychmiastowe echo znaku do terminala
    }
  }
}

// ==========================================
// OBSŁUGA POTRZĄŚNIĘCIA
// ==========================================
void triggerShake() {
  unsigned long now = millis();
  if (now - lastShakeTime < SHAKE_DEBOUNCE) return;
  lastShakeTime = now;

  // 1. Jeśli robot jest całkowicie rozładowany -> BRAK REAKCJI
  if (currentState == STATE_DEAD_SLEEP || currentState == STATE_LOW_BATTERY_ICON) {
    Serial.println("[ROBOT] Bateria rozładowana! Robot nie ma energii, by się obudzić.");
    return;
  }

  // 2. Jeśli robot się ładuje -> nie usypiaj go potrząsaniem
  if (currentState == STATE_CHARGING) {
    Serial.println("[ROBOT] Robot aktualnie się ładuje przez USB-C.");
    return;
  }

  // 3. Jeśli robot śpi -> WYBUDŹ GO
  if (currentState == STATE_SLEEP) {
    turnScreenOn();
    Serial.println("[ROBOT] --> WYBUDZANIE! Robot wstaje...");
    currentState = STATE_AWAKE;
    stateChangeTimestamp = now;
    playWakeUpAnimation();
    wakeUpTimestamp = millis(); // 2-sekundowa ochrona startuje od momentu pełnego otwarcia oczu!
    return;
  }

  // 4. Jeśli robot jest wybudzony
  if (currentState == STATE_AWAKE) {
    unsigned long timeSinceWake = now - wakeUpTimestamp;
    
    // Warunek: Przez 2 sekundy ignoruj kolejne potrząsanie!
    if (timeSinceWake < WAKE_IGNORE_DURATION) {
      Serial.printf("[ROBOT] Ignorowanie potrząsania (okres ochronny: %lu ms / 2000 ms)\n", timeSinceWake);
      return;
    }

    // Po 2 sekundach -> kolejne potrząśnięcie go USYPIA
    Serial.println("[ROBOT] --> USYPIANIE! Potrząśnięto po upływie 2s - robot idzie spać.");
    currentState = STATE_SLEEP;
    playSleepAnimation();
    stateChangeTimestamp = millis(); // 5 sekund odliczania do całkowitego wyłączenia ekranu
    isScreenTurnedOff = false;
  }
}

// ==========================================
// OBSŁUGA GESTU GŁASKANIA (TOUCH PINS 32 i 33)
// ==========================================

bool isPadTouched(int pin) {
  if (!isWokwiEnvironment) {
    // Sprzętowy odczyt pojemnościowy ESP32 dla pasków folii
    int val = touchRead(pin);
    int thresh = (pin == TOUCH_FRONT_PIN) ? touchThresholdFront : touchThresholdBack;
    if (val > 0 && val < thresh) return true;
  }
  // Odczyt cyfrowy (dla Wokwi oraz fizycznych przycisków / zwarcia do GND)
  if (digitalRead(pin) == LOW) return true;
  return false;
}

void triggerHappyPet(bool reverse) {
  // Jeśli robot jest rozładowany lub się ładuje, nie reaguj
  if (currentState == STATE_DEAD_SLEEP || currentState == STATE_LOW_BATTERY_ICON || currentState == STATE_CHARGING) {
    return;
  }

  turnScreenOn();
  currentState = STATE_HAPPY_PET;
  happyPetStartTime = millis();
  isHappySurprised = reverse;
  stateChangeTimestamp = happyPetStartTime;
  lastPurrTick = 0;

  if (reverse) {
    Serial.println("[ROBOT] --> Pogłaskano pod włos! Robot jest zdziwiony 😲");
    soundSurprised();
  } else {
    Serial.println("[ROBOT] --> Pogłaskano po głowie! Robot mruczy z zadowolenia 🥰");
    tone(BUZZER_PIN, 1600, 40);
  }

  // Natychmiast narysuj pierwszą klatkę animacji szczęścia na ekranie!
  drawHappyPetEyes(0, reverse);
}

void handleTouchGestures() {
  unsigned long now = millis();
  if (now < touchCooldownUntil) return;

  // Głaskać można gdy robot jest wybudzony (AWAKE) LUB gdy śpi (SLEEP)
  if (currentState != STATE_AWAKE && currentState != STATE_SLEEP) return;

  bool touchF = isPadTouched(TOUCH_FRONT_PIN);
  bool touchB = isPadTouched(TOUCH_BACK_PIN);

  // 1. Dotknięcie paska przedniego (Touch F / czoło)
  if (touchF && !lastPadF) {
    Serial.println("[TOUCH] >>> Pasek PRZOD (Touch F / GPIO 32) dotkniety! <<<");
    // Sprawdzamy czy tył był dotknięty w ciągu ostatnich 2500 ms (Tył -> Przód = Reverse)
    if (lastTouchBackTime > 0 && (now - lastTouchBackTime <= 2500)) {
      Serial.println("[GEST] --> Wykryto gest pod wlos (Tyl -> Przod)! Zdziwienie!");
      triggerHappyPet(true);
      lastTouchFrontTime = 0;
      lastTouchBackTime = 0;
      touchCooldownUntil = now + 1500;
      lastPadF = touchF;
      lastPadB = touchB;
      return;
    } else {
      lastTouchFrontTime = now;
      // Natychmiastowa reakcja na pojedynczy dotyk czoła: dźwięk + spojrzenie w górę
      tone(BUZZER_PIN, 1400, 30);
      drawEyes(24, 0, -4);
    }
  }

  // 2. Dotknięcie paska tylnego (Touch B / kark)
  if (touchB && !lastPadB) {
    Serial.println("[TOUCH] >>> Pasek TYL (Touch B / GPIO 33) dotkniety! <<<");
    // Sprawdzamy czy przód był dotknięty w ciągu ostatnich 2500 ms (Przód -> Tył = Normal Pet)
    if (lastTouchFrontTime > 0 && (now - lastTouchFrontTime <= 2500)) {
      Serial.println("[GEST] --> Wykryto pelny gest glaskania (Przod -> Tyl)! Mruczenie!");
      triggerHappyPet(false);
      lastTouchFrontTime = 0;
      lastTouchBackTime = 0;
      touchCooldownUntil = now + 1500;
      lastPadF = touchF;
      lastPadB = touchB;
      return;
    } else {
      lastTouchBackTime = now;
      // Natychmiastowa reakcja na pojedynczy dotyk tyłu: dźwięk + spojrzenie w bok
      tone(BUZZER_PIN, 1100, 30);
      drawEyes(24, 0, 4);
    }
  }

  // Wygaszenie starych zdarzeń dotyku po 2500 ms
  if (lastTouchFrontTime > 0 && (now - lastTouchFrontTime > 2500)) lastTouchFrontTime = 0;
  if (lastTouchBackTime > 0 && (now - lastTouchBackTime > 2500)) lastTouchBackTime = 0;

  lastPadF = touchF;
  lastPadB = touchB;
}

// ==========================================
// SETUP
// ==========================================
void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);

  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(CHARGER_PIN, INPUT);
  pinMode(SHAKE_BTN_PIN, INPUT_PULLUP);
  pinMode(BTN_LEFT_PIN, INPUT_PULLUP);
  pinMode(BTN_OK_PIN, INPUT_PULLUP);
  pinMode(BTN_RIGHT_PIN, INPUT_PULLUP);
  pinMode(TOUCH_FRONT_PIN, INPUT_PULLUP);
  pinMode(TOUCH_BACK_PIN, INPUT_PULLUP);

  // 1. Wykrywanie srodowiska (Wokwi vs Fizyczny ESP32)
  uint8_t mac[6];
  esp_efuse_mac_get_default(mac);
  if (mac[0] == 0x24 && mac[1] == 0x0a && mac[2] == 0xc4 && mac[3] == 0x00 && mac[4] == 0x01 && mac[5] == 0x10) {
    isWokwiEnvironment = true;
    Serial.println("[SYSTEM] Srodowisko: Symulator Wokwi");
  } else {
    isWokwiEnvironment = false;
    Serial.printf("[SYSTEM] Srodowisko: FIZYCZNY ESP32 (MAC: %02X:%02X:%02X:%02X:%02X:%02X)\n",
                  mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
  }

  // 2. Ekran OLED SSD1306 (probuje 0x3C, a jak nie ma to 0x3D)
  bool oledOk = display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  if (!oledOk) {
    oledOk = display.begin(SSD1306_SWITCHCAPVCC, 0x3D);
  }
  if (!oledOk) {
    Serial.println("\n[BLAD KRYTYCZNY] Nie wykryto ekranu SSD1306 (0x3C ani 0x3D)!");
    Serial.println("-> Sprawdz kable: SDA->GPIO 21, SCL->GPIO 22, VCC->3.3V, GND->GND\n");
  } else {
    Serial.println("[OLED] Ekran SSD1306 128x64 dziala poprawnie!");
  }

  // 3. Czujnik MPU6050 (0x68 lub 0x69, nie blokuje startu w razie braku)
  hasMpuSensor = mpu.begin(0x68);
  if (!hasMpuSensor) {
    hasMpuSensor = mpu.begin(0x69);
  }
  if (!hasMpuSensor) {
    Serial.println("[MPU6050] Brak czujnika zyr/acc (wybudzanie przyciskami LEWO/OK/PRAWO).");
  } else {
    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
    Serial.println("[MPU6050] Czujnik ruchu MPU6050 dziala poprawnie!");
  }

  // 4. Autokalibracja paskow dotykowych na fizycznym ESP32
  if (!isWokwiEnvironment) {
    long sumF = 0, sumB = 0;
    for (int i = 0; i < 15; i++) {
      sumF += touchRead(TOUCH_FRONT_PIN);
      sumB += touchRead(TOUCH_BACK_PIN);
      delay(10);
    }
    touchBaselineFront = sumF / 15;
    touchBaselineBack = sumB / 15;
    if (touchBaselineFront > 15) touchThresholdFront = (int)(touchBaselineFront * 0.65f);
    else touchThresholdFront = 40;
    if (touchBaselineBack > 15) touchThresholdBack = (int)(touchBaselineBack * 0.65f);
    else touchThresholdBack = 40;

    Serial.printf("[DOTYK] Autokalibracja: Przod (prog=%d, baza=%d), Tyl (prog=%d, baza=%d)\n",
                  touchThresholdFront, touchBaselineFront, touchThresholdBack, touchBaselineBack);
  }

  // 5. Inicjalizacja zasilania i start robota
  if (isWokwiEnvironment) {
    delay(50);
    int rawCharger = analogRead(CHARGER_PIN);
    isUsbConnected = (rawCharger > 2000);
    wasUsbConnected = isUsbConnected;
    if (isUsbConnected) {
      currentState = STATE_CHARGING;
      fullChargeTimestamp = millis();
    } else {
      currentState = STATE_SLEEP;
      stateChangeTimestamp = millis();
      isScreenTurnedOff = false;
      drawSleepEyes(2);
    }
  } else {
    // Na fizycznym ESP32 robot startuje od razu na biurku (100% zasilany z USB)
    isUsbConnected = true;
    wasUsbConnected = true;
    batteryPercent = 100.0f;
    currentState = STATE_AWAKE;
    wakeUpTimestamp = millis();
    stateChangeTimestamp = millis();
    isScreenTurnedOff = false;
    drawEyes(36, 0, 0);
    soundWakeUp();
  }

  Serial.println("\n==============================================");
  Serial.println("       DESK BUDDY ROBOT URUCHOMIONY!         ");
  Serial.println(" Wpisz 'help' w konsoli, aby zobaczyc komendy ");
  Serial.println("==============================================\n");
  Serial.print("robot> ");
}

// ==========================================
// LOOP
// ==========================================
void loop() {
  unsigned long now = millis();

  // 1. Obsługa poleceń z konsoli Wokwi Terminal
  handleSerialCommands();

  // 1b. Odczyt 3 przycisków fizycznych (LEWO, OK, PRAWO)
  bool btnLeftHit = isLeftPressed();
  bool btnOkHit = isOkPressed();
  bool btnRightHit = isRightPressed();

  // 2. Odczyt stanu zasilania / ładowania USB-C
  if (isWokwiEnvironment) {
    int rawCharger = analogRead(CHARGER_PIN);
    bool physicalUsbOn = (rawCharger > 2000);
    if (virtualUsb == 1) {
      isUsbConnected = true;
    } else if (virtualUsb == 0) {
      isUsbConnected = false;
    } else {
      isUsbConnected = physicalUsbOn;
    }
  } else {
    // Na fizycznym ESP32: zasilany z portu USB
    if (virtualUsb == 0) isUsbConnected = false;
    else isUsbConnected = true;
  }

  // Wykrycie momentu podłączenia kabla USB-C
  if (isUsbConnected && !wasUsbConnected) {
    Serial.println("\n[USB-C] --> PODLACZONO KABEL USB-C! Ladowanie startuje...");
    turnScreenOn();
    wasUsbConnected = true;
    currentState = STATE_CHARGING;
    stateChangeTimestamp = now;
    fullChargeTimestamp = now;
    soundChargerPlugged();
  } else if (!isUsbConnected && wasUsbConnected) {
    Serial.println("\n[USB-C] --> ODLACZONO KABEL USB-C!");
    wasUsbConnected = false;
    if (currentState == STATE_CHARGING) {
      if (batteryPercent > 20.0f) {
        currentState = STATE_AWAKE;
        wakeUpTimestamp = now;
        stateChangeTimestamp = now;
        drawEyes(36, 0, 0);
      } else {
        currentState = STATE_DEAD_SLEEP;
        stateChangeTimestamp = now;
        drawSleepEyes(2);
      }
    }
  }

  // 3. Obsługa akcelerometru MPU6050 (fizyczne potrząsanie)
  bool mpuShake = false;
  if (hasMpuSensor) {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    float totalAccel = sqrt(a.acceleration.x * a.acceleration.x +
                            a.acceleration.y * a.acceleration.y +
                            a.acceleration.z * a.acceleration.z);
    if (totalAccel > 15.0) {
      mpuShake = true;
    }
  }

  // Wstrząs gdy przeciążenie > 15 m/s² LUB wciśnięto zielony przycisk SHAKE
  bool buttonShake = (digitalRead(SHAKE_BTN_PIN) == LOW);
  if (mpuShake || buttonShake) {
    triggerShake();
  }

  // 3b. Obsługa gestów dotykowych (głaskanie obudowy robota)
  handleTouchGestures();

  // 4. Maszyna stanów i obsługa baterii / menu
  switch (currentState) {
    
    // --- ROBOT ŚPI ---
    case STATE_SLEEP:
      // Kliknięcie dowolnego z 3 przycisków również wybudza robota!
      if (btnOkHit || btnLeftHit || btnRightHit) {
        turnScreenOn();
        Serial.println("[ROBOT] Wybudzenie przyciskiem!");
        currentState = STATE_AWAKE;
        stateChangeTimestamp = now;
        playWakeUpAnimation();
        wakeUpTimestamp = millis();
        break;
      }

      if (!isScreenTurnedOff) {
        if (now - stateChangeTimestamp > 5000) {
          // Po 5 sekundach od uśpienia / 2. potrząśnięcia ekranik całkowicie gaśnie i się wyłącza!
          turnScreenOff();
        } else {
          // Przez pierwsze 5 sekund po uśpieniu: animacja spokojnego oddechu i literek "z Z Z" co 750 ms
          if (now - lastSleepAnimTick > 750) {
            lastSleepAnimTick = now;
            sleepAnimPhase = (sleepAnimPhase + 1) % 3;
            drawSleepEyes(sleepAnimPhase);
          }
        }
      }

      // Rozładowywanie baterii w spoczynku (tylko w symulatorze Wokwi przy odłączonym kablu)
      if (isWokwiEnvironment && !isUsbConnected && (now - lastBatteryTick > 6000)) {
        lastBatteryTick = now;
        if (batteryPercent > 0) batteryPercent -= 1.0f;
        if (batteryPercent < 15.0f) {
          turnScreenOn();
          currentState = STATE_LOW_BATTERY_SAD;
          stateChangeTimestamp = now;
        }
      }
      break;

    // --- ROBOT WYBUDZONY ---
    case STATE_AWAKE:
      // Wciśnięcie przycisku OK otwiera MENU GŁÓWNE!
      if (btnOkHit) {
        soundConfirm();
        currentState = STATE_MENU;
        currentMenuIndex = 0;
        drawMenuScreen();
        break;
      }
      // W zwykłym trybie czuwania przyciski LEWO/PRAWO nie zmieniają motywu/kształtu (tylko w Menu!)
      // Zamiast tego robot interaktywnie zerka w lewo lub w prawo:
      if (btnLeftHit) {
        soundNavClick();
        drawEyes(36, -14, 0);
        delay(160);
        drawEyes(36, 0, 0);
      }
      if (btnRightHit) {
        soundNavClick();
        drawEyes(36, 14, 0);
        delay(160);
        drawEyes(36, 0, 0);
      }

      // Rozładowywanie podczas aktywności (tylko w symulatorze Wokwi przy odłączonym kablu)
      if (isWokwiEnvironment && !isUsbConnected && (now - lastBatteryTick > 1500)) {
        lastBatteryTick = now;
        if (batteryPercent > 0) batteryPercent -= 1.0f;
        Serial.printf("[BATERIA] Pozostalo: %.0f%%\n", batteryPercent);

        // Wykrycie niskiego stanu baterii (< 20%)
        if (batteryPercent < 20.0f) {
          Serial.println("\n--> [UWAGA] BATERIA NA WYCZERPANIU! Robot jest zmeczony...");
          currentState = STATE_LOW_BATTERY_SAD;
          stateChangeTimestamp = now;
          drawSadTiredEyes();
          soundSadBattery();
          break;
        }
      }

      // Organiczne rozglądanie się w lewo i prawo oraz mruganie w stanie bezczynności
      handleIdleEyes(now);
      break;

    // --- ROBOT POGŁASKANY (MRUCZENIE I SERDUSZKA) ---
    case STATE_HAPPY_PET: {
      unsigned long cur = millis();
      if (cur < happyPetStartTime) happyPetStartTime = cur;
      unsigned long elapsed = cur - happyPetStartTime;

      if (elapsed > 3300) {
        // Po 3.3 sekundy wróć do normalnej twarzy robota
        currentState = STATE_AWAKE;
        wakeUpTimestamp = cur;
        stateChangeTimestamp = cur;
        drawEyes(36, 0, 0);
        break;
      }

      // Realistyczny, dwufazowy dźwięk mruczenia kota (wdech i wydech: cykl 600 ms)
      if (!isHappySurprised) {
        int purrPhase = elapsed % 600;
        if (purrPhase < 260 && (now - lastPurrTick > 45)) {
          lastPurrTick = now;
          int f = 260 + (purrPhase / 4);
          tone(BUZZER_PIN, f, 28);
        } else if (purrPhase >= 320 && purrPhase < 560 && (now - lastPurrTick > 45)) {
          lastPurrTick = now;
          int f = 320 - ((purrPhase - 320) / 4);
          tone(BUZZER_PIN, f, 28);
        }
      }

      // Kliknięcie OK otwiera menu również stąd
      if (btnOkHit) {
        soundConfirm();
        currentState = STATE_MENU;
        currentMenuIndex = 0;
        drawMenuScreen();
        break;
      }

      // Rysowanie animacji zadowolenia na ekranie
      drawHappyPetEyes(elapsed, isHappySurprised);
      break;
    }

    // --- MENU GŁÓWNE ---
    case STATE_MENU:
      if (btnLeftHit) {
        currentMenuIndex = (currentMenuIndex - 1 + MENU_ITEMS_COUNT) % MENU_ITEMS_COUNT;
        soundNavClick();
        drawMenuScreen();
      }
      if (btnRightHit) {
        currentMenuIndex = (currentMenuIndex + 1) % MENU_ITEMS_COUNT;
        soundNavClick();
        drawMenuScreen();
      }
      if (btnOkHit) {
        soundConfirm();
        if (currentMenuIndex == 0) {
          currentState = STATE_SUB_EYES;
          drawEyesSubMenu();
        } else if (currentMenuIndex == 1) {
          currentState = STATE_SUB_POMODORO;
          drawPomodoroScreen();
        } else if (currentMenuIndex == 2) {
          currentState = STATE_SUB_GAME;
          isGameOver = false;
          gameScore = 0;
          gamePlayerY = 44.0f;
          gamePlayerVy = 0.0f;
          gameObstacleX = 130;
          drawGameScreen();
        } else if (currentMenuIndex == 3) {
          // Powrót do oczek
          currentState = STATE_AWAKE;
          wakeUpTimestamp = now;
          drawEyes(36, 0, 0);
        }
      }
      break;

    // --- PODEKRAN: STYL I MOTYW OCZU ---
    case STATE_SUB_EYES:
      if (btnLeftHit) {
        currentTheme = (currentTheme + 1) % THEME_COUNT;
        soundNavClick();
        drawEyesSubMenu();
      }
      if (btnRightHit) {
        currentShape = (currentShape + 1) % SHAPE_COUNT;
        soundNavClick();
        drawEyesSubMenu();
      }
      if (btnOkHit) {
        soundConfirm();
        currentState = STATE_MENU;
        drawMenuScreen();
      }
      break;

    // --- PODEKRAN: MONITOR PODZESPOŁÓW PC ---
    case STATE_SUB_PC_MONITOR:
      updatePcStats();
      if (now - lastAnimTick > 150) {
        lastAnimTick = now;
        drawPcMonitorScreen();
      }
      if (btnOkHit || btnLeftHit) {
        soundBack();
        currentState = STATE_MENU;
        drawMenuScreen();
      }
      break;

    // --- PODEKRAN: POMODORO / STOPER ---
    case STATE_SUB_POMODORO:
      if (btnLeftHit) {
        pomodoroRunning = !pomodoroRunning;
        soundConfirm();
        drawPomodoroScreen();
      }
      if (btnRightHit) {
        pomodoroSecondsLeft = 25 * 60;
        pomodoroRunning = false;
        soundNavClick();
        drawPomodoroScreen();
      }
      if (btnOkHit) {
        soundBack();
        currentState = STATE_MENU;
        drawMenuScreen();
      }
      if (pomodoroRunning && (now - lastPomodoroTick >= 1000)) {
        lastPomodoroTick = now;
        if (pomodoroSecondsLeft > 0) {
          pomodoroSecondsLeft--;
          if (pomodoroSecondsLeft == 0) {
            pomodoroRunning = false;
            tone(BUZZER_PIN, 1000, 150);
            delay(180);
            tone(BUZZER_PIN, 1500, 300);
          }
        }
        drawPomodoroScreen();
      }
      break;

    // --- PODEKRAN: MINI-GRA DINO ROBOT ---
    case STATE_SUB_GAME:
      if (btnLeftHit) {
        soundBack();
        currentState = STATE_MENU;
        drawMenuScreen();
        break;
      }
      if (btnOkHit || btnRightHit) {
        if (isGameOver) {
          isGameOver = false;
          gameScore = 0;
          gamePlayerY = 44.0f;
          gamePlayerVy = 0.0f;
          gameObstacleX = 130;
          soundConfirm();
        } else if (!gameIsJumping) {
          gamePlayerVy = -5.6f;
          gameIsJumping = true;
          tone(BUZZER_PIN, 1200, 25);
        }
      }
      updateGame();
      drawGameScreen();
      break;

    // --- FAZA 1: SMUTNE, ZMĘCZONE OCZKA ---
    case STATE_LOW_BATTERY_SAD:
      drawSadTiredEyes();
      // Po 2.5 sekundzie smutnych oczu pokazujemy dużą ikonę baterii
      if (now - stateChangeTimestamp > 2500) {
        Serial.println("--> Pokazanie duzej ikony pustej baterii!");
        currentState = STATE_LOW_BATTERY_ICON;
        stateChangeTimestamp = now;
      }
      break;

    // --- FAZA 2: DUŻA IKONA PUSTEJ BATERII ---
    case STATE_LOW_BATTERY_ICON:
      // Migający wykrzyknik co 400 ms
      if (now - lastAnimTick > 400) {
        lastAnimTick = now;
        animFrame = !animFrame;
        drawBigEmptyBattery(animFrame);
      }

      // Po 4 sekundach wyświetlania ikony robot wyłącza się (idzie spać z braku prądu)
      if (now - stateChangeTimestamp > 4000) {
        Serial.println("--> Robot calkowicie zasypia z powodu rozladowania.");
        currentState = STATE_DEAD_SLEEP;
        stateChangeTimestamp = now;
        drawSleepEyes();
      }
      break;

    // --- FAZA 3: CAŁKOWICIE ROZŁADOWANY (DEAD SLEEP) ---
    case STATE_DEAD_SLEEP:
      // Robot śpi i nie reaguje na wstrząsy. Czeka na kabel USB-C.
      break;

    // --- FAZA 4: ŁADOWANIE USB-C ---
    case STATE_CHARGING:
      // Płynna animacja fali energii i pioruna co 180 ms
      if (now - lastAnimTick > 180) {
        lastAnimTick = now;
        animFrame++;
        drawBigChargingBattery((int)batteryPercent, animFrame);
      }

      // Przyrost naładowania baterii (+2% co 300 ms)
      if (batteryPercent < 100.0f) {
        if (now - lastBatteryTick > 300) {
          lastBatteryTick = now;
          batteryPercent += 2.0f;
          if (batteryPercent >= 100.0f) {
            batteryPercent = 100.0f;
            soundFullyCharged();
            fullChargeTimestamp = now;
            Serial.println("[USB-C] Bateria w 100% naladowana! Robot za chwile powroci do oczek...");
          }
        }
      } else {
        // Po osiągnięciu 100% odczekaj 1.5 sekundy, po czym wróć do otwartych oczu!
        if (now - fullChargeTimestamp > 1500) {
          Serial.println("[USB-C] Robot naladowany w 100%! Otwiera oczka (AWAKE).");
          currentState = STATE_AWAKE;
          wakeUpTimestamp = now;
          stateChangeTimestamp = now;
          drawEyes(36, 0, 0);
        }
      }
      break;
  }

  delay(30);
}