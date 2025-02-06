import bpy

from .operators import SpriteSheetExporter


def menu_func_export(self, context):
    self.layout.operator(SpriteSheetExporter.bl_idname,
                         text="Sprite Sheet Exporter")


def _register():
    bpy.utils.register_class(SpriteSheetExporter)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def _unregister():
    bpy.utils.unregister_class(SpriteSheetExporter)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
