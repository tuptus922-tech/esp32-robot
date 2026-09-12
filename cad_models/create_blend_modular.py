import bpy
import os
import math

print("=== Konfiguracja sceny Blender: Modułowy Stelaż Elektroniki (Universal Core) ===")

base_dir = '/home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/'
stl_el_dir = os.path.join(base_dir, 'blender_models')
stl_print_dir = os.path.join(base_dir, 'stl_print')
stl_dread_dir = os.path.join(stl_print_dir, 'dreadnought')
stl_kawaii_dir = os.path.join(stl_print_dir, 'mecha_kawaii')

# Czyszczenie istniejącej sceny
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# Helper materiałów PBR
def make_pbr(name, base_color, roughness=0.35, metallic=0.0, emission_color=None, emission_strength=1.0, alpha=1.0):
    mat = bpy.data.materials.new(name=name)
    nodes = mat.node_tree.nodes
    nodes.clear()
    node_out = nodes.new(type='ShaderNodeOutputMaterial')
    node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    mat.node_tree.links.new(node_bsdf.outputs['BSDF'], node_out.inputs['Surface'])

    node_bsdf.inputs['Base Color'].default_value = base_color
    node_bsdf.inputs['Roughness'].default_value = roughness
    node_bsdf.inputs['Metallic'].default_value = metallic

    if 'Alpha' in node_bsdf.inputs and alpha < 1.0:
        node_bsdf.inputs['Alpha'].default_value = alpha
        mat.blend_method = 'BLEND'

    if emission_color and 'Emission Color' in node_bsdf.inputs:
        node_bsdf.inputs['Emission Color'].default_value = emission_color
        if 'Emission Strength' in node_bsdf.inputs:
            node_bsdf.inputs['Emission Strength'].default_value = emission_strength

    return mat

# Definicje materiałów
mat_core_chassis = make_pbr('Mat_Core_Chassis', (0.12, 0.14, 0.18, 1.0), roughness=0.45, metallic=0.1) # Matowy polimer inżynieryjny
mat_esp = make_pbr('Mat_ESP32', (0.02, 0.12, 0.05, 1.0), roughness=0.3, metallic=0.2)
mat_mpu = make_pbr('Mat_MPU6050', (0.01, 0.25, 0.45, 1.0), roughness=0.3, metallic=0.1)
mat_oled_pcb = make_pbr('Mat_OLED_PCB', (0.03, 0.06, 0.25, 1.0), roughness=0.25, metallic=0.2)
mat_screen_glass = make_pbr('Mat_Screen_Glass', (0.01, 0.01, 0.01, 1.0), roughness=0.05, metallic=0.1)
mat_eyes = make_pbr('Mat_Eyes', (1.0, 0.65, 0.12, 1.0), roughness=0.1, emission_color=(1.0, 0.62, 0.08, 1.0), emission_strength=12.0)
mat_buzzer = make_pbr('Mat_Buzzer', (0.04, 0.04, 0.04, 1.0), roughness=0.5, metallic=0.0)
mat_switches = make_pbr('Mat_Switches', (0.80, 0.82, 0.85, 1.0), roughness=0.2, metallic=0.9)
mat_hood_ghost = make_pbr('Mat_Hood_Ghost', (0.22, 0.24, 0.28, 1.0), roughness=0.3, metallic=0.4)

# Kolekcje
col_core = bpy.data.collections.new("Stelaz_Core")
col_electronics = bpy.data.collections.new("Elektronika_W_Gniazdach")
col_swappable_hood = bpy.data.collections.new("Wymienna_Obudowa")

scene.collection.children.link(col_core)
scene.collection.children.link(col_electronics)
scene.collection.children.link(col_swappable_hood)

# 1. Import Stelaża Centralnego (Core Chassis)
core_stl = os.path.join(stl_print_dir, 'core_chassis.stl')
if os.path.exists(core_stl):
    bpy.ops.wm.stl_import(filepath=core_stl)
    obj_core = bpy.context.selected_objects[0]
    obj_core.name = "Universal_Core_Chassis"
    obj_core.data.materials.append(mat_core_chassis)
    for col in obj_core.users_collection:
        col.objects.unlink(obj_core)
    col_core.objects.link(obj_core)

# 2. Import Elektroniki osadzonej w stelażu
el_items = [
    ('OLED_Twarz.stl', 'OLED_SSD1306', mat_oled_pcb),
    ('ESP32_Podstawa.stl', 'ESP32_DevKit_V1', mat_esp),
    ('MPU6050_Ruch.stl', 'MPU6050_Sensor', mat_mpu),
    ('Buzzer.stl', 'Buzzer_Piezo_12mm', mat_buzzer),
    ('Przycisk_Lewo.stl', 'Switch_Lewo', mat_switches),
    ('Przycisk_OK.stl', 'Switch_OK', mat_switches),
    ('Przycisk_Prawo.stl', 'Switch_Prawo', mat_switches)
]

for fname, oname, omat in el_items:
    fpath = os.path.join(stl_el_dir, fname)
    if os.path.exists(fpath):
        bpy.ops.wm.stl_import(filepath=fpath)
        obj = bpy.context.selected_objects[0]
        obj.name = oname
        obj.data.materials.append(omat)
        for col in obj.users_collection:
            col.objects.unlink(obj)
        col_electronics.objects.link(obj)

# Ekran OLED szkło + oczy
mesh_glass = bpy.data.meshes.new("OLED_Glass")
obj_glass = bpy.data.objects.new("OLED_Glass", mesh_glass)
col_electronics.objects.link(obj_glass)
gw, gh = 23.0 / 2.0, 12.0 / 2.0
verts_g = [(-gw, -gh, 0.0), (gw, -gh, 0.0), (gw, gh, 0.0), (-gw, gh, 0.0)]
faces_g = [(0, 1, 2, 3)]
mesh_glass.from_pydata(verts_g, [], faces_g)
mesh_glass.update()
obj_glass.rotation_euler = (math.radians(80.0), 0, 0)
obj_glass.location = (0, -21.1, 27.5)
obj_glass.data.materials.append(mat_screen_glass)

for eye_name, eye_x in [("Oko_L", -5.5), ("Oko_P", 5.5)]:
    mesh_eye = bpy.data.meshes.new(eye_name)
    obj_eye = bpy.data.objects.new(eye_name, mesh_eye)
    col_electronics.objects.link(obj_eye)
    ew, eh = 2.4, 3.4
    verts_e = [(-ew, -eh, 0.08), (ew, -eh, 0.08), (ew, eh, 0.08), (-ew, eh, 0.08)]
    faces_e = [(0, 1, 2, 3)]
    mesh_eye.from_pydata(verts_e, [], faces_e)
    mesh_eye.update()
    obj_eye.rotation_euler = (math.radians(80.0), 0, 0)
    obj_eye.location = (eye_x, -21.1, 27.5)
    obj_eye.data.materials.append(mat_eyes)

# 3. Import wymiennej górnej obudowy Cyber-Titan Apex (uniesionej w powietrzu do demonstracji Slide-On)
hood_stl = os.path.join(stl_dread_dir, 'dreadnought_glowa.stl')
obj_hood = None
if os.path.exists(hood_stl):
    bpy.ops.wm.stl_import(filepath=hood_stl)
    obj_hood = bpy.context.selected_objects[0]
    obj_hood.name = "Wymienna_Glowa_Apex"
    obj_hood.data.materials.append(mat_hood_ghost)
    for col in obj_hood.users_collection:
        col.objects.unlink(obj_hood)
    col_swappable_hood.objects.link(obj_hood)
    # Uniesienie w górę o 35 mm (układ Quick-Swap)
    obj_hood.location = (0, 0, 35.0)

# Oświetlenie i studio
if not scene.world:
    scene.world = bpy.data.worlds.new('World')
world = scene.world
bg = world.node_tree.nodes.get('Background')
if bg:
    bg.inputs['Color'].default_value = (0.05, 0.05, 0.07, 1.0)
    bg.inputs['Strength'].default_value = 1.0

# Key Sun
sun_key = bpy.data.lights.new(name='Sun_Key', type='SUN')
sun_key.energy = 4.8
sun_key.color = (1.0, 0.98, 0.94)
sun_key_obj = bpy.data.objects.new(name='Sun_Key', object_data=sun_key)
scene.collection.objects.link(sun_key_obj)
sun_key_obj.rotation_euler = (math.radians(52.0), math.radians(15.0), math.radians(-38.0))

# Fill Sun
sun_fill = bpy.data.lights.new(name='Sun_Fill', type='SUN')
sun_fill.energy = 2.4
sun_fill.color = (0.75, 0.85, 1.0)
sun_fill_obj = bpy.data.objects.new(name='Sun_Fill', object_data=sun_fill)
scene.collection.objects.link(sun_fill_obj)
sun_fill_obj.rotation_euler = (math.radians(55.0), math.radians(-25.0), math.radians(45.0))

# Rim Sun
sun_rim = bpy.data.lights.new(name='Sun_Rim', type='SUN')
sun_rim.energy = 3.6
sun_rim.color = (1.0, 0.85, 0.65)
sun_rim_obj = bpy.data.objects.new(name='Sun_Rim', object_data=sun_rim)
scene.collection.objects.link(sun_rim_obj)
sun_rim_obj.rotation_euler = (math.radians(65.0), math.radians(10.0), math.radians(165.0))

# Cel kamery
target_empty = bpy.data.objects.new("Cel_Kamery", None)
scene.collection.objects.link(target_empty)
target_empty.location = (0, -2.0, 24.0)

cam_data = bpy.data.cameras.new(name="Camera")
cam_data.lens = 50.0
cam_obj = bpy.data.objects.new(name="Camera", object_data=cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (115, -145, 80)

track_con = cam_obj.constraints.new(type='TRACK_TO')
track_con.target = target_empty
track_con.track_axis = 'TRACK_NEGATIVE_Z'
track_con.up_axis = 'UP_Y'

scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.film_transparent = False

# -------------------------------------------------------------
# RENDER 1: Sam stelaż z osadzoną elektroniką (ukryta wymienna obudowa)
# -------------------------------------------------------------
if obj_hood:
    obj_hood.hide_render = True

target_empty.location = (0, -2.0, 20.0)
cam_obj.location = (110, -135, 75)
bpy.context.view_layer.update()

scene.render.filepath = os.path.join(base_dir, 'podglad_stelaz_elektronika.png')
bpy.ops.render.render(write_still=True)
print(f"Wyrenderowano podgląd stelaża z elektroniką: {scene.render.filepath}")

# -------------------------------------------------------------
# RENDER 2: Demonstracja Quick-Swap / Slide-On: Cyber-Titan Apex
# -------------------------------------------------------------
if obj_hood:
    obj_hood.hide_render = False

target_empty.location = (0, -2.0, 42.0)
cam_obj.location = (170, -210, 110)
bpy.context.view_layer.update()

scene.render.filepath = os.path.join(base_dir, 'podglad_modular_slide_on.png')
bpy.ops.render.render(write_still=True)
print(f"Wyrenderowano podgląd modułowego nasuwania Apex: {scene.render.filepath}")

# -------------------------------------------------------------
# RENDER 3: Demonstracja Quick-Swap / Slide-On: Mecha-Kawaii
# -------------------------------------------------------------
if obj_hood:
    obj_hood.hide_render = True

# Import głowy Mecha-Kawaii
kawaii_hood_stl = os.path.join(stl_kawaii_dir, 'mecha_kawaii_glowa.stl')
mat_kawaii = make_pbr('Mat_Kawaii_Pink', (0.92, 0.45, 0.65, 1.0), roughness=0.35, metallic=0.05)
if os.path.exists(kawaii_hood_stl):
    bpy.ops.wm.stl_import(filepath=kawaii_hood_stl)
    obj_kawaii = bpy.context.selected_objects[0]
    obj_kawaii.name = "Wymienna_Glowa_Kawaii"
    obj_kawaii.data.materials.append(mat_kawaii)
    for col in obj_kawaii.users_collection:
        col.objects.unlink(obj_kawaii)
    col_swappable_hood.objects.link(obj_kawaii)
    obj_kawaii.location = (0, 0, 35.0)

    target_empty.location = (0, -2.0, 38.0)
    cam_obj.location = (165, -200, 105)
    bpy.context.view_layer.update()

    scene.render.filepath = os.path.join(base_dir, 'podglad_modular_kawaii_slide_on.png')
    bpy.ops.render.render(write_still=True)
    print(f"Wyrenderowano podgląd modułowego nasuwania Kawaii: {scene.render.filepath}")
    obj_kawaii.hide_render = True

if obj_hood:
    obj_hood.hide_render = False

# Zapis projektu .blend
out_blend = os.path.join(base_dir, 'robot_modular_core.blend')
bpy.ops.wm.save_as_mainfile(filepath=out_blend)
print(f"Zapisano projekt Blendera: {out_blend}")
print("=== Zakończono pomyślnie konfigurację sceny modułowej! ===")
