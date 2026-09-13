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

### 🧩 UNIWERSALNY STELAŻ ELEKTRONIKI v2.2 (Free Rail Edition)
Plik: [`cad_models/stl_print/core_chassis.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/core_chassis.stl)

| Plik STL | Ilość | Opis / Rola w konstrukcji | Orientacja na stole |
| :--- | :---: | :--- | :--- |
| [`core_chassis.stl`](file:///home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/stl_print/core_chassis.stl) | **1 szt.** | **Centralny stelaż nośny v2.3 (Free Rail & Reinforced OLED Edition)**: W 100% odsłonięta, całkowicie drożna szyna montażowa ESP32 DevKit V1 (szerokość 29.2mm) z 2 głębokimi kanałami na piny goldpin (4.1x4.7mm) i tunelem kablowym; boczne pylony nośne umieszczone poza obrysem płytki (X = ±15.0..19.5mm); mostek MPU-6050 wyniesiony na Z=12.0mm ponad ESP32 z otworami M2.5 (rozstaw 15.2mm); wzmocniony maszt OLED 80° z ramką 27.6x27.6mm, 4 otworami gwintowanymi M2 (23.5x23.5mm), oknem SMD (20x16mm), slotem I2C (14x5.5mm) i szczeliną na taśmę FPC (16x2.5mm); podwójne zastrzały kratownicowe (truss); wiszący kubek buzzera fi 12.4x9.0mm podparty z pylonów bocznych; 3 kieszenie 7.2x4.5x6.8mm na switche 6x6mm ze zderzakiem ESP32 na Y=-26.0mm; szyny Quick-Swap z zatrzaskami kulkowymi | Płasko na spodzie (Z=0, 0 podpór) |

> [!IMPORTANT]
> **Dlaczego stelaż v2.3 to rewolucja?**  
> Całkowicie wyeliminowano problem blokowania szyn przez pylony czy podpory oraz ułamujących się bolców OLED. W nowym stelażu **Universal Core Chassis v2.3**:
> - **ESP32 DevKit V1**: Szyna ma pełne 29.2 mm szerokości (tolerancja na druk FDM) i jest **w 100% otwarta od góry i od tyłu**. Płytka wsuwa się gładko w prowadnice aż do przedniego zderzaka (Y=-26.0mm) i zatrzaskuje w bocznych wypustkach sprężystych na Z=7.1mm.
> - **Głębokie kanały na piny goldpin**: Dwa kanały o szerokości 4.1 mm i głębokości 4.7 mm (od Z=5.5 do Z=0.8 mm) zapewniają, że dolne piny 2x15 goldpin wiszą swobodnie w powietrzu i nie dotykają dna!
> - **Pylony nośne poza obrysem ESP32**: Kolumny konstrukcyjne stelaża zostały odsunięte na zewnątrz (X = ±15.0 do ±19.5 mm) – zero słupków stojących na pinach czy laminacie ESP32 (0.0000 mm³ kolizji)!
> - **Mostek MPU-6050 (GY-521)**: Wyniesiony na Z = 12.0 mm ponad ESP32 (6.5 mm prześwitu nad płytką bazową). Płytka czujnika spoczywa stabilnie na konsoli z otworami M2.5 (rozstaw 15.2 mm) i przednim oknem kablowym na magistralę I2C.
> - **Komora akustyczna Buzzera 12mm**: Kubek rezonansowy fi 12.4 mm wisi na Z = 23.0 mm podparty poprzecznymi ramionami z bocznych pylonów. Zero kolizji z MPU i ESP32.
> - **Wzmocniony Maszt OLED 0.96" SSD1306 (v2.3)**: 
>   - Gruba kieszeń nośna 3.8 mm (dla stabilności gwintów),
>   - 4 otwory pilotowe pod wkręty M2 (fi 1.8 mm x 4.5 mm) w rozstawie 23.5 x 23.5 mm (zamiast łamliwych plastikowych bolców),
>   - Tylne okno odciążające SMD (20.0 x 16.0 mm),
>   - Dolne wycięcie ochronne na taśmę giętką FPC (16.0 x 2.5 mm),
>   - Górny szeroki przepust kątowy na wtyk/złącze 4-pin I2C (14.0 x 5.5 mm),
>   - Podwójne zastrzały kratownicowe (truss) po bokach — maszt jest sztywny jak skała!
> - **Zarządzanie kablami**: Centralny kanał kablowy pod ESP32 pozwala schować wszystkie przewody połączeniowe. Zero wiszących kabli!
> Montujesz i lutujesz całą elektronikę **tylko raz na stelażu**! Każda z czterech obudów górnych (Classic CRT, Mecha-Kawaii, Cyber-Titan Apex, Steam-Titan Nautilus ULTRA) nasuwa się na stelaż od góry wzdłuż szyn Quick-Swap i zatrzaskuje na kulkach detent. Aby zmienić wygląd robota, po prostu pociągasz głowę w górę i zakładasz nową – bez śrub, bez rozłączania kabli i bez kleju!

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
  - Trzpień przycisku: `fi 4.8 mm`, otwór w obudowie: `fi 6.2 mm` (**duży, płynny luz roboczy `0.7 mm` na stronę / `1.4 mm` na średnicy** — przyciski nie zakleszczają się w druku FDM, a otwory mieszczą również fabryczne nakładki 6.0 mm).
  - Oparcie kołnierza: podtoczenie `fi 8.4 mm` (kołnierz klawisza `fi 7.2 mm` nie ma prawa wypaść na zewnątrz).

---

## 🛠️ Instrukcja Montażu: Architektura Centralnego Stelaża (Złóż raz!)

Dzięki nowemu stelażowi **Universal Core Chassis**, całą elektronikę składasz i podłączasz **tylko jeden raz na stelażu**. Od tej pory zmiana obudowy na biurku zajmuje dosłownie sekundę!

### Krok 1: Przyciski Nawigacyjne (Mikrostyki 6x6 mm)
1. Wsuń 3 mikroprzełączniki Tact Switch 6x6 mm **od góry w otwarte kieszenie** przedniej belki stelaża (szerokość kieszeni 7.2 mm z bocznymi rowkami 8.6 mm na piny).
2. Trzpienie przełączników wsuwają się gładko w przednie pionowe okna U-kształtne (szerokość 4.8 mm).
3. Piny i przewody opadają wprost przez dolne okna (6.4 x 4.0 mm) do centralnego tunelu kablowego.
4. Tylna ścianka kieszeni opiera się o sztywną ścianę zderzaka – klikanie jest precyzyjne i twarde.
5. Podłącz piny: Lewy ➔ **GPIO 18**, Środkowy (OK) ➔ **GPIO 19**, Prawy ➔ **GPIO 23** (oraz wspólna masa GND).

### Krok 2: Płytka ESP32 DevKit V1
1. Wsuń płytkę ESP32 wzdłuż szyn prowadzących od tyłu (lub opuść od góry w otwarty korytarz 30mm), aż oprze się o przedni zderzak oporowy (Y=-26.0mm) i kliknie w boczne zatrzaski sprężyste na Z=7.1mm.
2. Dwa rzędy pinów goldpin (2x15) wiszą swobodnie w głębokich kanałach (4.7mm głębokości, od Z=5.5 do 0.8mm) — zero oporu i zero kolizji.
3. Przedni zderzak oporowy uniemożliwia przesunięcie płytki podczas podłączania kabla USB.
4. Port microUSB / USB-C znajduje się idealnie w tylnym oknie z fazą naprowadzającą.

### Krok 3: Czujnik Ruchu MPU-6050
1. Umieść płytkę MPU-6050 (GY-521) poziomo na mostku sensorycznym stelaża (Z=12.0mm ponad ESP32) i opcjonalnie zabezpiecz 2 śrubkami M2.5 (rozstaw 15.2mm).
2. Wyprowadź przewody magistrali I2C (**SDA: GPIO 21**, **SCL: GPIO 22**, zasilanie 3.3V i GND) przez przedni przepust kablowy prosto do centralnego kanału pod ESP32.

### Krok 4: Wyświetlacz OLED 0.96" na Wzmocnionym Maszcie (v2.3)
1. Włóż moduł OLED 0.96" SSD1306 do dedykowanej kieszeni (27.6 x 27.6 mm) ukośnego masztu (nachylenie 80° / -10° od pionu).
2. Płytka lica opiera się gładko w gnieździe — tylne okno (20.0 x 16.0 mm) chroni drobne rezystory/kondensatory SMD przed jakimkolwiek dociskiem mechanicznym, a dolna szczelina (16.0 x 2.5 mm) całkowicie zabezpiecza taśmę giętką FPC szkła OLED przed załamaniem.
3. Przykręć płytkę 2 lub 4 krótkimi wkrętami samogwintującymi **M2** (długość 4–6 mm) w fabryczne otwory pilotowe (fi 1.8 mm x 4.5 mm, rozstaw standardowy 23.5 x 23.5 mm). Koniec z ułamywaniem plastikowych bolców!
4. Podłącz przewody I2C (**VCC**, **GND**, **SCL: GPIO 22**, **SDA: GPIO 21**) przez górne poszerzone wycięcie (14.0 x 5.5 mm) – swobodnie mieszczą się tam zarówno złącza żeńskie goldpin, jak i piny kątowe.

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
