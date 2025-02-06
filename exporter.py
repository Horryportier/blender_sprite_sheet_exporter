import os
import subprocess
import shutil
import bpy
import glob

from .classes import SpriteSheetExporterType

from PIL import Image


def export(operator: SpriteSheetExporterType, context):
    output_path = context.scene.render.filepath
    if output_path == "/tmp/":
        return {'CANCELLED'}
    if operator.clear_output_folder:
        for file in get_all_files_of_type(output_path, ".png"):
            os.remove(file)
    if operator.run_render:
        bpy.ops.render.render(animation=True)
    images = []
    for img_file in get_all_files_of_type(output_path, ".png"):
        images.append(Image.open(img_file))
    resolution =  (context.scene.render.resolution_x, context.scene.render.resolution_y)
    final_image = Image.new('RGBA', resolution)
    for img in images:
        final_image = get_concat_h(final_image, img)
    w, h = final_image.size
    final_image = final_image.crop((resolution[0], 0, w, h))
    final_image.save(operator.filepath)
    return {'FINISHED'}


def get_all_files_of_type(path, t):
    array = []
    for root, _dirs, files in os.walk(path):
        for file in files:
            if file.endswith(t):
                full_path = os.path.join(root, file)
                if os.path.exists(full_path):
                    array.append(full_path)
    return array


def get_concat_h(im1, im2):
    dst = Image.new('RGBA', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def get_concat_v(im1, im2):
    dst = Image.new('RGBA', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst
