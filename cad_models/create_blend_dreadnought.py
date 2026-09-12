import bpy
import os
import math

print("=== Konfiguracja sceny Blender dla ESP32 Robot: Cyber-Titan Apex (Mecha-Warrior) ===")

# 1. Reset sceny
bpy.ops.wm.read_factory_settings(use_empty=True)

scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 0.001
scene.unit_settings.length_unit = 'MILLIMETERS'

base_dir = '/home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/'
stl_el_dir = os.path.join(base_dir, 'blender_models')
stl_dread_dir = os.path.join(base_dir, 'stl_print', 'dreadnought')

def make_pbr_material(name, base_color, roughness=0.35, metallic=0.0, emission_color=None, emission_strength=1.0, alpha=1.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = base_color
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
        if 'Alpha' in bsdf.inputs and alpha < 1.0:
            bsdf.inputs['Alpha'].default_value = alpha
            mat.blend_method = 'BLEND'
        if emission_color and 'Emission Color' in bsdf.inputs:
            bsdf.inputs['Emission Color'].default_value = emission_color
            if 'Emission Strength' in bsdf.inputs:
                bsdf.inputs['Emission Strength'].default_value = emission_strength
    return mat

# --- Materiały Cyber-Titan Apex ---
mat_armor_dread = make_pbr_material("Mat_Dread_Gunmetal", (0.13, 0.14, 0.16, 1.0), roughness=0.28, metallic=0.30)
mat_btn_diamond = make_pbr_material("Mat_Klawisz_Diament", (0.98, 0.52, 0.06, 1.0), roughness=0.20, metallic=0.15)
mat_btn_arrow = make_pbr_material("Mat_Klawisz_Tytan", (0.28, 0.29, 0.32, 1.0), roughness=0.22, metallic=0.45)
mat_thruster_glow = make_pbr_material("Mat_Dopalacz_Ogien", (0.0, 0.0, 0.0, 1.0), emission_color=(1.0, 0.35, 0.02, 1.0), emission_strength=14.0)

# --- Materiały Elektroniki ---
mat_oled_pcb = make_pbr_material("Mat_OLED_PCB", (0.04, 0.06, 0.16, 1.0), roughness=0.4)
mat_screen_glass = make_pbr_material("Mat_OLED_Szklo", (0.012, 0.012, 0.015, 1.0), roughness=0.04)
# Płonące, bojowe oczy OLED (Hazard Flame Amber)
mat_oled_eyes_flame = make_pbr_material("Mat_OLED_Oczy_Flame", (0.0, 0.0, 0.0, 1.0), emission_color=(1.0, 0.38, 0.02, 1.0), emission_strength=14.0)

mat_esp = make_pbr_material("Mat_ESP32_PCB", (0.04, 0.14, 0.06, 1.0), roughness=0.45)
mat_mpu = make_pbr_material("Mat_MPU6050_PCB", (0.05, 0.12, 0.35, 1.0), roughness=0.45)
mat_buzzer = make_pbr_material("Mat_Buzzer", (0.12, 0.12, 0.14, 1.0), roughness=0.5)
mat_switches = make_pbr_material("Mat_Switche", (0.45, 0.45, 0.48, 1.0), metallic=0.7, roughness=0.3)

# Kolekcje sceny
col_dread = bpy.data.collections.new("Obudowa_Cyber_Titan_Apex")
col_el = bpy.data.collections.new("Elektronika")

scene.collection.children.link(col_dread)
scene.collection.children.link(col_el)

# 2. Import Elektroniki
el_parts = [
    ('OLED_Twarz.stl', 'OLED_Wyswietlacz', mat_oled_pcb),
    ('ESP32_Podstawa.stl', 'ESP32_DevKit', mat_esp),
    ('MPU6050_Ruch.stl', 'MPU6050_Zyroskop', mat_mpu),
    ('Buzzer.stl', 'Buzzer_Piezo', mat_buzzer),
    ('Przycisk_Lewo.stl', 'Switch_Lewo', mat_switches),
    ('Przycisk_OK.stl', 'Switch_OK', mat_switches),
    ('Przycisk_Prawo.stl', 'Switch_Prawo', mat_switches)
]

for filename, obj_name, material in el_parts:
    fpath = os.path.join(stl_el_dir, filename)
    if os.path.exists(fpath):
        bpy.ops.wm.stl_import(filepath=fpath)
        obj = bpy.context.selected_objects[0]
        obj.name = obj_name
        obj.data.materials.append(material)
        for c in obj.users_collection:
            c.objects.unlink(obj)
        col_el.objects.link(obj)

# Ekran OLED (Czarne szkło + płomienne oczy bojowe)
tilt_blender = math.radians(80.54)
mesh_glass = bpy.data.meshes.new("OLED_Szklo")
obj_glass = bpy.data.objects.new("OLED_Szklo", mesh_glass)
col_el.objects.link(obj_glass)
gw, gh = 23.0 / 2.0, 12.5 / 2.0
verts_g = [(-gw, -gh, 0.0), (gw, -gh, 0.0), (gw, gh, 0.0), (-gw, gh, 0.0)]
faces_g = [(0, 1, 2, 3)]
mesh_glass.from_pydata(verts_g, [], faces_g)
mesh_glass.update()
obj_glass.rotation_euler = (tilt_blender, 0, 0)
obj_glass.location = (0, -22.6, 27.5)
obj_glass.data.materials.append(mat_screen_glass)

for eye_name, eye_x in [("Oko_Lewe", -5.5), ("Oko_Prawe", 5.5)]:
    mesh_eye = bpy.data.meshes.new(eye_name)
    obj_eye = bpy.data.objects.new(eye_name, mesh_eye)
    col_el.objects.link(obj_eye)
    ew, eh = 2.6, 3.6
    verts_e = [(-ew, -eh, 0.08), (ew, -eh, 0.08), (ew, eh, 0.08), (-ew, eh, 0.08)]
    faces_e = [(0, 1, 2, 3)]
    mesh_eye.from_pydata(verts_e, [], faces_e)
    mesh_eye.update()
    obj_eye.rotation_euler = (tilt_blender, 0, 0)
    obj_eye.location = (eye_x, -22.6, 27.5)
    obj_eye.data.materials.append(mat_oled_eyes_flame)

# Płomienie z dysz silników odrzutowych (efekt świetlny dopalacza w dyszach)
for burner_name, bx in [("Dopalacz_L", -12.0), ("Dopalacz_P", 12.0)]:
    mesh_b = bpy.data.meshes.new(burner_name)
    obj_b = bpy.data.objects.new(burner_name, mesh_b)
    col_dread.objects.link(obj_b)
    br = 4.2
    b_verts = [(-br, 0, -br), (br, 0, -br), (br, 0, br), (-br, 0, br)]
    mesh_b.from_pydata(b_verts, [], [(0, 1, 2, 3)])
    mesh_b.update()
    obj_b.location = (bx, 28.5, 31.0)
    obj_b.data.materials.append(mat_thruster_glow)

# 3. Import Części Obudowy Apex
# 3.1 Podstawa z gąsienicami i wlotem turbiny
fpath_base = os.path.join(stl_dread_dir, 'dreadnought_podstawa.stl')
if os.path.exists(fpath_base):
    bpy.ops.wm.stl_import(filepath=fpath_base)
    obj_base = bpy.context.selected_objects[0]
    obj_base.name = "Apex_Podstawa_Gąsienice"
    obj_base.data.materials.append(mat_armor_dread)
    for c in obj_base.users_collection:
        c.objects.unlink(obj_base)
    col_dread.objects.link(obj_base)

# 3.2 Głowa z naramiennikami, rogami V-Fin, kłami i dyszami
fpath_hood = os.path.join(stl_dread_dir, 'dreadnought_glowa.stl')
if os.path.exists(fpath_hood):
    bpy.ops.wm.stl_import(filepath=fpath_hood)
    obj_hood = bpy.context.selected_objects[0]
    obj_hood.name = "Apex_Głowa_Naramienniki_Rogi"
    obj_hood.data.materials.append(mat_armor_dread)
    for c in obj_hood.users_collection:
        c.objects.unlink(obj_hood)
    col_dread.objects.link(obj_hood)

# 3.3 Klawisze Bojowe (Diament + Strzałki Chevron)
fpath_diamond = os.path.join(stl_dread_dir, 'dreadnought_przycisk_romb.stl')
fpath_arr_l = os.path.join(stl_dread_dir, 'dreadnought_przycisk_strzalka_l.stl')
fpath_arr_r = os.path.join(stl_dread_dir, 'dreadnought_przycisk_strzalka_p.stl')

if os.path.exists(fpath_diamond):
    bpy.ops.wm.stl_import(filepath=fpath_diamond)
    obj_d = bpy.context.selected_objects[0]
    obj_d.name = "Apex_Klawisz_Reaktor_Diament"
    obj_d.rotation_euler = (math.pi / 2.0, 0, 0)
    obj_d.location = (0.0, -28.7, 5.6)
    obj_d.data.materials.append(mat_btn_diamond)
    for c in obj_d.users_collection:
        c.objects.unlink(obj_d)
    col_dread.objects.link(obj_d)

if os.path.exists(fpath_arr_l):
    bpy.ops.wm.stl_import(filepath=fpath_arr_l)
    obj_l = bpy.context.selected_objects[0]
    obj_l.name = "Apex_Klawisz_Strzalka_Lewo"
    obj_l.rotation_euler = (math.pi / 2.0, 0, 0)
    obj_l.location = (-14.0, -28.7, 5.6)
    obj_l.data.materials.append(mat_btn_arrow)
    for c in obj_l.users_collection:
        c.objects.unlink(obj_l)
    col_dread.objects.link(obj_l)

if os.path.exists(fpath_arr_r):
    bpy.ops.wm.stl_import(filepath=fpath_arr_r)
    obj_r = bpy.context.selected_objects[0]
    obj_r.name = "Apex_Klawisz_Strzalka_Prawo"
    obj_r.rotation_euler = (math.pi / 2.0, 0, 0)
    obj_r.location = (14.0, -28.7, 5.6)
    obj_r.data.materials.append(mat_btn_arrow)
    for c in obj_r.users_collection:
        c.objects.unlink(obj_r)
    col_dread.objects.link(obj_r)

# 4. Konfiguracja Świata i Oświetlenia studyjnego
if not scene.world:
    scene.world = bpy.data.worlds.new('World')
world = scene.world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
if bg:
    bg.inputs['Color'].default_value = (0.04, 0.04, 0.06, 1.0)
    bg.inputs['Strength'].default_value = 1.0

# Główne światło słoneczne (Key Light)
sun_key_data = bpy.data.lights.new(name='Sun_Key', type='SUN')
sun_key_data.energy = 4.8
sun_key_data.color = (1.0, 0.97, 0.93)
sun_key_data.angle = math.radians(6.0)
sun_key_obj = bpy.data.objects.new(name='Sun_Key', object_data=sun_key_data)
scene.collection.objects.link(sun_key_obj)
sun_key_obj.rotation_euler = (math.radians(52.0), math.radians(15.0), math.radians(-38.0))

# Wypełniające światło błękitne (Fill Light z kontrą mecha)
sun_fill_data = bpy.data.lights.new(name='Sun_Fill', type='SUN')
sun_fill_data.energy = 2.4
sun_fill_data.color = (0.70, 0.85, 1.0)
sun_fill_obj = bpy.data.objects.new(name='Sun_Fill', object_data=sun_fill_data)
scene.collection.objects.link(sun_fill_obj)
sun_fill_obj.rotation_euler = (math.radians(55.0), math.radians(-25.0), math.radians(45.0))

# Konturowe światło górne (Rim Light na rogi V-Fin i krawędzie naramienników)
sun_rim_data = bpy.data.lights.new(name='Sun_Rim', type='SUN')
sun_rim_data.energy = 3.6
sun_rim_data.color = (1.0, 0.85, 0.65)
sun_rim_obj = bpy.data.objects.new(name='Sun_Rim', object_data=sun_rim_data)
scene.collection.objects.link(sun_rim_obj)
sun_rim_obj.rotation_euler = (math.radians(65.0), math.radians(10.0), math.radians(165.0))

# Cel kamery
target_empty = bpy.data.objects.new("Cel_Kamery", None)
scene.collection.objects.link(target_empty)
target_empty.location = (0, -2.0, 32.0)

# Kamera główna (odsunięta, by zmieścić szerokie 72mm bary i 68mm rogi)
cam_data = bpy.data.cameras.new(name="Camera_Glowna")
cam_data.lens = 52.0
cam_obj = bpy.data.objects.new(name="Camera_Glowna", object_data=cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (145, -190, 96)
track_con = cam_obj.constraints.new(type='TRACK_TO')
track_con.target = target_empty
track_con.track_axis = 'TRACK_NEGATIVE_Z'
track_con.up_axis = 'UP_Y'

scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.film_transparent = False

# -------------------------------------------------------------
# RENDEROWANIE PODGLĄDÓW APEX
# -------------------------------------------------------------

# Render 1: Widok Główny Front-Perspektywa (Wielkie Naramienniki, Rogi V-Fin, Kły, Oczy Ognia)
scene.render.filepath = os.path.join(base_dir, 'podglad_dreadnought_front.png')
bpy.ops.render.render(write_still=True)
print(f"Wyrenderowano podgląd Apex Front: {scene.render.filepath}")

# Render 2: Widok Profil Bok (Skrzydła Rogów, Żebra Radiatorów, Kły i Gąsienice)
cam_obj.location = (-240, -35, 50)
target_empty.location = (0, -4.0, 34.0)
bpy.context.view_layer.update()
scene.render.filepath = os.path.join(base_dir, 'podglad_dreadnought_profil.png')
bpy.ops.render.render(write_still=True)
print(f"Wyrenderowano podgląd Apex Profil: {scene.render.filepath}")

# Render 3: Widok Tył (Podwójne Dysze Odrzutowe z dopalaczem, USB, Rogi i Naramienniki)
cam_obj.location = (-135, 155, 100)
target_empty.location = (0, 0.0, 32.0)
bpy.context.view_layer.update()
scene.render.filepath = os.path.join(base_dir, 'podglad_dreadnought_tyl.png')
bpy.ops.render.render(write_still=True)
print(f"Wyrenderowano podgląd Apex Tył: {scene.render.filepath}")

# Przywrócenie kamery frontowej
cam_obj.location = (145, -190, 96)
target_empty.location = (0, -2.0, 32.0)

# Zapis pliku projektu Blender
out_dread_blend = os.path.join(base_dir, 'robot_dreadnought.blend')
bpy.ops.wm.save_as_mainfile(filepath=out_dread_blend)
print(f"Pomyślnie zapisano dedykowany projekt Blendera: {out_dread_blend}")

print("=== Sukces konfiguracji i renderowania Cyber-Titan Apex! ===")
