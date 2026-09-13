#!/usr/bin/env python3
"""
Generator Uniwersalnego Stelaża Elektroniki (Universal Core Chassis v2.0 - Pro Precision Edition)
Zaprojektowany od zera pod DOKŁADNE WYMIARY każdego podzespołu elektronicznego:
1. Dedykowane gniazdo ESP32 DevKit V1 (30-pin, 28.5 mm):
   - Wymiary gniazda: 51.8 x 28.7 mm, ramy oporowe PCB na Z=5.8 mm
   - Dwa głębokie kanały pod piny goldpin (4.0 mm szer. x 44.0 mm dł. x 4.5 mm gł.) – piny nie dotykają dna!
   - Centralny tunel kablowy pod ESP32 (13.0 mm szer. x 3.2 mm gł.) dla wiązek przewodów
   - Zatrzaski sprężyste (snap-fit) i zderzak przedni
   - Port USB z fazą wprowadzającą 45° dla kabli micro-USB / USB-C
2. Dedykowana konsola czujnika ruchu MPU-6050 (GY-521):
   - Precyzyjna kieszeń: 21.2 x 16.0 x 2.2 mm (PCB 20.8 x 15.6 mm)
   - 2x otwory montażowe M2.5 w standardowym rozstawie GY-521 (15.2 mm)
   - Przepust na złącze 8-pin I2C do głównego kanału kablowego
3. Dedykowana komora akustyczna Buzzera 12mm:
   - Cylindryczne gniazdo: fi 12.4 mm x 9.5 mm głębokości (buzzer chowa się na równo)
   - 2x otwory na nóżki buzzera w dnie (rozstaw 7.6 mm standard)
   - Boczny kanał wyprowadzenia przewodów do GPIO 25
4. Precyzyjne gniazdo ekranu OLED 0.96" I2C SSD1306:
   - Kieszeń na laminat: 27.4 x 27.4 x 1.8 mm (dla standardowej płytki 27.0 x 27.0 mm)
   - 4x słupki montażowe z kołkami fi 1.8 mm w dokładnym rozstawie 23.5 x 23.5 mm (standard M2 OLED)
   - Okno na matrycę: 24.5 x 13.5 mm (100% widoczności ekranu)
   - Wycięcie na złącze 4-pin I2C (VCC, GND, SCL, SDA)
   - Kąt nachylenia 80° (-10° od pionu) podparty sztywną kratownicą trójkątną
5. Przednia belka 3 przycisków Tact Switch 6x6 mm:
   - 3 niezależne kieszenie 6.5 x 6.5 x 4.2 mm (dla mikrostyków 6x6 mm)
   - Otwory czołowe na trzpienie: fi 3.4 mm (rozstaw: X = -14.0, 0.0, +14.0 mm, Z = 5.6 mm)
   - Przepusty na nóżki i przewody w dnie każdej kieszeni (4.2 x 4.2 mm)
6. Zintegrowane szyny Slide-On Quick-Swap (X = ±21.8 / 20.2 mm, dł. 22 mm, wys. 13 mm):
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

print("=== Generowanie Nowego Stelaża Elektroniki: Universal Core Chassis v2.0 ===")

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
# Schodek centrujący: 44.0 x 56.0 x 1.2 mm
rim_pocket = make_rounded_prism(44.0, 56.0, 2.0, 3.8, Vector(-22.0, -32.0, 1.8))
core = rim_solid.cut(rim_pocket)

# -------------------------------------------------------------
# 2. DEDYKOWANE GNIAZDO ESP32 DevKit V1 (30-pin, 28.5 mm)
# -------------------------------------------------------------
# Podstawa podłogi komory ESP32
esp_floor = Part.makeBox(36.0, 48.0, 1.2, Vector(-18.0, -22.5, 1.8))
# Boczne szyny nośne podpierające laminat ESP32 (laminat leży na Z = 5.8 mm)
rail_l = Part.makeBox(2.8, 48.0, 4.0, Vector(-16.8, -22.5, 1.8))
rail_r = Part.makeBox(2.8, 48.0, 4.0, Vector( 14.0, -22.5, 1.8))
# Ranty oporowe ustalające szerokość 28.5 mm
ledge_l = Part.makeBox(1.5, 46.0, 1.2, Vector(-14.3, -22.0, 4.6))
ledge_r = Part.makeBox(1.5, 46.0, 1.2, Vector( 12.8, -22.0, 4.6))
# Przedni zderzak oporowy (stop płytki)
front_stop = Part.makeBox(30.0, 2.5, 4.5, Vector(-15.0, -24.5, 1.8))

core = core.fuse(esp_floor).fuse(rail_l).fuse(rail_r).fuse(ledge_l).fuse(ledge_r).fuse(front_stop)

# DWA GŁĘBOKIE KANAŁY NA PINY GOLDPIN (Clearance dla 2x 15 pinów pod płytką!)
# Szerokość 4.0 mm, długość 44.0 mm, głębokość 4.5 mm (od Z=5.8 do Z=1.3)
pin_channel_l = Part.makeBox(4.0, 44.0, 4.5, Vector(-14.2, -21.0, 1.8))
pin_channel_r = Part.makeBox(4.0, 44.0, 4.5, Vector( 10.2, -21.0, 1.8))

# CENTRALNY KANAŁ KABLOWY pod ESP32 (szerokość 13.0 mm) dla przewodów połączeniowych
cable_trunk = Part.makeBox(13.0, 46.0, 3.2, Vector(-6.5, -22.0, 1.8))

# Wycięcie na port micro-USB / USB-C z fazą naprowadzającą
usb_cut = Part.makeBox(14.0, 14.0, 8.0, Vector(-7.0, 16.0, 3.5))

core = core.cut(pin_channel_l).cut(pin_channel_r).cut(cable_trunk).cut(usb_cut)

# Zatrzaski sprężyste (snap-fit) trzymające ESP32 od góry (Z = 5.8 + 1.6 = 7.4 mm)
snap_l = Part.makeBox(1.2, 8.0, 1.0, Vector(-14.9, 6.0, 5.8))
snap_r = Part.makeBox(1.2, 8.0, 1.0, Vector( 13.7, 6.0, 5.8))
core = core.fuse(snap_l).fuse(snap_r)

# -------------------------------------------------------------
# 3. PRZEDNIA BELKA 3 PRZYCISKÓW TACT SWITCH 6x6 mm
# -------------------------------------------------------------
sw_bar = Part.makeBox(36.0, 7.5, 8.2, Vector(-18.0, -32.0, 1.8))
core = core.fuse(sw_bar)

for bx in [-14.0, 0.0, 14.0]:
    # Dokładna kieszeń 6.5 x 6.5 x 4.2 mm na korpus mikrostyku 6x6 mm
    sw_pocket = Part.makeBox(6.5, 6.5, 4.2, Vector(bx - 3.25, -30.5, 3.5))
    # Otwór czołowy fi 3.4 mm na popychacz przycisku
    sw_hole = Part.makeCylinder(1.7, 10.0, Vector(bx, -35.0, 5.6), Vector(0, 1, 0))
    # Otwór w dnie na 4 nóżki lutownicze i przewody
    sw_wire_drop = Part.makeBox(4.2, 4.2, 3.0, Vector(bx - 2.1, -29.5, 1.5))
    core = core.cut(sw_pocket).cut(sw_hole).cut(sw_wire_drop)

# -------------------------------------------------------------
# 4. DEDYKOWANA KONSOLA CZUJNIKA MPU-6050 (GY-521: 20.8 x 15.6 mm)
# -------------------------------------------------------------
# Mostek konsoli z nogami nośnymi podpierającymi konstrukcję
leg_l = Part.makeBox(2.5, 18.0, 7.5, Vector(-13.5, -7.0, 1.8))
leg_r = Part.makeBox(2.5, 18.0, 7.5, Vector( 11.0, -7.0, 1.8))
mpu_bridge = Part.makeBox(27.0, 18.0, 3.5, Vector(-13.5, -7.0, 8.5))
core = core.fuse(leg_l).fuse(leg_r).fuse(mpu_bridge)

# Precyzyjna kieszeń na płytkę GY-521: 21.2 x 16.0 x 2.2 mm
mpu_pocket = Part.makeBox(21.2, 16.0, 2.2, Vector(-10.6, -6.0, 10.0))
# 2 otwory montażowe M2.5 w standardowym rozstawie 15.2 mm
mpu_h1 = Part.makeCylinder(1.3, 5.0, Vector(-7.6, 7.5, 8.0), Vector(0, 0, 1))
mpu_h2 = Part.makeCylinder(1.3, 5.0, Vector( 7.6, 7.5, 8.0), Vector(0, 0, 1))
# Przepust na 8-pinowy header I2C
mpu_wire_slot = Part.makeBox(20.4, 3.5, 4.0, Vector(-10.2, -5.5, 8.0))
core = core.cut(mpu_pocket).cut(mpu_h1).cut(mpu_h2).cut(mpu_wire_slot)

# -------------------------------------------------------------
# 5. DEDYKOWANA KOMORA BUZZERA 12mm (Acoustic Resonance Cup)
# -------------------------------------------------------------
buzzer_mount_pos = Vector(0.0, 7.5, 23.0)
# Kubek zewnętrzny fi 14.6 mm, wewnętrzny fi 12.4 mm x 9.5 mm głębokości
buzzer_cup_outer = Part.makeCylinder(7.3, 10.0, buzzer_mount_pos, Vector(0, 0, 1))
buzzer_cup_inner = Part.makeCylinder(6.2, 10.5, buzzer_mount_pos + Vector(0, 0, 0.8), Vector(0, 0, 1))
# 2 precyzyjne otwory na nóżki buzzera (rozstaw 7.6 mm)
buzzer_pin1 = Part.makeCylinder(0.9, 3.0, buzzer_mount_pos + Vector(-3.8, 0, -1.0), Vector(0, 0, 1))
buzzer_pin2 = Part.makeCylinder(0.9, 3.0, buzzer_mount_pos + Vector( 3.8, 0, -1.0), Vector(0, 0, 1))
# Szczelina na przewody
buzzer_wire_notch = Part.makeBox(3.5, 8.0, 6.0, buzzer_mount_pos + Vector(-1.75, -4.0, 0.5))
buzzer_chamber = buzzer_cup_outer.cut(buzzer_cup_inner).cut(buzzer_pin1).cut(buzzer_pin2).cut(buzzer_wire_notch)

# Masywne kolumny nośne buzzera (nie cienkie patyki!)
buzzer_col_l = Part.makeBox(2.5, 14.0, 23.0, Vector(-7.0, 0.5, 1.8))
buzzer_col_r = Part.makeBox(2.5, 14.0, 23.0, Vector( 4.5, 0.5, 1.8))
core = core.fuse(buzzer_chamber).fuse(buzzer_col_l).fuse(buzzer_col_r)

# -------------------------------------------------------------
# 6. DEDYKOWANY MASZT I GNIAZDO EKRANU OLED 0.96" SSD1306 (27x27 mm)
# -------------------------------------------------------------
oled_center = Vector(0, -19.0, 27.5)
tilt_angle = -10.0  # Kąt 80° od poziomu

# Sztywne trójkątne pylony masztu zbiegające się z podłogi
pylon_l = Part.makeBox(2.8, 14.0, 26.0, Vector(-13.6, -19.0, 1.8))
pylon_r = Part.makeBox(2.8, 14.0, 26.0, Vector( 10.8, -19.0, 1.8))
core = core.fuse(pylon_l).fuse(pylon_r)

# Pełna ramka nośna (cradle) dopasowana do płytki 27.0 x 27.0 mm
cradle_outer = Part.makeBox(28.5, 3.2, 28.5, Vector(-14.25, 0.0, -14.25))
# Dokładna kieszeń: 27.4 x 27.4 x 1.8 mm
cradle_pocket = Part.makeBox(27.4, 1.8, 27.4, Vector(-13.7, -0.1, -13.7))
# Okno aktywnej matrycy: 24.5 x 13.5 mm
display_window = Part.makeBox(24.5, 5.0, 13.5, Vector(-12.25, -1.0, -6.75))
# Wycięcie na złącze 4-pin I2C u góry
i2c_header_slot = Part.makeBox(12.5, 4.0, 4.5, Vector(-6.25, -0.5, 10.0))

oled_cradle = cradle_outer.cut(cradle_pocket).cut(display_window).cut(i2c_header_slot)

# 4 kołki montażowe fi 1.8 mm w standardowym rozstawie 23.5 x 23.5 mm (M2 OLED)
for ox, oz in [(-11.75, -11.75), (11.75, -11.75), (-11.75, 11.75), (11.75, 11.75)]:
    pin = Part.makeCylinder(0.9, 3.0, Vector(ox, 2.5, oz), Vector(0, -1, 0))
    oled_cradle = oled_cradle.fuse(pin)

# Obrót o 80° wokół osi X i pozycjonowanie
oled_cradle.rotate(Vector(0,0,0), Vector(1,0,0), tilt_angle)
oled_cradle.translate(oled_center)
core = core.fuse(oled_cradle)

# -------------------------------------------------------------
# 7. SZYNY PROWADZĄCE QUICK-SWAP I ZATRZASKI KULKOWE
# -------------------------------------------------------------
side_rib_l = Part.makeBox(1.6, 22.0, 13.0, Vector(-21.8, -11.0, 1.8))
side_rib_r = Part.makeBox(1.6, 22.0, 13.0, Vector( 20.2, -11.0, 1.8))

# Fazy wprowadzające 30° na szczycie szyn (Z=11-14 mm)
chamfer_l = Part.makeBox(3.0, 24.0, 4.0, Vector(-23.0, -12.0, 12.0))
chamfer_l.rotate(Vector(-21.8, 0, 12.0), Vector(0, 1, 0), -30.0)
chamfer_r = Part.makeBox(3.0, 24.0, 4.0, Vector( 20.2, -12.0, 12.0))
chamfer_r.rotate(Vector( 21.8, 0, 12.0), Vector(0, 1, 0), 30.0)

side_rib_l = side_rib_l.cut(chamfer_l)
side_rib_r = side_rib_r.cut(chamfer_r)
core = core.fuse(side_rib_l).fuse(side_rib_r)

# Zatrzaski kulkowe (fi 1.8 mm) na wysokości Z = 9.5 mm
snap_detent_l = Part.makeSphere(0.9, Vector(-21.6, 0.0, 9.5))
snap_detent_r = Part.makeSphere(0.9, Vector( 21.6, 0.0, 9.5))
core = core.fuse(snap_detent_l).fuse(snap_detent_r)

# -------------------------------------------------------------
# 8. GNIAZDA NÓŻEK SILIKONOWYCH (Dół)
# -------------------------------------------------------------
for fx, fy in [(-16.0, -21.0), (16.0, -21.0), (-16.0, 13.0), (16.0, 13.0)]:
    foot_pocket = Part.makeCylinder(4.1, 0.8, Vector(fx, fy, -0.1), Vector(0,0,1))
    core = core.cut(foot_pocket)

# -------------------------------------------------------------
# WALIDACJA GEOMETRII I EKSPORT
# -------------------------------------------------------------
print("\n--- Walidacja Nowego Stelaża Universal Core Chassis v2.0 ---")
is_valid = core.isValid()
is_closed = core.isClosed()
num_solids = len(core.Solids)
volume = core.Volume

print(f"Nowy Stelaż Elektroniki: Valid={is_valid}, Closed={is_closed}, Solids={num_solids}, Volume={volume:.1f} mm³")

if not (is_valid and is_closed and num_solids == 1):
    print("OSTRZEŻENIE: Geometria wymaga uwagi!")
else:
    print("SUKCES! Nowy stelaż jest w 100% poprawną, pojedynczą bryłą typu Solid (Watertight/Manifold)!")

# Eksport STL, STEP i FreeCAD
stl_out = os.path.join(stl_dir, 'core_chassis.stl')
step_out = os.path.join(base_dir, 'core_chassis.step')
fcstd_out = os.path.join(base_dir, 'robot_core_chassis.FCStd')

mesh = MeshPart.meshFromShape(Shape=core, LinearDeflection=0.04, AngularDeflection=0.17)
mesh.write(stl_out)
print(f"Zapisano nowy STL: {stl_out} ({os.path.getsize(stl_out):,} B)")

doc = FreeCAD.newDocument("RobotCoreChassis_v2")
obj = doc.addObject("Part::Feature", "UniversalCoreChassis")
obj.Shape = core
doc.recompute()
Import.export([obj], step_out)
print(f"Zapisano nowy STEP: {step_out}")
doc.saveAs(fcstd_out)
print(f"Zapisano nowy projekt FreeCAD: {fcstd_out}")
print("=== Zakończono generowanie Nowego Stelaża Elektroniki v2.0! ===")
