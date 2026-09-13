# 🖨️ Przewodnik Druku 3D i Montażu Obudowy Robota ESP32 Pet

Kompleksowa instrukcja przygotowania plików, ustawień slicera oraz montażu trzech unikalnych obudów biurkowych dla robota companion pet.

---

## 🎭 Cztery Unikalne Wersje Obudowy do Wyboru

Możesz wybrać jedną z czterech kompletnych, w 100% kompatybilnych z tą samą elektroniką obudów:

| Cecha | Wersja 1: Retro CRT Minimalist | Wersja 2: Cyber-Capsule Mecha-Kawaii | Wersja 3: Cyber-Titan Apex (Mecha) | Wersja 4: Steam-Titan Nautilus (Dieselpunk) |
| :--- | :--- | :--- | :--- | :--- |
| **Klimat / Styl** | Klasyczny retro komputer biurkowy | Cyberpunk / Anime Mecha Neko | Ciężki szturmowy mech bojowy / Gundam | Industrial Steampunk / BioShock Nautilus |
| **Sylwetka / Wymiary** | 50 x 50 x 48 mm, zaokrąglony prostopadłościan | 50 x 50 x 56 mm, kapsuła z uszkami | **72 mm szerokości**, **68 mm wysokości** | **54 mm kocioł ciśnieniowy**, podwójne kominy 58 mm |
| **Boki obudowy** | Gładkie zaokrąglenia R4 | 4 głębokie żebra ("szpontery") + Audio-Pod | Naramienniki 72mm z wyrzutniami rakiet | **Wielkie manometry parowe (fi 21mm)** + rurociągi miedziane |
| **Ekran OLED** | Zlicowane okno | Oktagonalny wizjer 3D + wąsy mecha | Pancerny kokpit, blast-shield 45° i kły | **Potrójna klatka ochronna iluminatora (roll-cage)** |
| **Głowa / Dach** | Płaski dach | Fasetowane uszka + kocia łapka | Rogi bojowe V-Fin 68mm | **Podwójne wiktoriańskie kominy z kryzami i radiatorami** |
| **Napęd / Tył** | Płaski tył | Płaski tył | Podwójne dysze odrzutowe dopalaczy | Półkolisty zbiornik z kołem ryglowym włazu inspekcyjnego |
| **Podstawa** | Standardowa niska baza | Baza z przednimi łapkami i pazurkami | Ciężkie gąsienice pancerne crawler 63mm | Baza kotła z 4 kołnierzami śrubowymi i żaluzją |
| **Przyciski** | 3 gładkie kopułki | Środek: Serduszko ❤️, Boki: Łapki 🐾 | Środek: Diament `◆`, Boki: Strzałki `◀` `▶` | Środek: Koło zaworu parowego, Boki: Płyty ryflowane |
| **Katalog STL** | `cad_models/stl_print/` | `cad_models/stl_print/mecha_kawaii/` | `cad_models/stl_print/dreadnought/` | `cad_models/stl_print/dieselpunk/` |
| **Plik Blender** | `robot_obudowa_klasyczna.blend` | `robot_mecha_kawaii.blend` | `robot_dreadnought.blend` | `robot_dieselpunk.blend` |

---

## 📂 Pliki STL do Druku

Wszystkie modele zostały zaprojektowane w pełnej zgodności z zasadami **Design for Additive Manufacturing (DFAM)**, są bryłami zamkniętymi (watertight/manifold) i posiadają zoptymalizowane tolerancje pasowania (0.25–0.35 mm).

---

### 🧩 UNIWERSALNY STELAŻ ELEKTRONIKI v2.0 (Pro Precision Edition)
Plik: [`cad_models/stl_print/core_chassis.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/core_chassis.stl)

| Plik STL | Ilość | Opis / Rola w konstrukcji | Orientacja na stole |
| :--- | :---: | :--- | :--- |
| [`core_chassis.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/core_chassis.stl) | **1 szt.** | **Centralny stelaż nośny v2.0**: Dedykowane gniazdo ESP32 DevKit V1 z 2 głębokimi kanałami na 2x15 pinów goldpin + centralny tunel kablowy; maszt OLED 80° z ramką 27.4x27.4mm i otworami M2 (rozstaw 23.5x23.5mm); dedykowany kubek buzzera fi 12.4x9.5mm z otworami na piny; dedykowana kieszeń MPU-6050 21.2x16.0mm z 2 otworami M2.5; 3 kieszenie 6.5x6.5mm na switche 6x6mm z otworami na nóżki; boczne szyny Quick-Swap z zatrzaskami kulkowymi | Płasko na spodzie (Z=0, 0 podpór) |

> [!IMPORTANT]
> **Dlaczego stelaż v2.0 to rewolucja?**  
> Wcześniej elektronika w wielu projektach DIY wisiała w powietrzu lub opierała się o ścianki obudowy. W nowym stelażu **Universal Core Chassis v2.0**:
> - **ESP32 DevKit V1**: Płytka leży na ramiakach oporowych na Z=5.8mm, a pod spodem znajdują się **dwa głębokie kanały (4.0mm szerokości x 4.5mm głębokości)** — piny goldpin lutowane od spodu nie opierają się o podłogę!
> - **OLED 0.96" SSD1306**: Kieszeń o wymiarach 27.4 x 27.4 mm mieści standardowy laminat 27x27 mm, a 4 słupki montażowe mają fabryczny rozstaw **23.5 x 23.5 mm** (standard otworów M2 w wyświetlaczach SSD1306).
> - **MPU-6050 (GY-521)**: Posiada własne, stabilne gniazdo na mostku konsoli z 2 otworami montażowymi M2.5 (rozstaw 15.2mm) i oknem na złącze 8-pin.
> - **Buzzer 12mm**: Zamknięty w cylindrycznym kubku akustycznym fi 12.4 x 9.5 mm z 2 otworami na nóżki (raster 7.6mm) w dnie.
> - **3x Tact Switch 6x6mm**: Każdy przycisk ma własną kieszeń 6.5 x 6.5 x 4.2 mm z oknem na nóżki lutownicze i otworem fi 3.4mm na trzpień.
> - **Zarządzanie kablami**: Centralny kanał kablowy pod ESP32 pozwala schować wszystkie przewody połączeniowe. Zero wiszących kabli!
> Montujesz i lutujesz całą elektronikę **tylko raz na stelażu**! Każda z trzech obudów górnych (Retro CRT, Mecha-Kawaii, Cyber-Titan Apex) nasuwa się na stelaż od góry wzdłuż pionowych szyn i zatrzaskuje na kulkach detent. Aby zmienić wygląd robota z Kawaii na Titana, po prostu pociągasz głowę w górę i zakładasz nową – bez śrub, bez kabli i bez kleju!

---

### 🛡️ Wersja 3: Cyber-Titan Apex (Katalog `cad_models/stl_print/dreadnought/`)

| Plik STL | Ilość | Opis / Rola w konstrukcji | Orientacja na stole |
| :--- | :---: | :--- | :--- |
| [`dreadnought_podstawa.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/dreadnought/dreadnought_podstawa.stl) | 1 szt. | Dolne chassis o rozpiętości 63mm z segmentami gąsienic czołgowych, szynami ESP32 i portem USB | Płasko na spodzie (Z=0) |
| [`dreadnought_glowa.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/dreadnought/dreadnought_glowa.stl) | 1 szt. | Głowa Apex: 72mm naramienniki z wyrzutniami, 68mm rogi V-Fin, daszek blast-shield, kły mandibles i dysze odrzutowe | Płasko dolnym kołnierzem do stołu |
| [`dreadnought_przycisk_romb.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/dreadnought/dreadnought_przycisk_romb.stl) | 1 szt. | Środkowy przycisk reaktora rdzenia (OK) z fasetowanym diamentem `◆` | Płasko kołnierzem do stołu |
| [`dreadnought_przycisk_strzalka_l.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/dreadnought/dreadnought_przycisk_strzalka_l.stl) | 1 szt. | Lewy przycisk nawigacyjny ze strzałką bojową `◀` | Płasko kołnierzem do stołu |
| [`dreadnought_przycisk_strzalka_p.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/dreadnought/dreadnought_przycisk_strzalka_p.stl) | 1 szt. | Prawy przycisk nawigacyjny ze strzałką bojową `▶` | Płasko kołnierzem do stołu |
| [`dreadnought_robot_kompletny.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/dreadnought/dreadnought_robot_kompletny.stl) | - | Pełne złożenie modelu Cyber-Titan Apex (do podglądu w slicerze) | - |

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

---

### ⚙️ Wersja 4: Steam-Titan Nautilus ULTRA (Katalog `cad_models/stl_print/dieselpunk/`)

| Plik STL | Ilość | Opis / Rola w konstrukcji | Orientacja na stole |
| :--- | :---: | :--- | :--- |
| [`dieselpunk_podstawa.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/dieselpunk/dieselpunk_podstawa.stl) | 1 szt. | Dolne chassis kotła z 4 stopami śrubowymi, dolną żaluzją pary i szynami ESP32 | Płasko na spodzie (Z=0) |
| [`dieselpunk_glowa.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/dieselpunk/dieselpunk_glowa.stl) | 1 szt. | Głowa Nautilus ULTRA: 54mm kocioł parowy, 29 nitów 3D, potrójna klatka iluminatora, podwójne kominy z potrójnymi kryzami i kołnierzami, boczne manometry (fi 21mm), rurociągi, koła zębate napędowe, mosiężne iluminatory, żaluzje chłodzące, zawory bezpieczeństwa, wieżyczka peryskopowa i tylny właz inspekcyjny | Płasko dolnym kołnierzem do stołu |
| [`dieselpunk_przycisk_zawor.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/dieselpunk/dieselpunk_przycisk_zawor.stl) | 1 szt. | Środkowy przycisk: 6-ramienne mosiężne koło zaworu parowego z wieńcem i centralną nakrętką | Płasko kołnierzem do stołu |
| [`dieselpunk_przycisk_ryfel_l.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/dieselpunk/dieselpunk_przycisk_ryfel_l.stl) | 1 szt. | Lewy przycisk nawigacyjny: płyta z industrialną blachą ryflowaną i chevronem `◀` | Płasko kołnierzem do stołu |
| [`dieselpunk_przycisk_ryfel_p.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/dieselpunk/dieselpunk_przycisk_ryfel_p.stl) | 1 szt. | Prawy przycisk nawigacyjny: płyta z industrialną blachą ryflowaną i chevronem `▶` | Płasko kołnierzem do stołu |
| [`dieselpunk_robot_kompletny.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/dieselpunk/dieselpunk_robot_kompletny.stl) | - | Pełne złożenie modelu Steam-Titan Nautilus ULTRA (do podglądu w slicerze) | - |

#### Elementy składowe dla wielomateriałowego renderera (Folder `components/`):
- `nautilus_kominy.stl` – masywne wiktoriańskie kominy z potrójnymi kryzami chłodzącymi (Mosiądz)
- `nautilus_manometry.stl` – analogowe zegary ciśnienia pary z tarczami i wskazówkami (Mosiądz)
- `nautilus_rurociagi.stl` – rurociągi parowe wysokociśnieniowe z kołnierzami (Miedź)
- `nautilus_klatka_okna.stl` – potrójna klatka ochronna iluminatora ekranu OLED (Mosiądz)
- `nautilus_kola_zebate.stl` – odsłonięty zespół przekładni zębatych napędowych (Mosiądz)
- `nautilus_iluminatory.stl` – boczne bulaje okrętowe ze śrubami ryglowymi (Mosiądz)

> [!TIP]
> W katalogu `cad_models/` znajdują się dedykowane pliki **Blender**:
> - [`robot_dieselpunk.blend`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/robot_dieselpunk.blend) – gotowa scena z modelem Steam-Titan Nautilus w stylu industrial steampunk (mosiądz, miedź, patynowana stal)!
> - [`robot_dreadnought.blend`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/robot_dreadnought.blend) – gotowa scena z modelem Cyber-Titan Dreadnought w kolorze Gunmetal Carbon!
> - [`robot_mecha_kawaii.blend`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/robot_mecha_kawaii.blend) – gotowa scena z modelem Mecha Kawaii w kolorze Sakura!
> - [`robot_obudowa_klasyczna.blend`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/robot_obudowa_klasyczna.blend) – gotowa scena z modelem Retro CRT
> - [`robot_modular_core.blend`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/robot_modular_core.blend) – demonstracja stelaża Universal Core i beznarzędziowej wymiany obudów
> Dostępne są również pliki źródłowe **STEP** (`.step`) oraz parametryczne projekty **FreeCAD** (`robot_dieselpunk_3d.FCStd`, `robot_dreadnought_3d.FCStd`, `robot_mecha_kawaii_3d.FCStd`, `robot_obudowa_3d.FCStd`, `robot_core_chassis.FCStd`).

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

## 🔬 Matematyczna Weryfikacja Systemu Modularnego Quick-Swap (Obliczenia CAD)

Poniższa tabela przedstawia wyniki dokładnych obliczeń booleańskich wykonanych bezpośrednio w silniku OpenCASCADE (FreeCAD) na modelach geometrycznych stelaża centralnego (`Universal Core Chassis`) oraz wszystkich 4 wersji głowic:

| Wersja Stylistyczna | Plik CAD (.FCStd) | Objętość Głowy | Liczba Brył (Solids) | Kolizja ze Stelażem | Pasowanie Kinematyczne (Z=30 $\to$ 0 mm) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **1. Retro CRT** | `robot_obudowa_3d.FCStd` | `16,009.2 mm³` | **1 (Manifold)** | **0.0000 mm³** | **Czyste (0.0000 mm³)** |
| **2. Mecha-Kawaii** | `robot_mecha_kawaii_3d.FCStd` | `19,853.5 mm³` | **1 (Manifold)** | **0.0000 mm³** | **Czyste (0.0000 mm³)** |
| **3. Cyber-Titan Apex** | `robot_dreadnought_3d.FCStd` | `33,005.3 mm³` | **1 (Manifold)** | **0.0000 mm³** | **Czyste (0.0000 mm³)** |
| **4. Steam-Titan Nautilus ULTRA** | `robot_dieselpunk_3d.FCStd` | `33,560.8 mm³` | **1 (Manifold)** | **0.0000 mm³** | **Czyste (0.0000 mm³)** |

### Precyzyjne Wymiary i Luzy Montażowe:
- **Szyny prowadzące Quick-Swap**:
  - Szyna stelaża: grubość `1.6 mm`, długość `22.0 mm`, wysokość `13.0 mm`, faza wprowadzająca $30^\circ$.
  - Rowek w głowie: szerokość `2.6 mm`, długość `24.0 mm`, głębokość `6.0 mm`.
  - **Luz roboczy**: `0.5 mm` na stronę (idealny dla technologii FDM — gładki poślizg bez oporu i zacięć).
- **Zatrzaski kulkowe (Ball Detents)**:
  - Promień kulki: `R = 0.9 mm` (fi 1.8 mm) na wysokości $Z = 9.5\text{ mm}$.
  - Zapewniają pewny, sprężysty "klik" blokujący głowę bez użycia jakichkolwiek śrub.
- **Kieszeń ekranu OLED (0.96" I2C)**:
  - Kąt pochylenia: $80^\circ$ ($-10^\circ$ od pionu).
  - Wymiary kieszeni: $28.0 \times 28.0\text{ mm}$, prześwit wokół laminatu: `2.4 mm` (zero naprężeń na szkle).
- **Kieszeń buzzera 12mm**:
  - Średnica cylindra stelaża: `14.4 mm`, kieszeń w głowie: `17.2 mm` (luz promieniowy `1.4 mm`).
- **Prowadnice przycisków**:
  - Trzpień przycisku: `fi 5.2 mm`, otwór w obudowie: `fi 5.6 mm` (precyzyjny luz suwliwy `0.2 mm` na promieniu).

---

## 🛠️ Instrukcja Montażu: Architektura Centralnego Stelaża (Złóż raz!)

Dzięki nowemu stelażowi **Universal Core Chassis**, całą elektronikę składasz i podłączasz **tylko jeden raz na stelażu**. Od tej pory zmiana obudowy na biurku zajmuje dosłownie sekundę!

### Krok 1: Przyciski Nawigacyjne (Mikrostyki 6x6 mm)
1. Wsuń 3 mikroprzełączniki Tact Switch 6x6 mm w dedykowane gniazda przedniej belki stelaża.
2. Ich tylna ścianka opiera się o sztywną ścianę stelaża – nawet mocne klikanie nie ugnie konstrukcji.
3. Podłącz piny: Lewy ➔ **GPIO 18**, Środkowy (OK) ➔ **GPIO 19**, Prawy ➔ **GPIO 23** (oraz wspólna masa GND).

### Krok 2: Płytka ESP32 DevKit V1
1. Wsuń płytkę ESP32 w szyny prowadzące stelaża od góry, aż kliknie w zatrzaski krawędziowe.
2. Przedni opór uniemożliwia przesunięcie płytki podczas podłączania kabla USB.
3. Port USB-C / microUSB znajduje się idealnie w tylnym oknie.

### Krok 3: Czujnik Ruchu MPU-6050
1. Umieść płytkę MPU-6050 poziomo w dedykowanej niecce między szynami.
2. Połącz przewody magistrali I2C (**SDA: GPIO 21**, **SCL: GPIO 22**, zasilanie 3.3V i GND).

### Krok 4: Wyświetlacz OLED 0.96" na Sztywnym Maszcie
1. Wsuń płytkę OLED w ramkę ukośnego masztu (nachylenie 80°).
2. Cztery wbudowane kołki ustalające (fi 1.6 mm) wchodzą w otwory montażowe płytki – ekran siedzi sztywno i zlicowany z kątem twarzy.
3. Wyprowadź 4 przewody I2C przez tylne okno masztu prosto do szyn ESP32.

### Krok 5: Buzzer Piezoelektryczny 12 mm
1. Wciśnij przetwornik buzzer 12mm od góry w cylindryczny koszyk na szczycie wieży (press-fit na klik).
2. Przełóż wyprowadzenia przez dolny kanał kablowy prosto do pinu **GPIO 25** i GND.
3. Buzzer skierowany jest ku górze, wprost w szczeliny akustyczne dachu robota!

### Krok 6: Podklejenie nóżek antypoślizgowych
1. Wklej 4 silikonowe nóżki (fi 8 mm) w gniazda na spodzie stelaża. Stelaż stoi stabilnie na biurku.

---

## 🎭 Błyskawiczna Wymiana Obudów (Quick-Swap / Slide-On)

1. Wybierz dowolną obudowę górną (**Retro CRT**, **Mecha-Kawaii** lub **Cyber-Titan Apex**).
2. Wsuń od środka w otwory czołowe danej obudowy jej stylizowane nakładki przycisków (kołnierz zabezpiecza je przed wypadnięciem na zewnątrz).
3. Nałóż obudowę od góry na stelaż – wewnętrzne szyny prowadzące gładko poprowadzą obudowę w dół, a dolne zatrzaski kulkowe (snap-detents) klikną w dolnym położeniu.
4. **Chcesz zmienić wygląd robota?** Po prostu pociągnij głowę w górę i nałóż inną! Wszystkie kable, ekran, ESP32 i buzzer zostają nienaruszone na biurku!

---

## 🚀 Gotowe!
Podłącz kabel USB z tyłu robota, wgraj kod (`pio run -t upload`) i ciesz się w pełni modułowym, niesamowitym robotem biurkowym!
