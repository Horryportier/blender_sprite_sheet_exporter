import os
import bpy
import math

from .classes import SpriteSheetExporterType

from PIL import Image


def export(operator: SpriteSheetExporterType, context):
    output_path = context.scene.render.filepath
    if output_path == "/tmp/":
        return {'CANCELLED'}
    camera_pivot = bpy.data.objects.get(operator.camera_pivot_name)
    match operator.export_angels:
        case "one":
            render_to_sprite(operator.filepath, operator, context)
        case "four":
            if camera_pivot == None:
                return {'CANCELLED'}
            directions = [("S", 0), ("W", 90), ("N", 180), ("E", 270)]
            render_directionals_to_sprite(directions, camera_pivot, operator, context)
        case "eight":
            if camera_pivot == None:
                return {'CANCELLED'}
            directions = [("S", 0), ("SW", 45),  ("W", 90), ("NW", 135), ("N", 180), ("NE", 225), ("E", 270), ("SE", 315)]
            render_directionals_to_sprite(directions, camera_pivot, operator, context)
    return {'FINISHED'}

def render_directionals_to_sprite(directions: list[(str, int)], camera_pivot, operator: SpriteSheetExporterType, context):
        dir_file_names = []
        for direction in directions:
            camera_pivot.rotation_euler[2] =  math.radians(direction[1])
            dir_file_name = get_direction_file_name(operator.filepath, direction[0])
            dir_file_names.append(dir_file_name)
            render_to_sprite(dir_file_name, operator, context)
        camera_pivot.rotation_euler[2] = 0
        if operator.safe_type != "direction":
            packed = combine_vertical(dir_file_names, operator.padding_v)
            packed.save(operator.filepath)
        if operator.safe_type == "packed":
            for path in dir_file_names:
                os.remove(path)

def render_to_sprite(path: str, operator: SpriteSheetExporterType, context):
    output_path = context.scene.render.filepath
    if operator.clear_output_folder:
        for file in get_all_files_of_type(output_path, ".png"):
            os.remove(file)
    if operator.run_render:
        bpy.ops.render.render(animation=True)
    images = []
    for img_file in get_all_files_of_type(output_path, ".png"):
        images.append(Image.open(img_file))
    resolution = (context.scene.render.resolution_x,
                  context.scene.render.resolution_y)
    final_image = Image.new('RGBA', resolution)
    for img in images:
        final_image = get_concat_h(final_image, img, operator.padding_h)
    w, h = final_image.size
    final_image = final_image.crop((resolution[0], 0, w, h))
    final_image.save(path)

def combine_vertical(paths: list[str], padding: int) -> Image:
    images = []
    for path in paths:
        images.append(Image.open(path))
    if len(images) == 0:
        return None
    resolution = images[0].size
    dst = Image.new('RGBA', resolution)
    for image in images:
        dst = get_concat_v(dst, image, padding)
    w, h  = dst.size
    dst = dst.crop((0, resolution[1], w, h))
    return dst

def get_all_files_of_type(path, t):
    array = []
    for root, _dirs, files in os.walk(path):
        for file in files:
            if file.endswith(t):
                full_path = os.path.join(root, file)
                if os.path.exists(full_path):
                    array.append(full_path)
    array.sort()
    return array

def get_direction_file_name(path: str, direction: str) -> str:
    return path.replace(".png", "_" + direction + ".png")

def get_concat_h(im1, im2, padding = 0):
    dst = Image.new('RGBA', (im1.width + im2.width + padding, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width + padding, 0))
    return dst


def get_concat_v(im1, im2, padding = 0):
    dst = Image.new('RGBA', (im1.width, im1.height + im2.height + padding))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height + padding))
    return dst
