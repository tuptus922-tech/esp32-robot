#!/usr/bin/env python3
"""
Generator parametrycznej obudowy robota ESP32: Wersja 3 - Cyber-Titan Dreadnought
Ciężki pancerz bojowy, fasetowana geometria stealth, osłona czołowa blast-shield,
masywne radiatory chłodzenia, podwójne stateczniki aero i taktyczne klawisze.
"""

import sys
import os
import math

sys.path.append('/usr/lib/freecad/lib')
import FreeCAD
import Part
import Mesh
import MeshPart
from FreeCAD import Vector

print("=== Generowanie nowej bryły: CYBER-TITAN DREADNOUGHT (Ciężki Pancerz Mecha) ===")

base_dir = '/home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models'
stl_dread_dir = os.path.join(base_dir, 'stl_print', 'dreadnought')
os.makedirs(stl_dread_dir, exist_ok=True)

split_z = 10.5

# -------------------------------------------------------------
# 1. GŁÓWNY PROFIL BRYŁY MECHA (YZ) I FASYTOWANIE STEALTH
# -------------------------------------------------------------
p_outer = [
    Vector(0,  24.0,  0.0), # Tył dół
    Vector(0, -34.0,  0.0), # Przód dół (masywny zderzak)
    Vector(0, -34.0,  9.0), # Pionowy przód bazy
    Vector(0, -28.0, 14.5), # Skośny chin-guard
    Vector(0, -25.5, 20.0), # Przejście na twarz OLED
    Vector(0, -23.0, 35.0), # Góra okna OLED
    Vector(0, -27.0, 39.0), # Pancerny daszek czołowy (Blast Shield brow - 45° overhang)
    Vector(0, -12.0, 46.5), # Przejście daszka na pancerz dachu
    Vector(0,  19.0, 46.5), # Dach
    Vector(0,  24.0, 42.0), # Tył góra faza
    Vector(0,  24.0,  0.0)  # Zamknięcie
]

p_inner = [
    Vector(0,  22.0,  2.0),
    Vector(0, -31.5,  2.0),
    Vector(0, -31.5,  8.5),
    Vector(0, -25.5, 13.5),
    Vector(0, -23.0, 19.5),
    Vector(0, -20.5, 35.0),
    Vector(0, -24.0, 38.5),
    Vector(0, -11.0, 44.5),
    Vector(0,  17.0, 44.5),
    Vector(0,  22.0, 40.5),
    Vector(0,  22.0,  2.0)
]

lines_out = [Part.makeLine(p_outer[i], p_outer[i+1]) for i in range(len(p_outer)-1)]
lines_in = [Part.makeLine(p_inner[i], p_inner[i+1]) for i in range(len(p_inner)-1)]

prism_out = Part.Face(Part.Wire(lines_out)).extrude(Vector(60, 0, 0)).translate(Vector(-30, 0, 0))
prism_in = Part.Face(Part.Wire(lines_in)).extrude(Vector(44, 0, 0)).translate(Vector(-22, 0, 0))

# Fasetowanie narożników w stylu stealth fighter (4.0 mm 45° chamfers)
hw, hl = 25.0, 36.0
c = 4.0
pts_stealth = [
    Vector(-hw + c, -hl, 0),
    Vector( hw - c, -hl, 0),
    Vector( hw, -hl + c, 0),
    Vector( hw,  hl - c, 0),
    Vector( hw - c,  hl, 0),
    Vector(-hw + c,  hl, 0),
    Vector(-hw,  hl - c, 0),
    Vector(-hw, -hl + c, 0),
    Vector(-hw + c, -hl, 0)
]
stealth_cutter = Part.Face(Part.Wire([Part.makeLine(pts_stealth[i], pts_stealth[i+1]) for i in range(len(pts_stealth)-1)])).extrude(Vector(0, 0, 60))

body_outer = prism_out.common(stealth_cutter)
shell = body_outer.cut(prism_in)

base_raw = shell.common(Part.makeBox(70, 80, split_z, Vector(-35, -40, 0)))
hood_raw = shell.common(Part.makeBox(70, 80, 50, Vector(-35, -40, split_z)))

# -------------------------------------------------------------
# 2. PODSTAWA DREADNOUGHT (Pancerne płozy narożne, wlot turbiny)
# -------------------------------------------------------------
base = base_raw

# 2.1 Prowadnice ESP32
rail_left = Part.makeBox(2.2, 50.0, 2.5, Vector(-16.0, -29.0, 2.0))
rail_right = Part.makeBox(2.2, 50.0, 2.5, Vector(13.8, -29.0, 2.0))
ledge_left = Part.makeBox(1.5, 48.0, 1.2, Vector(-14.5, -28.0, 2.0))
ledge_right = Part.makeBox(1.5, 48.0, 1.2, Vector(13.0, -28.0, 2.0))
front_stop = Part.makeBox(28.0, 2.0, 2.5, Vector(-14.0, -29.5, 2.0))
base = base.fuse(rail_left).fuse(rail_right).fuse(ledge_left).fuse(ledge_right).fuse(front_stop)

# 2.2 Wycięcie USB
usb_cut_base = Part.makeBox(13.0, 6.0, split_z - 2.8 + 0.5, Vector(-6.5, 21.0, 2.8))
base = base.cut(usb_cut_base)

# 2.3 Pancerne płozy narożne (Outrigger Skid Pods)
# Poszerzają bazę do X = +/- 27.5 mm z fasetami 45°
for sx in [-1.0, 1.0]:
    # Przednia płoza
    pod_f = Part.makeBox(3.5, 12.0, 9.5, Vector(-28.0 if sx < 0 else 24.5, -34.5, 0.0))
    c_f = Part.makeBox(5.0, 5.0, 11.0, Vector(-28.0 if sx < 0 else 28.0, -34.5, -0.5))
    c_f.rotate(Vector(-28.0 if sx < 0 else 28.0, -34.5, 0), Vector(0,0,1), 45.0 if sx < 0 else -45.0)
    pod_f = pod_f.cut(c_f)
    
    # Tylna płoza
    pod_r = Part.makeBox(3.5, 12.0, 9.5, Vector(-28.0 if sx < 0 else 24.5, 12.0, 0.0))
    c_r = Part.makeBox(5.0, 5.0, 11.0, Vector(-28.0 if sx < 0 else 28.0, 24.0, -0.5))
    c_r.rotate(Vector(-28.0 if sx < 0 else 28.0, 24.0, 0), Vector(0,0,1), -45.0 if sx < 0 else 45.0)
    pod_r = pod_r.cut(c_r)
    
    base = base.fuse(pod_f).fuse(pod_r)

# 2.4 Heksagonalny wlot turbiny na dolnym zderzaku
chin_intake = Part.makeBox(16.0, 4.0, 4.0, Vector(-8.0, -35.5, 2.5))
# Fasetowanie wlotu
c_in_1 = Part.makeBox(3.0, 5.0, 3.0, Vector(-8.0, -36.0, 2.5))
c_in_1.rotate(Vector(-8.0, -34.0, 2.5), Vector(0,1,0), 45.0)
c_in_2 = Part.makeBox(3.0, 5.0, 3.0, Vector(8.0, -36.0, 2.5))
c_in_2.rotate(Vector(8.0, -34.0, 2.5), Vector(0,1,0), -45.0)
chin_intake = chin_intake.cut(c_in_1).cut(c_in_2)
# Środkowa łopatka wlotu (divider vane)
vane = Part.makeBox(16.0, 3.0, 0.8, Vector(-8.0, -35.0, 4.1))
chin_intake = chin_intake.cut(vane)
base = base.cut(chin_intake)

# 2.5 Otwory na 3 przyciski taktyczne
for bx in [-14.0, 0.0, 14.0]:
    btn_hole = Part.makeCylinder(2.8, 6.0, Vector(bx, -36.0, 5.6), Vector(0, 1, 0))
    btn_shld = Part.makeCylinder(3.8, 2.0, Vector(bx, -32.5, 5.6), Vector(0, 1, 0))
    base = base.cut(btn_hole).cut(btn_shld)

# 2.6 Kołnierz centrujący U-kształtny
lip_l = Part.makeBox(1.2, 43.0, 1.6, Vector(-23.0, -21.0, split_z))
lip_r = Part.makeBox(1.2, 43.0, 1.6, Vector( 21.8, -21.0, split_z))
lip_back = Part.makeBox(43.6, 1.2, 1.6, Vector(-21.8, 20.8, split_z))
interlock_lip = lip_l.fuse(lip_r).fuse(lip_back).cut(Part.makeBox(14.0, 4.0, 3.0, Vector(-7.0, 20.0, split_z - 0.5)))
base = base.fuse(interlock_lip)

# 2.7 Słupki montażowe M3
screw_positions = [(-18.8, -15.0), (18.8, -15.0), (-18.8, 18.5), (18.8, 18.5)]
for sx, sy in screw_positions:
    post = Part.makeCylinder(3.5, split_z - 2.0, Vector(sx, sy, 2.0), Vector(0,0,1))
    base = base.fuse(post)
    hole = Part.makeCylinder(1.7, split_z + 2.0, Vector(sx, sy, -0.5), Vector(0,0,1))
    cbore = Part.makeCylinder(3.1, 2.0, Vector(sx, sy, -0.1), Vector(0,0,1))
    base = base.cut(hole).cut(cbore)

# 2.8 Nóżki antypoślizgowe
for fx, fy in [(-18.0, -22.0), (18.0, -22.0), (-18.0, 14.0), (18.0, 14.0)]:
    foot = Part.makeCylinder(4.1, 0.8, Vector(fx, fy, -0.1), Vector(0,0,1))
    base = base.cut(foot)

# -------------------------------------------------------------
# 3. GŁOWA DREADNOUGHT (Blast Shield, Radiatory, Stateczniki)
# -------------------------------------------------------------
hood = hood_raw

# 3.1 Okno ekranu OLED i Oktagonalny Pancerz Wizjera
oled_z = 27.5
# Ściana od Z=20 (Y=-25.5) do Z=35 (Y=-23.0)
oled_y = -25.5 + (oled_z - 20.0) * (2.5 / 15.0) # -24.25 mm
tilt_angle = -9.46

# Oktagonalna ramka pancerza wokół ekranu (wystaje o 2.2 mm)
ow, oh, oc = 29.0, 16.5, 3.0
how, hoh = ow / 2.0, oh / 2.0
o_pts = [
    Vector(-how + oc, 0,  hoh),
    Vector( how - oc, 0,  hoh),
    Vector( how,      0,  hoh - oc),
    Vector( how,      0, -hoh + oc),
    Vector( how - oc, 0, -hoh),
    Vector(-how + oc, 0, -hoh),
    Vector(-how,      0, -hoh + oc),
    Vector(-how,      0,  hoh - oc),
    Vector(-how + oc, 0,  hoh)
]
o_wire = Part.Wire([Part.makeLine(o_pts[i], o_pts[i+1]) for i in range(len(o_pts)-1)])
o_solid = Part.Face(o_wire).extrude(Vector(0, -2.2, 0))

# Wycięcie wewnętrzne
iw, ih, ic = 23.5, 12.5, 1.2
hiw, hih = iw / 2.0, ih / 2.0
i_pts = [
    Vector(-hiw + ic, 0,  hih),
    Vector( hiw - ic, 0,  hih),
    Vector( hiw,      0,  hih - ic),
    Vector( hiw,      0, -hih + ic),
    Vector( hiw - ic, 0, -hih),
    Vector(-hiw + ic, 0, -hih),
    Vector(-hiw,      0, -hih + ic),
    Vector(-hiw,      0,  hih - ic),
    Vector(-hiw + ic, 0,  hih)
]
i_wire = Part.Wire([Part.makeLine(i_pts[i], i_pts[i+1]) for i in range(len(i_pts)-1)])
o_cut = Part.Face(i_wire).extrude(Vector(0, -6.0, 0)).translate(Vector(0, 1.0, 0))
oled_frame = o_solid.cut(o_cut)

oled_frame.rotate(Vector(0,0,0), Vector(1,0,0), tilt_angle)
oled_frame.translate(Vector(0, oled_y, oled_z))
hood = hood.fuse(oled_frame)

# Przestrzelenie okna ekranu na wylot
screen_cut = Part.Face(i_wire).extrude(Vector(0, 15.0, 0)).translate(Vector(0, -5.0, 0))
screen_cut.rotate(Vector(0,0,0), Vector(1,0,0), tilt_angle)
screen_cut.translate(Vector(0, oled_y, oled_z))
hood = hood.cut(screen_cut)

# Wewnętrzna kieszeń oporowa na OLED
oled_pocket = Part.makeBox(27.4, 2.0, 27.4, Vector(-13.7, 0.0, -13.7))
oled_pocket.rotate(Vector(0,0,0), Vector(1,0,0), tilt_angle)
oled_pocket.translate(Vector(0, -21.8, oled_z))
hood = hood.cut(oled_pocket)

# 3.2 Masywne Radiatory Boczne (Heavy Stepped Heat-Sinks)
# 4 głębokie żebra chłodzące pod kątem 45° na każdym boku (X = +/- 25)
for r_z in [16.0, 22.0, 28.0, 34.0]:
    # Lewy radiator
    rl = Part.makeBox(2.5, 34.0, 2.5, Vector(-1.25, -17.0, -1.25))
    rl.rotate(Vector(0,0,0), Vector(0,1,0), 45.0)
    rl.translate(Vector(-25.0, 0.0, r_z))
    # Prawy radiator
    rr = Part.makeBox(2.5, 34.0, 2.5, Vector(-1.25, -17.0, -1.25))
    rr.rotate(Vector(0,0,0), Vector(0,1,0), 45.0)
    rr.translate(Vector(25.0, 0.0, r_z))
    hood = hood.cut(rl).cut(rr)

# Boczne płyty pancerza reaktora (Armor Plating Slabs)
slab_l = Part.makeBox(2.5, 24.0, 20.0, Vector(-26.5, -12.0, 16.0))
c_top = Part.makeBox(4.0, 26.0, 4.0, Vector(-27.0, -13.0, 34.0))
c_top.rotate(Vector(-26.5, 0, 36.0), Vector(0,1,0), 45.0)
c_bot = Part.makeBox(4.0, 26.0, 4.0, Vector(-27.0, -13.0, 14.0))
c_bot.rotate(Vector(-26.5, 0, 16.0), Vector(0,1,0), -45.0)
slab_l = slab_l.cut(c_top).cut(c_bot)

slab_r = Part.makeBox(2.5, 24.0, 20.0, Vector(24.0, -12.0, 16.0))
c_top_r = Part.makeBox(4.0, 26.0, 4.0, Vector(23.0, -13.0, 34.0))
c_top_r.rotate(Vector(26.5, 0, 36.0), Vector(0,1,0), -45.0)
c_bot_r = Part.makeBox(4.0, 26.0, 4.0, Vector(23.0, -13.0, 14.0))
c_bot_r.rotate(Vector(26.5, 0, 16.0), Vector(0,1,0), 45.0)
slab_r = slab_r.cut(c_top_r).cut(c_bot_r)

hood = hood.fuse(slab_l).fuse(slab_r)

# 3.3 Podwójne Stateczniki Taktyczne (Aero Stealth Fins)
fin_pts = [
    Vector(0, -6.0, 45.5),
    Vector(0,  5.0, 56.5),
    Vector(0, 13.0, 56.5),
    Vector(0, 18.0, 45.5),
    Vector(0, -6.0, 45.5)
]
f_wire = Part.Wire([Part.makeLine(fin_pts[i], fin_pts[i+1]) for i in range(len(fin_pts)-1)])
f_face = Part.Face(f_wire)
fin_l = f_face.extrude(Vector(2.5, 0, 0)).translate(Vector(-18.5, 0, 0))
fin_r = f_face.extrude(Vector(2.5, 0, 0)).translate(Vector( 16.0, 0, 0))
hood = hood.fuse(fin_l).fuse(fin_r)

# 3.4 Podwójne wyloty chłodzenia i akustyki na plecach (Exhaust Vents)
for vent_z in [34.0, 39.5]:
    vent = Part.makeBox(22.0, 4.0, 2.2, Vector(-11.0, 22.0, vent_z))
    # 45-deg nachylenie żaluzji wydechowych
    v_bevel = Part.makeBox(24.0, 3.0, 3.0, Vector(-12.0, 22.0, vent_z))
    v_bevel.rotate(Vector(0, 24.0, vent_z), Vector(1,0,0), 45.0)
    hood = hood.cut(vent)

# 3.5 Kieszenie na sensory dotyku pod pancerzem dachu (strop 1.0 mm)
touch_front = Part.makeBox(28.0, 11.0, 1.2, Vector(-14.0, -11.0, 45.3))
touch_rear = Part.makeBox(28.0, 13.0, 1.2, Vector(-14.0,  3.0, 45.3))
hood = hood.cut(touch_front).cut(touch_rear)

# Grawerowane linie pancerza na dachu (Tactical Armor Seam)
seam = Part.makeBox(1.2, 28.0, 0.8, Vector(-0.6, -10.0, 46.0))
hood = hood.cut(seam)

# 3.6 Rowek na kołnierz centrujący
rec_l = Part.makeBox(1.8, 44.0, 2.0, Vector(-23.3, -21.5, split_z - 0.2))
rec_r = Part.makeBox(1.8, 44.0, 2.0, Vector( 21.5, -21.5, split_z - 0.2))
rec_back = Part.makeBox(44.8, 1.8, 2.0, Vector(-22.4, 20.5, split_z - 0.2))
hood = hood.cut(rec_l.fuse(rec_r).fuse(rec_back))

# 3.7 Wycięcie USB i 4 słupki montażowe
usb_cut_hood = Part.makeBox(13.0, 6.0, 1.2, Vector(-6.5, 21.0, split_z - 0.2))
hood = hood.cut(usb_cut_hood)

for sx, sy in screw_positions:
    post_upper = Part.makeCylinder(3.5, 6.0, Vector(sx, sy, split_z), Vector(0,0,1))
    hood = hood.fuse(post_upper)
    pilot = Part.makeCylinder(1.4, 7.0, Vector(sx, sy, split_z - 0.2), Vector(0,0,1))
    hood = hood.cut(pilot)

# -------------------------------------------------------------
# 4. PRZYCISKI TAKTYCZNE (Romb/Diament + Strzałki Chevron)
# -------------------------------------------------------------
btn_flange = Part.makeCylinder(3.6, 1.2, Vector(0,0,0), Vector(0,0,1))
btn_stem = Part.makeCylinder(2.6, 4.0, Vector(0,0,1.2), Vector(0,0,1))
btn_pusher = Part.makeCylinder(1.1, 1.5, Vector(0,0,-1.5), Vector(0,0,1))
btn_head = Part.makeBox(4.8, 4.8, 2.5, Vector(-2.4, -2.4, 5.2))
for cx, cy in [(-2.4, -2.4), (2.4, -2.4), (2.4, 2.4), (-2.4, 2.4)]:
    cc = Part.makeBox(1.5, 1.5, 3.0, Vector(cx - 0.75, cy - 0.75, 5.0))
    cc.rotate(Vector(cx, cy, 5.0), Vector(0,0,1), 45.0)
    btn_head = btn_head.cut(cc)

base_cap = btn_flange.fuse(btn_stem).fuse(btn_head).fuse(btn_pusher).translate(Vector(0,0,1.5))

# 4.1 Klawisz Środkowy: Diament / Romb (◆)
d_cutter = Part.makeBox(2.2, 2.2, 1.2, Vector(-1.1, -1.1, 7.2))
d_cutter.rotate(Vector(0,0,7.2), Vector(0,0,1), 45.0)
diamond_cap = base_cap.cut(d_cutter)

# 4.2 Klawisz Lewy: Strzałka / Chevron Lewo (◀)
arr_l = Part.makeBox(2.4, 2.4, 1.2, Vector(-0.5, -1.2, 7.2))
arr_l.rotate(Vector(0, 0, 7.2), Vector(0,0,1), 45.0)
arr_mask_l = Part.makeBox(3.0, 3.0, 1.5, Vector(0.2, -1.5, 7.1))
arrow_l_cap = base_cap.cut(arr_l.cut(arr_mask_l))

# 4.3 Klawisz Prawy: Strzałka / Chevron Prawo (▶)
arr_r = Part.makeBox(2.4, 2.4, 1.2, Vector(-1.9, -1.2, 7.2))
arr_r.rotate(Vector(0, 0, 7.2), Vector(0,0,1), 45.0)
arr_mask_r = Part.makeBox(3.0, 3.0, 1.5, Vector(-3.2, -1.5, 7.1))
arrow_r_cap = base_cap.cut(arr_r.cut(arr_mask_r))

# -------------------------------------------------------------
# 5. WALIDACJA GEOMETRII
# -------------------------------------------------------------
parts_to_verify = [
    ("Podstawa Dreadnought", base),
    ("Głowa Dreadnought", hood),
    ("Klawisz Diament (Środek)", diamond_cap),
    ("Klawisz Strzałka Lewo", arrow_l_cap),
    ("Klawisz Strzałka Prawo", arrow_r_cap)
]

print("\n--- Walidacja brył CAD Cyber-Titan Dreadnought ---")
all_valid = True
for name, p in parts_to_verify:
    valid = p.isValid() and p.isClosed() and len(p.Solids) == 1
    print(f"{name:26s}: Valid={p.isValid()}, Closed={p.isClosed()}, Solids={len(p.Solids)}, Volume={p.Volume:.1f} mm³")
    if not valid:
        all_valid = False

if not all_valid:
    print("OSTRZEŻENIE: Niektóre bryły mogą zawierać błędy!")
else:
    print("Wszystkie bryły są w 100% prawidłowymi, zamkniętymi bryłami typu Solid (Watertight/Manifold)!")

# -------------------------------------------------------------
# 6. EKSPORT STL I STEP
# -------------------------------------------------------------
print("\n--- Eksport plików STL Dreadnought do druku 3D ---")

def export_stl(shape, filename):
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.04, AngularDeflection=0.17)
    mesh.write(filename)
    print(f"Zapisano STL: {os.path.basename(filename)} ({os.path.getsize(filename):,} bajtów)")

stl_base = os.path.join(stl_dread_dir, 'dreadnought_podstawa.stl')
stl_hood = os.path.join(stl_dread_dir, 'dreadnought_glowa.stl')
stl_diamond = os.path.join(stl_dread_dir, 'dreadnought_przycisk_romb.stl')
stl_arrow_l = os.path.join(stl_dread_dir, 'dreadnought_przycisk_strzalka_l.stl')
stl_arrow_r = os.path.join(stl_dread_dir, 'dreadnought_przycisk_strzalka_p.stl')
stl_asm = os.path.join(stl_dread_dir, 'dreadnought_robot_kompletny.stl')

export_stl(base, stl_base)
export_stl(hood, stl_hood)
export_stl(diamond_cap, stl_diamond)
export_stl(arrow_l_cap, stl_arrow_l)
export_stl(arrow_r_cap, stl_arrow_r)

dread_assembly = base.fuse(hood)
export_stl(dread_assembly, stl_asm)

print("\n--- Eksport plików STEP Dreadnought ---")
Part.export([base], os.path.join(base_dir, 'dreadnought_podstawa.step'))
Part.export([hood], os.path.join(base_dir, 'dreadnought_glowa.step'))
Part.export([diamond_cap], os.path.join(base_dir, 'dreadnought_przycisk_romb.step'))
Part.export([arrow_l_cap], os.path.join(base_dir, 'dreadnought_przycisk_strzalka_l.step'))
Part.export([arrow_r_cap], os.path.join(base_dir, 'dreadnought_przycisk_strzalka_p.step'))
Part.export([base, hood], os.path.join(base_dir, 'dreadnought_robot_zlozenie.step'))
print("Pomyślnie wyeksportowano pliki STEP Dreadnought.")

# Zapis FreeCAD
fc_doc_path = os.path.join(base_dir, 'robot_dreadnought_3d.FCStd')
doc = FreeCAD.newDocument("RobotDreadnought3D")
o_base = doc.addObject("Part::Feature", "Dreadnought_Podstawa")
o_base.Shape = base
o_hood = doc.addObject("Part::Feature", "Dreadnought_Glowa")
o_hood.Shape = hood
o_diamond = doc.addObject("Part::Feature", "Dreadnought_Przycisk_Romb")
o_diamond.Shape = diamond_cap
o_arr_l = doc.addObject("Part::Feature", "Dreadnought_Przycisk_Strzalka_L")
o_arr_l.Shape = arrow_l_cap
o_arr_r = doc.addObject("Part::Feature", "Dreadnought_Przycisk_Strzalka_P")
o_arr_r.Shape = arrow_r_cap
doc.saveAs(fc_doc_path)
print(f"Zapisano projekt FreeCAD: {fc_doc_path}")

print("\n=== Zakończono pomyślnie generowanie modeli Cyber-Titan Dreadnought! ===")
