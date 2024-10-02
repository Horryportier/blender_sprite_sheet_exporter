import subprocess
import bpy
import os 
import shutil

bl_info = {
    "name": "Sprite Sheet Exporter",
    "blender": (4, 2, 1),
    "category": "Tooling",
    "author": "Horry Portier",
    "version": (0, 0, 1),
    "location": "3D View > Sidebar > Sprite Sheet Exporter",
    "description": "spritesheet exporter tool uses image magic",
}


class SpriteSheetExporter(bpy.types.Operator):
    bl_idname = "object.sprite_sheet_exporter"
    bl_label = "Sprite Sheet Exporter"

    def execute(self, context):
        row = self.layout.row()
        row.operator("object.sprite_sheet_exporter_setup", text="Export Sprite")
        return {'FINISHED'}


class SpriteSheetExporterUI(bpy.types.Panel):
    bl_idname = "object.sprite_sheet_exporter_ui"
    bl_label = "Sprite Sheet Exporter"
    bl_category = "Sprite Sheet Exporter UI"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        row = self.layout.row()
        row.operator("object.sprite_sheet_exporter_setup", text="Export Sprite")


class SpriteSheetExporterSetup(bpy.types.Operator):
    bl_idname = "object.sprite_sheet_exporter_setup"
    bl_label = "Sprite Sheet Exporter"

    safe_path: bpy.props.StringProperty(name="Sprite Sheet Path:")
    r: bpy.props.IntProperty(name="Rows")
    c: bpy.props.IntProperty(name="Cols")
    t: bpy.props.BoolProperty(name="Transparency", default=True)
    custom_background: bpy.props.StringProperty(name="Cusotom Background", default="#000000")
    width: bpy.props.IntProperty(name="Sprite Width")
    height: bpy.props.IntProperty(name="Sprite Height")
    rerender: bpy.props.BoolProperty(name="Re Render", default=True)
    
    def execute(self, context):
        if  shutil.which("montage") == None:
            self.report({'ERROR'}, "montage not in PATH")
        sprite_sheet_safe_path = self.safe_path
        cols = self.c
        rows = self.r
        sprite_height = self.height
        sprite_width = self.width
        transparency = self.t
        custom_background = self.custom_background
        rerender = self.rerender
        
        final_color = "transparent" if transparency else '\'' + custom_background + '\''
    
        output_path = bpy.data.scenes["Scene"].render.filepath
        cmd = f"montage {output_path}* -tile {rows}x{cols} -geometry {sprite_width}x{sprite_height}+0+0 -background {final_color} {sprite_sheet_safe_path}"
        
        
        self.report({'INFO'}, "runnig: {:s}".format(cmd))
        if rerender:
            bpy.ops.render.render(animation=True)
        res = subprocess.run(cmd, shell = True, capture_output=True)

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


def register():
    bpy.utils.register_class(SpriteSheetExporter)
    bpy.utils.register_class(SpriteSheetExporterUI)
    bpy.utils.register_class(SpriteSheetExporterSetup)


def unregister():
    bpy.utils.unregister_class(SpriteSheetExporter)
    bpy.utils.unregister_class(SpriteSheetExporterUI)
    bpy.utils.unregister_class(SpriteSheetExporterSetup)


if __name__ == "__main__":
    register()
