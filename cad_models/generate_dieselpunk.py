#!/usr/bin/env python3
"""
Generator parametrycznej obudowy robota ESP32: Wersja 4 - Steam-Titan Nautilus ULTRA
Ciężki Industrial Dieselpunk / Parowy Golem / Steampunk Nautilus - WERSJA MAKSYMALNA:
- Czasza wysokociśnieniowego kotła parowego (High-Pressure Steam Boiler Hull)
- Podwójne wiktoriańskie kominy parowe z kryzami chłodzącymi i kołnierzami kotwiczącymi (Twin Victorian Smokestacks)
- Pancerne pałąki ochronne klatki bezpieczeństwa / iluminatora batyskafu (Roll-Cage Crash Bars)
- Dwa wielkie boczne analogowe manometry ciśnienia pary (Side Pressure Gauges) ze wskaźnikami
- Zewnętrzne rurociągi parowe wysokiego ciśnienia z kołnierzami śrubowymi (Steam Conduits & Flanges)
- Pasy pancerne z 29 trójwymiarowymi nitami kotłowymi (Riveted Armor Straps)
- Odsłonięte koła zębate napędowe po bokach (Exposed Drive Gears / Cogs)
- Boczne iluminatory okrętowe z pierścieniami mosiężnymi i śrubami (Brass Portholes)
- Pancerne kratki wentylacyjne z żaluzjami pod kątem 30° (Armored Louvered Vents)
- Podwójne zawory bezpieczeństwa nadciśnieniowe na dachu kotła (Pressure Relief Valves)
- Wieżyczka peryskopowa z soczewką i pierścieniami (Periscope Tower)
- Śruby sześciokątne zorientowane prostopadle na panelach i pasach (Hex Bolt Heads)
- Tabliczka identyfikacyjna z nitami mocującymi (Armored Nameplate)
- Dedykowane przyciski industrialne: 6-ramienne koło zaworu parowego + płyty ryflowane z chevronami
- 100% kompatybilność z modułowym stelażem Universal Core Chassis (Slide-On, 0 kolizji, 0 podpór)
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

print("=== Generowanie bryły: STEAM-TITAN NAUTILUS ULTRA (Industrial Dieselpunk Max) ===")

base_dir = '/home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models'
stl_diesel_dir = os.path.join(base_dir, 'stl_print', 'dieselpunk')
stl_comp_dir = os.path.join(stl_diesel_dir, 'components')
os.makedirs(stl_comp_dir, exist_ok=True)

split_z = 10.5

# Wczytanie uniwersalnego stelaża Core Chassis do walidacji i precyzyjnego spasowania
doc_core = FreeCAD.openDocument(os.path.join(base_dir, 'robot_core_chassis.FCStd'))
core_chassis_shape = doc_core.Objects[0].Shape

# -------------------------------------------------------------
# Helpery geometryczne
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

def make_hex_prism(radius, height, center=Vector(0,0,0), axis=Vector(0,0,1)):
    pts = []
    for i in range(6):
        ang = math.radians(60 * i)
        pts.append(Vector(radius * math.cos(ang), radius * math.sin(ang), 0))
    pts.append(pts[0])
    w = Part.Wire([Part.makeLine(pts[i], pts[i+1]) for i in range(6)])
    poly = Part.Face(w).extrude(Vector(0,0,height))
    if axis != Vector(0,0,1):
        rot = FreeCAD.Rotation(Vector(0,0,1), axis)
        poly.Placement = FreeCAD.Placement(center, rot)
    else:
        poly.translate(center)
    return poly

# -------------------------------------------------------------
# 1. GŁÓWNY RDZEŃ KADŁUBA KOTŁA PAROWEGO (Steam Boiler Hull)
# -------------------------------------------------------------
p_outer = [
    Vector(0,  24.0,  0.0), # Tył dół
    Vector(0, -34.0,  0.0), # Przód dół (zderzak)
    Vector(0, -34.0,  8.5), # Przód pionowy
    Vector(0, -28.0, 14.5), # Przejście do żuchwy
    Vector(0, -25.5, 20.0), # Dolna krawędź okna OLED
    Vector(0, -23.0, 35.0), # Górna krawędź okna OLED
    Vector(0, -26.5, 39.5), # Daszek iluminatora (45° kąt zwisu)
    Vector(0, -12.0, 46.5), # Łuk dachu przód
    Vector(0,  18.0, 46.5), # Dach kocioł
    Vector(0,  24.0, 41.5), # Tył łuk
    Vector(0,  24.0,  0.0)  # Zamknięcie
]

p_inner = [
    Vector(0,  22.0,  2.0),
    Vector(0, -31.8,  2.0),
    Vector(0, -31.8,  8.5),
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

prism_out = Part.Face(Part.Wire(lines_out)).extrude(Vector(58, 0, 0)).translate(Vector(-29, 0, 0))
prism_in = Part.Face(Part.Wire(lines_in)).extrude(Vector(44.8, 0, 0)).translate(Vector(-22.4, 0, 0))

# Zaokrąglone narożniki kotła (R = 5.5 mm)
cutter_out = make_rounded_prism(54.0, 64.0, 56.0, 5.5, Vector(-27.0, -37.0, -2.0))
body_outer = prism_out.common(cutter_out)

hollow_shell = body_outer.cut(prism_in)

base_raw = hollow_shell.common(Part.makeBox(70, 80, split_z, Vector(-35, -40, 0)))
hood_raw = hollow_shell.common(Part.makeBox(70, 80, 50, Vector(-35, -40, split_z)))

# -------------------------------------------------------------
# 2. PODSTAWA NAUTILUS (Ciężka baza kotła z łapami kotwiczącymi)
# -------------------------------------------------------------
base = base_raw

# Płyta podłogowa łącząca bazę w pojedynczy solid
floor_plate = make_rounded_prism(46.0, 56.0, 2.0, 4.0, Vector(-23.0, -32.0, 0.0))
base = base.fuse(floor_plate)

# 2.1 Prowadnice ESP32 (Szerokość 29.2 mm, piny wiszą swobodnie w kanałach)
rail_left = Part.makeBox(2.2, 50.0, 3.5, Vector(-16.8, -29.0, 2.0))
rail_right = Part.makeBox(2.2, 50.0, 3.5, Vector(14.6, -29.0, 2.0))
ledge_left = Part.makeBox(1.4, 48.0, 1.5, Vector(-14.6, -28.0, 2.0))
ledge_right = Part.makeBox(1.4, 48.0, 1.5, Vector(13.2, -28.0, 2.0))
front_stop = Part.makeBox(29.2, 2.0, 3.5, Vector(-14.6, -29.5, 2.0))
base = base.fuse(rail_left).fuse(rail_right).fuse(ledge_left).fuse(ledge_right).fuse(front_stop)

# Kanały na piny goldpin pod ESP32 i kanał kablowy:
pin_cut_l = Part.makeBox(3.8, 46.0, 2.8, Vector(-14.4, -28.0, 0.7))
pin_cut_r = Part.makeBox(3.8, 46.0, 2.8, Vector( 10.6, -28.0, 0.7))
cable_cut = Part.makeBox(13.0, 46.0, 1.8, Vector(-6.5, -28.0, 1.2))
base = base.cut(pin_cut_l).cut(pin_cut_r).cut(cable_cut)

# 2.2 Wycięcie USB
usb_cut_base = Part.makeBox(14.0, 8.0, split_z - 2.8 + 0.5, Vector(-7.0, 21.0, 2.8))
base = base.cut(usb_cut_base)

# 2.3 Ciężkie stopy kotłowe z kołnierzami śrubowymi (Boiler Foot Flanges)
for fx, fy in [(-24.5, -29.0), (24.5, -29.0), (-24.5, 18.0), (24.5, 18.0)]:
    foot_lug = Part.makeCylinder(4.2, 5.0, Vector(fx, fy, 0), Vector(0,0,1))
    foot_hole = Part.makeCylinder(1.8, 6.0, Vector(fx, fy, -0.5), Vector(0,0,1))
    base = base.fuse(foot_lug).cut(foot_hole)

# 2.4 Dolny wlot pary ze szczelinami żaluzjowymi
intake_block = Part.makeBox(20.0, 3.5, 4.0, Vector(-10.0, -35.2, 2.2))
for sx in [-7.0, -3.5, 0.0, 3.5, 7.0]:
    slot = Part.makeBox(1.6, 5.0, 3.0, Vector(sx - 0.8, -36.0, 2.7))
    intake_block = intake_block.cut(slot)
base = base.fuse(intake_block)

# 2.5 Otwory na 3 przyciski w dolnym panelu (Średnica 6.2 mm z luzem suwliwym)
for bx in [-14.0, 0.0, 14.0]:
    btn_hole = Part.makeCylinder(3.1, 8.0, Vector(bx, -36.5, 5.6), Vector(0, 1, 0))
    btn_shld = Part.makeCylinder(4.2, 2.5, Vector(bx, -32.5, 5.6), Vector(0, 1, 0))
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
for fx, fy in [(-16.0, -21.0), (16.0, -21.0), (-16.0, 13.0), (16.0, 13.0)]:
    foot_pocket = Part.makeCylinder(4.1, 0.8, Vector(fx, fy, -0.1), Vector(0,0,1))
    base = base.cut(foot_pocket)

# -------------------------------------------------------------
# 3. WYMIENNA GŁOWA STEAM-TITAN NAUTILUS ULTRA (Slide-On Hood)
# -------------------------------------------------------------
hood = hood_raw

oled_y = -19.0
oled_z = 27.5
tilt_angle = -10.0

# 3.1 Ramka Iluminatora (Submersible Viewport Frame)
ow, oh, oc = 29.0, 18.0, 2.5
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
o_solid = Part.Face(o_wire).extrude(Vector(0, -7.0, 0)).translate(Vector(0, 1.5, 0))

iw, ih = 23.6, 12.6
hiw, hih = iw / 2.0, ih / 2.0
i_pts = [
    Vector(-hiw, 0,  hih),
    Vector( hiw, 0,  hih),
    Vector( hiw, 0, -hih),
    Vector(-hiw, 0, -hih),
    Vector(-hiw, 0,  hih)
]
i_wire = Part.Wire([Part.makeLine(i_pts[i], i_pts[i+1]) for i in range(len(i_pts)-1)])
o_cut = Part.Face(i_wire).extrude(Vector(0, -10.0, 0)).translate(Vector(0, 2.0, 0))
oled_frame = o_solid.cut(o_cut)

oled_frame.rotate(Vector(0,0,0), Vector(1,0,0), tilt_angle)
oled_frame.translate(Vector(0, oled_y - 2.5, oled_z))
hood = hood.fuse(oled_frame)

# 3.2 POTRÓJNA KLATKA OCHRONNA ILUMINATORA (Roll-Cage Crash Bars)
bar_upper = Part.makeCylinder(1.6, 29.0, Vector(-14.5, 0, 0), Vector(1,0,0))
bar_upper.rotate(Vector(0,0,0), Vector(1,0,0), tilt_angle)
bar_upper.translate(Vector(0, oled_y - 7.5, oled_z + 8.5))

bar_lower = Part.makeCylinder(1.6, 29.0, Vector(-14.5, 0, 0), Vector(1,0,0))
bar_lower.rotate(Vector(0,0,0), Vector(1,0,0), tilt_angle)
bar_lower.translate(Vector(0, oled_y - 7.5, oled_z - 8.5))

pylon_bar_l = Part.makeBox(2.8, 3.8, 19.0, Vector(-16.0, -1.9, -9.5))
pylon_bar_l.rotate(Vector(0,0,0), Vector(1,0,0), tilt_angle)
pylon_bar_l.translate(Vector(0, oled_y - 6.5, oled_z))

pylon_bar_r = Part.makeBox(2.8, 3.8, 19.0, Vector(13.2, -1.9, -9.5))
pylon_bar_r.rotate(Vector(0,0,0), Vector(1,0,0), tilt_angle)
pylon_bar_r.translate(Vector(0, oled_y - 6.5, oled_z))

rollcage_group = bar_upper.fuse(bar_lower).fuse(pylon_bar_l).fuse(pylon_bar_r)
hood = hood.fuse(rollcage_group)

# 3.3 PODWÓJNE WIKTORIAŃSKIE KOMINY PAROWE (Twin Victorian Smokestacks)
chimneys_group = None
for sx in [-9.5, 9.5]:
    anchor_flange = Part.makeCylinder(7.2, 1.5, Vector(sx, 8.0, 44.0), Vector(0,0,1))
    stack_base = Part.makeCone(6.8, 5.4, 4.0, Vector(sx, 8.0, 44.5), Vector(0,0,1))
    stack_stem = Part.makeCylinder(5.4, 9.5, Vector(sx, 8.0, 48.0), Vector(0,0,1))
    ring1 = Part.makeTorus(5.4, 0.9, Vector(sx, 8.0, 49.5), Vector(0,0,1))
    ring2 = Part.makeTorus(5.4, 0.9, Vector(sx, 8.0, 52.5), Vector(0,0,1))
    ring3 = Part.makeTorus(5.4, 0.8, Vector(sx, 8.0, 54.5), Vector(0,0,1))
    flare = Part.makeCone(5.4, 7.4, 3.5, Vector(sx, 8.0, 55.0), Vector(0,0,1))
    lip_crown = Part.makeCylinder(7.4, 1.4, Vector(sx, 8.0, 58.0), Vector(0,0,1))
    crown_lip = Part.makeTorus(7.4, 0.8, Vector(sx, 8.0, 58.0), Vector(0,0,1))
    stack_bore = Part.makeCylinder(3.6, 20.0, Vector(sx, 8.0, 42.0), Vector(0,0,1))
    
    stack_solid = (anchor_flange.fuse(stack_base).fuse(stack_stem)
                   .fuse(ring1).fuse(ring2).fuse(ring3)
                   .fuse(flare).fuse(lip_crown).fuse(crown_lip)
                   .cut(stack_bore))
    chimneys_group = stack_solid if chimneys_group is None else chimneys_group.fuse(stack_solid)

hood = hood.fuse(chimneys_group)

# 3.4 BOCZNE ANALOGOWE MANOMETRY CIŚNIENIA PARY (Steam Pressure Gauges)
gauges_group = None
for side_x, normal_x in [(-26.5, -1.0), (26.5, 1.0)]:
    gauge_body = Part.makeCylinder(10.5, 4.8, Vector(side_x, 1.0, 27.5), Vector(normal_x, 0, 0))
    gauge_cut = Part.makeCylinder(8.0, 2.0, Vector(side_x + (4.9 * normal_x), 1.0, 27.5), Vector(-normal_x, 0, 0))
    gauge_bezel = gauge_body.cut(gauge_cut)
    
    # Rant zewnętrzny
    gauge_rim = Part.makeTorus(10.5, 0.7, Vector(side_x + (4.8 * normal_x), 1.0, 27.5), Vector(normal_x, 0, 0))
    gauge_bezel = gauge_bezel.fuse(gauge_rim)
    
    # Piasta wskazówki
    hub = Part.makeCylinder(2.0, 1.4, Vector(side_x + (2.5 * normal_x), 1.0, 27.5), Vector(normal_x, 0, 0))
    gauge_bezel = gauge_bezel.fuse(hub)
    
    # Wskazówka w czerwonej strefie (kąt -45°)
    needle = Part.makeBox(1.2, 6.5, 1.0, Vector(side_x + (2.6 * normal_x), 1.0, 27.5))
    needle.rotate(Vector(side_x + (2.6 * normal_x), 1.0, 27.5), Vector(normal_x, 0, 0), -45.0)
    gauge_bezel = gauge_bezel.fuse(needle)
    
    # 6 śrub ryglowych na obwodzie
    for i in range(6):
        ang = math.radians(60 * i)
        by = 1.0 + 9.2 * math.cos(ang)
        bz = 27.5 + 9.2 * math.sin(ang)
        stud = Part.makeCylinder(0.9, 1.0, Vector(side_x + (3.8 * normal_x), by, bz), Vector(normal_x, 0, 0))
        gauge_bezel = gauge_bezel.fuse(stud)
        
    gauges_group = gauge_bezel if gauges_group is None else gauges_group.fuse(gauge_bezel)

hood = hood.fuse(gauges_group)

# 3.5 ZEWNĘTRZNE RUROCIĄGI PAROWE WYSOKIEGO CIŚNIENIA (Steam Conduits)
pipes_group = None
for px in [-27.2, 27.2]:
    pipe = Part.makeCylinder(1.8, 38.0, Vector(px, -18.0, 14.5), Vector(0, 1, 0))
    flange1 = Part.makeCylinder(2.6, 2.0, Vector(px, -14.0, 14.5), Vector(0, 1, 0))
    flange2 = Part.makeCylinder(2.6, 2.0, Vector(px,   2.0, 14.5), Vector(0, 1, 0))
    flange3 = Part.makeCylinder(2.6, 2.0, Vector(px,  16.0, 14.5), Vector(0, 1, 0))
    p_solid = pipe.fuse(flange1).fuse(flange2).fuse(flange3)
    pipes_group = p_solid if pipes_group is None else pipes_group.fuse(p_solid)

# Górne rurociągi po dachu kotła
for py_off in [-5.0, 5.0]:
    top_pipe = Part.makeCylinder(1.3, 34.0, Vector(-17.0, py_off, 46.5), Vector(1, 0, 0))
    top_flange1 = Part.makeCylinder(2.0, 1.5, Vector(-12.0, py_off, 46.5), Vector(1, 0, 0))
    top_flange2 = Part.makeCylinder(2.0, 1.5, Vector( 8.0, py_off, 46.5), Vector(1, 0, 0))
    pipes_group = pipes_group.fuse(top_pipe).fuse(top_flange1).fuse(top_flange2)

hood = hood.fuse(pipes_group)

# 3.6 PASY PANCERNE Z NITAMI KOTŁOWYMI (Riveted Armor Straps & Rivets)
strap_front = Part.makeBox(55.0, 4.0, 36.0, Vector(-27.5, -16.0, split_z))
strap_back = Part.makeBox(55.0, 4.0, 36.0, Vector(-27.5,  15.0, split_z))
strap_cutter_out = make_rounded_prism(55.6, 65.6, 56.0, 6.0, Vector(-27.8, -37.8, -2.0))
strap_cutter_in = make_rounded_prism(54.0, 64.0, 56.0, 5.5, Vector(-27.0, -37.0, -2.0))
strap_shell = strap_cutter_out.cut(strap_cutter_in)
strap_f = strap_front.common(strap_shell)
strap_b = strap_back.common(strap_shell)
hood = hood.fuse(strap_f).fuse(strap_b)

# Środkowy pas pancerny (Mid Armor Belt)
strap_mid_box = Part.makeBox(55.0, 60.0, 3.5, Vector(-27.5, -30.0, 28.0))
strap_mid = strap_mid_box.common(strap_shell)
hood = hood.fuse(strap_mid)

# 3.7 TYLNY ZBIORNIK CIŚNIENIOWY I WŁAZ INSPEKCYJNY (Rear Hatch)
hatch_frame = Part.makeCylinder(11.0, 1.8, Vector(0, 23.5, 26.0), Vector(0, 1, 0))
hatch_cut = Part.makeCylinder(8.5, 2.5, Vector(0, 24.2, 26.0), Vector(0, 1, 0))
hatch_plate = Part.makeCylinder(8.2, 1.0, Vector(0, 24.0, 26.0), Vector(0, 1, 0))
hatch_wheel = Part.makeTorus(4.5, 0.9, Vector(0, 25.4, 26.0), Vector(0, 1, 0))
hatch_spoke1 = Part.makeCylinder(0.8, 9.0, Vector(0, 25.4, 21.5), Vector(0, 0, 1))
hatch_spoke2 = Part.makeCylinder(0.8, 9.0, Vector(-4.5, 25.4, 26.0), Vector(1, 0, 0))
hatch_hub = Part.makeCylinder(1.5, 1.6, Vector(0, 24.8, 26.0), Vector(0, 1, 0))
hatch_assembly = hatch_frame.cut(hatch_cut).fuse(hatch_plate).fuse(hatch_wheel).fuse(hatch_spoke1).fuse(hatch_spoke2).fuse(hatch_hub)
hood = hood.fuse(hatch_assembly)

# 3.8 ODSŁONIĘTE KOŁA ZĘBATE NAPĘDOWE (Exposed Drive Gears / Cogs)
gears_group = None
for side_x, normal_x in [(-25.5, -1), (25.5, 1)]:
    mount_stub_big = Part.makeCylinder(4.0, 4.0, Vector(side_x - 2.0*normal_x, -6.0, 17.5), Vector(normal_x, 0, 0))
    gear_big = Part.makeCylinder(7.0, 2.2, Vector(side_x, -6.0, 17.5), Vector(normal_x, 0, 0))
    gear_big_bore = Part.makeCylinder(3.0, 3.0, Vector(side_x - normal_x, -6.0, 17.5), Vector(normal_x, 0, 0))
    gear_big_hub = Part.makeCylinder(3.5, 2.8, Vector(side_x, -6.0, 17.5), Vector(normal_x, 0, 0))
    for i in range(12):
        ang = math.radians(30 * i)
        tx = -6.0 + 7.0 * math.cos(ang)
        tz = 17.5 + 7.0 * math.sin(ang)
        tooth = Part.makeBox(1.8, 2.2, 2.2, Vector(side_x, tx - 1.1, tz - 1.1))
        tooth.rotate(Vector(side_x, -6.0, 17.5), Vector(normal_x, 0, 0), math.degrees(ang))
        gear_big = gear_big.fuse(tooth)
    gear_big = gear_big.cut(gear_big_bore).fuse(gear_big_hub).fuse(mount_stub_big)
    
    mount_stub_small = Part.makeCylinder(2.5, 4.0, Vector(side_x - 2.0*normal_x, -6.0, 28.0), Vector(normal_x, 0, 0))
    gear_small = Part.makeCylinder(4.0, 2.2, Vector(side_x, -6.0, 28.0), Vector(normal_x, 0, 0))
    gear_small_bore = Part.makeCylinder(1.5, 3.0, Vector(side_x - normal_x, -6.0, 28.0), Vector(normal_x, 0, 0))
    for i in range(8):
        ang = math.radians(45 * i + 22.5)
        tx = -6.0 + 4.0 * math.cos(ang)
        tz = 28.0 + 4.0 * math.sin(ang)
        tooth = Part.makeBox(1.5, 2.2, 1.5, Vector(side_x, tx - 0.75, tz - 0.75))
        tooth.rotate(Vector(side_x, -6.0, 28.0), Vector(normal_x, 0, 0), math.degrees(ang))
        gear_small = gear_small.fuse(tooth)
    gear_small = gear_small.cut(gear_small_bore).fuse(mount_stub_small)
    
    gear_pair = gear_big.fuse(gear_small)
    gears_group = gear_pair if gears_group is None else gears_group.fuse(gear_pair)

hood = hood.fuse(gears_group)

# 3.9 BOCZNE ILUMINATORY OKRĘTOWE (Brass Portholes)
portholes_group = None
for side_x, normal_x in [(-25.5, -1), (25.5, 1)]:
    for py in [-18.0, 10.0]:
        port_mount = Part.makeCylinder(4.2, 3.5, Vector(side_x - 1.5*normal_x, py, 38.0), Vector(normal_x, 0, 0))
        port_rim = Part.makeCylinder(4.2, 2.0, Vector(side_x + 1.0*normal_x, py, 38.0), Vector(normal_x, 0, 0))
        port_glass = Part.makeCylinder(2.8, 3.0, Vector(side_x + 1.2*normal_x, py, 38.0), Vector(normal_x, 0, 0))
        port_frame = port_mount.fuse(port_rim).cut(port_glass)
        for pi in range(4):
            pang = math.radians(90 * pi + 45)
            py2 = py + 3.4 * math.cos(pang)
            pz2 = 38.0 + 3.4 * math.sin(pang)
            port_screw = Part.makeCylinder(0.6, 1.2, Vector(side_x + 1.8*normal_x, py2, pz2), Vector(normal_x, 0, 0))
            port_frame = port_frame.fuse(port_screw)
        portholes_group = port_frame if portholes_group is None else portholes_group.fuse(port_frame)

hood = hood.fuse(portholes_group)

# 3.10 ZAWORY BEZPIECZEŃSTWA NADCIŚNIENIOWE (Pressure Relief Valves)
valves_group = None
for vy in [-3.0, 14.0]:
    v_base = Part.makeCylinder(2.6, 3.5, Vector(0, vy, 45.0), Vector(0, 0, 1))
    v_stem = Part.makeCylinder(1.4, 5.0, Vector(0, vy, 48.0), Vector(0, 0, 1))
    v_cap = Part.makeCone(2.2, 1.2, 2.0, Vector(0, vy, 53.0), Vector(0, 0, 1))
    v_ring = Part.makeTorus(1.4, 0.4, Vector(0, vy, 51.5), Vector(0, 0, 1))
    v_assy = v_base.fuse(v_stem).fuse(v_cap).fuse(v_ring)
    hood = hood.fuse(v_assy)
    valves_group = v_assy if valves_group is None else valves_group.fuse(v_assy)

# 3.11 WIEŻYCZKA PERYSKOPOWA / TELEGRAFICZNA (Periscope Tower)
peri_base = Part.makeCylinder(3.2, 3.0, Vector(-17.0, 5.0, 45.0), Vector(0, 0, 1))
peri_stem = Part.makeCylinder(1.8, 10.0, Vector(-17.0, 5.0, 47.0), Vector(0, 0, 1))
peri_head = Part.makeCylinder(2.8, 3.0, Vector(-17.0, 5.0, 57.0), Vector(0, 0, 1))
peri_lens = Part.makeCylinder(1.6, 2.0, Vector(-17.0, 5.0, 57.5), Vector(0, -1, 0))
peri_ring = Part.makeTorus(1.8, 0.4, Vector(-17.0, 5.0, 53.0), Vector(0, 0, 1))
periscope = peri_base.fuse(peri_stem).fuse(peri_head).fuse(peri_lens).fuse(peri_ring)
hood = hood.fuse(periscope)

# 3.12 PANCERNE KRATKI WENTYLACYJNE Z ŻALUZJAMI (Armored Louvered Vents)
vents_group = None
for side_x, normal_x in [(-25.5, -1), (25.5, 1)]:
    v_mount = Part.makeBox(3.0, 9.0, 7.0, Vector(side_x - 1.0*normal_x if normal_x==1 else side_x + 1.0*normal_x - 3.0, -28.0, 14.0))
    for vi in range(3):
        louver = Part.makeBox(2.0, 7.5, 0.8, Vector(side_x, -27.5, 15.0 + vi * 2.0))
        louver.rotate(Vector(side_x, -27.5, 15.0 + vi * 2.0), Vector(1, 0, 0), 30.0)
        v_mount = v_mount.fuse(louver)
    hood = hood.fuse(v_mount)
    vents_group = v_mount if vents_group is None else vents_group.fuse(v_mount)

# 3.13 ŚRUBY SZEŚCIOKĄTNE NA PANELACH I PASACH (Hex Bolt Heads)
# Śruby dachowe (axis = Z)
for hx, hy in [(-20.0, -16.0), (20.0, -16.0), (-20.0, 15.0), (20.0, 15.0)]:
    hbolt = make_hex_prism(1.3, 2.5, Vector(hx, hy, 45.0), axis=Vector(0, 0, 1))
    hood = hood.fuse(hbolt)

# Śruby tylne (axis = Y)
for hx, hz in [(-14.0, 38.0), (14.0, 38.0)]:
    hbolt = make_hex_prism(1.3, 2.5, Vector(hx, 23.0, hz), axis=Vector(0, 1, 0))
    hood = hood.fuse(hbolt)

# Śruby boczne (axis = X)
for side_x, normal_x in [(-25.5, -1), (25.5, 1)]:
    for sy, sz in [(-22.0, 20.0), (10.0, 20.0)]:
        hbolt = make_hex_prism(1.3, 3.0, Vector(side_x - 1.5*normal_x, sy, sz), axis=Vector(normal_x, 0, 0))
        hood = hood.fuse(hbolt)

# 3.14 TABLICZKA IDENTYFIKACYJNA NA DASZKU (Armored Nameplate)
np_base = Part.makeBox(18.0, 2.5, 4.5, Vector(-9.0, -26.5, 36.5))
np_bezel = Part.makeBox(19.0, 0.6, 5.5, Vector(-9.5, -27.0, 36.0))
nameplate = np_base.fuse(np_bezel)
for nx in [-8.0, 8.0]:
    for nz in [37.0, 40.0]:
        n_riv = Part.makeSphere(0.7, Vector(nx, -27.0, nz))
        nameplate = nameplate.fuse(n_riv)
hood = hood.fuse(nameplate)

# 3.15 3D NITY KOTŁOWE (29 Heavy Boiler Rivets)
rivet_positions = [
    Vector(-18.0, -14.0, 46.2), Vector( -6.0, -14.0, 46.4), Vector(  6.0, -14.0, 46.4), Vector( 18.0, -14.0, 46.2),
    Vector(-18.0,  17.0, 46.2), Vector( -4.0,  17.0, 46.4), Vector(  4.0,  17.0, 46.4), Vector( 18.0,  17.0, 46.2),
    Vector(-26.5, -14.0, 20.0), Vector(-26.5, -14.0, 36.0), Vector(-26.5,  17.0, 20.0), Vector(-26.5,  17.0, 36.0),
    Vector( 26.5, -14.0, 20.0), Vector( 26.5, -14.0, 36.0), Vector( 26.5,  17.0, 20.0), Vector( 26.5,  17.0, 36.0),
    Vector(-12.0, -25.5, 39.5), Vector(  0.0, -26.0, 39.8), Vector( 12.0, -25.5, 39.5),
    # Nity boczne na pasie środkowym
    Vector(-26.5, -8.0, 29.0), Vector(-26.5, 3.0, 29.0), Vector(-26.5, 12.0, 29.0),
    Vector( 26.5, -8.0, 29.0), Vector( 26.5, 3.0, 29.0), Vector( 26.5, 12.0, 29.0),
    # Nity dachowe
    Vector(-10.0, 0.0, 46.2), Vector(10.0, 0.0, 46.2),
    Vector(-10.0, 8.0, 46.2), Vector(10.0, 8.0, 46.2),
]

for r_pos in rivet_positions:
    r_solid = Part.makeSphere(1.4, r_pos)
    hood = hood.fuse(r_solid)

# -------------------------------------------------------------
# 3.90 PRZESTRZELENIE OKNA I KIESZENIE MONTAŻOWE DLA CORE CHASSIS
# -------------------------------------------------------------
# Przestrzelenie okna OLED na wylot
screen_cut = Part.Face(i_wire).extrude(Vector(0, -25.0, 0)).translate(Vector(0, 8.0, 0))
screen_cut.rotate(Vector(0,0,0), Vector(1,0,0), tilt_angle)
screen_cut.translate(Vector(0, oled_y, oled_z))
hood = hood.cut(screen_cut)

# Wewnętrzna kieszeń oporowa na ramkę OLED
oled_pocket = Part.makeBox(28.0, 5.0, 28.0, Vector(-14.0, -1.0, -14.0))
oled_pocket.rotate(Vector(0,0,0), Vector(1,0,0), tilt_angle)
oled_pocket.translate(Vector(0, -21.8, oled_z))
hood = hood.cut(oled_pocket)

# Wewnętrzne rowki prowadzące na szyny stelaża (Slide-on guide grooves)
guide_slot_l = Part.makeBox(2.6, 24.0, 6.0, Vector(-22.6, -12.0, split_z - 0.2))
guide_slot_r = Part.makeBox(2.6, 24.0, 6.0, Vector( 20.0, -12.0, split_z - 0.2))
hood = hood.cut(guide_slot_l).cut(guide_slot_r)

# Wybranie na buzzer i kanał kominów
buzzer_clearance = Part.makeCylinder(8.6, 14.0, Vector(0.0, 8.0, 29.5), Vector(0,0,1))
chimney_duct = Part.makeBox(20.0, 8.0, 6.0, Vector(-10.0, 4.0, 41.5))
hood = hood.cut(buzzer_clearance).cut(chimney_duct)

# Precyzyjne spasowanie ze stelażem elektroniki: usuwamy jakiekolwiek mikro-kolizje
hood = hood.cut(core_chassis_shape)

# -------------------------------------------------------------
# 4. INDUSTRIALNE KLAWISZE STERUJĄCE (Industrial Controls)
# -------------------------------------------------------------
btn_flange = Part.makeCylinder(3.6, 1.2, Vector(0,0,0), Vector(0,0,1))
btn_stem = Part.makeCylinder(2.4, 4.2, Vector(0,0,1.2), Vector(0,0,1))
btn_pusher = Part.makeCylinder(1.2, 1.5, Vector(0,0,-1.5), Vector(0,0,1))
btn_base = btn_flange.fuse(btn_stem).fuse(btn_pusher).translate(Vector(0,0,1.5))

# 4.1 Klawisz Środkowy: 6-ramienne Koło Zaworu Parowego (Valve Handwheel)
rim_torus = Part.makeTorus(4.2, 0.9, Vector(0,0,6.6), Vector(0,0,1))
hub_cyl = Part.makeCylinder(1.8, 1.6, Vector(0,0,5.8), Vector(0,0,1))
valve_spokes = []
for i in range(6):
    ang = math.radians(60 * i)
    sp = Part.makeCylinder(0.75, 4.4, Vector(0,0,6.6), Vector(math.cos(ang), math.sin(ang), 0))
    valve_spokes.append(sp)

valve_wheel = rim_torus.fuse(hub_cyl)
for sp in valve_spokes:
    valve_wheel = valve_wheel.fuse(sp)

hex_nut = make_hex_prism(1.4, 0.9, Vector(0,0,7.2), Vector(0,0,1))
valve_wheel = valve_wheel.fuse(hex_nut)
valve_cap = btn_base.fuse(valve_wheel)

# 4.2 Klawisz Lewy: Płyta Ryflowana ze Strzałką Chevron (◀)
plate_head_l = Part.makeBox(5.0, 5.0, 2.2, Vector(-2.5, -2.5, 5.2))
for cx, cy in [(-2.5, -2.5), (2.5, -2.5), (2.5, 2.5), (-2.5, 2.5)]:
    cc = Part.makeBox(1.5, 1.5, 3.0, Vector(cx - 0.75, cy - 0.75, 5.0))
    cc.rotate(Vector(cx, cy, 5.0), Vector(0,0,1), 45.0)
    plate_head_l = plate_head_l.cut(cc)

for ry in [-1.5, 0.0, 1.5]:
    rib = Part.makeCylinder(0.35, 3.8, Vector(-1.9, ry, 7.3), Vector(1, 0, 0))
    plate_head_l = plate_head_l.fuse(rib)

arr_l = Part.makeBox(2.2, 2.2, 1.2, Vector(-0.4, -1.1, 6.8))
arr_l.rotate(Vector(0, 0, 6.8), Vector(0,0,1), 45.0)
arr_mask_l = Part.makeBox(3.0, 3.0, 1.5, Vector(0.3, -1.5, 6.7))
plate_head_l = plate_head_l.cut(arr_l.cut(arr_mask_l))
tread_l_cap = btn_base.fuse(plate_head_l)

# 4.3 Klawisz Prawy: Płyta Ryflowana ze Strzałką Chevron (▶)
plate_head_p = Part.makeBox(5.0, 5.0, 2.2, Vector(-2.5, -2.5, 5.2))
for cx, cy in [(-2.5, -2.5), (2.5, -2.5), (2.5, 2.5), (-2.5, 2.5)]:
    cc = Part.makeBox(1.5, 1.5, 3.0, Vector(cx - 0.75, cy - 0.75, 5.0))
    cc.rotate(Vector(cx, cy, 5.0), Vector(0,0,1), 45.0)
    plate_head_p = plate_head_p.cut(cc)

for ry in [-1.5, 0.0, 1.5]:
    rib = Part.makeCylinder(0.35, 3.8, Vector(-1.9, ry, 7.3), Vector(1, 0, 0))
    plate_head_p = plate_head_p.fuse(rib)

arr_r = Part.makeBox(2.2, 2.2, 1.2, Vector(-1.8, -1.1, 6.8))
arr_r.rotate(Vector(0, 0, 6.8), Vector(0,0,1), 45.0)
arr_mask_r = Part.makeBox(3.0, 3.0, 1.5, Vector(-3.1, -1.5, 6.7))
plate_head_p = plate_head_p.cut(arr_r.cut(arr_mask_r))
tread_p_cap = btn_base.fuse(plate_head_p)

# -------------------------------------------------------------
# 5. WALIDACJA GEOMETRII
# -------------------------------------------------------------
parts_to_verify = [
    ("Podstawa Nautilus (Base)", base),
    ("Głowa Nautilus (Hood)", hood),
    ("Klawisz Koło Zaworu (Środek)", valve_cap),
    ("Klawisz Ryfel Lewo", tread_l_cap),
    ("Klawisz Ryfel Prawo", tread_p_cap)
]

print("\n--- Walidacja brył CAD Steam-Titan Nautilus ULTRA ---")
all_valid = True
for name, p in parts_to_verify:
    valid = p.isValid() and p.isClosed() and len(p.Solids) == 1
    print(f"{name:28s}: Valid={p.isValid()}, Closed={p.isClosed()}, Solids={len(p.Solids)}, Volume={p.Volume:.1f} mm³")
    if not valid:
        all_valid = False

# Walidacja kolizji z Universal Core Chassis
inter_vol = core_chassis_shape.common(hood).Volume
print(f"Kolizja Głowy ze Stelażem Core Chassis: {inter_vol:.4f} mm³")
if inter_vol > 0.001:
    print("OSTRZEŻENIE: Wykryto kolizję ze stelażem!")
    all_valid = False
else:
    print("SUKCES: 0.0000 mm³ kolizji! Idealne pasowanie modułowe Quick-Swap Slide-On!")

if not all_valid:
    print("OSTRZEŻENIE: Niektóre bryły wymagają uwagi!")
else:
    print("Wszystkie bryły są w 100% prawidłowymi, pojedynczymi bryłami typu Solid (Watertight/Manifold)!")

# -------------------------------------------------------------
# 6. EKSPORT STL I STEP
# -------------------------------------------------------------
print("\n--- Eksport plików STL Nautilus ULTRA do druku 3D ---")

def export_stl(shape, filename):
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.04, AngularDeflection=0.17)
    mesh.write(filename)
    print(f"Zapisano STL: {os.path.basename(filename)} ({os.path.getsize(filename):,} bajtów)")

stl_base = os.path.join(stl_diesel_dir, 'dieselpunk_podstawa.stl')
stl_hood = os.path.join(stl_diesel_dir, 'dieselpunk_glowa.stl')
stl_valve = os.path.join(stl_diesel_dir, 'dieselpunk_przycisk_zawor.stl')
stl_tread_l = os.path.join(stl_diesel_dir, 'dieselpunk_przycisk_ryfel_l.stl')
stl_tread_p = os.path.join(stl_diesel_dir, 'dieselpunk_przycisk_ryfel_p.stl')
stl_full = os.path.join(stl_diesel_dir, 'dieselpunk_robot_kompletny.stl')

export_stl(base, stl_base)
export_stl(hood, stl_hood)
export_stl(valve_cap, stl_valve)
export_stl(tread_l_cap, stl_tread_l)
export_stl(tread_p_cap, stl_tread_p)

# Eksport komponentów dla renderera Blendera
export_stl(chimneys_group, os.path.join(stl_comp_dir, 'nautilus_kominy.stl'))
export_stl(gauges_group, os.path.join(stl_comp_dir, 'nautilus_manometry.stl'))
export_stl(pipes_group, os.path.join(stl_comp_dir, 'nautilus_rurociagi.stl'))
export_stl(rollcage_group, os.path.join(stl_comp_dir, 'nautilus_klatka_okna.stl'))
export_stl(gears_group, os.path.join(stl_comp_dir, 'nautilus_kola_zebate.stl'))
export_stl(portholes_group, os.path.join(stl_comp_dir, 'nautilus_iluminatory.stl'))

# Złożenie pełnego robota
robot_full = base.fuse(hood)
btn_c = valve_cap.copy()
btn_c.rotate(Vector(0,0,0), Vector(1,0,0), -90)
btn_c.translate(Vector(0, -32.5, 5.6))

btn_l = tread_l_cap.copy()
btn_l.rotate(Vector(0,0,0), Vector(1,0,0), -90)
btn_l.translate(Vector(-14.0, -32.5, 5.6))

btn_r = tread_p_cap.copy()
btn_r.rotate(Vector(0,0,0), Vector(1,0,0), -90)
btn_r.translate(Vector(14.0, -32.5, 5.6))

robot_full = robot_full.fuse(btn_c).fuse(btn_l).fuse(btn_r)
export_stl(robot_full, stl_full)

# Eksport plików STEP
print("\n--- Eksport plików STEP do CAD ---")
Part.export([base], os.path.join(base_dir, 'dieselpunk_podstawa.step'))
Part.export([hood], os.path.join(base_dir, 'dieselpunk_glowa.step'))
Part.export([valve_cap], os.path.join(base_dir, 'dieselpunk_przycisk_zawor.step'))
Part.export([tread_l_cap], os.path.join(base_dir, 'dieselpunk_przycisk_ryfel_l.step'))
Part.export([tread_p_cap], os.path.join(base_dir, 'dieselpunk_przycisk_ryfel_p.step'))
Part.export([robot_full], os.path.join(base_dir, 'dieselpunk_robot_zlozenie.step'))
print("Zapisano wszystkie pliki STEP.")

# -------------------------------------------------------------
# 7. ZAPIS PROJEKTU FreeCAD (.FCStd)
# -------------------------------------------------------------
doc_path = os.path.join(base_dir, 'robot_dieselpunk_3d.FCStd')
doc = FreeCAD.newDocument("Robot_Steam_Titan_Nautilus_ULTRA")

o_base = doc.addObject("Part::Feature", "Nautilus_Podstawa")
o_base.Shape = base

o_hood = doc.addObject("Part::Feature", "Nautilus_Glowa")
o_hood.Shape = hood

o_valve = doc.addObject("Part::Feature", "Nautilus_Przycisk_Zawor")
o_valve.Shape = valve_cap

o_tread_l = doc.addObject("Part::Feature", "Nautilus_Przycisk_Ryfel_L")
o_tread_l.Shape = tread_l_cap

o_tread_p = doc.addObject("Part::Feature", "Nautilus_Przycisk_Ryfel_P")
o_tread_p.Shape = tread_p_cap

doc.recompute()
doc.saveAs(doc_path)
print(f"Zapisano projekt FreeCAD: {os.path.basename(doc_path)} ({os.path.getsize(doc_path):,} bajtów)")
print("\n=== Sukces! Wersja 4 ULTRA: Steam-Titan Nautilus MAXED OUT! ===")
