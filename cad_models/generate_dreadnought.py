#!/usr/bin/env python3
"""
Generator parametrycznej obudowy robota ESP32: Wersja 3 - Cyber-Titan Apex
Ekstremalny Mecha-Warrior / Kabuto Prime:
- Sylwetka V-Taper (szerokość 72 mm w naramiennikach)
- Wielkie Rogi Bojowe V-Fin (wysokość 68 mm)
- Naramienniki bojowe (Heavy Pauldrons) z wyrzutniami mikro-rakiet
- Głęboko ukryty kokpit OLED pod daszkiem blast-shield
- Szczęka mecha z przednimi mandiblami / kłami
- Podwójne dysze silników odrzutowych z tyłu
- Pancerne stopy gąsienicowe (Crawler Treads)
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

print("=== Generowanie nowej bryły: CYBER-TITAN APEX (Ekstremalny Mecha-Warrior) ===")

base_dir = '/home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models'
stl_dread_dir = os.path.join(base_dir, 'stl_print', 'dreadnought')
os.makedirs(stl_dread_dir, exist_ok=True)

split_z = 10.5

# -------------------------------------------------------------
# 1. GŁÓWNY RDZEŃ BRYŁY (YZ) I FASATOWANIE STEALTH
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

# Fasetowanie stealth narożników (4.0 mm 45° chamfers)
hw, hl = 24.5, 35.5
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

base_raw = shell.common(Part.makeBox(80, 90, split_z, Vector(-40, -45, 0)))
hood_raw = shell.common(Part.makeBox(80, 90, 50, Vector(-40, -45, split_z)))

# -------------------------------------------------------------
# 2. PODSTAWA APEX (Pancerne gąsienice crawler, wlot turbiny)
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

# 2.3 Pancerne gąsienice / stopy crawlera (rozszerzają bazę do X = +/- 32.5 mm!)
tread_r = Part.makeBox(9.5, 58.0, 9.5, Vector(22.0, -34.0, 0.0))
c_front = Part.makeBox(12.0, 8.0, 8.0, Vector(21.0, -34.5, -4.0))
c_front.rotate(Vector(21.5, -34.0, 0.0), Vector(1,0,0), -45.0)
tread_r = tread_r.cut(c_front)
c_rear = Part.makeBox(12.0, 8.0, 8.0, Vector(21.0, 23.5, -4.0))
c_rear.rotate(Vector(21.5, 23.5, 0.0), Vector(1,0,0), 45.0)
tread_r = tread_r.cut(c_rear)

for gy in [-20.0, -8.0, 4.0, 14.0]:
    groove = Part.makeBox(2.0, 2.5, 10.0, Vector(30.5, gy, -0.2))
    tread_r = tread_r.cut(groove)

tread_l = tread_r.mirror(Vector(0,0,0), Vector(1,0,0))
base = base.fuse(tread_r).fuse(tread_l)

# 2.4 Heksagonalny wlot turbiny na zderzaku
chin_intake = Part.makeBox(16.0, 4.0, 4.0, Vector(-8.0, -35.5, 2.5))
c_in_1 = Part.makeBox(3.0, 5.0, 3.0, Vector(-8.0, -36.0, 2.5))
c_in_1.rotate(Vector(-8.0, -34.0, 2.5), Vector(0,1,0), 45.0)
c_in_2 = Part.makeBox(3.0, 5.0, 3.0, Vector(8.0, -36.0, 2.5))
c_in_2.rotate(Vector(8.0, -34.0, 2.5), Vector(0,1,0), -45.0)
chin_intake = chin_intake.cut(c_in_1).cut(c_in_2)
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
# 3. GŁOWA APEX (Wielkie Naramienniki, Rogi V-Fin, Dysze Odrzutowe)
# -------------------------------------------------------------
hood = hood_raw

# 3.1 Okno ekranu OLED i Oktagonalna Osłona Kokpitu
oled_z = 27.5
oled_y = -25.5 + (oled_z - 20.0) * (2.5 / 15.0) # -24.25 mm
tilt_angle = -9.46

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

# Przestrzelenie okna na wylot
screen_cut = Part.Face(i_wire).extrude(Vector(0, 15.0, 0)).translate(Vector(0, -5.0, 0))
screen_cut.rotate(Vector(0,0,0), Vector(1,0,0), tilt_angle)
screen_cut.translate(Vector(0, oled_y, oled_z))
hood = hood.cut(screen_cut)

# Wewnętrzna kieszeń oporowa na płytkę OLED
oled_pocket = Part.makeBox(28.0, 3.8, 28.0, Vector(-14.0, -0.5, -14.0))
oled_pocket.rotate(Vector(0,0,0), Vector(1,0,0), tilt_angle)
oled_pocket.translate(Vector(0, -21.8, oled_z))
hood = hood.cut(oled_pocket)

# Wewnętrzne rowki prowadzące na szyny stelaża (Slide-on guide grooves)
guide_slot_l = Part.makeBox(2.4, 24.0, 5.0, Vector(-22.4, -12.0, split_z - 0.2))
guide_slot_r = Part.makeBox(2.4, 24.0, 5.0, Vector( 20.0, -12.0, split_z - 0.2))
hood = hood.cut(guide_slot_l).cut(guide_slot_r)

# 3.2 Przednie Kły / Mandible Żuchwy (Wysunięte do przodu na Y = -34.5)
pts_fang = [
    Vector(11.5, -28.0, 0),
    Vector(11.5, -34.5, 0),
    Vector(15.5, -31.5, 0),
    Vector(15.5, -28.0, 0),
    Vector(11.5, -28.0, 0)
]
f_fang = Part.Face(Part.Wire([Part.makeLine(pts_fang[i], pts_fang[i+1]) for i in range(len(pts_fang)-1)]))
fang_r = f_fang.extrude(Vector(0, 0, 7.5)).translate(Vector(0, 0, 11.0))
fang_l = fang_r.mirror(Vector(0,0,0), Vector(1,0,0))
hood = hood.fuse(fang_r).fuse(fang_l)

# 3.3 Wielkie Pancerne Naramienniki (Pauldrons) z Wyrzutniami Rakiet
# Rozszerzają sylwetkę robota do potężnych 72 mm!
pts_p = [
    Vector(21.0, -14.0, 22.0),
    Vector(36.0,  -6.0, 22.0),
    Vector(36.0,  14.0, 22.0),
    Vector(21.0,  19.0, 22.0),
    Vector(21.0, -14.0, 22.0)
]
f_p = Part.Face(Part.Wire([Part.makeLine(pts_p[i], pts_p[i+1]) for i in range(len(pts_p)-1)]))
pauldron_r = f_p.extrude(Vector(0, 0, 21.0))
c_box = Part.makeBox(18, 38, 15, Vector(31.0, -16.0, 36.0))
c_box.rotate(Vector(36.0, 0, 42.0), Vector(0,1,0), 45.0)
pauldron_r = pauldron_r.cut(c_box)

# 6-komorowa wyrzutnia mikro-rakiet na przedniej ścianie naramiennika
for my in range(2):
    for mz in range(3):
        m_tube = Part.makeCylinder(1.4, 2.5, Vector(29.0 + my * 4.0, -9.0, 26.0 + mz * 4.2), Vector(0, -1, 0))
        pauldron_r = pauldron_r.cut(m_tube)

# Boczne żebra chłodzące na zewnętrznym pancerzu naramiennika
for rz in [25.0, 30.0, 35.0]:
    gill = Part.makeBox(2.2, 14.0, 2.0, Vector(35.0, -4.0, rz))
    pauldron_r = pauldron_r.cut(gill)

pauldron_l = pauldron_r.mirror(Vector(0,0,0), Vector(1,0,0))
hood = hood.fuse(pauldron_r).fuse(pauldron_l)

# 3.4 Potężne Rogi Bojowe V-Fin (Wznoszą się na 68 mm!)
b_pts = [
    Vector(15.0, -8.0, 45.0),
    Vector(18.5, -8.0, 45.0),
    Vector(18.5,  17.0, 45.0),
    Vector(15.0,  17.0, 45.0),
    Vector(15.0, -8.0, 45.0)
]
w_base = Part.Wire([Part.makeLine(b_pts[i], b_pts[i+1]) for i in range(len(b_pts)-1)])

t_pts = [
    Vector(18.0, 4.0, 68.0),
    Vector(20.5, 4.0, 68.0),
    Vector(20.5, 11.0, 68.0),
    Vector(18.0, 11.0, 68.0),
    Vector(18.0, 4.0, 68.0)
]
w_tip = Part.Wire([Part.makeLine(t_pts[i], t_pts[i+1]) for i in range(len(t_pts)-1)])

horn_r = Part.makeLoft([w_base, w_tip], True)
horn_l = horn_r.mirror(Vector(0,0,0), Vector(1,0,0))
hood = hood.fuse(horn_r).fuse(horn_l)

# 3.5 Podwójne Dysze Silników Odrzutowych z Tyłu (Twin Jet Thrusters)
cyl_out_r = Part.makeCylinder(6.2, 7.5, Vector(12.0, 23.5, 31.0), Vector(0, 1, 0))
cyl_in_r = Part.makeCylinder(4.6, 8.5, Vector(12.0, 23.0, 31.0), Vector(0, 1, 0))
nozzle_r = cyl_out_r.cut(cyl_in_r)
nozzle_l = nozzle_r.mirror(Vector(0,0,0), Vector(1,0,0))
hood = hood.fuse(nozzle_r).fuse(nozzle_l)

# 3.6 Pancerne Wyloty Akustyczne dla Buzzera na Plecach
for vent_z in [39.0, 43.0]:
    vent = Part.makeBox(18.0, 4.0, 1.8, Vector(-9.0, 22.0, vent_z))
    hood = hood.cut(vent)

# 3.7 Kieszenie dotykowe na dachu między rogami (strop 1.0 mm)
touch_front = Part.makeBox(26.0, 11.0, 1.2, Vector(-13.0, -11.0, 45.3))
touch_rear = Part.makeBox(26.0, 13.0, 1.2, Vector(-13.0,  3.0, 45.3))
hood = hood.cut(touch_front).cut(touch_rear)

# Pancerne linie podziału na dachu
seam = Part.makeBox(1.2, 28.0, 0.8, Vector(-0.6, -10.0, 46.0))
hood = hood.cut(seam)

# 3.8 Rowek na kołnierz centrujący bazy
rec_l = Part.makeBox(1.8, 44.0, 2.0, Vector(-23.3, -21.5, split_z - 0.2))
rec_r = Part.makeBox(1.8, 44.0, 2.0, Vector( 21.5, -21.5, split_z - 0.2))
rec_back = Part.makeBox(44.8, 1.8, 2.0, Vector(-22.4, 20.5, split_z - 0.2))
hood = hood.cut(rec_l.fuse(rec_r).fuse(rec_back))

# 3.9 Wycięcie USB i 4 słupki montażowe
usb_cut_hood = Part.makeBox(13.0, 6.0, 1.2, Vector(-6.5, 21.0, split_z - 0.2))
hood = hood.cut(usb_cut_hood)

for sx, sy in screw_positions:
    post_upper = Part.makeCylinder(3.5, 6.0, Vector(sx, sy, split_z), Vector(0,0,1))
    hood = hood.fuse(post_upper)
    pilot = Part.makeCylinder(1.4, 7.0, Vector(sx, sy, split_z - 0.2), Vector(0,0,1))
    hood = hood.cut(pilot)

# -------------------------------------------------------------
# 4. KLAWISZE BOJOWE APEX (Heksagonalny Reaktor + Strzałki Chevron)
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

# 4.1 Klawisz Środkowy: Rdzeń Reaktora Diament (◆)
d_cutter = Part.makeBox(2.2, 2.2, 1.2, Vector(-1.1, -1.1, 7.2))
d_cutter.rotate(Vector(0,0,7.2), Vector(0,0,1), 45.0)
diamond_cap = base_cap.cut(d_cutter)

# 4.2 Klawisz Lewy: Pancerne Strzałki Chevron (◀)
arr_l = Part.makeBox(2.4, 2.4, 1.2, Vector(-0.5, -1.2, 7.2))
arr_l.rotate(Vector(0, 0, 7.2), Vector(0,0,1), 45.0)
arr_mask_l = Part.makeBox(3.0, 3.0, 1.5, Vector(0.2, -1.5, 7.1))
arrow_l_cap = base_cap.cut(arr_l.cut(arr_mask_l))

# 4.3 Klawisz Prawy: Pancerne Strzałki Chevron (▶)
arr_r = Part.makeBox(2.4, 2.4, 1.2, Vector(-1.9, -1.2, 7.2))
arr_r.rotate(Vector(0, 0, 7.2), Vector(0,0,1), 45.0)
arr_mask_r = Part.makeBox(3.0, 3.0, 1.5, Vector(-3.2, -1.5, 7.1))
arrow_r_cap = base_cap.cut(arr_r.cut(arr_mask_r))

# -------------------------------------------------------------
# 5. WALIDACJA GEOMETRII
# -------------------------------------------------------------
parts_to_verify = [
    ("Podstawa Apex (Base)", base),
    ("Głowa Apex (Hood)", hood),
    ("Klawisz Reaktor (Środek)", diamond_cap),
    ("Klawisz Strzałka Lewo", arrow_l_cap),
    ("Klawisz Strzałka Prawo", arrow_r_cap)
]

print("\n--- Walidacja brył CAD Cyber-Titan Apex ---")
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
print("\n--- Eksport plików STL Apex do druku 3D ---")

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

print("\n--- Eksport plików STEP Apex ---")
Part.export([base], os.path.join(base_dir, 'dreadnought_podstawa.step'))
Part.export([hood], os.path.join(base_dir, 'dreadnought_glowa.step'))
Part.export([diamond_cap], os.path.join(base_dir, 'dreadnought_przycisk_romb.step'))
Part.export([arrow_l_cap], os.path.join(base_dir, 'dreadnought_przycisk_strzalka_l.step'))
Part.export([arrow_r_cap], os.path.join(base_dir, 'dreadnought_przycisk_strzalka_p.step'))
Part.export([base, hood], os.path.join(base_dir, 'dreadnought_robot_zlozenie.step'))
print("Pomyślnie wyeksportowano pliki STEP Apex.")

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

print("\n=== Zakończono pomyślnie generowanie modeli Cyber-Titan Apex! ===")
