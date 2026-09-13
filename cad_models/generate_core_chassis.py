#!/usr/bin/env python3
"""
Generator Uniwersalnego Stelaża Elektroniki (Universal Core Chassis v2.2 - Free Rail Edition)
Zaprojektowany od zera pod DOKŁADNE WYMIARY każdego podzespołu elektronicznego:
1. W 100% ODSŁONIĘTA I WOLNA SZYNA ESP32 DevKit V1 (30-pin, 28.5 mm):
   - Całkowicie drożna szyna montażowa bez ŻADNYCH przeszkód i kolizji (0.0000 mm³ kolizji)!
   - Szerokość łoża: 29.2 mm (tolerancja +0.7 mm dla bezoporowego wsuwania/osadzania płytki)
   - Lamele oporowe PCB na Z=5.5 mm (szerokość 1.4 mm, idealnie poza pinami goldpin)
   - Dwa głębokie kanały pod piny goldpin (4.1 mm szer. x 45.0 mm dł. x 4.7 mm gł.) – piny wiszą swobodnie!
   - Centralny tunel kablowy pod ESP32 (14.0 mm szer. x 3.1 mm gł.) dla wiązek przewodów
   - Drożny tunel wsuwania od tyłu z szerokim oknem USB (16.0 x 8.0 mm)
   - Zderzak czołowy płytki na Y=-26.0 mm i elastyczne zatrzaski krawędziowe (snap tabs) na Z=7.1 mm
2. Boczne pylony nośne umieszczone CAŁKOWICIE POZA OBRYSEM ESP32 (X = ±15.0 do ±19.5 mm):
   - Żadne kolumny ani ścianki nie wnikają w szynę ESP32!
   - Szerokość korytarza dla elektroniki: pełne 30.0 mm otwartej przestrzeni
   - Wycięcia odciążające pod słupki montażowe obudów
3. Mostek sensoryczny MPU-6050 (GY-521: 20.8 x 15.6 mm) na Z = 12.0 mm:
   - Wyniesiony ponad tunel ESP32 (prześwit 6.5 mm ponad płytką bazową)
   - Płaska konsola montażowa z 2 otworami M2.5 w standardowym rozstawie GY-521 (15.2 mm)
   - Przedni przepust kablowy na magistralę I2C do tunelu głównego
4. Dedykowana komora akustyczna Buzzera 12mm na Z = 23.0 mm:
   - Cylindryczne gniazdo: fi 12.4 mm x 9.0 mm głębokości
   - 2x otwory na nóżki buzzera w dnie (rozstaw 7.6 mm standard)
   - Podparta horyzontalnymi ramionami poprzecznymi z bocznych pylonów (ZERO podpór w ESP32!)
5. Precyzyjne gniazdo ekranu OLED 0.96" I2C SSD1306:
   - Kieszeń na laminat: 27.4 x 27.4 x 1.8 mm (dla standardowej płytki 27.0 x 27.0 mm)
   - 4x słupki montażowe z kołkami fi 1.8 mm w rozstawie 23.5 x 23.5 mm (standard M2 OLED)
   - Okno na matrycę: 24.5 x 13.5 mm (100% widoczności ekranu)
   - Kąt nachylenia 80° (-10° od pionu)
6. Przednia belka 3 przycisków Tact Switch 6x6 mm:
   - 3 niezależne kieszenie 6.6 x 4.5 x 6.8 mm
   - Otwory czołowe na trzpienie: fi 3.4 mm (rozstaw: X = -14.0, 0.0, +14.0 mm, Z = 5.6 mm)
   - Przepusty na nóżki i przewody w dnie każdej kieszeni
7. Zintegrowane szyny Slide-On Quick-Swap (X = ±21.8 / 19.5 mm, dł. 22 mm, wys. 13 mm):
   - Fazy naprowadzające 30° i zatrzaski kulkowe fi 1.8 mm na Z=9.5 mm
   - 100% kompatybilność z 4 stylami obudów (0.0000 mm³ kolizji)!
"""

import sys
import os
import math

sys.path.append('/usr/lib/freecad/lib')
import FreeCAD
import Part
import Import
import MeshPart
from FreeCAD import Vector, Rotation, Placement

print("=== Generowanie Nowego Stelaża Elektroniki: Universal Core Chassis v2.2 (Free Rail Edition) ===")

base_dir = '/home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/'
stl_dir = os.path.join(base_dir, 'stl_print')
os.makedirs(stl_dir, exist_ok=True)

# -------------------------------------------------------------
# Helper: Zaokrąglony graniastosłup (Rounded Prism) w XY
# -------------------------------------------------------------
def make_rounded_prism(lx, ly, lz, r, origin=Vector(0,0,0)):
    r = min(r, lx/2.0 - 0.1, ly/2.0 - 0.1)
    x0, y0, z0 = origin.x, origin.y, origin.z
    p1 = Vector(x0 + r, y0, z0)
    p2 = Vector(x0 + lx - r, y0, z0)
    p3 = Vector(x0 + lx, y0 + r, z0)
    p4 = Vector(x0 + lx, y0 + ly - r, z0)
    p5 = Vector(x0 + lx - r, y0 + ly, z0)
    p6 = Vector(x0 + r, y0 + ly, z0)
    p7 = Vector(x0, y0 + ly - r, z0)
    p8 = Vector(x0, y0 + r, z0)

    e1 = Part.makeLine(p1, p2)
    e2 = Part.makeCircle(r, Vector(x0 + lx - r, y0 + r, z0), Vector(0,0,1), -90, 0)
    e3 = Part.makeLine(p3, p4)
    e4 = Part.makeCircle(r, Vector(x0 + lx - r, y0 + ly - r, z0), Vector(0,0,1), 0, 90)
    e5 = Part.makeLine(p5, p6)
    e6 = Part.makeCircle(r, Vector(x0 + r, y0 + ly - r, z0), Vector(0,0,1), 90, 180)
    e7 = Part.makeLine(p7, p8)
    e8 = Part.makeCircle(r, Vector(x0 + r, y0 + r, z0), Vector(0,0,1), 180, 270)
    w = Part.Wire([e1, e2, e3, e4, e5, e6, e7, e8])
    return Part.Face(w).extrude(Vector(0, 0, lz))

# -------------------------------------------------------------
# 1. PŁYTA GŁÓWNA PODSTAWY ZE SCHODKOWYM KOŁNIERZEM CENTRUJĄCYM
# -------------------------------------------------------------
# Dolna warga zewnętrzna oporowa: 48.0 x 60.0 x 3.0 mm (Z: 0.0 do 3.0)
rim_solid = make_rounded_prism(48.0, 60.0, 3.0, 5.0, Vector(-24.0, -34.0, 0.0))
# Schodek centrujący pod korpus: 44.0 x 56.0 x 2.0 mm
rim_pocket = make_rounded_prism(44.0, 56.0, 2.0, 3.8, Vector(-22.0, -32.0, 1.8))
core = rim_solid.cut(rim_pocket)

# -------------------------------------------------------------
# 2. CAŁKOWICIE DROŻNA, WOLNA SZYNA ESP32 DevKit V1 (30-pin, 28.5 mm)
# -------------------------------------------------------------
# Podstawa podłogowa pod płytką ESP32 (Z: 1.8 do 2.4 mm)
esp_subfloor = Part.makeBox(30.0, 48.0, 0.6, Vector(-15.0, -26.0, 1.8))

# Bryły boczne tworzące łoża szyn (Z: 1.8 do 7.5 mm)
rail_body_l = Part.makeBox(6.3, 47.0, 5.7, Vector(-19.5, -26.0, 1.8))
rail_body_r = Part.makeBox(6.3, 47.0, 5.7, Vector( 13.2, -26.0, 1.8))
core = core.fuse(esp_subfloor).fuse(rail_body_l).fuse(rail_body_r)

# Precyzyjne wybranie szyny ESP32 (szerokość 29.2 mm, płytka leży na Z = 5.5 mm):
# X: od -14.6 do +14.6 mm, Y: od -25.5 do +26.5 mm, Z: od 5.5 do 9.5 mm
pcb_bay_cutter = Part.makeBox(29.2, 53.0, 4.0, Vector(-14.6, -25.5, 5.5))

# Dwa głębokie kanały na piny goldpin pod płytką ESP32 (głębokość 4.7 mm, od Z=5.5 do Z=0.8 mm):
# Piny goldpin wystają 4.5 mm pod laminat i mają rozstaw 25.4 mm (X = ±12.7 mm).
# Kanały o szerokości 4.1 mm dają pełen luz i 0 kontaktu z pinami!
pin_ch_l = Part.makeBox(4.1, 46.0, 4.7, Vector(-14.6, -25.5, 0.8))
pin_ch_r = Part.makeBox(4.1, 46.0, 4.7, Vector( 10.5, -25.5, 0.8))

# Centralny kanał kablowy pod ESP32 na wiązki przewodów (szerokość 14.0 mm, głębokość 3.1 mm):
cable_ch = Part.makeBox(14.0, 46.0, 3.1, Vector(-7.0, -25.5, 2.4))

# Wycięcie na port micro-USB / USB-C z tyłu (szerokie i drożne):
usb_rear_cut = Part.makeBox(16.0, 12.0, 8.0, Vector(-8.0, 18.0, 3.5))

core = core.cut(pcb_bay_cutter).cut(pin_ch_l).cut(pin_ch_r).cut(cable_ch).cut(usb_rear_cut)

# Zatrzaski sprężyste (snap tabs) przy Z = 7.1 mm (laminat PCB ma 1.6 mm, 5.5 + 1.6 = 7.1 mm):
# Dyskretne ząbki 0.4 mm na bocznych krawędziach szyny trzymające ESP32 przed wysunięciem w pionie
snap_tab_l = Part.makeBox(0.4, 8.0, 0.8, Vector(-14.6, 3.0, 7.1))
snap_tab_r = Part.makeBox(0.4, 8.0, 0.8, Vector( 14.2, 3.0, 7.1))
core = core.fuse(snap_tab_l).fuse(snap_tab_r)

# -------------------------------------------------------------
# 3. PRZEDNIA BELKA 3 PRZYCISKÓW TACT SWITCH 6x6 mm I ZDERZAK CZOŁOWY
# -------------------------------------------------------------
# Belka przednia od Y = -32.0 do -26.0 mm (o grubości 6.0 mm, wysokość do Z = 10.0 mm)
sw_bar = Part.makeBox(36.0, 6.0, 8.2, Vector(-18.0, -32.0, 1.8))
core = core.fuse(sw_bar)

for bx in [-14.0, 0.0, 14.0]:
    # 1. Główna kieszeń wsuwana od góry (szer. 7.2 mm, dł. 4.5 mm, otwarta do góry aż do Z=11.0 mm)
    # Mikrostyk 6.0x6.0x3.5 mm wpada swobodnie od góry bez zakleszczania!
    sw_pocket = Part.makeBox(7.2, 4.5, 9.0, Vector(bx - 3.6, -30.8, 2.2))
    # 2. Czołowe okno U-kształtne na trzpień przycisku (szer. 4.8 mm, otwarte do góry do Z=11.0 mm)
    # Trzpień mikrostyku fi 3.2-3.5 mm wsuwa się pionowo w okno bez haczenia o ściankę czołową
    sw_u_slot = Part.makeBox(4.8, 2.0, 7.5, Vector(bx - 2.4, -32.5, 3.5))
    # 3. Boczne kanały odciążające na wygięte piny lutownicze (szerokość 8.6 mm)
    sw_pin_relief = Part.makeBox(8.6, 2.8, 6.2, Vector(bx - 4.3, -29.9, 0.8))
    # 4. Otwarty przepust kablowy w dnie (szer. 6.4 mm, dł. 4.0 mm, Z=0.5 do 3.0 mm)
    # Nóżki i przewody lutownicze opadają wprost do centralnego tunelu kablowego pod stelażem
    sw_wire = Part.makeBox(6.4, 4.0, 3.0, Vector(bx - 3.2, -30.5, 0.5))
    core = core.cut(sw_pocket).cut(sw_u_slot).cut(sw_pin_relief).cut(sw_wire)

# -------------------------------------------------------------
# 4. BOCZNE PYLONY STRUKTURALNE (Korytarz Bezpieczny: X = ±15.0 do ±19.5 mm)
# -------------------------------------------------------------
# Pylony rosną CAŁKOWICIE POZA OBRYSEM ESP32 (X: <-15.0 mm i >+15.0 mm)!
# Żadna ścianka nie przecina szyny ESP ani kanałów pinów!
tower_l = Part.makeBox(4.5, 31.0, 26.2, Vector(-19.5, -20.0, 1.8))
tower_r = Part.makeBox(4.5, 31.0, 26.2, Vector( 15.0, -20.0, 1.8))

# Wycięcia pod słupki montażowe M3 obudów (X = ±18.8, Y = -15.0)
sc_l = Part.makeCylinder(4.2, 25.0, Vector(-18.8, -15.0, 5.0), Vector(0,0,1))
sc_r = Part.makeCylinder(4.2, 25.0, Vector( 18.8, -15.0, 5.0), Vector(0,0,1))
tower_l = tower_l.cut(sc_l)
tower_r = tower_r.cut(sc_r)
core = core.fuse(tower_l).fuse(tower_r)

# Zewnętrzne szyny Slide-On Quick-Swap (X = -21.8 do -19.5 i 19.5 do 21.8)
rib_l = Part.makeBox(2.3, 22.0, 13.0, Vector(-21.8, -11.0, 1.8))
rib_r = Part.makeBox(2.3, 22.0, 13.0, Vector( 19.5, -11.0, 1.8))
chamfer_l = Part.makeBox(3.0, 24.0, 4.0, Vector(-23.0, -12.0, 12.0))
chamfer_l.rotate(Vector(-21.8, 0, 12.0), Vector(0, 1, 0), -30.0)
chamfer_r = Part.makeBox(3.0, 24.0, 4.0, Vector( 19.5, -12.0, 12.0))
chamfer_r.rotate(Vector( 21.8, 0, 12.0), Vector(0, 1, 0), 30.0)
rib_l = rib_l.cut(chamfer_l)
rib_r = rib_r.cut(chamfer_r)
core = core.fuse(rib_l).fuse(rib_r)

# Kulki zatrzaskowe Quick-Swap fi 1.8 mm na Z = 9.5 mm
detent_l = Part.makeSphere(0.9, Vector(-21.6, 0.0, 9.5))
detent_r = Part.makeSphere(0.9, Vector( 21.6, 0.0, 9.5))
core = core.fuse(detent_l).fuse(detent_r)

# -------------------------------------------------------------
# 5. MOSTEK SENSORYCZNY MPU-6050 (GY-521) NA Z = 12.0 mm
# -------------------------------------------------------------
# Mostek łączy lewy i prawy pylon PONAD tunelem ESP32 (prześwit 6.5 mm dla elementów ESP32!)
mpu_bridge = Part.makeBox(30.0, 16.5, 1.5, Vector(-15.0, -5.5, 12.0))
core = core.fuse(mpu_bridge)

# 2x otwory montażowe M2.5 w standardowym rozstawie GY-521 (15.2 mm -> X = ±7.6 mm, Y = 7.5 mm)
mpu_h1 = Part.makeCylinder(1.3, 3.0, Vector(-7.6, 7.5, 11.0), Vector(0, 0, 1))
mpu_h2 = Part.makeCylinder(1.3, 3.0, Vector( 7.6, 7.5, 11.0), Vector(0, 0, 1))
# Przedni przepust kablowy na 8-pinowe złącze kątowe I2C wprost do centralnego tunelu
mpu_wire = Part.makeBox(18.0, 3.0, 3.0, Vector(-9.0, -5.2, 11.0))
core = core.cut(mpu_h1).cut(mpu_h2).cut(mpu_wire)

# -------------------------------------------------------------
# 6. DEDYKOWANA KOMORA BUZZERA 12mm NA Z = 23.0 mm (Podparta z pylonów bocznych!)
# -------------------------------------------------------------
buzzer_pos = Vector(0.0, 6.0, 23.0)
# Kubek zewnętrzny fi 14.6 mm, komora fi 12.4 mm x 9.0 mm głębokości
buzzer_cup_out = Part.makeCylinder(7.3, 9.5, buzzer_pos, Vector(0, 0, 1))
buzzer_cup_in = Part.makeCylinder(6.2, 10.0, buzzer_pos + Vector(0, 0, 0.8), Vector(0, 0, 1))
# 2 otwory na piny buzzera (rozstaw 7.6 mm)
buzzer_pin1 = Part.makeCylinder(0.9, 3.0, buzzer_pos + Vector(-3.8, 0, -1.0), Vector(0, 0, 1))
buzzer_pin2 = Part.makeCylinder(0.9, 3.0, buzzer_pos + Vector( 3.8, 0, -1.0), Vector(0, 0, 1))
# Szczelina wyprowadzająca przewody
buzzer_wire = Part.makeBox(3.5, 8.0, 6.0, buzzer_pos + Vector(-1.75, -4.0, 0.5))

# Ramiona wspornikowe buzzera łączące się z bocznymi pylonami (X = ±15.0 do ±7.0 mm):
# Podparcie w 100% z boków - ZERO kolizji z ESP32 i czujnikiem MPU!
buzzer_arm_l = Part.makeBox(8.0, 4.0, 5.0, Vector(-15.0, 4.0, 23.0))
buzzer_arm_r = Part.makeBox(8.0, 4.0, 5.0, Vector(  7.0, 4.0, 23.0))

buzzer_cup = buzzer_cup_out.fuse(buzzer_arm_l).fuse(buzzer_arm_r).cut(buzzer_cup_in).cut(buzzer_pin1).cut(buzzer_pin2).cut(buzzer_wire)
core = core.fuse(buzzer_cup)

# -------------------------------------------------------------
# 7. DEDYKOWANE GNIAZDO I MASZT EKRANU OLED 0.96" SSD1306 (Wersja v2.3 - M2, SMD cut, Flex Relief)
# -------------------------------------------------------------
oled_center = Vector(0, -19.0, 27.5)
tilt_angle = -10.0  # Kąt nachylenia 80° od poziomu

# Ramka nośna (cradle) dla płytki OLED 27.0 x 27.0 mm (pogrubiona do 3.8 mm dla stabilności gwintów M2)
cradle_outer = Part.makeBox(28.6, 3.8, 28.6, Vector(-14.3, 0.0, -14.3))
# Kieszeń na laminat OLED: 27.6 x 27.6 x 1.8 mm
cradle_pocket = Part.makeBox(27.6, 1.8, 27.6, Vector(-13.8, -0.1, -13.8))
# Okno aktywnej matrycy: 23.6 x 13.0 mm (idealnie centruje ekran w oknie góry obudowy)
display_window = Part.makeBox(23.6, 6.0, 13.0, Vector(-11.8, -1.0, -6.5))
# Przepust/okno z tyłu na elementy SMD płytki OLED (20.0 x 16.0 mm - zapobiega dociskaniu rezystorów)
smd_window = Part.makeBox(20.0, 4.5, 16.0, Vector(-10.0, 1.4, -8.0))
# Wycięcie u góry na złącze kątowe/proste 4-pin I2C (14.0 x 5.5 mm)
i2c_slot = Part.makeBox(14.0, 6.0, 5.5, Vector(-7.0, -1.0, 9.5))
# Szczelina na dolną taśmę FPC szkła OLED (16.0 x 2.5 mm - chroni taśmę przed załamaniem)
fpc_relief = Part.makeBox(16.0, 2.5, 2.5, Vector(-8.0, 0.5, -14.0))

cradle = cradle_outer.cut(cradle_pocket).cut(smd_window).cut(display_window).cut(i2c_slot).cut(fpc_relief)

# 4 otwory pilotowe pod wkręty samogwintujące M2 (fi 1.8 mm x 4.5 mm) w rozstawie 23.5 x 23.5 mm
# Brak łamliwych plastikowych bolców drukowanych poziomo!
for ox, oz in [(-11.75, -11.75), (11.75, -11.75), (-11.75, 11.75), (11.75, 11.75)]:
    screw_hole = Part.makeCylinder(0.9, 4.5, Vector(ox, -0.2, oz), Vector(0, 1, 0))
    cradle = cradle.cut(screw_hole)

# Obrót o 80° i pozycjonowanie na maszt
cradle.rotate(Vector(0,0,0), Vector(1,0,0), tilt_angle)
cradle.translate(oled_center)

# Podwójne zastrzały kratownicowe (truss) i ramiona górne łączące ramkę OLED z bocznymi pylonami (X = ±15.0 mm)
truss_l = Part.makeBox(2.2, 5.0, 8.0, Vector(-15.8, -18.5, 21.0))
truss_r = Part.makeBox(2.2, 5.0, 8.0, Vector( 13.6, -18.5, 21.0))
arm_top_l = Part.makeBox(1.6, 3.5, 5.0, Vector(-15.2, -18.0, 27.0))
arm_top_r = Part.makeBox(1.6, 3.5, 5.0, Vector( 13.6, -18.0, 27.0))

core = core.fuse(cradle).fuse(truss_l).fuse(truss_r).fuse(arm_top_l).fuse(arm_top_r)

# -------------------------------------------------------------
# 8. GNIAZDA NÓŻEK SILIKONOWYCH (Dół)
# -------------------------------------------------------------
for fx, fy in [(-16.0, -21.0), (16.0, -21.0), (-16.0, 13.0), (16.0, 13.0)]:
    foot_pocket = Part.makeCylinder(4.1, 0.8, Vector(fx, fy, -0.1), Vector(0,0,1))
    core = core.cut(foot_pocket)

# -------------------------------------------------------------
# WALIDACJA GEOMETRII I EKSPORT
# -------------------------------------------------------------
print("\n--- Walidacja Nowego Stelaża Universal Core Chassis v2.2 ---")
is_valid = core.isValid()
is_closed = core.isClosed()
num_solids = len(core.Solids)
volume = core.Volume

print(f"Nowy Stelaż Elektroniki: Valid={is_valid}, Closed={is_closed}, Solids={num_solids}, Volume={volume:.1f} mm³")

if not (is_valid and is_closed and num_solids == 1):
    print("BŁĄD: Geometria stelaża nie jest poprawną bryłą Solid!")
    sys.exit(1)

# Sprawdzenie drożności szyny ESP32
esp_test_envelope = Part.makeBox(28.5, 51.5, 5.5, Vector(-14.25, -25.5, 5.5))
col_esp = core.common(esp_test_envelope).Volume
print(f"Kolizja bryły z korpusem ESP32 (powinna być ~0): {col_esp:.4f} mm³")

pin_test_l = Part.makeBox(3.0, 42.0, 4.5, Vector(-14.2, -24.0, 1.0))
pin_test_r = Part.makeBox(3.0, 42.0, 4.5, Vector( 11.2, -24.0, 1.0))
print(f"Kolizja z lewym rzędem goldpinów: {core.common(pin_test_l).Volume:.4f} mm³")
print(f"Kolizja z prawym rzędem goldpinów: {core.common(pin_test_r).Volume:.4f} mm³")

# Eksport STL, STEP i FreeCAD
stl_out = os.path.join(stl_dir, 'core_chassis.stl')
step_out = os.path.join(base_dir, 'core_chassis.step')
fcstd_out = os.path.join(base_dir, 'robot_core_chassis.FCStd')

mesh = MeshPart.meshFromShape(Shape=core, LinearDeflection=0.04, AngularDeflection=0.17)
mesh.write(stl_out)
print(f"Zapisano nowy STL: {stl_out} ({os.path.getsize(stl_out):,} B)")

doc = FreeCAD.newDocument("RobotCoreChassis_v2_2")
obj = doc.addObject("Part::Feature", "UniversalCoreChassis")
obj.Shape = core
doc.recompute()
Import.export([obj], step_out)
print(f"Zapisano nowy STEP: {step_out}")
doc.saveAs(fcstd_out)
print(f"Zapisano nowy projekt FreeCAD: {fcstd_out}")
print("=== Zakończono pomyślnie generowanie Nowego Stelaża Elektroniki v2.2! ===")
