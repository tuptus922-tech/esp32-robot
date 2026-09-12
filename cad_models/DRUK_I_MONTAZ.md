# 🖨️ Przewodnik Druku 3D i Montażu Obudowy Robota ESP32 Pet

Kompleksowa instrukcja przygotowania plików, ustawień slicera oraz montażu trzech unikalnych obudów biurkowych dla robota companion pet.

---

## 🎭 Trzy Unikalne Wersje Obudowy do Wyboru

Możesz wybrać jedną z trzech kompletnych, w 100% kompatybilnych z tą samą elektroniką obudów:

| Cecha | Wersja 1: Retro CRT Minimalist | Wersja 2: Cyber-Capsule Mecha-Kawaii | Wersja 3: Cyber-Titan Dreadnought |
| :--- | :--- | :--- | :--- |
| **Klimat / Styl** | Klasyczny retro komputer biurkowy, gładki, minimalistyczny | Cyberpunk / Anime Mecha Neko, dynamiczny, uroczy | Ciężki mech bojowy / Stealth Titan, agresywny, pancerny |
| **Boki obudowy** | Gładkie, opływowe zaokrąglenia R4 | 4 głębokie żebra pancerza ("szpontery") + kapsuły Audio-Pod | Wielopoziomowe radiatory chłodzenia (stepped heat-sinks) + płyty pancerza |
| **Ekran OLED** | Zlicowane okno w ścianie czołowej | Przestrzenny oktagonalny wizjer 3D + kocie wąsy mecha | Pancerny daszek czołowy (Blast Shield brow) + oktagonalna osłona |
| **Głowa / Dach** | Płaski, ergonomiczny dach | Fasetowane kocie uszka + wygrawerowana łapka | Podwójne skrzydłowe stateczniki aero + taktyczne spawy pancerza |
| **Podstawa** | Standardowa niska baza z szynami ESP32 | Baza z przednimi łapkami i pazurkami | Baza z pancernymi płozami narożnymi (skid pods) i wlotem turbiny |
| **Przyciski** | 3 gładkie, ergonomiczne kopułki | Środek: Serduszko ❤️, Boki: Łapki 🐾 | Środek: Diament `◆`, Boki: Strzałki Chevron `◀` `▶` |
| **Katalog STL** | `cad_models/stl_print/` | `cad_models/stl_print/mecha_kawaii/` | `cad_models/stl_print/dreadnought/` |
| **Plik Blender** | `robot_obudowa_klasyczna.blend` | `robot_mecha_kawaii.blend` | `robot_dreadnought.blend` |

---

## 📂 Pliki STL do Druku

Wszystkie modele zostały zaprojektowane w pełnej zgodności z zasadami **Design for Additive Manufacturing (DFAM)**, są bryłami zamkniętymi (watertight/manifold) i posiadają zoptymalizowane tolerancje pasowania (0.25–0.35 mm).

### 🛡️ Wersja 3: Cyber-Titan Dreadnought (Katalog `cad_models/stl_print/dreadnought/`)

| Plik STL | Ilość | Opis / Rola w konstrukcji | Orientacja na stole |
| :--- | :---: | :--- | :--- |
| [`dreadnought_podstawa.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/dreadnought/dreadnought_podstawa.stl) | 1 szt. | Dolne chassis z płozami narożnymi, wlotem turbiny i szynami ESP32 | Płasko na spodzie (Z=0) |
| [`dreadnought_glowa.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/dreadnought/dreadnought_glowa.stl) | 1 szt. | Głowa ze statecznikami stealth, daszkiem blast-shield i radiatorami | Płasko dolnym kołnierzem do stołu |
| [`dreadnought_przycisk_romb.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/dreadnought/dreadnought_przycisk_romb.stl) | 1 szt. | Środkowy przycisk taktyczny (OK) z fasetowanym diamentem `◆` | Płasko kołnierzem do stołu |
| [`dreadnought_przycisk_strzalka_l.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/dreadnought/dreadnought_przycisk_strzalka_l.stl) | 1 szt. | Lewy przycisk nawigacyjny ze strzałką bojową `◀` | Płasko kołnierzem do stołu |
| [`dreadnought_przycisk_strzalka_p.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/dreadnought/dreadnought_przycisk_strzalka_p.stl) | 1 szt. | Prawy przycisk nawigacyjny ze strzałką bojową `▶` | Płasko kołnierzem do stołu |
| [`dreadnought_robot_kompletny.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/dreadnought/dreadnought_robot_kompletny.stl) | - | Pełne złożenie modelu (do podglądu w slicerze) | - |

---

### 🌸 Wersja 2: Cyber-Capsule Mecha-Kawaii (Katalog `cad_models/stl_print/mecha_kawaii/`)

| Plik STL | Ilość | Opis / Rola w konstrukcji | Orientacja na stole |
| :--- | :---: | :--- | :--- |
| [`mecha_kawaii_podstawa.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/mecha_kawaii/mecha_kawaii_podstawa.stl) | 1 szt. | Dolne chassis z szynami ESP32, wycięciem USB i przednimi łapkami mecha | Płasko na spodzie (Z=0) |
| [`mecha_kawaii_glowa.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/mecha_kawaii/mecha_kawaii_glowa.stl) | 1 szt. | Głowa ze szponterami, wizjerem 3D, uszkami, nausznikami i torem głaskania | Płasko dolnym kołnierzem do stołu |
| [`mecha_kawaii_przycisk_serce.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/mecha_kawaii/mecha_kawaii_przycisk_serce.stl) | 1 szt. | Środkowy przycisk nawigacyjny (OK) z wytłoczonym serduszkiem | Płasko kołnierzem do stołu |
| [`mecha_kawaii_przycisk_lapka.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/mecha_kawaii/mecha_kawaii_przycisk_lapka.stl) | **2 szt.** | Boczne przyciski (Lewo / Prawo) z wytłoczoną kocią łapką | Płasko kołnierzem do stołu |
| [`mecha_kawaii_robot_kompletny.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/mecha_kawaii/mecha_kawaii_robot_kompletny.stl) | - | Pełne złożenie modelu (do podglądu w slicerze) | - |

---

### 📺 Wersja 1: Retro CRT Minimalist (Katalog `cad_models/stl_print/`)

| Plik STL | Ilość | Opis / Rola w konstrukcji | Orientacja na stole |
| :--- | :---: | :--- | :--- |
| [`obudowa_dol_podstawa.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/obudowa_dol_podstawa.stl) | 1 szt. | Dolne chassis z szynami ESP32, wycięciem USB i gniazdami śrub M3 | Płasko na spodzie (Z=0) |
| [`obudowa_gora_glowa.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/obudowa_gora_glowa.stl) | 1 szt. | Korpus: okno OLED 0.96", kieszenie dotyku, grill akustyczny buzzera | Płasko dolnym kołnierzem do stołu |
| [`przycisk_nakladka.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/przycisk_nakladka.stl) | **3 szt.** | Ergonomiczne klawisze przycisków z kołnierzem zabezpieczającym | Płasko kołnierzem do stołu |
| [`uchwyt_oled.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/uchwyt_oled.stl) | 1 szt. | Wewnętrzny wspornik dociskowy ekranu OLED | Płasko na stole |
| [`robot_obudowa_kompletna.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/robot_obudowa_kompletna.stl) | - | Pełne złożenie modelu klasycznego | - |

> [!TIP]
> W katalogu `cad_models/` znajdują się dedykowane pliki **Blender**:
> - [`robot_dreadnought.blend`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/robot_dreadnought.blend) – gotowa scena z modelem Cyber-Titan Dreadnought w kolorze Gunmetal Carbon z bursztynowym oświetleniem!
> - [`robot_mecha_kawaii.blend`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/robot_mecha_kawaii.blend) – gotowa scena z modelem Mecha Kawaii w kolorze Sakura!
> - [`robot_obudowa_klasyczna.blend`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/robot_obudowa_klasyczna.blend) – gotowa scena z modelem Retro CRT
> - [`robot_projekt.blend`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/robot_projekt.blend) – projekt zawierający wszystkie wersje robota
> Dostępne są również pliki źródłowe **STEP** (`.step`) oraz parametryczne projekty **FreeCAD** (`robot_dreadnought_3d.FCStd`, `robot_mecha_kawaii_3d.FCStd`, `robot_obudowa_3d.FCStd`).

---

## ⚙️ Zalecane Parametry Slicera (Bambu Studio / OrcaSlicer / PrusaSlicer / Cura)

- **Materiał**: 
  - **PLA** (Zalecany): Najwyższa precyzja, brak skurczu, idealne pasowanie zatrzasków, kołnierzy i przycisków.
  - **PETG**: Bardzo dobra trwałość mechaniczna i odporność termiczna.
- **Średnica dyszy (Nozzle)**: `0.4 mm`
- **Wysokość warstwy (Layer height)**:
  - Obudowy (baza i głowa): `0.20 mm`
  - Przyciski taktyczne oraz detale: `0.16 mm` (dla perfekcyjnej ostrości krawędzi)
- **Ścianki / Obrysy (Perimeters / Wall loops)**: `3 lub 4` (min. 1.2–1.6 mm grubości) — gwarantuje pełną szczelność optyczną.
- **Warstwy górne i dolne (Top/Bottom layers)**: `4-5 warstw` (min. 0.8–1.0 mm).
- **Wypełnienie (Infill)**: `15% – 20%` (Zalecany wzór: **Gyroid**).
- **Podpory (Supports)**:
  - **Podstawa (Base)**: **BEZ PODPÓR (Supports: OFF)** — drukuje się w 100% na płasko.
  - **Głowa (Hood)**: Daszek blast-shield oraz boczne radiatory zaprojektowano pod bezpiecznym kątem **45°**, co drukuje się czysto bez podpór na każdej drukarce FDM.
  - **Przyciski taktyczne**: **BEZ PODPÓR** (drukowane kołnierzem do dołu na stole).

---

## 🎨 Sugestie Kolorystyczne

### 🛡️ Wersja Cyber-Titan Dreadnought
1. **Pancerz (Baza i Głowa)**: Matowy grafit / czerń węglowa (Matte Charcoal / Carbon Black) lub tytanowy szary (Gunmetal Grey).
2. **Klawisz Środkowy (Diament)**: Cyberpunkowy pomarańcz (Hazard Orange / Amber) lub złoty metalik.
3. **Klawisze Boczne (Strzałki)**: Ciemny tytan (Dark Titanium).

### 🌸 Wersja Mecha-Kawaii
1. **Korpus (Baza i Głowa)**: Pastel Sakura Pink (pudrowy róż) lub perłowa biel (Pearl White).
2. **Klawisze**: Neon fuksja (serduszko) + śmietankowa biel (łapki).

### 📺 Wersja Klasyczna Retro
1. **Korpus**: Matowy jasnoszary lub kość słoniowa (Vintage Off-White / Industrial Grey).
2. **Klawisze**: Turkusowy (Cyan), żółty lub pomarańczowy akcent retro.

---

## 🛠️ Instrukcja Montażu Krok po Kroku

### Krok 1: Strefy Głaskania (Pojemnościowe sensory dotyku)
1. Wytnij dwa paski zwykłej kuchennej folii aluminiowej o wymiarach ok. **15 mm x 32 mm**.
2. Wklej paski w dwie dedykowane kieszenie na wewnętrznej stronie dachu:
   - Przednia kieszeń: **Czoło** ➔ kabelek do **GPIO 32** (T9).
   - Tylna kieszeń: **Tył głowy** ➔ kabelek do **GPIO 33** (T8).
3. Ścianka plastiku nad kieszeniami ma zredukowaną grubość (1.0 mm), co zapewnia natychmiastową, czułą reakcję na dotyk dłoni przez plastik.

### Krok 2: Przyciski Nawigacyjne
1. Wsuń od środka 3 drukowane nakładki przycisków w otwory na przedniej ścianie.
2. Ich kołnierz oporowy oprze się o wewnętrzne gniazdo – przyciski nigdy nie wypadną na zewnątrz!
3. Zamontuj za nimi mikrostyki Tact Switch 6x6 mm podłączone do pinów:
   - Lewy: **GPIO 18**
   - Środkowy (OK): **GPIO 19**
   - Prawy: **GPIO 23**

### Krok 3: Wyświetlacz OLED 0.96" I2C
1. Wsuń wyświetlacz OLED w wewnętrzną kieszeń ustalającą za oknem frontowym.
2. Zabezpiecz rogi płytki odrobiną kleju termotopliwego lub elementem dociskowym.
3. Wyprowadź przewody I2C (**SDA: GPIO 21**, **SCL: GPIO 22**, **VCC: 3.3V**, **GND**).

### Krok 4: Buzzer Pasywny i Czujnik Ruchu MPU-6050
1. Umieść przetwornik piezoelektryczny buzzer 12mm w górnej części korpusu (sygnał do **GPIO 25**).
2. Czujnik MPU-6050 zamocuj poziomo na szynie I2C (SDA 21, SCL 22).

### Krok 5: Płytka ESP32 i Zamknięcie Obudowy
1. Wsuń płytkę ESP32 DevKit V1 w szyny prowadzące dolnego chassis – gniazdo USB idealnie zgra się z tylnym oknem.
2. Połącz przewody Dupont zgodnie ze schematem z `README.md`.
3. Nałóż górną obudowę na kołnierz centrujący dolnej podstawy.
4. Skręć obie części od spodu za pomocą **4 standardowych śrub M3** (długość 8–10 mm).
5. Wklej 4 silikonowe nóżki antypoślizgowe (fi 8 mm) w gniazda na spodzie – zakryją one łby śrub i ustabilizują robota na biurku!

---

## 🚀 Gotowe!
Podłącz kabel USB z tyłu robota, wgraj kod (`pio run -t upload`) i ciesz się w pełni funkcjonalnym, niesamowitym robotem biurkowym!
