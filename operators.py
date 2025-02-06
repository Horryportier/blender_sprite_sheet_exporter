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
            ("1", "One", "exports default direction"),
            ("2", "Four", "exports 4 directions S/W/N/E"),
            ("3", "Eight", "exports 8 direction SW/W/NW/N/NE/E/SE"),
        ))
    safe_type: bpy.props.EnumProperty(
        name="Safe Type",
        description="Choose wich files to safe",
        items=(
            ("packed", "Packed", "Save only final packed sprite"),
            ("direction", "Direction", "Save only as direction only"),
            ("all", "All", "Save as packed and direction"),
        ))
    camera_pivot_name: bpy.props.StringProperty(name="Camera Pivot", default="Empty", description="camera pivot which is rotated")
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

        self.report({'INFO'}, "export_angle: {:s} ".format(self.export_angels))
        sprite_sheet_exporter_type = SpriteSheetExporterType()
        sprite_sheet_exporter_type.filepath = self.filepath
        sprite_sheet_exporter_type.run_render = self.run_render
        sprite_sheet_exporter_type.clear_output_folder = self.clear_output_folder
        sprite_sheet_exporter_type.export_angels = self.export_angels
        sprite_sheet_exporter_type.camera_pivot_name = self.camera_pivot_name
        return export(sprite_sheet_exporter_type, context)
