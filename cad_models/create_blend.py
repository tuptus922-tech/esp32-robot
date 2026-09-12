import bpy
import os
import math

print("=== Konfiguracja sceny Blender dla ESP32 Robot Desk Pet ===")

# 1. Reset sceny
bpy.ops.wm.read_factory_settings(use_empty=True)

scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 0.001
scene.unit_settings.length_unit = 'MILLIMETERS'

base_dir = '/home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/'
stl_el_dir = os.path.join(base_dir, 'blender_models')
stl_enc_dir = os.path.join(base_dir, 'stl_print')

# Helper do tworzenia materiałów PBR
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

# Tworzenie materiałów
mat_body = make_pbr_material("Mat_Obudowa_PLA", (0.88, 0.89, 0.91, 1.0), roughness=0.32) # Elegancki matowy jasny plastik PLA
mat_buttons = make_pbr_material("Mat_Klawisze_Akcent", (0.02, 0.65, 0.86, 1.0), roughness=0.22) # Turkusowy / cyan akcent
mat_bracket = make_pbr_material("Mat_Uchwyt_OLED", (0.2, 0.2, 0.22, 1.0), roughness=0.5)

mat_oled_pcb = make_pbr_material("Mat_OLED_PCB", (0.04, 0.06, 0.16, 1.0), roughness=0.4)
mat_screen_glass = make_pbr_material("Mat_OLED_Szklo", (0.012, 0.012, 0.015, 1.0), roughness=0.04)
mat_oled_eyes = make_pbr_material("Mat_OLED_Oczy_Emissive", (0.0, 0.0, 0.0, 1.0), emission_color=(0.08, 0.92, 1.0, 1.0), emission_strength=10.0)

mat_esp = make_pbr_material("Mat_ESP32_PCB", (0.04, 0.14, 0.06, 1.0), roughness=0.45)
mat_mpu = make_pbr_material("Mat_MPU6050_PCB", (0.05, 0.12, 0.35, 1.0), roughness=0.45)
mat_buzzer = make_pbr_material("Mat_Buzzer", (0.12, 0.12, 0.14, 1.0), roughness=0.5)
mat_switches = make_pbr_material("Mat_Switche", (0.45, 0.45, 0.48, 1.0), metallic=0.7, roughness=0.3)

# Kolekcje
col_enclosure = bpy.data.collections.new("Obudowa_3D")
col_electronics = bpy.data.collections.new("Elektronika")
scene.collection.children.link(col_enclosure)
scene.collection.children.link(col_electronics)

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
        for col in obj.users_collection:
            col.objects.unlink(obj)
        col_electronics.objects.link(obj)

# 3. Import Obudowy 3D
enc_parts = [
    ('obudowa_dol_podstawa.stl', 'Obudowa_Dol_Podstawa', mat_body, (0, 0, 0), (0, 0, 0)),
    ('obudowa_gora_glowa.stl', 'Obudowa_Gora_Glowa', mat_body, (0, 0, 0), (0, 0, 0)),
    ('uchwyt_oled.stl', 'Uchwyt_Docisk_OLED', mat_bracket, (0, -20.0, 15.0), (math.radians(80.0), 0, 0))
]

for filename, obj_name, material, loc, rot in enc_parts:
    fpath = os.path.join(stl_enc_dir, filename)
    if os.path.exists(fpath):
        bpy.ops.wm.stl_import(filepath=fpath)
        obj = bpy.context.selected_objects[0]
        obj.name = obj_name
        obj.location = loc
        obj.rotation_euler = rot
        obj.data.materials.append(material)
        for col in obj.users_collection:
            col.objects.unlink(obj)
        col_enclosure.objects.link(obj)

# 3.1 Import 3 klawiszy przycisków do obudowy
btn_coords = [
    ('Przycisk_Klawisz_Lewo', -14.0),
    ('Przycisk_Klawisz_OK', 0.0),
    ('Przycisk_Klawisz_Prawo', 14.0)
]
btn_stl = os.path.join(stl_enc_dir, 'przycisk_nakladka.stl')

for btn_name, bx in btn_coords:
    if os.path.exists(btn_stl):
        bpy.ops.wm.stl_import(filepath=btn_stl)
        obj = bpy.context.selected_objects[0]
        obj.name = btn_name
        obj.rotation_euler = (math.pi / 2.0, 0, 0)
        obj.location = (bx, -26.0, 5.6)
        obj.data.materials.append(mat_buttons)
        for col in obj.users_collection:
            col.objects.unlink(obj)
        col_enclosure.objects.link(obj)

# 4. Dodanie wirtualnego świecącego ekranu OLED (Cute Animated Robot Eyes)
# Czarne tło szkła OLED w płaszczyźnie ekranu (nachylenie 80°)
mesh_glass = bpy.data.meshes.new("OLED_Szklo")
obj_glass = bpy.data.objects.new("OLED_Szklo", mesh_glass)
col_electronics.objects.link(obj_glass)
gw, gh = 23.0 / 2.0, 12.5 / 2.0
# Tworzenie w płaszczyźnie XY, obrót o 80° wokół X
verts_g = [(-gw, -gh, 0.0), (gw, -gh, 0.0), (gw, gh, 0.0), (-gw, gh, 0.0)]
faces_g = [(0, 1, 2, 3)]
mesh_glass.from_pydata(verts_g, [], faces_g)
mesh_glass.update()
obj_glass.rotation_euler = (math.radians(80.0), 0, 0)
obj_glass.location = (0, -21.1, 27.5)
obj_glass.data.materials.append(mat_screen_glass)

# Świecące oczy robota OLED (dwa animowane kocie/robotyczne oczka)
for eye_name, eye_x in [("Oko_Lewe", -5.5), ("Oko_Prawe", 5.5)]:
    mesh_eye = bpy.data.meshes.new(eye_name)
    obj_eye = bpy.data.objects.new(eye_name, mesh_eye)
    col_electronics.objects.link(obj_eye)
    ew, eh = 2.6, 3.6
    # Odsunięcie o 0.08 mm wzdłuż normalnej ku przodowi (lokalne +Z)
    verts_e = [(-ew, -eh, 0.08), (ew, -eh, 0.08), (ew, eh, 0.08), (-ew, eh, 0.08)]
    faces_e = [(0, 1, 2, 3)]
    mesh_eye.from_pydata(verts_e, [], faces_e)
    mesh_eye.update()
    obj_eye.rotation_euler = (math.radians(80.0), 0, 0)
    obj_eye.location = (eye_x, -21.1, 27.5)
    obj_eye.data.materials.append(mat_oled_eyes)

# 5. Konfiguracja Świata i Oświetlenia studyjnego
if not scene.world:
    scene.world = bpy.data.worlds.new('World')
world = scene.world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
if bg:
    bg.inputs['Color'].default_value = (0.06, 0.07, 0.09, 1.0)
    bg.inputs['Strength'].default_value = 1.0

# Główne światło słoneczne (Key Light)
sun_key_data = bpy.data.lights.new(name='Sun_Key', type='SUN')
sun_key_data.energy = 4.2
sun_key_data.angle = math.radians(6.0)
sun_key_obj = bpy.data.objects.new(name='Sun_Key', object_data=sun_key_data)
scene.collection.objects.link(sun_key_obj)
sun_key_obj.rotation_euler = (math.radians(52.0), math.radians(15.0), math.radians(-38.0))

# Wypełniające światło błękitne (Fill Light)
sun_fill_data = bpy.data.lights.new(name='Sun_Fill', type='SUN')
sun_fill_data.energy = 1.8
sun_fill_data.color = (0.82, 0.90, 1.0)
sun_fill_obj = bpy.data.objects.new(name='Sun_Fill', object_data=sun_fill_data)
scene.collection.objects.link(sun_fill_obj)
sun_fill_obj.rotation_euler = (math.radians(55.0), math.radians(-25.0), math.radians(45.0))

# Konturowe światło górne (Rim Light na dach i strefę głaskania)
sun_rim_data = bpy.data.lights.new(name='Sun_Rim', type='SUN')
sun_rim_data.energy = 2.0
sun_rim_data.color = (1.0, 0.96, 0.90)
sun_rim_obj = bpy.data.objects.new(name='Sun_Rim', object_data=sun_rim_data)
scene.collection.objects.link(sun_rim_obj)
sun_rim_obj.rotation_euler = (math.radians(65.0), math.radians(10.0), math.radians(165.0))

# 6. Cel kamery (Empty w środku geometrycznym robota)
target_empty = bpy.data.objects.new("Cel_Kamery", None)
scene.collection.objects.link(target_empty)
target_empty.location = (0, -4.5, 23.5)

# Kamera główna
cam_data = bpy.data.cameras.new(name="Camera_Główna")
cam_data.lens = 52.0
cam_obj = bpy.data.objects.new(name="Camera_Główna", object_data=cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (95, -125, 75)

# Constraint Track To
track_con = cam_obj.constraints.new(type='TRACK_TO')
track_con.target = target_empty
track_con.track_axis = 'TRACK_NEGATIVE_Z'
track_con.up_axis = 'UP_Y'

# Ustawienia renderera
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.film_transparent = False

# Zapis pliku projektu Blendera
out_blend = os.path.join(base_dir, 'robot_projekt.blend')
bpy.ops.wm.save_as_mainfile(filepath=out_blend)
print(f"Pomyślnie zaktualizowano plik Blendera: {out_blend}")

# Wyrenderowanie podglądu PNG
render_out = os.path.join(base_dir, 'podglad_obudowy_3d.png')
scene.render.filepath = render_out
bpy.ops.render.render(write_still=True)
print(f"Pomyślnie wyrenderowano podgląd 3D: {render_out} ({os.path.getsize(render_out):,} bajtów)")

print("=== Sukces konfiguracji Blendera! ===")
