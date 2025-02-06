from enum import Enum

class ExportAngels(Enum):
    One = 1
    Four = 2
    Eight = 3

class SpriteSheetExporterType:
    filepath: str
    clear_output_folder: bool
    run_render: bool
    export_angels: ExportAngels
    camera_pivot_name: str
