import sys
sys.path.append('/usr/lib/freecad/lib')
import FreeCAD
import Part
import Import
from FreeCAD import Vector

print("Generowanie modeli CAD dla ESP32 Robot Desk Pet...")

doc = FreeCAD.newDocument("RobotPodzespoly")

# 1. OLED 0.96 SSD1306
oled_pcb = Part.makeBox(27.0, 27.0, 1.6)
for x, y in [(2.5, 2.5), (24.5, 2.5), (24.5, 24.5), (2.5, 24.5)]:
    hole = Part.makeCylinder(1.1, 3.0, Vector(x, y, -0.5), Vector(0, 0, 1))
    oled_pcb = oled_pcb.cut(hole)

glass = Part.makeBox(26.7, 19.3, 1.4, Vector(0.15, 2.0, 1.6))
screen = Part.makeBox(21.7, 11.2, 0.3, Vector(2.65, 6.0, 3.0))
oled_shape = oled_pcb.fuse(glass).fuse(screen)
obj_oled = doc.addObject("Part::Feature", "OLED_0_96_SSD1306")
obj_oled.Shape = oled_shape

# 2. ESP32 DevKit V1 (30-pin, 28.5 mm wide)
esp_pcb = Part.makeBox(51.5, 28.5, 1.6, Vector(0, 0, 0))
usb = Part.makeBox(7.5, 8.0, 3.2, Vector(-1.5, (28.5 - 8.0) / 2.0, 1.6))
shield = Part.makeBox(18.0, 16.0, 3.2, Vector(28.0, (28.5 - 16.0) / 2.0, 1.6))
esp_shape = esp_pcb.fuse(usb).fuse(shield)
obj_esp = doc.addObject("Part::Feature", "ESP32_DevKit_V1")
obj_esp.Shape = esp_shape
obj_esp.Placement.Base = Vector(35, 0, 0)

# 3. MPU-6050 (GY-521)
mpu_pcb = Part.makeBox(20.5, 15.6, 1.6)
h1 = Part.makeCylinder(1.5, 3.0, Vector(18.0, 3.0, -0.5), Vector(0, 0, 1))
h2 = Part.makeCylinder(1.5, 3.0, Vector(18.0, 12.6, -0.5), Vector(0, 0, 1))
mpu_pcb = mpu_pcb.cut(h1).cut(h2)
mpu_chip = Part.makeBox(4.0, 4.0, 1.0, Vector(8.0, 5.8, 1.6))
mpu_shape = mpu_pcb.fuse(mpu_chip)
obj_mpu = doc.addObject("Part::Feature", "MPU6050_GY521")
obj_mpu.Shape = mpu_shape
obj_mpu.Placement.Base = Vector(0, 35, 0)

# 4. Buzzer 12mm
buzzer_body = Part.makeCylinder(6.0, 8.5, Vector(0, 0, 0), Vector(0, 0, 1))
sound_hole = Part.makeCylinder(1.2, 1.5, Vector(0, 0, 7.5), Vector(0, 0, 1))
buzzer_shape = buzzer_body.cut(sound_hole)
obj_buzzer = doc.addObject("Part::Feature", "Buzzer_12mm")
obj_buzzer.Shape = buzzer_shape
obj_buzzer.Placement.Base = Vector(35, 35, 0)

# 5. Tact Switch 6x6 mm (3 sztuki)
sw_base = Part.makeBox(6.0, 6.0, 3.5, Vector(-3.0, -3.0, 0))
sw_btn = Part.makeCylinder(1.7, 3.0, Vector(0, 0, 3.5), Vector(0, 0, 1))
sw_shape = sw_base.fuse(sw_btn)

obj_sw1 = doc.addObject("Part::Feature", "Przycisk_Lewo")
obj_sw1.Shape = sw_shape
obj_sw1.Placement.Base = Vector(0, -15, 0)

obj_sw2 = doc.addObject("Part::Feature", "Przycisk_OK")
obj_sw2.Shape = sw_shape
obj_sw2.Placement.Base = Vector(12, -15, 0)

obj_sw3 = doc.addObject("Part::Feature", "Przycisk_Prawo")
obj_sw3.Shape = sw_shape
obj_sw3.Placement.Base = Vector(24, -15, 0)

doc.recompute()

# Eksport pojedynczych plików STEP
base_path = '/home/tuptus/Dokumenty/PlatformIO/Projects/robot/cad_models/'
Import.export([obj_oled], base_path + 'oled_0_96_ssd1306.step')
Import.export([obj_esp], base_path + 'esp32_devkit_v1.step')
Import.export([obj_mpu], base_path + 'mpu6050_gy521.step')
Import.export([obj_buzzer], base_path + 'buzzer_12mm.step')
Import.export([obj_sw2], base_path + 'tact_switch_6x6.step')

# Zapis projektu FreeCAD
doc.saveAs(base_path + 'robot_podzespoly.FCStd')
print("Wszystkie modele wygenerowane i zapisane w:", base_path)
