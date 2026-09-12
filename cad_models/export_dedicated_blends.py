import bpy
import os
import math

base_dir = '/home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/'
stl_el_dir = os.path.join(base_dir, 'blender_models')
stl_enc_dir = os.path.join(base_dir, 'stl_print')
stl_mecha_dir = os.path.join(base_dir, 'stl_print', 'mecha_kawaii')

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

def setup_studio_lighting_and_camera(scene):
    if not scene.world:
        scene.world = bpy.data.worlds.new('World')
    world = scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes.get('Background')
    if bg:
        bg.inputs['Color'].default_value = (0.06, 0.07, 0.09, 1.0)
        bg.inputs['Strength'].default_value = 1.0

    # Key Sun
    sun_key_data = bpy.data.lights.new(name='Sun_Key', type='SUN')
    sun_key_data.energy = 4.5
    sun_key_data.angle = math.radians(6.0)
    sun_key_obj = bpy.data.objects.new(name='Sun_Key', object_data=sun_key_data)
    scene.collection.objects.link(sun_key_obj)
    sun_key_obj.rotation_euler = (math.radians(52.0), math.radians(15.0), math.radians(-38.0))

    # Fill Sun
    sun_fill_data = bpy.data.lights.new(name='Sun_Fill', type='SUN')
    sun_fill_data.energy = 2.0
    sun_fill_data.color = (0.82, 0.90, 1.0)
    sun_fill_obj = bpy.data.objects.new(name='Sun_Fill', object_data=sun_fill_data)
    scene.collection.objects.link(sun_fill_obj)
    sun_fill_obj.rotation_euler = (math.radians(55.0), math.radians(-25.0), math.radians(45.0))

    # Rim Sun
    sun_rim_data = bpy.data.lights.new(name='Sun_Rim', type='SUN')
    sun_rim_data.energy = 2.8
    sun_rim_data.color = (1.0, 0.96, 0.90)
    sun_rim_obj = bpy.data.objects.new(name='Sun_Rim', object_data=sun_rim_data)
    scene.collection.objects.link(sun_rim_obj)
    sun_rim_obj.rotation_euler = (math.radians(65.0), math.radians(10.0), math.radians(165.0))

    # Target & Camera
    target_empty = bpy.data.objects.new("Cel_Kamery", None)
    scene.collection.objects.link(target_empty)
    target_empty.location = (0, -4.5, 25.0)

    cam_data = bpy.data.cameras.new(name="Camera_Glowna")
    cam_data.lens = 52.0
    cam_obj = bpy.data.objects.new(name="Camera_Glowna", object_data=cam_data)
    scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    cam_obj.location = (95, -125, 78)

    track_con = cam_obj.constraints.new(type='TRACK_TO')
    track_con.target = target_empty
    track_con.track_axis = 'TRACK_NEGATIVE_Z'
    track_con.up_axis = 'UP_Y'

    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080

def add_electronics(target_col):
    mat_oled_pcb = make_pbr_material("Mat_OLED_PCB", (0.04, 0.06, 0.16, 1.0), roughness=0.4)
    mat_screen_glass = make_pbr_material("Mat_OLED_Szklo", (0.012, 0.012, 0.015, 1.0), roughness=0.04)
    mat_oled_eyes_cyan = make_pbr_material("Mat_OLED_Oczy_Cyan", (0.0, 0.0, 0.0, 1.0), emission_color=(0.08, 0.92, 1.0, 1.0), emission_strength=10.0)
    mat_esp = make_pbr_material("Mat_ESP32_PCB", (0.04, 0.14, 0.06, 1.0), roughness=0.45)
    mat_mpu = make_pbr_material("Mat_MPU6050_PCB", (0.05, 0.12, 0.35, 1.0), roughness=0.45)
    mat_buzzer = make_pbr_material("Mat_Buzzer", (0.12, 0.12, 0.14, 1.0), roughness=0.5)
    mat_switches = make_pbr_material("Mat_Switche", (0.45, 0.45, 0.48, 1.0), metallic=0.7, roughness=0.3)

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
            target_col.objects.link(obj)

    # Ekran OLED
    mesh_glass = bpy.data.meshes.new("OLED_Szklo")
    obj_glass = bpy.data.objects.new("OLED_Szklo", mesh_glass)
    target_col.objects.link(obj_glass)
    gw, gh = 23.0 / 2.0, 12.5 / 2.0
    verts_g = [(-gw, -gh, 0.0), (gw, -gh, 0.0), (gw, gh, 0.0), (-gw, gh, 0.0)]
    mesh_glass.from_pydata(verts_g, [], [(0, 1, 2, 3)])
    mesh_glass.update()
    obj_glass.rotation_euler = (math.radians(80.0), 0, 0)
    obj_glass.location = (0, -21.1, 27.5)
    obj_glass.data.materials.append(mat_screen_glass)

    # Animowane oczy mecha
    for eye_name, eye_x in [("Oko_Lewe", -5.5), ("Oko_Prawe", 5.5)]:
        mesh_eye = bpy.data.meshes.new(eye_name)
        obj_eye = bpy.data.objects.new(eye_name, mesh_eye)
        target_col.objects.link(obj_eye)
        ew, eh = 2.6, 3.6
        verts_e = [(-ew, -eh, 0.08), (ew, -eh, 0.08), (ew, eh, 0.08), (-ew, eh, 0.08)]
        mesh_eye.from_pydata(verts_e, [], [(0, 1, 2, 3)])
        mesh_eye.update()
        obj_eye.rotation_euler = (math.radians(80.0), 0, 0)
        obj_eye.location = (eye_x, -21.1, 27.5)
        obj_eye.data.materials.append(mat_oled_eyes_cyan)

# =============================================================
# 1. TWORZENIE PLIKU: robot_mecha_kawaii.blend
# =============================================================
print("\n--- Generowanie dedykowanego pliku Blender dla Mecha Kawaii ---")
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 0.001
scene.unit_settings.length_unit = 'MILLIMETERS'

col_mecha = bpy.data.collections.new("Obudowa_Mecha_Kawaii")
col_el = bpy.data.collections.new("Elektronika")
scene.collection.children.link(col_mecha)
scene.collection.children.link(col_el)

add_electronics(col_el)

mat_body_mecha = make_pbr_material("Mat_Mecha_Sakura", (0.95, 0.68, 0.78, 1.0), roughness=0.30)
mat_btn_heart = make_pbr_material("Mat_Klawisz_Serce", (0.96, 0.18, 0.42, 1.0), roughness=0.20)
mat_btn_paw = make_pbr_material("Mat_Klawisz_Lapka", (0.99, 0.94, 0.96, 1.0), roughness=0.20)

# Import Mecha Podstawa
fpath_mecha_base = os.path.join(stl_mecha_dir, 'mecha_kawaii_podstawa.stl')
if os.path.exists(fpath_mecha_base):
    bpy.ops.wm.stl_import(filepath=fpath_mecha_base)
    obj_base = bpy.context.selected_objects[0]
    obj_base.name = "Mecha_Podstawa"
    obj_base.data.materials.append(mat_body_mecha)
    for c in obj_base.users_collection:
        c.objects.unlink(obj_base)
    col_mecha.objects.link(obj_base)

# Import Mecha Głowa
fpath_mecha_hood = os.path.join(stl_mecha_dir, 'mecha_kawaii_glowa.stl')
if os.path.exists(fpath_mecha_hood):
    bpy.ops.wm.stl_import(filepath=fpath_mecha_hood)
    obj_hood = bpy.context.selected_objects[0]
    obj_hood.name = "Mecha_Glowa"
    obj_hood.data.materials.append(mat_body_mecha)
    for c in obj_hood.users_collection:
        c.objects.unlink(obj_hood)
    col_mecha.objects.link(obj_hood)

# Klawisz Serce
fpath_heart = os.path.join(stl_mecha_dir, 'mecha_kawaii_przycisk_serce.stl')
if os.path.exists(fpath_heart):
    bpy.ops.wm.stl_import(filepath=fpath_heart)
    obj_heart = bpy.context.selected_objects[0]
    obj_heart.name = "Mecha_Klawisz_Serce_OK"
    obj_heart.rotation_euler = (math.pi / 2.0, 0, 0)
    obj_heart.location = (0.0, -28.7, 5.6)
    obj_heart.data.materials.append(mat_btn_heart)
    for c in obj_heart.users_collection:
        c.objects.unlink(obj_heart)
    col_mecha.objects.link(obj_heart)

# Klawisze Łapki
fpath_paw = os.path.join(stl_mecha_dir, 'mecha_kawaii_przycisk_lapka.stl')
for paw_name, px in [("Mecha_Klawisz_Lapka_Lewo", -14.0), ("Mecha_Klawisz_Lapka_Prawo", 14.0)]:
    if os.path.exists(fpath_paw):
        bpy.ops.wm.stl_import(filepath=fpath_paw)
        obj_paw = bpy.context.selected_objects[0]
        obj_paw.name = paw_name
        obj_paw.rotation_euler = (math.pi / 2.0, 0, 0)
        obj_paw.location = (px, -28.7, 5.6)
        obj_paw.data.materials.append(mat_btn_paw)
        for c in obj_paw.users_collection:
            c.objects.unlink(obj_paw)
        col_mecha.objects.link(obj_paw)

setup_studio_lighting_and_camera(scene)

out_mecha_blend = os.path.join(base_dir, 'robot_mecha_kawaii.blend')
bpy.ops.wm.save_as_mainfile(filepath=out_mecha_blend)
print(f"Zapisano dedykowany plik Mecha Kawaii: {out_mecha_blend}")

# =============================================================
# 2. TWORZENIE PLIKU: robot_obudowa_klasyczna.blend
# =============================================================
print("\n--- Generowanie dedykowanego pliku Blender dla Obudowy Klasycznej ---")
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 0.001
scene.unit_settings.length_unit = 'MILLIMETERS'

col_classic = bpy.data.collections.new("Obudowa_Klasyczna")
col_el = bpy.data.collections.new("Elektronika")
scene.collection.children.link(col_classic)
scene.collection.children.link(col_el)

add_electronics(col_el)

mat_body_classic = make_pbr_material("Mat_Obudowa_Klasyczna", (0.88, 0.89, 0.91, 1.0), roughness=0.32)
mat_btn_classic = make_pbr_material("Mat_Klawisze_Klasyczne", (0.02, 0.65, 0.86, 1.0), roughness=0.22)
mat_bracket = make_pbr_material("Mat_Uchwyt_OLED", (0.2, 0.2, 0.22, 1.0), roughness=0.5)

classic_parts = [
    ('obudowa_dol_podstawa.stl', 'Klasyczna_Podstawa', mat_body_classic, (0, 0, 0), (0, 0, 0)),
    ('obudowa_gora_glowa.stl', 'Klasyczna_Glowa', mat_body_classic, (0, 0, 0), (0, 0, 0)),
    ('uchwyt_oled.stl', 'Klasyczny_Uchwyt_OLED', mat_bracket, (0, -20.0, 15.0), (math.radians(80.0), 0, 0))
]

for filename, obj_name, material, loc, rot in classic_parts:
    fpath = os.path.join(stl_enc_dir, filename)
    if os.path.exists(fpath):
        bpy.ops.wm.stl_import(filepath=fpath)
        obj = bpy.context.selected_objects[0]
        obj.name = obj_name
        obj.location = loc
        obj.rotation_euler = rot
        obj.data.materials.append(material)
        for c in obj.users_collection:
            c.objects.unlink(obj)
        col_classic.objects.link(obj)

btn_coords_classic = [('Klasyczny_Klawisz_Lewo', -14.0), ('Klasyczny_Klawisz_OK', 0.0), ('Klasyczny_Klawisz_Prawo', 14.0)]
btn_stl_classic = os.path.join(stl_enc_dir, 'przycisk_nakladka.stl')
for btn_name, bx in btn_coords_classic:
    if os.path.exists(btn_stl_classic):
        bpy.ops.wm.stl_import(filepath=btn_stl_classic)
        obj = bpy.context.selected_objects[0]
        obj.name = btn_name
        obj.rotation_euler = (math.pi / 2.0, 0, 0)
        obj.location = (bx, -26.0, 5.6)
        obj.data.materials.append(mat_btn_classic)
        for c in obj.users_collection:
            c.objects.unlink(obj)
        col_classic.objects.link(obj)

setup_studio_lighting_and_camera(scene)

out_classic_blend = os.path.join(base_dir, 'robot_obudowa_klasyczna.blend')
bpy.ops.wm.save_as_mainfile(filepath=out_classic_blend)
print(f"Zapisano dedykowany plik Klasyczny: {out_classic_blend}")

print("\n=== Zakończono generowanie osobnych plików .blend! ===")
