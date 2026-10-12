import os
import bpy

OUTPUT_DIR = os.path.join("assets", "renders")
REFERENCE_IMAGE = os.path.join("assets", "reference", "reference.png")

# Limpa a cena atual
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.film_transparent = False
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.fps = 30

# Chão do palco
bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0), scale=(10, 7, 1))
floor_obj = bpy.context.object
floor_obj.name = "StageFloor"
mat_floor = bpy.data.materials.new(name="FloorMaterial")
mat_floor.use_nodes = True
bsdf_floor = mat_floor.node_tree.nodes.get("Principled BSDF")
bsdf_floor.inputs[0].default_value = (0.09, 0.07, 0.06, 1.0)
bsdf_floor.inputs[4].default_value = 0.25
floor_obj.data.materials.append(mat_floor)

# Fundo do palco
bpy.ops.mesh.primitive_plane_add(location=(0, 0, 4.5), scale=(12, 7, 1))
backdrop = bpy.context.object
backdrop.name = "Backdrop"
mat_backdrop = bpy.data.materials.new(name="BackdropMaterial")
mat_backdrop.use_nodes = True
bsdf_back = mat_backdrop.node_tree.nodes.get("Principled BSDF")
bsdf_back.inputs[0].default_value = (0.18, 0.10, 0.05, 1.0)
bsdf_back.inputs[4].default_value = 0.18
backdrop.data.materials.append(mat_backdrop)

# Iluminação
bpy.ops.object.light_add(type='AREA', location=(0, 4.5, 4.5))
main_light = bpy.context.object
main_light.name = "MainLight"
main_light.data.energy = 3000
main_light.data.shape = 'RECTANGLE'
main_light.data.size = 5
main_light.data.size_y = 4

bpy.ops.object.light_add(type='AREA', location=(-5, 2.5, 3.0))
left_light = bpy.context.object
left_light.name = "LeftLight"
left_light.data.energy = 1800
left_light.data.shape = 'RECTANGLE'
left_light.data.size = 4
left_light.data.size_y = 3

bpy.ops.object.light_add(type='AREA', location=(5, 2.5, 3.0))
right_light = bpy.context.object
right_light.name = "RightLight"
right_light.data.energy = 1800
right_light.data.shape = 'RECTANGLE'
right_light.data.size = 4
right_light.data.size_y = 3

# Câmera
bpy.ops.object.camera_add(location=(0, -8, 2.5), rotation=(1.15, 0, 0))
camera = bpy.context.object
camera.name = "CameraMain"
scene.camera = camera
camera.data.lens = 45

# Microfones
for x in (-2.6, 2.3):
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.08, depth=1.7, location=(x, -0.4, 2.2))
    mic = bpy.context.object
    mic.name = f"Microphone_{x}"
    mic.rotation_euler[2] = 0.3
    mat_mic = bpy.data.materials.new(name=f"MicMaterial_{x}")
    mat_mic.use_nodes = True
    bsdf_mic = mat_mic.node_tree.nodes.get("Principled BSDF")
    bsdf_mic.inputs[0].default_value = (0.08, 0.08, 0.08, 1.0)
    mic.data.materials.append(mat_mic)

    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.06, depth=0.6, location=(x, -0.2, 3.2))
    stand = bpy.context.object
    stand.name = f"MicStand_{x}"
    stand.rotation_euler[2] = 0.9
    stand.data.materials.append(mat_mic)

# Plano de referência
if os.path.exists(REFERENCE_IMAGE):
    bpy.ops.mesh.primitive_plane_add(location=(0, 0.1, 2.2), rotation=(1.55, 0, 0), scale=(5.7, 4.1, 1))
    ref_plane = bpy.context.object
    ref_plane.name = "ReferencePlane"

    mat_ref = bpy.data.materials.new(name="ReferenceMaterial")
    mat_ref.use_nodes = True
    tex = mat_ref.node_tree.nodes.new(type='ShaderNodeTexImage')
    tex.image = bpy.data.images.load(REFERENCE_IMAGE)
    bsdf_ref = mat_ref.node_tree.nodes.get("Principled BSDF")
    mat_ref.node_tree.links.new(tex.outputs['Color'], bsdf_ref.inputs['Base Color'])
    ref_plane.data.materials.append(mat_ref)

scene.eevee.use_gtao = True
scene.eevee.taa_render_samples = 64
scene.eevee.use_bloom = True

os.makedirs(OUTPUT_DIR, exist_ok=True)
scene.render.filepath = os.path.join(OUTPUT_DIR, "frame_####.png")
print("Cena configurada. Renderização em andamento via Blender.")
