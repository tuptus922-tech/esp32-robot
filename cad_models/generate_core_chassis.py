import sys
import os
import math

sys.path.append('/usr/lib/freecad/lib')
import FreeCAD
import Part
import Import
import MeshPart
from FreeCAD import Vector, Rotation, Placement

print("=== Generowanie Uniwersalnego Stelaża Elektroniki (Universal Core Chassis) ===")

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
# Wybranie schodkowe pod korpus stelaża: zostawia kołnierz o grubości 2.0 mm na obwodzie
rim_pocket = make_rounded_prism(44.0, 56.0, 2.0, 3.8, Vector(-22.0, -32.0, 1.8))
core = rim_solid.cut(rim_pocket)

# -------------------------------------------------------------
# 2. SZYNY MONTAŻOWE ESP32 DevKit V1 (28.5 mm szerokości)
# -------------------------------------------------------------
rail_left_body = Part.makeBox(2.2, 45.0, 3.8, Vector(-16.3, -22.5, 1.8))
rail_right_body = Part.makeBox(2.2, 45.0, 3.8, Vector(14.1, -22.5, 1.8))

ledge_l = Part.makeBox(1.5, 45.0, 1.2, Vector(-14.3, -22.5, 1.8))
ledge_r = Part.makeBox(1.5, 45.0, 1.2, Vector(12.8, -22.5, 1.8))

front_stop = Part.makeBox(28.0, 2.4, 3.8, Vector(-14.0, -24.9, 1.8))
usb_notch = Part.makeBox(14.0, 12.0, 8.0, Vector(-7.0, 18.0, 2.8))

core = core.fuse(rail_left_body).fuse(rail_right_body).fuse(ledge_l).fuse(ledge_r).fuse(front_stop)
core = core.cut(usb_notch)

snap_esp_l = Part.makeBox(1.1, 8.0, 0.9, Vector(-14.9, 5.0, 4.7))
snap_esp_r = Part.makeBox(1.1, 8.0, 0.9, Vector(13.8, 5.0, 4.7))
core = core.fuse(snap_esp_l).fuse(snap_esp_r)

# -------------------------------------------------------------
# 3. KIESZEŃ NA CZUJNIK RUCHU MPU-6050 (GY-521)
# -------------------------------------------------------------
mpu_wall_l = Part.makeBox(1.5, 17.0, 2.8, Vector(-11.2, -22.5, 1.8))
mpu_wall_r = Part.makeBox(1.5, 17.0, 2.8, Vector(9.7, -22.5, 1.8))
mpu_floor = Part.makeBox(19.4, 17.0, 0.8, Vector(-9.7, -22.5, 1.8))
core = core.fuse(mpu_wall_l).fuse(mpu_wall_r).fuse(mpu_floor)

# -------------------------------------------------------------
# 4. PRZEDNIA BELKA NA 3 MIKROSTYKI TACT SWITCH 6x6 mm
# -------------------------------------------------------------
sw_bar = Part.makeBox(36.0, 5.0, 8.2, Vector(-18.0, -31.8, 1.8))
core = core.fuse(sw_bar)

for bx in [-14.0, 0.0, 14.0]:
    sw_pocket = Part.makeBox(6.4, 3.8, 6.4, Vector(bx - 3.2, -30.4, 2.4))
    sw_hole = Part.makeCylinder(2.1, 8.0, Vector(bx, -35.0, 5.6), Vector(0, 1, 0))
    core = core.cut(sw_pocket).cut(sw_hole)

# -------------------------------------------------------------
# 5. SZTYWNY MASZT MONTAŻOWY EKRANU OLED 0.96" (Kąt 80°)
# -------------------------------------------------------------
oled_center = Vector(0, -19.0, 27.5)

# Pylony nośne masztu zbiegające się z podłogi (szerokość 2.8 mm każdy, X: -13.6 do -10.8 oraz 10.8 do 13.6)
pylon_l = Part.makeBox(2.8, 14.0, 26.0, Vector(-13.6, -19.0, 1.8))
pylon_r = Part.makeBox(2.8, 14.0, 26.0, Vector( 10.8, -19.0, 1.8))
core = core.fuse(pylon_l).fuse(pylon_r)

# Ramka nośna OLED 0.96" (szer. 23.2 mm, wys. 22.0 mm, grubość 3.0 mm)
oled_cradle = Part.makeBox(23.2, 3.0, 22.0, Vector(-11.6, 0.0, -11.0))
oled_recess = Part.makeBox(22.0, 1.6, 20.0, Vector(-11.0, -0.1, -10.0))
oled_window = Part.makeBox(20.0, 5.0, 12.0, Vector(-10.0, -1.0, -6.0))

oled_frame = oled_cradle.cut(oled_recess).cut(oled_window)

# 4 kołki ustalające fi 1.6 mm pod otwory laminatu OLED (rozstaw 18.0 x 18.0 mm)
for ox, oz in [(-9.0, -9.0), (9.0, -9.0), (-9.0, 9.0), (9.0, 9.0)]:
    pin = Part.makeCylinder(0.8, 2.5, Vector(ox, 1.5, oz), Vector(0, -1, 0))
    oled_frame = oled_frame.fuse(pin)

# Obrót o -10° wokół osi X (nachylenie 80° od poziomu) i przesunięcie do oled_center
oled_frame.rotate(Vector(0,0,0), Vector(1,0,0), -10.0)
oled_frame.translate(oled_center)
core = core.fuse(oled_frame)

# -------------------------------------------------------------
# 6. KOSZYK MONTAŻOWY BUZZERA 12 mm (Buzzer Cradle)
# -------------------------------------------------------------
buzzer_mount_pos = Vector(0.0, 8.0, 30.0)
buzzer_outer = Part.makeCylinder(7.2, 9.5, buzzer_mount_pos, Vector(0,0,1))
buzzer_hole = Part.makeCylinder(6.15, 10.5, buzzer_mount_pos + Vector(0,0,-0.5), Vector(0,0,1))
wire_slot = Part.makeBox(4.0, 8.0, 6.0, buzzer_mount_pos + Vector(-2.0, -4.0, -3.0))
buzzer_cradle = buzzer_outer.cut(buzzer_hole).cut(wire_slot)

strut_l = Part.makeBox(2.2, 17.0, 30.0, Vector(-8.6, -8.0, 1.8))
strut_r = Part.makeBox(2.2, 17.0, 30.0, Vector( 6.4, -8.0, 1.8))
core = core.fuse(buzzer_cradle).fuse(strut_l).fuse(strut_r)

# -------------------------------------------------------------
# 7. SZYNY PROWADZĄCE I ZATRZASKI SZYBKIEJ WYMIANY (Quick-Swap Rails)
# -------------------------------------------------------------
side_rib_l = Part.makeBox(1.6, 22.0, 13.0, Vector(-21.8, -11.0, 1.8))
side_rib_r = Part.makeBox(1.6, 22.0, 13.0, Vector( 20.2, -11.0, 1.8))

# Fazki naprowadzające na szczycie żeber (Z=11 do 14)
chamfer_l = Part.makeBox(3.0, 24.0, 4.0, Vector(-23.0, -12.0, 12.0))
chamfer_l.rotate(Vector(-21.8, 0, 12.0), Vector(0, 1, 0), -30.0)
chamfer_r = Part.makeBox(3.0, 24.0, 4.0, Vector( 20.2, -12.0, 12.0))
chamfer_r.rotate(Vector( 21.8, 0, 12.0), Vector(0, 1, 0), 30.0)

side_rib_l = side_rib_l.cut(chamfer_l)
side_rib_r = side_rib_r.cut(chamfer_r)
core = core.fuse(side_rib_l).fuse(side_rib_r)

# Wypusty zatrzaskowe na bokach żeber prowadzących przy Z = 9.5 mm
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
# Weryfikacja geometrii i integralności bryły
# -------------------------------------------------------------
print("\n--- Walidacja stelaża Universal Core Chassis ---")
is_valid = core.isValid()
is_closed = core.isClosed()
num_solids = len(core.Solids)
volume = core.Volume

print(f"Stelaż Elektroniki: Valid={is_valid}, Closed={is_closed}, Solids={num_solids}, Volume={volume:.1f} mm³")

if not (is_valid and is_closed and num_solids == 1):
    print("OSTRZEŻENIE: Geometria wymaga naprawy topologii!")
else:
    print("SUKCES! Stelaż jest pojedynczą, w 100% zamkniętą bryłą Solid (Watertight/Manifold)!")

# Eksport STL i STEP
stl_out = os.path.join(stl_dir, 'core_chassis.stl')
step_out = os.path.join(base_dir, 'core_chassis.step')
fcstd_out = os.path.join(base_dir, 'robot_core_chassis.FCStd')

mesh = MeshPart.meshFromShape(Shape=core, LinearDeflection=0.04, AngularDeflection=0.17)
mesh.write(stl_out)
print(f"Zapisano STL: {stl_out} ({os.path.getsize(stl_out):,} B)")

doc = FreeCAD.newDocument("RobotCoreChassis")
obj = doc.addObject("Part::Feature", "UniversalCoreChassis")
obj.Shape = core
doc.recompute()
Import.export([obj], step_out)
print(f"Zapisano STEP: {step_out}")
doc.saveAs(fcstd_out)
print(f"Zapisano projekt FreeCAD: {fcstd_out}")
print("=== Zakończono generowanie Uniwersalnego Stelaża! ===")
