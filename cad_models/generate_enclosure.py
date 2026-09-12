import sys
import os
import math

sys.path.append('/usr/lib/freecad/lib')
import FreeCAD
import Part
import Import
import MeshPart
from FreeCAD import Vector, Rotation, Placement

print("=== Generowanie parametrycznej obudowy 3D dla ESP32 Robot Desk Pet ===")

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
# 1. Tworzenie bryły głównej obudowy
# -------------------------------------------------------------
p_outer = [
    Vector(0,  24.0,  0.0),    # 0: Spód tył
    Vector(0, -32.5,  0.0),    # 1: Spód przód
    Vector(0, -32.5,  9.5),    # 2: Broda przód (przyciski)
    Vector(0, -25.5, 14.5),    # 3: Przejście 45° do ekranu OLED
    Vector(0, -20.5, 43.5),    # 4: Góra ekranu OLED (kąt 80°)
    Vector(0, -15.0, 47.0),    # 5: Czoło dachu
    Vector(0,  20.0, 47.0),    # 6: Tył dachu
    Vector(0,  24.0, 43.0),    # 7: Zaokrąglenie tylnego rogu dachu
    Vector(0,  24.0,  0.0)     # 8: Tył dół
]

lines_out = [Part.makeLine(p_outer[i], p_outer[i+1]) for i in range(len(p_outer)-1)]
prism_out = Part.Face(Part.Wire(lines_out)).extrude(Vector(60, 0, 0))
prism_out.translate(Vector(-30, 0, 0))
cutter_out = make_rounded_prism(48, 62, 52, 5.0, Vector(-24, -35, -2))
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
cutter_in = make_rounded_prism(44, 58, 52, 3.5, Vector(-22, -33, -2))
body_full_inner = prism_in.common(cutter_in)

hollow_shell = body_full_outer.cut(body_full_inner)

split_z = 10.5
box_lower_cutter = Part.makeBox(60, 70, split_z, Vector(-30, -38, 0))
base_raw = hollow_shell.common(box_lower_cutter)

box_upper_cutter = Part.makeBox(60, 70, 50, Vector(-30, -38, split_z))
hood_raw = hollow_shell.common(box_upper_cutter)

# -------------------------------------------------------------
# 2. DETALE PODSTAWY (Bottom Chassis)
# -------------------------------------------------------------
base = base_raw

# 2.1 Szyny i łoże dla ESP32 DevKit V1
rail_left = Part.makeBox(2.2, 50.0, 2.5, Vector(-16.0, -29.0, 2.0))
rail_right = Part.makeBox(2.2, 50.0, 2.5, Vector(13.8, -29.0, 2.0))
ledge_left = Part.makeBox(1.5, 48.0, 1.2, Vector(-14.5, -28.0, 2.0))
ledge_right = Part.makeBox(1.5, 48.0, 1.2, Vector(13.0, -28.0, 2.0))
front_stop = Part.makeBox(28.0, 2.0, 2.5, Vector(-14.0, -29.5, 2.0))

base = base.fuse(rail_left).fuse(rail_right).fuse(ledge_left).fuse(ledge_right).fuse(front_stop)

# 2.2 Wycięcie na port USB
usb_cut_base = Part.makeBox(13.0, 6.0, split_z - 2.8 + 0.5, Vector(-6.5, 21.0, 2.8))
base = base.cut(usb_cut_base)

# 2.3 Kołnierz centrujący (Interlocking Lip) w kształcie U wzdłuż boków i tyłu
lip_l = Part.makeBox(1.2, 43.0, 1.6, Vector(-23.0, -21.0, split_z))
lip_r = Part.makeBox(1.2, 43.0, 1.6, Vector( 21.8, -21.0, split_z))
lip_back = Part.makeBox(43.6, 1.2, 1.6, Vector(-21.8, 20.8, split_z))
interlock_lip = lip_l.fuse(lip_r).fuse(lip_back).cut(Part.makeBox(14.0, 4.0, 3.0, Vector(-7.0, 20.0, split_z - 0.5)))
base = base.fuse(interlock_lip)

# Pozycje słupków montażowych łączących obie połówki
screw_positions = [
    (-18.8, -15.0),
    ( 18.8, -15.0),
    (-18.8,  18.5),
    ( 18.8,  18.5)
]

# 2.4 Słupki montażowe w podstawie
for sx, sy in screw_positions:
    post_solid = Part.makeCylinder(3.5, split_z - 2.0, Vector(sx, sy, 2.0), Vector(0,0,1))
    base = base.fuse(post_solid)
    screw_hole = Part.makeCylinder(1.7, split_z + 2.0, Vector(sx, sy, -0.5), Vector(0,0,1))
    screw_cbore = Part.makeCylinder(3.1, 2.0, Vector(sx, sy, -0.1), Vector(0,0,1))
    base = base.cut(screw_hole).cut(screw_cbore)

# 2.5 4 gniazda na nóżki antypoślizgowe (fi 8.2 mm)
for fx, fy in [(-16.0, -21.0), (16.0, -21.0), (-16.0, 13.0), (16.0, 13.0)]:
    foot_pocket = Part.makeCylinder(4.1, 0.8, Vector(fx, fy, -0.1), Vector(0,0,1))
    base = base.cut(foot_pocket)

# 2.6 Otwory na 3 przyciski w dolnej brodzie
for bx in [-14.0, 0.0, 14.0]:
    btn_cut = Part.makeCylinder(2.8, 6.0, Vector(bx, -35.0, 5.6), Vector(0, 1, 0))
    btn_shoulder = Part.makeCylinder(3.8, 2.0, Vector(bx, -31.5, 5.6), Vector(0, 1, 0))
    base = base.cut(btn_cut).cut(btn_shoulder)

# -------------------------------------------------------------
# 3. DETALE GÓRNEJ OBUDOWY / GŁOWY (Top Shell / Hood)
# -------------------------------------------------------------
hood = hood_raw

# 3.1 Wybranie na kołnierz centrujący bazy (z tolerancją pasowania 0.3 mm)
rec_l = Part.makeBox(1.8, 44.0, 2.0, Vector(-23.3, -21.5, split_z - 0.2))
rec_r = Part.makeBox(1.8, 44.0, 2.0, Vector( 21.5, -21.5, split_z - 0.2))
rec_back = Part.makeBox(44.8, 1.8, 2.0, Vector(-22.4, 20.5, split_z - 0.2))
hood_groove = rec_l.fuse(rec_r).fuse(rec_back)
hood = hood.cut(hood_groove)

# 3.2 Wycięcie na port USB w górnej obudowie
usb_cut_hood = Part.makeBox(13.0, 6.0, 1.2, Vector(-6.5, 21.0, split_z - 0.2))
hood = hood.cut(usb_cut_hood)

# 3.3 Słupki montażowe w górnej obudowie z otworem pilotażowym M3
for sx, sy in screw_positions:
    post_upper = Part.makeCylinder(3.5, 6.0, Vector(sx, sy, split_z), Vector(0,0,1))
    hood = hood.fuse(post_upper)
    pilot_hole = Part.makeCylinder(1.4, 7.0, Vector(sx, sy, split_z - 0.2), Vector(0,0,1))
    hood = hood.cut(pilot_hole)

# 3.4 Okno na wyświetlacz OLED 0.96" (nachylenie 80°, centrum Y=-21.0, Z=27.5)
oled_center = Vector(0, -21.0, 27.5)

screen_cut_box = Part.makeBox(23.5, 8.0, 13.0, Vector(-11.75, -4.0, -6.5))
screen_cut_box.rotate(Vector(0,0,0), Vector(1,0,0), 80.0)
screen_cut_box.translate(oled_center)
hood = hood.cut(screen_cut_box)

oled_pocket = Part.makeBox(27.4, 2.0, 27.4, Vector(-13.7, 0.0, -13.7))
oled_pocket.rotate(Vector(0,0,0), Vector(1,0,0), 80.0)
oled_pocket.translate(Vector(0, -20.2, 27.5))
hood = hood.cut(oled_pocket)

# 3.5 Kieszenie na folię dotykową pod dachem (strop o grubości 1.0 mm)
touch_front_pocket = Part.makeBox(32.0, 11.0, 1.2, Vector(-16.0, -12.5, 45.0))
touch_rear_pocket = Part.makeBox(32.0, 13.0, 1.2, Vector(-16.0, 3.0, 45.0))
hood = hood.cut(touch_front_pocket).cut(touch_rear_pocket)

# 3.6 Grill akustyczny dla Buzzera (5 szczelin dźwiękowych)
for slot_idx in range(-2, 3):
    slot_y = 10.0 + slot_idx * 2.5
    sound_slot = Part.makeBox(12.0, 1.4, 8.0, Vector(-6.0, slot_y - 0.7, 42.0))
    hood = hood.cut(sound_slot)

# 3.7 Wytłoczenia / Wskaźniki stref głaskania na dachu
touch_indicator_1 = Part.makeBox(8.0, 1.2, 1.0, Vector(-4.0, -7.0, 46.7))
touch_indicator_2 = Part.makeBox(8.0, 1.2, 1.0, Vector(-4.0,  9.5, 46.7))
hood = hood.cut(touch_indicator_1).cut(touch_indicator_2)

# -------------------------------------------------------------
# 4. KLAWISZ PRZYCISKU (Button Cap x3)
# -------------------------------------------------------------
btn_flange = Part.makeCylinder(3.6, 1.2, Vector(0,0,0), Vector(0,0,1))
btn_stem = Part.makeCylinder(2.6, 4.0, Vector(0,0,1.2), Vector(0,0,1))
btn_dome = Part.makeSphere(2.6, Vector(0,0,5.2))
dome_box = Part.makeBox(6, 6, 3, Vector(-3, -3, 5.2))
btn_dome = btn_dome.common(dome_box)
btn_pusher = Part.makeCylinder(1.1, 1.5, Vector(0,0,-1.5), Vector(0,0,1))

button_cap = btn_flange.fuse(btn_stem).fuse(btn_dome).fuse(btn_pusher)
button_cap.translate(Vector(0, 0, 1.5))

# -------------------------------------------------------------
# 5. UCHWYT DOCISKOWY EKRANU OLED (OLED Bracket)
# -------------------------------------------------------------
bracket = Part.makeBox(31.0, 27.0, 2.0, Vector(-15.5, 0.0, -2.0))
window = Part.makeBox(21.0, 16.0, 5.0, Vector(-10.5, 5.5, -3.0))
h_m2_1 = Part.makeCylinder(1.1, 5.0, Vector(-12.0, 13.5, -3.0), Vector(0,0,1))
h_m2_2 = Part.makeCylinder(1.1, 5.0, Vector( 12.0, 13.5, -3.0), Vector(0,0,1))
oled_bracket = bracket.cut(window).cut(h_m2_1).cut(h_m2_2)

# -------------------------------------------------------------
# Walidacja geometrii
# -------------------------------------------------------------
parts_to_verify = [
    ("Podstawa (Bottom)", base),
    ("Głowa (Top Shell)", hood),
    ("Klawisz (Button Cap)", button_cap),
    ("Uchwyt OLED (Bracket)", oled_bracket)
]

print("\n--- Walidacja brył CAD ---")
all_valid = True
for name, p in parts_to_verify:
    valid = p.isValid() and p.isClosed() and len(p.Solids) == 1
    print(f"{name:25s}: Valid={p.isValid()}, Closed={p.isClosed()}, Solids={len(p.Solids)}, Volume={p.Volume:.1f} mm³")
    if not valid:
        all_valid = False

if not all_valid:
    print("OSTRZEŻENIE: Niektóre bryły mogą zawierać błędy topologiczne!")
else:
    print("Wszystkie bryły są w 100% prawidłowymi, zamkniętymi bryłami typu Solid (Watertight/Manifold)!")

# -------------------------------------------------------------
# Eksport STL wysokiej precyzji do druku 3D
# -------------------------------------------------------------
print("\n--- Eksport plików STL do druku 3D ---")

def export_stl(shape, filename):
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.04, AngularDeflection=0.17)
    mesh.write(filename)
    print(f"Zapisano STL: {os.path.basename(filename)} ({os.path.getsize(filename):,} bajtów)")

stl_base = os.path.join(stl_dir, 'obudowa_dol_podstawa.stl')
stl_hood = os.path.join(stl_dir, 'obudowa_gora_glowa.stl')
stl_btn = os.path.join(stl_dir, 'przycisk_nakladka.stl')
stl_bracket = os.path.join(stl_dir, 'uchwyt_oled.stl')

export_stl(base, stl_base)
export_stl(hood, stl_hood)
export_stl(button_cap, stl_btn)
export_stl(oled_bracket, stl_bracket)

# Złożenie kompletnej obudowy w jednym STL
assembly = base.fuse(hood)
stl_asm = os.path.join(stl_dir, 'robot_obudowa_kompletna.stl')
export_stl(assembly, stl_asm)

# -------------------------------------------------------------
# Eksport STEP
# -------------------------------------------------------------
print("\n--- Eksport plików STEP ---")
Part.export([base], os.path.join(base_dir, 'obudowa_dol_podstawa.step'))
Part.export([hood], os.path.join(base_dir, 'obudowa_gora_glowa.step'))
Part.export([button_cap], os.path.join(base_dir, 'przycisk_nakladka.step'))
Part.export([oled_bracket], os.path.join(base_dir, 'uchwyt_oled.step'))
Part.export([base, hood], os.path.join(base_dir, 'robot_zlozenie_obudowa.step'))
print("Pomyślnie wyeksportowano pliki STEP.")

# -------------------------------------------------------------
# Zapis projektu FreeCAD (.FCStd)
# -------------------------------------------------------------
fc_doc_path = os.path.join(base_dir, 'robot_obudowa_3d.FCStd')
doc = FreeCAD.newDocument("RobotObudowa3D")
o_base = doc.addObject("Part::Feature", "Obudowa_Dol_Podstawa")
o_base.Shape = base
o_hood = doc.addObject("Part::Feature", "Obudowa_Gora_Glowa")
o_hood.Shape = hood
o_btn = doc.addObject("Part::Feature", "Przycisk_Nakladka")
o_btn.Shape = button_cap
o_brk = doc.addObject("Part::Feature", "Uchwyt_OLED")
o_brk.Shape = oled_bracket
doc.recompute()
doc.saveAs(fc_doc_path)
print(f"Zapisano projekt FreeCAD: {fc_doc_path}")

print("\n=== Zakończono pomyślnie generowanie modeli obudowy robota! ===")
