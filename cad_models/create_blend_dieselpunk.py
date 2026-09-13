import bpy
import os
import math

print("=== Konfiguracja sceny Blender dla ESP32 Robot: Steam-Titan Nautilus (Dieselpunk) ===")

# 1. Reset sceny
bpy.ops.wm.read_factory_settings(use_empty=True)

scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 0.001
scene.unit_settings.length_unit = 'MILLIMETERS'

base_dir = '/home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/'
stl_el_dir = os.path.join(base_dir, 'blender_models')
stl_diesel_dir = os.path.join(base_dir, 'stl_print', 'dieselpunk')
stl_comp_dir = os.path.join(stl_diesel_dir, 'components')
stl_print_dir = os.path.join(base_dir, 'stl_print')

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

# --- Materiały Steampunk / Industrial Dieselpunk ---
mat_boiler_steel = make_pbr_material("Mat_Boiler_CastIron", (0.13, 0.14, 0.16, 1.0), roughness=0.36, metallic=0.75)
mat_brass = make_pbr_material("Mat_Steampunk_Brass", (0.86, 0.65, 0.20, 1.0), roughness=0.20, metallic=0.92)
mat_copper = make_pbr_material("Mat_Copper_Pipes", (0.82, 0.44, 0.22, 1.0), roughness=0.24, metallic=0.88)
mat_treadplate = make_pbr_material("Mat_Treadplate_Steel", (0.24, 0.25, 0.28, 1.0), roughness=0.26, metallic=0.65)
mat_gauge_dial = make_pbr_material("Mat_Gauge_Dial", (0.92, 0.88, 0.76, 1.0), roughness=0.30, emission_color=(0.95, 0.78, 0.45, 1.0), emission_strength=2.0)

# --- Materiały Elektroniki ---
mat_oled_pcb = make_pbr_material("Mat_OLED_PCB", (0.04, 0.06, 0.16, 1.0), roughness=0.4)
mat_screen_glass = make_pbr_material("Mat_OLED_Szklo", (0.012, 0.012, 0.015, 1.0), roughness=0.04)
# Płonące, miodowo-bursztynowe lampowe oczy Nixie
mat_oled_eyes_amber = make_pbr_material("Mat_OLED_Oczy_Nixie", (0.0, 0.0, 0.0, 1.0), emission_color=(1.0, 0.58, 0.08, 1.0), emission_strength=16.0)

mat_esp = make_pbr_material("Mat_ESP32_PCB", (0.04, 0.14, 0.06, 1.0), roughness=0.45)
mat_mpu = make_pbr_material("Mat_MPU6050_PCB", (0.05, 0.12, 0.35, 1.0), roughness=0.45)
mat_buzzer = make_pbr_material("Mat_Buzzer", (0.12, 0.12, 0.14, 1.0), roughness=0.5)
mat_switches = make_pbr_material("Mat_Switche", (0.45, 0.45, 0.48, 1.0), metallic=0.7, roughness=0.3)

# Kolekcje sceny
col_diesel = bpy.data.collections.new("Obudowa_Steam_Titan_Nautilus")
col_el = bpy.data.collections.new("Elektronika")

scene.collection.children.link(col_diesel)
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

# Ekran OLED (Czarne szkło + bursztynowe oczy lampowe Nixie)
tilt_blender = math.radians(80.0)
mesh_glass = bpy.data.meshes.new("OLED_Szklo")
obj_glass = bpy.data.objects.new("OLED_Szklo", mesh_glass)
col_el.objects.link(obj_glass)
gw, gh = 23.0 / 2.0, 12.5 / 2.0
verts_g = [(-gw, -gh, 0.0), (gw, -gh, 0.0), (gw, gh, 0.0), (-gw, gh, 0.0)]
faces_g = [(0, 1, 2, 3)]
mesh_glass.from_pydata(verts_g, [], faces_g)
mesh_glass.update()
obj_glass.rotation_euler = (tilt_blender, 0, 0)
obj_glass.location = (0, -21.4, 27.5)
obj_glass.data.materials.append(mat_screen_glass)

for eye_name, eye_x in [("Oko_Lewe", -5.5), ("Oko_Prawe", 5.5)]:
    mesh_eye = bpy.data.meshes.new(eye_name)
    obj_eye = bpy.data.objects.new(eye_name, mesh_eye)
    col_el.objects.link(obj_eye)
    ew, eh = 2.4, 3.4
    verts_e = [(-ew, -eh, 0.08), (ew, -eh, 0.08), (ew, eh, 0.08), (-ew, eh, 0.08)]
    faces_e = [(0, 1, 2, 3)]
    mesh_eye.from_pydata(verts_e, [], faces_e)
    mesh_eye.update()
    obj_eye.rotation_euler = (tilt_blender, 0, 0)
    obj_eye.location = (eye_x, -21.4, 27.5)
    obj_eye.data.materials.append(mat_oled_eyes_amber)

# 3. Import Części Nautilus
d_parts = [
    (os.path.join(stl_diesel_dir, 'dieselpunk_podstawa.stl'), 'Nautilus_Podstawa', mat_boiler_steel, (0, 0, 0), (0, 0, 0)),
    (os.path.join(stl_diesel_dir, 'dieselpunk_glowa.stl'), 'Nautilus_Glowa_Kadlub', mat_boiler_steel, (0, 0, 0), (0, 0, 0)),
    (os.path.join(stl_comp_dir, 'nautilus_kominy.stl'), 'Nautilus_Kominy_Mosiadz', mat_brass, (0, 0, 0), (0, 0, 0)),
    (os.path.join(stl_comp_dir, 'nautilus_manometry.stl'), 'Nautilus_Manometry_Mosiadz', mat_brass, (0, 0, 0), (0, 0, 0)),
    (os.path.join(stl_comp_dir, 'nautilus_rurociagi.stl'), 'Nautilus_Rury_Miedz', mat_copper, (0, 0, 0), (0, 0, 0)),
    (os.path.join(stl_comp_dir, 'nautilus_klatka_okna.stl'), 'Nautilus_Klatka_Iluminatora', mat_brass, (0, 0, 0), (0, 0, 0)),
    (os.path.join(stl_comp_dir, 'nautilus_kola_zebate.stl'), 'Nautilus_Kola_Zebate', mat_brass, (0, 0, 0), (0, 0, 0)),
    (os.path.join(stl_comp_dir, 'nautilus_iluminatory.stl'), 'Nautilus_Iluminatory', mat_brass, (0, 0, 0), (0, 0, 0)),
    (os.path.join(stl_diesel_dir, 'dieselpunk_przycisk_zawor.stl'), 'Klawisz_Kolo_Zaworu', mat_brass, (math.radians(-90.0), 0, 0), (0, -32.5, 5.6)),
    (os.path.join(stl_diesel_dir, 'dieselpunk_przycisk_ryfel_l.stl'), 'Klawisz_Ryfel_Lewo', mat_treadplate, (math.radians(-90.0), 0, 0), (-14.0, -32.5, 5.6)),
    (os.path.join(stl_diesel_dir, 'dieselpunk_przycisk_ryfel_p.stl'), 'Klawisz_Ryfel_Prawo', mat_treadplate, (math.radians(-90.0), 0, 0), (14.0, -32.5, 5.6))
]

for fpath, obj_name, material, rot, loc in d_parts:
    if os.path.exists(fpath):
        bpy.ops.wm.stl_import(filepath=fpath)
        obj = bpy.context.selected_objects[0]
        obj.name = obj_name
        obj.rotation_euler = rot
        obj.location = loc
        obj.data.materials.append(material)
        for c in obj.users_collection:
            c.objects.unlink(obj)
        col_diesel.objects.link(obj)

# 4. Oświetlenie studyjne - Klimat Industrial Steampunk
world = bpy.data.worlds.new('Dieselpunk_World')
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
if bg:
    bg.inputs['Color'].default_value = (0.04, 0.045, 0.06, 1.0)
    bg.inputs['Strength'].default_value = 1.0

# Ciepłe złocisto-mosiężne światło główne (Key Sun)
sun_key = bpy.data.lights.new(name='Sun_Steam_Key', type='SUN')
sun_key.energy = 5.4
sun_key.color = (1.0, 0.94, 0.82)
sun_key_obj = bpy.data.objects.new(name='Sun_Steam_Key', object_data=sun_key)
scene.collection.objects.link(sun_key_obj)
sun_key_obj.rotation_euler = (math.radians(50.0), math.radians(18.0), math.radians(-38.0))

# Chłodne światło wypełniające (Fill Sun)
sun_fill = bpy.data.lights.new(name='Sun_Steam_Fill', type='SUN')
sun_fill.energy = 2.4
sun_fill.color = (0.65, 0.80, 1.0)
sun_fill_obj = bpy.data.objects.new(name='Sun_Steam_Fill', object_data=sun_fill)
scene.collection.objects.link(sun_fill_obj)
sun_fill_obj.rotation_euler = (math.radians(60.0), math.radians(-25.0), math.radians(45.0))

# Miedziowe światło krawędziowe (Rim Sun)
sun_rim = bpy.data.lights.new(name='Sun_Steam_Rim', type='SUN')
sun_rim.energy = 4.5
sun_rim.color = (1.0, 0.65, 0.35)
sun_rim_obj = bpy.data.objects.new(name='Sun_Steam_Rim', object_data=sun_rim)
scene.collection.objects.link(sun_rim_obj)
sun_rim_obj.rotation_euler = (math.radians(65.0), math.radians(10.0), math.radians(165.0))

# Cel kamery
target_empty = bpy.data.objects.new("Cel_Kamery", None)
scene.collection.objects.link(target_empty)
target_empty.location = (0, -3.0, 26.0)

# Kamera
cam_data = bpy.data.cameras.new(name="Camera_Dieselpunk")
cam_data.lens = 52.0
cam_obj = bpy.data.objects.new(name="Camera_Dieselpunk", object_data=cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj

track_con = cam_obj.constraints.new(type='TRACK_TO')
track_con.target = target_empty
track_con.track_axis = 'TRACK_NEGATIVE_Z'
track_con.up_axis = 'UP_Y'

# Konfiguracja silnika renderującego EEVEE
scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'RenderSettings') and 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.film_transparent = False

# Zapis pliku projektu .blend
blend_path = os.path.join(base_dir, 'robot_dieselpunk.blend')
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print(f"Zapisano projekt Blender: {os.path.basename(blend_path)} ({os.path.getsize(blend_path):,} bajtów)")

# 5. Generowanie renderów podglądowych
renders = [
    ('podglad_dieselpunk_front.png', (120.0, -145.0, 85.0)),
    ('podglad_dieselpunk_profil.png', (185.0, 0.0, 50.0)),
    ('podglad_dieselpunk_gora.png', (65.0, -85.0, 165.0))
]

for img_name, cam_pos in renders:
    cam_obj.location = cam_pos
    bpy.context.view_layer.update()
    out_img = os.path.join(base_dir, img_name)
    scene.render.filepath = out_img
    bpy.ops.render.render(write_still=True)
    print(f"Wyrenderowano: {img_name} ({os.path.getsize(out_img):,} bajtów)")

# 6. Render Slide-On Modular (Uniesiona głowa w powietrzu nad stelażem elektroniki)
hood_objs = [
    bpy.data.objects.get("Nautilus_Glowa_Kadlub"),
    bpy.data.objects.get("Nautilus_Kominy_Mosiadz"),
    bpy.data.objects.get("Nautilus_Manometry_Mosiadz"),
    bpy.data.objects.get("Nautilus_Rury_Miedz"),
    bpy.data.objects.get("Nautilus_Klatka_Iluminatora"),
    bpy.data.objects.get("Nautilus_Kola_Zebate"),
    bpy.data.objects.get("Nautilus_Iluminatory")
]
for ho in hood_objs:
    if ho:
        ho.location = (0, 0, 35.0)

# Import stelaża Core pod spodem
core_stl = os.path.join(stl_print_dir, 'core_chassis.stl')
mat_core_chassis = make_pbr_material('Mat_Core_Chassis', (0.12, 0.14, 0.18, 1.0), roughness=0.45, metallic=0.1)
if os.path.exists(core_stl):
    bpy.ops.wm.stl_import(filepath=core_stl)
    obj_core = bpy.context.selected_objects[0]
    obj_core.name = "Universal_Core_Chassis"
    obj_core.data.materials.append(mat_core_chassis)
    for c in obj_core.users_collection:
        c.objects.unlink(obj_core)
    col_diesel.objects.link(obj_core)

# Wyłączamy podstawę, pokazując sam stelaż i uniesioną głowę
obj_base = bpy.data.objects.get("Nautilus_Podstawa")
if obj_base:
    obj_base.hide_render = True

cam_obj.location = (125.0, -150.0, 95.0)
target_empty.location = (0, -2.0, 35.0)
bpy.context.view_layer.update()

out_slide = os.path.join(base_dir, 'podglad_modular_dieselpunk_slide_on.png')
scene.render.filepath = out_slide
bpy.ops.render.render(write_still=True)
print(f"Wyrenderowano: podglad_modular_dieselpunk_slide_on.png ({os.path.getsize(out_slide):,} bajtów)")

# Przywrócenie pozycji i zapis finalnego pliku .blend z widokiem złożenia
for ho in hood_objs:
    if ho:
        ho.location = (0, 0, 0)
if obj_base:
    obj_base.hide_render = False
if 'obj_core' in locals():
    obj_core.hide_render = True

bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("\n=== Sukces! Wszystkie rendery i plik Blender gotowe! ===")
