from bpy_extras.io_utils import ExportHelper
from .exporter import export
import bpy
from .classes import SpriteSheetExporterType


class SpriteSheetExporter(bpy.types.Operator, ExportHelper):
    bl_idname = "object.sprite_sheet_exporter"
    bl_label = "Export"

    filename_ext = ".png"
    export_angels: bpy.props.EnumProperty(
        name="Render Angels",
        description="Choose direction One/Four/Eight",
        items=(
            ("one", "One", "exports default direction"),
            ("four", "Four", "exports 4 directions S/W/N/E"),
            ("eight", "Eight", "exports 8 direction SW/W/NW/N/NE/E/SE"),
        ))
    safe_type: bpy.props.EnumProperty(
        name="Safe Type",
        description="Choose wich files to safe",
        items=(
            ("packed", "Packed", "Save only final packed sprite"),
            ("direction", "Direction", "Save only as direction only"),
            ("all", "All", "Save as packed and direction"),
        ))
    camera_pivot_name: bpy.props.StringProperty(
        name="Camera Pivot",
        default="Empty",
        description="camera pivot which is rotated")
    padding_v: bpy.props.IntProperty(
        name="Padding Vertical",
        default=0,
        description="amount of verctial padding in spritesheeet")
    padding_h: bpy.props.IntProperty(
        name="Padding Horizontal",
        default=0,
        description="amount of horizontal padding in spritesheeet")
    run_render: bpy.props.BoolProperty(
        name="Run Render",
        default=True,
        description="will render animation before exporting sprite sheet")
    clear_output_folder: bpy.props.BoolProperty(
        name="Clear Output, Property",
        default=True,
        description=
        "will delete contents of 'output path' before exporting run only with 'run render'"
    )

    def execute(self, context):
        sprite_sheet_exporter_type = SpriteSheetExporterType()
        sprite_sheet_exporter_type.filepath = self.filepath
        sprite_sheet_exporter_type.run_render = self.run_render
        sprite_sheet_exporter_type.clear_output_folder = self.clear_output_folder
        sprite_sheet_exporter_type.export_angels = self.export_angels
        sprite_sheet_exporter_type.camera_pivot_name = self.camera_pivot_name
        sprite_sheet_exporter_type.safe_type  = self.safe_type
        sprite_sheet_exporter_type.padding_v = self.padding_v
        sprite_sheet_exporter_type.padding_h = self.padding_h
        return export(sprite_sheet_exporter_type, context)
