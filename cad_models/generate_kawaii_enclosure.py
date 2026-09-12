import sys
import os
import math

sys.path.append('/usr/lib/freecad/lib')
import FreeCAD
import Part
import Import
import MeshPart
from FreeCAD import Vector, Rotation, Placement

print("=== Generowanie obudowy CUTE KAWAII (Neko Cat Edition) dla ESP32 Robot Desk Pet ===")

base_dir = '/home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/'
stl_kawaii_dir = os.path.join(base_dir, 'stl_print', 'kawaii')
os.makedirs(stl_kawaii_dir, exist_ok=True)

# -------------------------------------------------------------
# Helper: Zaokrąglony graniastosłup w XY
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
# 1. Bryła korpusu (pełna zgodność z podstawą)
# -------------------------------------------------------------
p_outer = [
    Vector(0,  24.0,  0.0),
    Vector(0, -32.5,  0.0),
    Vector(0, -32.5,  9.5),
    Vector(0, -25.5, 14.5),
    Vector(0, -20.5, 43.5),
    Vector(0, -15.0, 47.0),
    Vector(0,  20.0, 47.0),
    Vector(0,  24.0, 43.0),
    Vector(0,  24.0,  0.0)
]

lines_out = [Part.makeLine(p_outer[i], p_outer[i+1]) for i in range(len(p_outer)-1)]
prism_out = Part.Face(Part.Wire(lines_out)).extrude(Vector(60, 0, 0))
prism_out.translate(Vector(-30, 0, 0))
# Miększe, urocze zaokrąglenie rogów (R = 5.5 mm)
cutter_out = make_rounded_prism(48, 62, 52, 5.5, Vector(-24, -35, -2))
body_full_outer = prism_out.common(cutter_out)

p_inner = [
    Vector(0,  22.0,  2.0),
    Vector(0, -30.5,  2.0),
    Vector(0, -30.5,  8.5),
    Vector(0, -23.5, 13.5),
    Vector(0, -18.5, 42.0),
    Vector(0, -13.5, 45.2),
    Vector(0,  18.0, 45.2),
    Vector(0,  22.0, 41.5),
    Vector(0,  22.0,  2.0)
]

lines_in = [Part.makeLine(p_inner[i], p_inner[i+1]) for i in range(len(p_inner)-1)]
prism_in = Part.Face(Part.Wire(lines_in)).extrude(Vector(60, 0, 0))
prism_in.translate(Vector(-30, 0, 0))
cutter_in = make_rounded_prism(44, 58, 52, 3.8, Vector(-22, -33, -2))
body_full_inner = prism_in.common(cutter_in)

hollow_shell = body_full_outer.cut(body_full_inner)

split_z = 10.5
box_upper_cutter = Part.makeBox(60, 70, 50, Vector(-30, -38, split_z))
hood = hollow_shell.common(box_upper_cutter)

# -------------------------------------------------------------
# 2. USZKA KOTKA (Organic Cat Ears)
# -------------------------------------------------------------
# Zaprojektowane z zachowaniem kątów druku bez podpór (draft angle <= 20° od pionu)
# Podstawa ucha lewego na dachu (Z = 46.5)
p1 = Vector(-13.0, -7.0, 46.5)
p2 = Vector(-20.5, -1.0, 46.5)
p3 = Vector(-11.5,  4.0, 46.5)
w_base = Part.makePolygon([p1, p2, p3, p1])

# Środek ucha (Z = 53.0)
m1 = Vector(-14.5, -4.5, 53.0)
m2 = Vector(-18.5, -1.0, 53.0)
m3 = Vector(-13.5,  2.0, 53.0)
w_mid = Part.makePolygon([m1, m2, m3, m1])

# Zaokrąglony czubek ucha (Z = 58.5)
t1 = Vector(-15.8, -1.8, 58.5)
t2 = Vector(-17.0, -1.0, 58.5)
t3 = Vector(-15.5, -0.2, 58.5)
w_tip = Part.makePolygon([t1, t2, t3, t1])

ear_left = Part.makeLoft([w_base, w_mid, w_tip], True, False)

# Wewnętrzne wgłębienie ucha (Inner Ear Fold)
ip1 = Vector(-14.0, -6.5, 48.0)
ip2 = Vector(-19.0, -2.0, 48.0)
ip3 = Vector(-16.0, -1.5, 56.5)
w_in = Part.makePolygon([ip1, ip2, ip3, ip1])
f_in = Part.Face(w_in)
cutter_ear_in = f_in.extrude(Vector(0, -2.5, 0))
ear_left = ear_left.cut(cutter_ear_in)

# Prawe ucho (symetryczne odbicie lustrzane)
ear_right = ear_left.mirror(Vector(0,0,0), Vector(1,0,0))

# Dołączenie uszek do głowy
hood = hood.fuse(ear_left).fuse(ear_right)

# -------------------------------------------------------------
# 3. INTERFEJS MATINGU I SŁUPKI (Zgodność z podstawą)
# -------------------------------------------------------------
# Rowek na kołnierz w kształcie U
rec_l = Part.makeBox(1.8, 44.0, 2.0, Vector(-23.3, -21.5, split_z - 0.2))
rec_r = Part.makeBox(1.8, 44.0, 2.0, Vector( 21.5, -21.5, split_z - 0.2))
rec_back = Part.makeBox(44.8, 1.8, 2.0, Vector(-22.4, 20.5, split_z - 0.2))
hood_groove = rec_l.fuse(rec_r).fuse(rec_back)
hood = hood.cut(hood_groove)

# Wycięcie USB
usb_cut_hood = Part.makeBox(13.0, 6.0, 1.2, Vector(-6.5, 21.0, split_z - 0.2))
hood = hood.cut(usb_cut_hood)

# 4 słupki montażowe M3
screw_positions = [
    (-18.8, -15.0),
    ( 18.8, -15.0),
    (-18.8,  18.5),
    ( 18.8,  18.5)
]
for sx, sy in screw_positions:
    post_upper = Part.makeCylinder(3.5, 6.0, Vector(sx, sy, split_z), Vector(0,0,1))
    hood = hood.fuse(post_upper)
    pilot_hole = Part.makeCylinder(1.4, 7.0, Vector(sx, sy, split_z - 0.2), Vector(0,0,1))
    hood = hood.cut(pilot_hole)

# -------------------------------------------------------------
# 4. OKNO EKRANU OLED I KIESZEŃ
# -------------------------------------------------------------
oled_center = Vector(0, -21.0, 27.5)

# Okno frontowe ekranu (23.5 x 12.5 mm z obrotem 80°)
screen_cut_box = Part.makeBox(23.5, 8.0, 13.0, Vector(-11.75, -4.0, -6.5))
screen_cut_box.rotate(Vector(0,0,0), Vector(1,0,0), 80.0)
screen_cut_box.translate(oled_center)
hood = hood.cut(screen_cut_box)

# Wewnętrzna kieszeń oporowa na płytkę OLED
oled_pocket = Part.makeBox(27.4, 2.0, 27.4, Vector(-13.7, 0.0, -13.7))
oled_pocket.rotate(Vector(0,0,0), Vector(1,0,0), 80.0)
oled_pocket.translate(Vector(0, -20.2, 27.5))
hood = hood.cut(oled_pocket)

# -------------------------------------------------------------
# 5. KIESZENIE DOTYKU (Ścieżka do głaskania między uszkami)
# -------------------------------------------------------------
# Czoło między uszkami: Y od -13 do -1 mm, szerokość 16 mm (strop 1.0 mm)
touch_front_pocket = Part.makeBox(18.0, 11.0, 1.2, Vector(-9.0, -12.5, 45.0))
# Tył głowy: Y od +3 do +16 mm, szerokość 28 mm
touch_rear_pocket = Part.makeBox(28.0, 13.0, 1.2, Vector(-14.0, 3.0, 45.0))
hood = hood.cut(touch_front_pocket).cut(touch_rear_pocket)

# -------------------------------------------------------------
# 6. KOCIA ŁAPKA JAKO GRILL AKUSTYCZNY BUZZERA (`🐾`)
# -------------------------------------------------------------
# Duża poduszeczka centralna
paw_center = Part.makeCylinder(2.8, 8.0, Vector(0, 10.0, 42.0), Vector(0,0,1))
hood = hood.cut(paw_center)

# 4 małe paluszki w łuku
toes = [
    Vector(-3.3, 14.0, 42.0),
    Vector(-1.2, 15.3, 42.0),
    Vector( 1.2, 15.3, 42.0),
    Vector( 3.3, 14.0, 42.0)
]
for t in toes:
    toe_cyl = Part.makeCylinder(1.15, 8.0, t, Vector(0,0,1))
    hood = hood.cut(toe_cyl)

# Drobne wytłoczenie serduszka z tyłu głowy wskazujące strefę głaskania
heart_ind_1 = Part.makeCylinder(1.2, 1.0, Vector(-1.0, -7.0, 46.7), Vector(0,0,1))
heart_ind_2 = Part.makeCylinder(1.2, 1.0, Vector( 1.0, -7.0, 46.7), Vector(0,0,1))
heart_ind_tip = Part.makeBox(2.2, 2.2, 1.0, Vector(-1.1, -8.6, 46.7))
heart_ind_tip.rotate(Vector(0, -7.5, 46.7), Vector(0,0,1), 45.0)
hood = hood.cut(heart_ind_1).cut(heart_ind_2).cut(heart_ind_tip)

# -------------------------------------------------------------
# 7. KLAWISZE KAWAII (Button Caps)
# -------------------------------------------------------------
# 7.1 Klawisz Serduszko (Środkowy - OK)
btn_flange = Part.makeCylinder(3.6, 1.2, Vector(0,0,0), Vector(0,0,1))
btn_stem = Part.makeCylinder(2.6, 4.0, Vector(0,0,1.2), Vector(0,0,1))
btn_dome = Part.makeSphere(2.6, Vector(0,0,5.2)).common(Part.makeBox(6, 6, 3, Vector(-3, -3, 5.2)))
btn_pusher = Part.makeCylinder(1.1, 1.5, Vector(0,0,-1.5), Vector(0,0,1))
heart_cap = btn_flange.fuse(btn_stem).fuse(btn_dome).fuse(btn_pusher).translate(Vector(0,0,1.5))

c1 = Part.makeCylinder(0.65, 1.5, Vector(-0.55,  0.4, 6.8), Vector(0,0,1))
c2 = Part.makeCylinder(0.65, 1.5, Vector( 0.55,  0.4, 6.8), Vector(0,0,1))
v_tip = Part.makeBox(1.5, 1.5, 1.5, Vector(-0.75, -0.75, 6.8))
v_tip.rotate(Vector(0,0,6.8), Vector(0,0,1), 45.0)
heart_cut = c1.fuse(c2).fuse(v_tip)
heart_cap = heart_cap.cut(heart_cut)

# 7.2 Klawisz Łapka (Lewo i Prawo)
paw_cap = btn_flange.fuse(btn_stem).fuse(btn_dome).fuse(btn_pusher).translate(Vector(0,0,1.5))
p_main = Part.makeCylinder(0.75, 1.5, Vector(0, -0.3, 6.8), Vector(0,0,1))
toe1 = Part.makeCylinder(0.32, 1.5, Vector(-0.75, 0.65, 6.8), Vector(0,0,1))
toe2 = Part.makeCylinder(0.35, 1.5, Vector( 0.0,  0.95, 6.8), Vector(0,0,1))
toe3 = Part.makeCylinder(0.32, 1.5, Vector( 0.75, 0.65, 6.8), Vector(0,0,1))
paw_cap = paw_cap.cut(p_main).cut(toe1).cut(toe2).cut(toe3)

# -------------------------------------------------------------
# 8. Import dolnej podstawy dla kompletnego złożenia
# -------------------------------------------------------------
doc_base = FreeCAD.openDocument(os.path.join(base_dir, 'robot_obudowa_3d.FCStd'))
base = doc_base.getObject('Obudowa_Dol_Podstawa').Shape

# -------------------------------------------------------------
# Walidacja geometrii
# -------------------------------------------------------------
parts_to_verify = [
    ("Głowa Kawaii (Top Shell)", hood),
    ("Klawisz Serduszko (Heart)", heart_cap),
    ("Klawisz Łapka (Paw)", paw_cap)
]

print("\n--- Walidacja brył CAD Kawaii ---")
all_valid = True
for name, p in parts_to_verify:
    valid = p.isValid() and p.isClosed() and len(p.Solids) == 1
    print(f"{name:26s}: Valid={p.isValid()}, Closed={p.isClosed()}, Solids={len(p.Solids)}, Volume={p.Volume:.1f} mm³")
    if not valid:
        all_valid = False

if not all_valid:
    print("OSTRZEŻENIE: Niektóre bryły Kawaii mogą zawierać błędy!")
else:
    print("Wszystkie bryły Kawaii są w 100% prawidłowymi, zamkniętymi bryłami typu Solid (Watertight/Manifold)!")

# -------------------------------------------------------------
# Eksport STL wysokiej precyzji do druku 3D
# -------------------------------------------------------------
print("\n--- Eksport plików STL Kawaii do druku 3D ---")

def export_stl(shape, filename):
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.04, AngularDeflection=0.17)
    mesh.write(filename)
    print(f"Zapisano STL: {os.path.basename(filename)} ({os.path.getsize(filename):,} bajtów)")

stl_hood = os.path.join(stl_kawaii_dir, 'kawaii_obudowa_gora_glowa.stl')
stl_heart = os.path.join(stl_kawaii_dir, 'kawaii_przycisk_serce.stl')
stl_paw = os.path.join(stl_kawaii_dir, 'kawaii_przycisk_lapka.stl')
stl_asm = os.path.join(stl_kawaii_dir, 'kawaii_robot_kompletny.stl')

export_stl(hood, stl_hood)
export_stl(heart_cap, stl_heart)
export_stl(paw_cap, stl_paw)

# Złożenie kompletne (Baza + Głowa Kawaii)
kawaii_assembly = base.fuse(hood)
export_stl(kawaii_assembly, stl_asm)

# -------------------------------------------------------------
# Eksport STEP
# -------------------------------------------------------------
print("\n--- Eksport plików STEP Kawaii ---")
Import.export([hood], os.path.join(base_dir, 'kawaii_obudowa_gora_glowa.step'))
Import.export([heart_cap], os.path.join(base_dir, 'kawaii_przycisk_serce.step'))
Import.export([paw_cap], os.path.join(base_dir, 'kawaii_przycisk_lapka.step'))
Import.export([base, hood], os.path.join(base_dir, 'kawaii_robot_zlozenie.step'))
print("Pomyślnie wyeksportowano pliki STEP Kawaii.")

# -------------------------------------------------------------
# Zapis projektu FreeCAD (.FCStd)
# -------------------------------------------------------------
fc_doc_path = os.path.join(base_dir, 'robot_kawaii_3d.FCStd')
doc = FreeCAD.newDocument("RobotKawaii3D")
o_base = doc.addObject("Part::Feature", "Obudowa_Dol_Podstawa")
o_base.Shape = base
o_hood = doc.addObject("Part::Feature", "Kawaii_Obudowa_Gora_Glowa")
o_hood.Shape = hood
o_heart = doc.addObject("Part::Feature", "Kawaii_Przycisk_Serce")
o_heart.Shape = heart_cap
o_paw = doc.addObject("Part::Feature", "Kawaii_Przycisk_Lapka")
o_paw.Shape = paw_cap
doc.recompute()
doc.saveAs(fc_doc_path)
print(f"Zapisano projekt FreeCAD Kawaii: {fc_doc_path}")

print("\n=== Zakończono pomyślnie generowanie modeli Cute Kawaii! ===")
