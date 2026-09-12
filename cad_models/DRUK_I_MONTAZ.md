# 🖨️ Przewodnik Druku 3D i Montażu Obudowy Robota ESP32 Pet

Kompleksowa instrukcja przygotowania plików, ustawień slicera oraz montażu przemyślanej obudowy biurkowej dla robota companion pet.

---

## 📂 Pliki do Druku (Katalog `cad_models/stl_print/`)

Wszystkie modele zostały zaprojektowane w pełnej zgodności z zasadami **Design for Additive Manufacturing (DFAM)**, są bryłami zamkniętymi (watertight/manifold) i posiadają zoptymalizowane tolerancje pasowania (0.25–0.35 mm).

| Plik STL | Ilość | Opis / Rola w konstrukcji | Orientacja na stole |
| :--- | :---: | :--- | :--- |
| [`obudowa_dol_podstawa.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/obudowa_dol_podstawa.stl) | 1 szt. | Dolne chassis z szynami ESP32, wycięciem USB i gniazdami śrub M3 | Płasko na spodzie (Z=0) |
| [`obudowa_gora_glowa.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/obudowa_gora_glowa.stl) | 1 szt. | Górny korpus / głowa: okno OLED 0.96", kieszenie dotyku, grill buzzera | Płasko dolną krawędzią (kołnierzem) do stołu |
| [`przycisk_nakladka.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/przycisk_nakladka.stl) | **3 szt.** | Ergonomiczne klawisze przycisków z kołnierzem zapobiegającym wypadaniu | Płasko kołnierzem do stołu |
| [`uchwyt_oled.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/uchwyt_oled.stl) | 1 szt. | Wewnętrzny wspornik dociskowy ekranu OLED bez konieczności klejenia | Płasko na stole |
| [`robot_obudowa_kompletna.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/robot_obudowa_kompletna.stl) | - | Model poglądowy całego złożenia (do inspekcji w slicerze) | - |

> [!TIP]
> Dla miłośników edycji CAD w folderze `cad_models/` znajdują się również pliki źródłowe **STEP** (`.step`) oraz projekt parametryczny **FreeCAD** (`robot_obudowa_3d.FCStd`) i **Blender** (`robot_projekt.blend`).

---

## ⚙️ Zalecane Parametry Slicera (Cura / PrusaSlicer / Bambu Studio / OrcaSlicer)

- **Materiał**: 
  - **PLA** (Zalecany): Najwyższa precyzja wymiarowa, zerowy skurcz termiczny, idealne spasowanie kołnierzy i przycisków.
  - **PETG** lub **ASA**: Bardzo dobra wytrzymałość i odporność termiczna.
- **Średnica dyszy (Nozzle)**: `0.4 mm`
- **Wysokość warstwy (Layer height)**:
  - Obudowa (dół i góra): `0.20 mm`
  - Przyciski (nakładki) oraz uchwyt OLED: `0.16 mm` lub `0.20 mm`
- **Ścianki / Obrysy (Perimeters / Wall loops)**: `3 lub 4` (min. 1.2–1.6 mm grubości) — zapewnia pełną szczelność optyczną (światło z wnętrza nie przebija przez plastik).
- **Warstwy górne i dolne (Top/Bottom layers)**: `4-5 warstw` (min. 0.8–1.0 mm).
- **Wypełnienie (Infill)**: `15% – 20%` (Zalecany wzór: **Gyroid** lub **Grid**).
- **Podpory (Supports)**:
  - `obudowa_dol_podstawa.stl`: **BEZ PODPÓR (Supports: OFF)** — model drukuje się w 100% na płasko.
  - `obudowa_gora_glowa.stl`: Ściany są nachylone pod kątem zaledwie 10° od pionu, co nie wymaga podpór. Jeśli Twoja drukarka ma słabsze chłodzenie mostków, włącz podpory organiczne/drzewiaste (**Tree Supports: touching buildplate only**) wyłącznie pod nadprożem okna ekranu OLED.
  - `przycisk_nakladka.stl`: **BEZ PODPÓR** (drukowany kołnierzem do dołu).

---

## 🎨 Sugestie Kolorystyczne (Multi-Color lub Osobne Wydruki)

Możesz uzyskać fantastyczny efekt retro-robota biurkowego bez systemu wielokolorowego:
1. **Korpus (Góra i Dół)**: Matowy biały, jasnoszary lub ciemny grafitowy PLA (np. *Matte White / Concrete Grey*).
2. **Klawisze przycisków (3 sztuki)**: Kontrastowy akcent — turkusowy (cyan), pomarańczowy, żółty lub czerwony.
3. **Ekran**: Czarna płytka OLED z szybką maskującą ramkę sprawia, że oczy robota wyglądają jak wyświetlane na jednolitej szklanej tafli!

---

## 🛠️ Instrukcja Montażu Krok po Kroku

### Krok 1: Strefy Głaskania (Pojemnościowe sensory dotyku)
1. Wytnij dwa paski zwykłej kuchennej folii aluminiowej o wymiarach ok. **15 mm x 32 mm**.
2. Wklej paski (za pomocą cienkiej taśmy dwustronnej lub kropli kleju) w dwie dedykowane kieszenie na wewnętrznej stronie dachu górnej obudowy:
   - Przednia kieszeń: **Przód / Czoło** ➔ kabelek do **GPIO 32** (T9).
   - Tylna kieszeń: **Tył głowy** ➔ kabelek do **GPIO 33** (T8).
3. Ścianka plastiku nad kieszeniami ma zredukowaną grubość (1.0 mm), co zapewnia natychmiastową, czułą reakcję na dotyk dłoni przez plastik.

### Krok 2: Przyciski Nawigacyjne
1. Wsuń od środka 3 drukowane nakładki przycisków (`przycisk_nakladka.stl`) w otwory na dolnej brodzie.
2. Ich kołnierz oporowy oprze się o wewnętrzne gniazdo – przyciski nigdy nie wypadną na zewnątrz!
3. Zamontuj za nimi mikrostyki Tact Switch 6x6 mm podłączone do pinów:
   - Lewy: **GPIO 18**
   - Środkowy (OK): **GPIO 19**
   - Prawy: **GPIO 23**

### Krok 3: Wyświetlacz OLED 0.96" I2C
1. Wsuń wyświetlacz OLED w wewnętrzną kieszeń ustalającą za oknem frontowym głowy.
2. Załóż od tyłu element dociskowy `uchwyt_oled.stl` lub zabezpiecz rogi płytki odrobiną kleju termotopliwego / dwoma wkrętami M2.
3. Wyprowadź przewody I2C (**SDA: GPIO 21**, **SCL: GPIO 22**, **VCC: 3.3V**, **GND**).

### Krok 4: Buzzer Pasywny i Czujnik Ruchu MPU-6050
1. Umieść przetwornik piezoelektryczny buzzer 12mm w górnej części korpusu, bezpośrednio pod 5 szczelinami grilla akustycznego (sygnał do **GPIO 25**).
2. Czujnik MPU-6050 zamocuj poziomo na półce montażowej (wspólna szyna I2C: SDA 21, SCL 22).

### Krok 5: Płytka ESP32 i Zamknięcie Obudowy
1. Wsuń płytkę ESP32 DevKit V1 w szyny prowadzące dolnego chassis – gniazdo USB idealnie zgra się z tylnym oknem.
2. Połącz przewody Dupont zgodnie ze schematem z `README.md`.
3. Nałóż górną obudowę na kołnierz centrujący dolnej podstawy.
4. Skręć obie części od spodu za pomocą **4 standardowych śrub M3** (długość 8–10 mm) wkręcanych w otwory pilotażowe.
5. Wklej 4 silikonowe nóżki antypoślizgowe (fi 8 mm) w gniazda na spodzie – zakryją one łby śrub i ustabilizują robota na biurku!

---

## 🚀 Gotowe!
Podłącz kabel USB z tyłu robota, wgraj kod (`pio run -t upload`) i ciesz się w pełni funkcjonalnym, uroczym robotem biurkowym!
