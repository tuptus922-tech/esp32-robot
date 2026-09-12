import sys
import os
import math

sys.path.append('/usr/lib/freecad/lib')
import FreeCAD
import Part
import Import
import MeshPart
from FreeCAD import Vector, Rotation, Placement

print("=== Generowanie nowej bryły: CYBER-CAPSULE MECHA-NEKO (ze szponterami i użebrowaniem) ===")

base_dir = '/home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/'
stl_mecha_dir = os.path.join(base_dir, 'stl_print', 'mecha_kawaii')
os.makedirs(stl_mecha_dir, exist_ok=True)

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
# 1. BAZOWY KORPUS O WALCOWATYM / PĘKATYM KSZTAŁCIE
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
prism_out = Part.Face(Part.Wire(lines_out)).extrude(Vector(62, 0, 0))
prism_out.translate(Vector(-31, 0, 0))
cutter_out = make_rounded_prism(50, 62, 52, 6.5, Vector(-25, -35, -2))
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
cutter_in = make_rounded_prism(44, 58, 52, 4.0, Vector(-22, -33, -2))
body_full_inner = prism_in.common(cutter_in)

hollow_shell = body_full_outer.cut(body_full_inner)

split_z = 10.5
box_lower_cutter = Part.makeBox(64, 72, split_z, Vector(-32, -39, 0))
base_raw = hollow_shell.common(box_lower_cutter)

box_upper_cutter = Part.makeBox(64, 72, 50, Vector(-32, -39, split_z))
hood_raw = hollow_shell.common(box_upper_cutter)

# -------------------------------------------------------------
# 2. PODSTAWA MECHA (Zintegrowane łapki ze szponterami)
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

# 2.3 Przednie łapki robota mecha (Paws z nacięciami paluszków)
paw_l = Part.makeBox(9.5, 4.5, 6.5, Vector(-21.0, -36.0, 0))
# Szpontery / nacięcia palców
t1_l = Part.makeBox(1.0, 3.5, 8.0, Vector(-18.0, -37.0, -0.5))
t2_l = Part.makeBox(1.0, 3.5, 8.0, Vector(-14.5, -37.0, -0.5))
paw_l = paw_l.cut(t1_l).cut(t2_l)

paw_r = Part.makeBox(9.5, 4.5, 6.5, Vector(11.5, -36.0, 0))
t1_r = Part.makeBox(1.0, 3.5, 8.0, Vector(14.5, -37.0, -0.5))
t2_r = Part.makeBox(1.0, 3.5, 8.0, Vector(18.0, -37.0, -0.5))
paw_r = paw_r.cut(t1_r).cut(t2_r)

base = base.fuse(paw_l).fuse(paw_r)

# 2.4 U-kształtny kołnierz centrujący
lip_l = Part.makeBox(1.2, 43.0, 1.6, Vector(-23.0, -21.0, split_z))
lip_r = Part.makeBox(1.2, 43.0, 1.6, Vector( 21.8, -21.0, split_z))
lip_back = Part.makeBox(43.6, 1.2, 1.6, Vector(-21.8, 20.8, split_z))
interlock_lip = lip_l.fuse(lip_r).fuse(lip_back).cut(Part.makeBox(14.0, 4.0, 3.0, Vector(-7.0, 20.0, split_z - 0.5)))
base = base.fuse(interlock_lip)

# 2.5 Słupki montażowe M3
screw_positions = [(-18.8, -15.0), (18.8, -15.0), (-18.8, 18.5), (18.8, 18.5)]
for sx, sy in screw_positions:
    post_solid = Part.makeCylinder(3.5, split_z - 2.0, Vector(sx, sy, 2.0), Vector(0,0,1))
    base = base.fuse(post_solid)
    screw_hole = Part.makeCylinder(1.7, split_z + 2.0, Vector(sx, sy, -0.5), Vector(0,0,1))
    screw_cbore = Part.makeCylinder(3.1, 2.0, Vector(sx, sy, -0.1), Vector(0,0,1))
    base = base.cut(screw_hole).cut(screw_cbore)

# 2.6 Nóżki antypoślizgowe
for fx, fy in [(-16.0, -21.0), (16.0, -21.0), (-16.0, 13.0), (16.0, 13.0)]:
    foot_pocket = Part.makeCylinder(4.1, 0.8, Vector(fx, fy, -0.1), Vector(0,0,1))
    base = base.cut(foot_pocket)

# 2.7 Otwory na 3 przyciski
for bx in [-14.0, 0.0, 14.0]:
    btn_cut = Part.makeCylinder(2.8, 6.0, Vector(bx, -35.0, 5.6), Vector(0, 1, 0))
    btn_shoulder = Part.makeCylinder(3.8, 2.0, Vector(bx, -31.5, 5.6), Vector(0, 1, 0))
    base = base.cut(btn_cut).cut(btn_shoulder)

# -------------------------------------------------------------
# 3. GŁOWA MECHA: WIZJER 3D, WĄSY MECHA, BOCZNE ŻEBRA, AUDIO-PODY
# -------------------------------------------------------------
hood = hood_raw

# 3.1 Przestrzenny Wizjer Mecha 3D (Oktagonalna ramka gogli mecha nachylona pod kątem czoła)
oled_z = 27.5
oled_y = -25.0 + (oled_z - 14.5) * (5.0 / 28.5) # Dokładny punkt na skośnej ścianie czołowej (-22.72 mm)
tilt_angle = -9.95 # Kąt odchylenia ściany czołowej od pionu

# Oktagonalny obrys ramki wizjera
vw, vh, vc = 29.0, 16.5, 3.0
hvw, hvh = vw / 2.0, vh / 2.0
v_pts = [
    Vector(-hvw + vc, 0,  hvh),
    Vector( hvw - vc, 0,  hvh),
    Vector( hvw,      0,  hvh - vc),
    Vector( hvw,      0, -hvh + vc),
    Vector( hvw - vc, 0, -hvh),
    Vector(-hvw + vc, 0, -hvh),
    Vector(-hvw,      0, -hvh + vc),
    Vector(-hvw,      0,  hvh - vc),
    Vector(-hvw + vc, 0,  hvh)
]
v_wire = Part.Wire([Part.makeLine(v_pts[i], v_pts[i+1]) for i in range(len(v_pts)-1)])
visor_solid = Part.Face(v_wire).extrude(Vector(0, -2.4, 0)) # Wystaje o 2.4 mm do przodu

# Okno ekranu OLED (wycięcie wewnętrzne ramki)
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
visor_hole = Part.Face(i_wire).extrude(Vector(0, -6.0, 0)).translate(Vector(0, 1.0, 0))
visor_frame = visor_solid.cut(visor_hole)

# Prawidłowe obrócenie i dopasowanie do skośnego czoła
visor_frame.rotate(Vector(0,0,0), Vector(1,0,0), tilt_angle)
visor_frame.translate(Vector(0, oled_y, oled_z))
hood = hood.fuse(visor_frame)

# Przestrzelenie okna ekranu na wylot przez ścianę i wizjer
screen_cut = Part.Face(i_wire).extrude(Vector(0, 15.0, 0)).translate(Vector(0, -5.0, 0))
screen_cut.rotate(Vector(0,0,0), Vector(1,0,0), tilt_angle)
screen_cut.translate(Vector(0, oled_y, oled_z))
hood = hood.cut(screen_cut)

# Wewnętrzna kieszeń oporowa na płytkę OLED (również nachylona równolegle do czoła)
oled_pocket = Part.makeBox(28.0, 3.8, 28.0, Vector(-14.0, -0.5, -14.0))
oled_pocket.rotate(Vector(0,0,0), Vector(1,0,0), tilt_angle)
oled_pocket.translate(Vector(0, -20.2, oled_z))
hood = hood.cut(oled_pocket)

# Wewnętrzne rowki prowadzące na szyny stelaża (Slide-on guide grooves)
guide_slot_l = Part.makeBox(2.4, 24.0, 5.0, Vector(-22.4, -12.0, split_z - 0.2))
guide_slot_r = Part.makeBox(2.4, 24.0, 5.0, Vector( 20.0, -12.0, split_z - 0.2))
hood = hood.cut(guide_slot_l).cut(guide_slot_r)

# 3.2 Kocie wąsy mecha na policzkach (2 subtelne skośne rowki po bokach wizjera)
whiskers_cut = None
for i, zw in enumerate([24.5, 29.5]):
    wl = Part.makeBox(4.8, 1.2, 1.2, Vector(-20.5, -0.6, -0.6))
    wr = Part.makeBox(4.8, 1.2, 1.2, Vector( 15.7, -0.6, -0.6))
    pair = wl.fuse(wr)
    pair.rotate(Vector(0,0,0), Vector(1,0,0), tilt_angle)
    yw = -25.0 + (zw - 14.5) * (5.0 / 28.5)
    pair.translate(Vector(0, yw, zw))
    whiskers_cut = pair if whiskers_cut is None else whiskers_cut.fuse(pair)
hood = hood.cut(whiskers_cut)

# 3.3 Boczne żebra pancerza (45° V-grooves na bokach obudowy - "szpontery")
for r_z in [16.5, 23.0, 29.5, 36.0]:
    # Lewa strona (X = -25)
    gl = Part.makeBox(2.2, 42.0, 2.2, Vector(-1.1, -21.0, -1.1))
    gl.rotate(Vector(0,0,0), Vector(0,1,0), 45.0)
    gl.translate(Vector(-25.0, 0.0, r_z))
    # Prawa strona (X = +25)
    gr = Part.makeBox(2.2, 42.0, 2.2, Vector(-1.1, -21.0, -1.1))
    gr.rotate(Vector(0,0,0), Vector(0,1,0), 45.0)
    gr.translate(Vector(25.0, 0.0, r_z))
    hood = hood.cut(gl).cut(gr)

# 3.4 Cyber-Nauszniki (Audio-Pod Ear Cups po bokach głowy)
pod_l = Part.makeCylinder(6.5, 2.8, Vector(-24.5, 3.0, 40.5), Vector(-1, 0, 0))
pod_ring_l = Part.makeCylinder(4.8, 1.0, Vector(-26.3, 3.0, 40.5), Vector(-1, 0, 0))
pod_inner_l = Part.makeCylinder(3.2, 1.2, Vector(-26.3, 3.0, 40.5), Vector(-1, 0, 0))
pod_l = pod_l.cut(pod_ring_l.cut(pod_inner_l))

pod_r = pod_l.mirror(Vector(0,0,0), Vector(1,0,0))
hood = hood.fuse(pod_l).fuse(pod_r)

# 3.5 Fasetowane uszka mecha na dachu (Faceted Mecha Ears)
p1 = Vector(-13.0, -7.0, 46.5)
p2 = Vector(-20.5, -1.0, 46.5)
p3 = Vector(-11.5,  4.0, 46.5)
w_base = Part.makePolygon([p1, p2, p3, p1])

m1 = Vector(-14.5, -4.5, 53.0)
m2 = Vector(-18.5, -1.0, 53.0)
m3 = Vector(-13.5,  2.0, 53.0)
w_mid = Part.makePolygon([m1, m2, m3, m1])

t1 = Vector(-15.8, -1.8, 58.5)
t2 = Vector(-17.0, -1.0, 58.5)
t3 = Vector(-15.5, -0.2, 58.5)
w_tip = Part.makePolygon([t1, t2, t3, t1])

ear_l = Part.makeLoft([w_base, w_mid, w_tip], True, False)

# Fasetowane wycięcie wewnętrzne uszka
ip1 = Vector(-14.0, -6.5, 48.0)
ip2 = Vector(-19.0, -2.0, 48.0)
ip3 = Vector(-16.0, -1.5, 56.5)
w_in = Part.makePolygon([ip1, ip2, ip3, ip1])
cutter_ear_in = Part.Face(w_in).extrude(Vector(0, -2.5, 0))
ear_l = ear_l.cut(cutter_ear_in)

ear_r = ear_l.mirror(Vector(0,0,0), Vector(1,0,0))
hood = hood.fuse(ear_l).fuse(ear_r)

# 3.6 Rynienka do głaskania wzdłuż grzbietu (Petting Track)
track = Part.makeBox(12.0, 36.0, 1.0, Vector(-6.0, -14.0, 46.5))
hood = hood.cut(track)

# Kieszenie na folię dotykową wewnątrz stropu
touch_front_pocket = Part.makeBox(16.0, 11.0, 1.0, Vector(-8.0, -12.5, 45.0))
touch_rear_pocket = Part.makeBox(24.0, 13.0, 1.0, Vector(-12.0, 3.0, 45.0))
hood = hood.cut(touch_front_pocket).cut(touch_rear_pocket)

# 3.7 Kocia łapka jako grill akustyczny nad buzzerem (`🐾`)
paw_center = Part.makeCylinder(2.6, 8.0, Vector(0, 10.0, 42.0), Vector(0,0,1))
toes = [
    Vector(-3.1, 13.8, 42.0),
    Vector(-1.1, 15.1, 42.0),
    Vector( 1.1, 15.1, 42.0),
    Vector( 3.1, 13.8, 42.0)
]
for t in toes:
    paw_center = paw_center.fuse(Part.makeCylinder(1.1, 8.0, t, Vector(0,0,1)))
hood = hood.cut(paw_center)

# 3.8 Rowek na kołnierz centrujący
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
    pilot_hole = Part.makeCylinder(1.4, 7.0, Vector(sx, sy, split_z - 0.2), Vector(0,0,1))
    hood = hood.cut(pilot_hole)

# -------------------------------------------------------------
# 4. KLAWISZE MECHA-KAWAII (Serce + Łapki)
# -------------------------------------------------------------
btn_flange = Part.makeCylinder(3.6, 1.2, Vector(0,0,0), Vector(0,0,1))
btn_stem = Part.makeCylinder(2.6, 4.0, Vector(0,0,1.2), Vector(0,0,1))
btn_dome = Part.makeSphere(2.6, Vector(0,0,5.2)).common(Part.makeBox(6, 6, 3, Vector(-3, -3, 5.2)))
btn_pusher = Part.makeCylinder(1.1, 1.5, Vector(0,0,-1.5), Vector(0,0,1))
base_cap = btn_flange.fuse(btn_stem).fuse(btn_dome).fuse(btn_pusher).translate(Vector(0,0,1.5))

# Klawisz Serce
c1 = Part.makeCylinder(0.65, 1.5, Vector(-0.55,  0.4, 6.8), Vector(0,0,1))
c2 = Part.makeCylinder(0.65, 1.5, Vector( 0.55,  0.4, 6.8), Vector(0,0,1))
v_tip = Part.makeBox(1.5, 1.5, 1.5, Vector(-0.75, -0.75, 6.8))
v_tip.rotate(Vector(0,0,6.8), Vector(0,0,1), 45.0)
heart_cap = base_cap.cut(c1.fuse(c2).fuse(v_tip))

# Klawisz Łapka
paw_cap = base_cap.copy()
p_main = Part.makeCylinder(0.75, 1.5, Vector(0, -0.3, 6.8), Vector(0,0,1))
toe1 = Part.makeCylinder(0.32, 1.5, Vector(-0.75, 0.65, 6.8), Vector(0,0,1))
toe2 = Part.makeCylinder(0.35, 1.5, Vector( 0.0,  0.95, 6.8), Vector(0,0,1))
toe3 = Part.makeCylinder(0.32, 1.5, Vector( 0.75, 0.65, 6.8), Vector(0,0,1))
paw_cap = paw_cap.cut(p_main).cut(toe1).cut(toe2).cut(toe3)

# -------------------------------------------------------------
# Walidacja geometrii
# -------------------------------------------------------------
parts_to_verify = [
    ("Podstawa Mecha (Base)", base),
    ("Głowa Mecha (Hood)", hood),
    ("Klawisz Serce (Heart)", heart_cap),
    ("Klawisz Łapka (Paw)", paw_cap)
]

print("\n--- Walidacja brył CAD Cyber-Capsule Mecha-Neko ---")
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
# Eksport plików STL i STEP
# -------------------------------------------------------------
print("\n--- Eksport plików STL Mecha-Kawaii do druku 3D ---")

def export_stl(shape, filename):
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.04, AngularDeflection=0.17)
    mesh.write(filename)
    print(f"Zapisano STL: {os.path.basename(filename)} ({os.path.getsize(filename):,} bajtów)")

stl_base = os.path.join(stl_mecha_dir, 'mecha_kawaii_podstawa.stl')
stl_hood = os.path.join(stl_mecha_dir, 'mecha_kawaii_glowa.stl')
stl_heart = os.path.join(stl_mecha_dir, 'mecha_kawaii_przycisk_serce.stl')
stl_paw = os.path.join(stl_mecha_dir, 'mecha_kawaii_przycisk_lapka.stl')
stl_asm = os.path.join(stl_mecha_dir, 'mecha_kawaii_robot_kompletny.stl')

export_stl(base, stl_base)
export_stl(hood, stl_hood)
export_stl(heart_cap, stl_heart)
export_stl(paw_cap, stl_paw)

mecha_assembly = base.fuse(hood)
export_stl(mecha_assembly, stl_asm)

# Eksport STEP
print("\n--- Eksport plików STEP Mecha-Kawaii ---")
Part.export([base], os.path.join(base_dir, 'mecha_kawaii_podstawa.step'))
Part.export([hood], os.path.join(base_dir, 'mecha_kawaii_glowa.step'))
Part.export([heart_cap], os.path.join(base_dir, 'mecha_kawaii_przycisk_serce.step'))
Part.export([paw_cap], os.path.join(base_dir, 'mecha_kawaii_przycisk_lapka.step'))
Part.export([base, hood], os.path.join(base_dir, 'mecha_kawaii_robot_zlozenie.step'))
print("Pomyślnie wyeksportowano pliki STEP Mecha-Kawaii.")

# Zapis FreeCAD
fc_doc_path = os.path.join(base_dir, 'robot_mecha_kawaii_3d.FCStd')
doc = FreeCAD.newDocument("RobotMechaKawaii3D")
o_base = doc.addObject("Part::Feature", "Mecha_Kawaii_Podstawa")
o_base.Shape = base
o_hood = doc.addObject("Part::Feature", "Mecha_Kawaii_Glowa")
o_hood.Shape = hood
o_heart = doc.addObject("Part::Feature", "Mecha_Kawaii_Przycisk_Serce")
o_heart.Shape = heart_cap
o_paw = doc.addObject("Part::Feature", "Mecha_Kawaii_Przycisk_Lapka")
o_paw.Shape = paw_cap
doc.recompute()
doc.saveAs(fc_doc_path)
print(f"Zapisano projekt FreeCAD: {fc_doc_path}")

print("\n=== Zakończono pomyślnie generowanie modeli Cyber-Capsule Mecha-Neko! ===")
