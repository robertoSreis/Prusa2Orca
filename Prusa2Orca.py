import os
import sys
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import configparser
import datetime
import traceback
import argparse
from typing import Dict, List, Optional

def _main_log(message: str) -> None:
    print(f"[MAIN] {message}", flush=True)

def _main_fatal(message: str) -> None:
    print(f"[MAIN FATAL] {message}", file=sys.stderr, flush=True)

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Constants
APP_NAME = "SE3D - Prusa/Orca Converter"
AUTHOR = "Roberto Reis - Aracaju/SE [BR]"
ORCA_SLICER_VERSION = '1.6.0.0'

# Supported languages
LANGUAGES = {
    "en": "English",
    "pt": "Português",
    "es": "Español"
}

# Translation dictionary
TRANSLATIONS = {
    "en": {
        "Main": "Main",
        "Settings": "Settings",
        "About": "About",
        "Input PrusaSlicer File:": "Input PrusaSlicer File:",
        "Output Directory:": "Output Directory:",
        "Browse...": "Browse...",
        "Printer Settings": "Printer Settings",
        "Filaments": "Filaments",
        "Printers": "Printers",
        "Log:": "Log:",
        "Convert": "Convert",
        "Language:": "Language:",
        "On Existing Files:": "On Existing Files:",
        "Skip": "Skip",
        "Overwrite": "Overwrite",
        "Merge": "Merge",
        "Apply Settings": "Apply Settings",
        "Select input file": "Select input file",
        "Select output directory": "Select output directory",
        "PrusaSlicer files": "PrusaSlicer files",
        "All files": "All files",
        "Please select an input file": "Please select an input file",
        "Please select an output directory": "Please select an output directory",
        "Conversion completed successfully": "Conversion completed successfully",
        "Conversion failed": "Conversion failed",
        "An error occurred during conversion:": "An error occurred during conversion:",
        "Settings applied successfully": "Settings applied successfully",
        "Error": "Error",
        "Warning": "Warning",
        "Success": "Success",
        "Info": "Info"
    },
    "pt": {
        "Main": "Principal",
        "Settings": "Configurações",
        "About": "Sobre",
        "Input PrusaSlicer File:": "Arquivo PrusaSlicer:",
        "Output Directory:": "Diretório de Saída:",
        "Browse...": "Procurar...",
        "Printer Settings": "Configurações da Impressora",
        "Filaments": "Filamentos",
        "Printers": "Impressoras",
        "Log:": "Log:",
        "Convert": "Converter",
        "Language:": "Idioma:",
        "On Existing Files:": "Em Arquivos Existentes:",
        "Skip": "Pular",
        "Overwrite": "Sobrescrever",
        "Merge": "Mesclar",
        "Apply Settings": "Aplicar Configurações",
        "Select input file": "Selecionar arquivo de entrada",
        "Select output directory": "Selecionar diretório de saída",
        "PrusaSlicer files": "Arquivos PrusaSlicer",
        "All files": "Todos os arquivos",
        "Please select an input file": "Por favor, selecione um arquivo de entrada",
        "Please select an output directory": "Por favor, selecione um diretório de saída",
        "Conversion completed successfully": "Conversão concluída com sucesso",
        "Conversion failed": "Falha na conversão",
        "An error occurred during conversion:": "Ocorreu um erro durante a conversão:",
        "Settings applied successfully": "Configurações aplicadas com sucesso",
        "Error": "Erro",
        "Warning": "Aviso",
        "Success": "Sucesso",
        "Info": "Informação"
    },
    "es": {
        "Main": "Principal",
        "Settings": "Configuración",
        "About": "Acerca de",
        "Input PrusaSlicer File:": "Archivo PrusaSlicer:",
        "Output Directory:": "Directorio de Salida:",
        "Browse...": "Examinar...",
        "Printer Settings": "Configuración de Impresora",
        "Filaments": "Filamentos",
        "Printers": "Impresoras",
        "Log:": "Registro:",
        "Convert": "Convertir",
        "Language:": "Idioma:",
        "On Existing Files:": "En Archivos Existentes:",
        "Skip": "Omitir",
        "Overwrite": "Sobrescribir",
        "Merge": "Combinar",
        "Apply Settings": "Aplicar Configuración",
        "Select input file": "Seleccionar archivo de entrada",
        "Select output directory": "Seleccionar directorio de salida",
        "PrusaSlicer files": "Archivos PrusaSlicer",
        "All files": "Todos los archivos",
        "Please select an input file": "Por favor, seleccione un archivo de entrada",
        "Please select an output directory": "Por favor, seleccione un directorio de salida",
        "Conversion completed successfully": "Conversión completada exitosamente",
        "Conversion failed": "Falló la conversión",
        "An error occurred during conversion:": "Ocurrió un error durante la conversión:",
        "Settings applied successfully": "Configuración aplicada con éxito",
        "Error": "Error",
        "Warning": "Advertencia",
        "Success": "Éxito",
        "Info": "Información"
    }
}

class PrusaOrcaConverter:
    def __init__(self, log_callback=None):
        
        """Initialize the converter with optional log callback"""
        self.log_callback = log_callback
        self.initialize_parameter_mappings()
        
    def initialize_parameter_mappings(self):
        """Initialize parameter mappings between Prusa and Orca"""
        self.parameter_map = {
            'print': {
                # Shell
                'bottom_solid_layers': 'bottom_shell_layers',
                'top_solid_layers': 'top_shell_layers',
                'bottom_solid_min_thickness': 'bottom_shell_thickness',
                'top_solid_min_thickness': 'top_shell_thickness',
                'perimeters': 'wall_loops',
                'layer_height': 'layer_height',
                'perimeter_generator': 'wall_generator',
                'fill_pattern': 'sparse_infill_pattern',
                'fill_density': 'sparse_infill_density',
                'gap_fill_speed': 'gap_infill_speed',
                # Speeds
                'infill_speed': 'sparse_infill_speed',
                'perimeter_speed': 'outer_wall_speed',
                'external_perimeter_speed': 'outer_wall_speed',
                'small_perimeter_speed': 'small_perimeter_speed',
                'solid_infill_speed': 'internal_solid_infill_speed',
                'top_solid_infill_speed': 'top_surface_speed',
                'bridge_speed': 'bridge_speed',
                'first_layer_speed': 'initial_layer_speed',
                'first_layer_infill_speed': 'initial_layer_infill_speed',
                'travel_speed': 'travel_speed',
                'travel_speed_z': 'travel_speed_z',
                'ironing_speed': 'ironing_speed',
                'support_material_speed': 'support_speed',
                'support_material_interface_speed': 'support_interface_speed',
                # Overhang speeds
                'enable_dynamic_overhang_speeds': 'enable_overhang_speed',
                'overhang_speed_0': 'overhang_1_4_speed',
                'overhang_speed_1': 'overhang_2_4_speed',
                'overhang_speed_2': 'overhang_3_4_speed',
                'overhang_speed_3': 'overhang_4_4_speed',
                # Accelerations
                'default_acceleration': 'default_acceleration',
                'perimeter_acceleration': 'inner_wall_acceleration',
                'external_perimeter_acceleration': 'outer_wall_acceleration',
                'infill_acceleration': 'sparse_infill_acceleration',
                'solid_infill_acceleration': 'internal_solid_infill_acceleration',
                'top_solid_infill_acceleration': 'top_surface_acceleration',
                'bridge_acceleration': 'bridge_acceleration',
                'first_layer_acceleration': 'initial_layer_acceleration',
                'travel_acceleration': 'travel_acceleration',
                # Ironing
                'ironing_type': 'ironing_type',
                'ironing_flowrate': 'ironing_flow',
                'ironing_spacing': 'ironing_spacing',
                # Seam
                'seam_position': 'seam_position',
                'seam_gap_distance': 'seam_gap',
                'staggered_inner_seams': 'staggered_inner_seams',
                # Support
                'support_material': 'enable_support',
                'support_material_style': 'support_style',
                'support_material_pattern': 'support_base_pattern',
                'support_material_contact_distance': 'support_top_z_distance',
                'support_material_bottom_contact_distance': 'support_bottom_z_distance',
                'support_material_interface_layers': 'support_interface_top_layers',
                'support_material_interface_pattern': 'support_interface_pattern',
                'support_material_interface_spacing': 'support_interface_spacing',
                'support_material_spacing': 'support_base_pattern_spacing',
                'support_material_buildplate_only': 'support_on_build_plate_only',
                'support_material_xy_spacing': 'support_object_xy_distance',
                'support_material_threshold': 'support_threshold_angle',
                'support_material_extruder': 'support_filament',
                'support_material_interface_extruder': 'support_interface_filament',
                'dont_support_bridges': 'bridge_no_support',
                'raft_layers': 'raft_layers',
                # Tree support
                'support_tree_angle': 'tree_support_branch_angle',
                'support_tree_branch_diameter': 'tree_support_branch_diameter',
                'support_tree_branch_distance': 'tree_support_branch_distance',
                'support_tree_tip_diameter': 'tree_support_tip_diameter',
                # Skirt / Brim
                'skirts': 'skirt_loops',
                'skirt_distance': 'skirt_distance',
                'skirt_height': 'skirt_height',
                'brim_width': 'brim_width',
                'brim_type': 'brim_type',
                'brim_separation': 'brim_object_gap',
                # Fuzzy skin
                'fuzzy_skin': 'fuzzy_skin',
                'fuzzy_skin_thickness': 'fuzzy_skin_thickness',
                'fuzzy_skin_point_dist': 'fuzzy_skin_point_distance',
                # First layer
                'first_layer_height': 'initial_layer_print_height',
                # Quality / features
                'thin_walls': 'detect_thin_wall',
                'overhangs': 'detect_overhang_wall',
                'extra_perimeters_on_overhangs': 'extra_perimeters_on_overhangs',
                'thick_bridges': 'thick_bridges',
                'avoid_crossing_perimeters': 'reduce_crossing_wall',
                'avoid_crossing_perimeters_max_detour': 'max_travel_detour_distance',
                'interface_shells': 'interface_shells',
                'elefant_foot_compensation': 'elefant_foot_compensation',
                'spiral_vase': 'spiral_mode',
                'standby_temperature_delta': 'standby_temperature_delta',
                'ooze_prevention': 'ooze_prevention',
                'single_extruder_multi_material_priming': 'single_extruder_multi_material_priming',
                # Infill
                'fill_angle': 'infill_direction',
                'infill_overlap': 'infill_wall_overlap',
                'solid_infill_below_area': 'minimum_sparse_infill_area',
                'bottom_fill_pattern': 'bottom_surface_pattern',
                'top_fill_pattern': 'top_surface_pattern',
                # Arc
                'arc_fitting': 'enable_arc_fitting',
                # Misc
                'resolution': 'resolution',
                'slice_closing_radius': 'slice_closing_radius',
                'slicing_mode': 'slicing_mode',
                'draft_shield': 'draft_shield',
                'xy_size_compensation': 'xy_contour_compensation',
            },
            'filament': {
                'bed_temperature': 'hot_plate_temp',
                'temperature': 'nozzle_temperature',
                'first_layer_temperature': 'nozzle_temperature_initial_layer',
                'filament_type': 'filament_type',
                'filament_density': 'filament_density',
                'filament_diameter': 'filament_diameter',
                'filament_max_volumetric_speed': 'filament_max_volumetric_speed',
                'extrusion_multiplier': 'filament_flow_ratio',
                'chamber_temperature': 'chamber_temperature',
                'chamber_minimal_temperature': 'chamber_minimal_temperature',
                # Fan
                'max_fan_speed': 'fan_max_speed',
                'min_fan_speed': 'fan_min_speed',
                'fan_below_layer_time': 'fan_cooling_layer_time',
                'slowdown_below_layer_time': 'slow_down_layer_time',
                'full_fan_speed_layer': 'full_fan_speed_layer',
            },
            'printer': {
                'bed_shape': 'printable_area',
                'nozzle_diameter': 'nozzle_diameter',
                'extruder_offset': 'extruder_offset',
                'max_print_height': 'printable_height',
                'printer_model': 'printer_model',
                'printer_variant': 'printer_variant',
                'printer_notes': 'printer_notes',
                'gcode_flavor': 'gcode_flavor',
                'print_host': 'print_host',
                'printhost_apikey': 'printhost_apikey',
                'silent_mode': 'silent_mode',
                'use_firmware_retraction': 'use_firmware_retraction',
                'use_relative_e_distances': 'use_relative_e_distances',
                'host_type': 'host_type',
                'high_current_on_filament_swap': 'high_current_on_filament_swap',
                'machine_max_acceleration_x': 'machine_max_acceleration_x',
                'machine_max_acceleration_y': 'machine_max_acceleration_y',
                'machine_max_acceleration_z': 'machine_max_acceleration_z',
                'machine_max_acceleration_e': 'machine_max_acceleration_e',
                'machine_max_acceleration_extruding': 'machine_max_acceleration_extruding',
                'machine_max_acceleration_retracting': 'machine_max_acceleration_retracting',
                'machine_max_acceleration_travel': 'machine_max_acceleration_travel',
                'machine_max_feedrate_x': 'machine_max_speed_x',
                'machine_max_feedrate_y': 'machine_max_speed_y',
                'machine_max_feedrate_z': 'machine_max_speed_z',
                'machine_max_feedrate_e': 'machine_max_speed_e',
                'machine_max_jerk_x': 'machine_max_jerk_x',
                'machine_max_jerk_y': 'machine_max_jerk_y',
                'machine_max_jerk_z': 'machine_max_jerk_z',
                'machine_max_jerk_e': 'machine_max_jerk_e',
                'machine_max_junction_deviation': 'machine_max_junction_deviation',
                'machine_min_extruding_rate': 'machine_min_extruding_rate',
                'machine_min_travel_rate': 'machine_min_travel_rate',
                'max_layer_height': 'max_layer_height',
                'min_layer_height': 'min_layer_height',
                'start_gcode': 'machine_start_gcode',
                'end_gcode': 'machine_end_gcode',
                'before_layer_gcode': 'before_layer_change_gcode',
                'toolchange_gcode': 'change_filament_gcode',
            },
        }
        self.value_map = {
            'print': {
                'support_material_style': {
                    'tree': 'tree_slim',
                    'organic': 'organic',
                    'grid': 'grid',
                    'snug': 'snug',
                },
                'seam_position': {
                    'nearest': 'nearest',
                    'aligned': 'aligned',
                    'rear': 'back',
                    'random': 'random',
                },
                'ironing_type': {
                    '0': 'no ironing',
                    'all': 'solid',
                    'topmost': 'topmost',
                    'top': 'top',
                },
                'fuzzy_skin': {
                    'none': 'none',
                    'all': 'all',
                    'exterior': 'external',
                },
                'slicing_mode': {
                    'regular': 'regular',
                    'even-odd': 'even_odd',
                    'close-holes': 'close_holes',
                },
                'support_material_interface_pattern': {
                    'rectilinear-interlaced': 'rectilinear_interlaced',
                },
                'brim_type': {
                    'no_brim': 'no_brim',
                    'outer_only': 'outer_only',
                    'inner_only': 'inner_only',
                    'outer_brim': 'outer_only',
                    'inner_brim': 'inner_only',
                },
                # Prusa 2.9.x stores this as an enum ("disabled"/"emit_center"),
                # but Orca's enable_arc_fitting is a plain bool.
                'arc_fitting': {
                    'disabled': '0',
                    'emit_center': '1',
                },
            },
        }
        self.extra_param_map = {
            'print': {
                'support_material_style': {
                    'grid': {'support_type': 'normal(auto)'},
                    'snug': {'support_type': 'normal(auto)'},
                    'tree': {'support_type': 'tree(auto)'},
                    'organic': {'support_type': 'tree(auto)'},
                },
            },
        }
        # Orca option keys whose value must be a JSON array of strings (per-extruder /
        # nullable-override types: coFloats, coInts, coBools, coPercents, coPoints).
        # Prusa stores these as a single string, comma-separated when there are
        # multiple extruders. Scoped to only the keys this file's parameter_map
        # actually maps to - verified against Orca v2.4.1's PrintConfig.cpp types.
        self.vector_orca_keys = {
            'hot_plate_temp', 'nozzle_temperature', 'nozzle_temperature_initial_layer',
            'filament_density', 'filament_diameter', 'filament_flow_ratio',
            'filament_max_volumetric_speed',
            'chamber_temperature', 'chamber_minimal_temperature', 'fan_max_speed',
            'fan_min_speed', 'fan_cooling_layer_time', 'slow_down_layer_time',
            'full_fan_speed_layer', 'printable_area', 'nozzle_diameter', 'extruder_offset',
            'machine_max_acceleration_x', 'machine_max_acceleration_y',
            'machine_max_acceleration_z', 'machine_max_acceleration_e',
            'machine_max_acceleration_extruding', 'machine_max_acceleration_retracting',
            'machine_max_acceleration_travel', 'machine_max_speed_x', 'machine_max_speed_y',
            'machine_max_speed_z', 'machine_max_speed_e', 'machine_max_jerk_x',
            'machine_max_jerk_y', 'machine_max_jerk_z', 'machine_max_jerk_e',
            'machine_max_junction_deviation', 'machine_min_extruding_rate',
            'machine_min_travel_rate', 'max_layer_height', 'min_layer_height',
        }
        # Subset of the above whose Prusa-side type is coStrings, which Slic3r/PrusaSlicer
        # serializes as cstyle-quoted, ';'-separated text (see escape_strings_cstyle() in
        # libslic3r/Config.cpp) instead of a plain comma-joined list.
        self.vector_string_keys = {
            'filament_type',
        }
        # Prusa (source) keys whose type is a scalar coString. Slic3r/PrusaSlicer
        # serializes these with escape_string_cstyle(): literal "\n"/"\r"/"\\" text
        # sequences instead of real newlines/backslashes, e.g. multi-line custom
        # G-code blocks. Must be unescaped back to real characters on read, or Orca
        # will render a literal backslash-n instead of a line break.
        self.scalar_string_keys = {
            'printer_model', 'printer_variant', 'printer_notes', 'print_host',
            'printhost_apikey', 'start_gcode', 'end_gcode', 'before_layer_gcode',
            'toolchange_gcode',
        }

    @staticmethod
    def _unescape_strings_cstyle(value: str) -> List[str]:
        """Parse a Slic3r/PrusaSlicer cstyle-escaped, ';'-separated string list."""
        if value == '':
            return []
        out = []
        i, n = 0, len(value)
        while i < n:
            while i < n and value[i] in ' \t':
                i += 1
            if i >= n:
                break
            buf = []
            if value[i] == '"':
                i += 1
                while i < n and value[i] != '"':
                    c = value[i]
                    if c == '\\' and i + 1 < n:
                        i += 1
                        c = {'r': '\r', 'n': '\n'}.get(value[i], value[i])
                    buf.append(c)
                    i += 1
                i += 1  # skip closing quote
            else:
                while i < n and value[i] != ';':
                    buf.append(value[i])
                    i += 1
            out.append(''.join(buf))
            while i < n and value[i] in ' \t':
                i += 1
            if i < n and value[i] == ';':
                i += 1
        return out

    @staticmethod
    def _unescape_string_cstyle(value: str) -> str:
        """Unescape a Slic3r/PrusaSlicer cstyle-escaped scalar string (\\n, \\r, \\\\)."""
        if '\\' not in value:
            return value
        out = []
        i, n = 0, len(value)
        while i < n:
            c = value[i]
            if c == '\\' and i + 1 < n:
                i += 1
                c = {'r': '\r', 'n': '\n'}.get(value[i], value[i])
            out.append(c)
            i += 1
        return ''.join(out)

    def log(self, level: str, message: str):
        """Log a message with timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {level.upper()}: {message}"
        if self.log_callback:
            self.log_callback(log_message)

    def log_mapping_summary(self, configs: Dict[str, Dict[str, str]]) -> None:
        """Log per-section total vs mappable param count, for both UI and headless."""
        for section_name, config in configs.items():
            ini_type = section_name.split(":")[0].lower() if ":" in section_name else "print"
            mapped = self.parameter_map.get(ini_type, {})
            mappable = sum(1 for k in config if k in mapped)
            self.log("info", f"Section {section_name}: {mappable} of {len(config)} parameters are mappable")
    
    def read_ini_file(self, file_path: Path) -> Dict[str, Dict[str, str]]:
        """Read an INI file and return a dictionary of sections and key-value pairs"""
        self.log("info", f"Reading INI file: {file_path}")
        config = configparser.ConfigParser(interpolation=None)
        config.optionxform = str  # Preserve case
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config.read_file(f)
            
            parsed_config = {}
            for section in config.sections():
                parsed_config[section] = dict(config.items(section))
                n = len(parsed_config[section])
                self.log("debug", f"Section {section} has {n} parameters")
            
            total_params = sum(len(v) for v in parsed_config.values())
            self.log("info", f"Read {len(parsed_config)} sections, {total_params} total parameters")
            return parsed_config
        except Exception as e:
            self.log("error", f"Failed to read INI file: {str(e)}")
            return {}
    
    def convert_config(self, input_file: Path, output_dir: Path, updated_configs: Dict[str, Dict[str, str]]) -> bool:
        """Convert config from Prusa to Orca format"""
        try:
            self.log("info", f"Starting conversion for {input_file.name}")
            
            if not updated_configs:
                self.log("error", "No configurations provided for conversion")
                return False
            
            # Create output directory if it doesn't exist
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Process each section
            for section_name, config in updated_configs.items():
                # "[presets]" is bundle metadata (which profile is selected in each
                # category), not an actual settings profile - skip it.
                if section_name.strip().lower() == "presets":
                    self.log("info", f"  Skipping metadata section: {section_name}")
                    continue
                # Determine config type from section name
                if ":" in section_name:
                    ini_type = section_name.split(":")[0].lower()
                    profile_name = section_name.split(":")[1].strip()
                else:
                    ini_type = "print"
                    profile_name = section_name


                if ini_type not in self.parameter_map:
                    self.log("warning", f"Skipping unsupported section type: {ini_type}")
                    continue

                self.log("info", f"  Converting [{ini_type}] {profile_name} ({len(config)} params)")

                # Create Orca config structure
                # NOTE: filament_settings_id is coStrings (a JSON array) in Orca, while
                # print_settings_id/printer_settings_id are plain coString scalars.
                settings_id_value = [profile_name] if ini_type == "filament" else profile_name
                orca_config = {
                    f"{ini_type}_settings_id": settings_id_value,
                    "name": profile_name,
                    "from": "User",
                    "version": ORCA_SLICER_VERSION
                }

                mapped_count = 0
                # Convert parameters with value mapping
                for param, value in config.items():
                    if param in self.parameter_map[ini_type]:
                        orca_param = self.parameter_map[ini_type][param]
                        if ini_type in self.value_map and param in self.value_map[ini_type]:
                            value = self.value_map[ini_type][param].get(value, value)
                        if param in self.scalar_string_keys:
                            value = self._unescape_string_cstyle(value)
                        if orca_param in self.vector_string_keys:
                            orca_config[orca_param] = self._unescape_strings_cstyle(value)
                        elif orca_param in self.vector_orca_keys:
                            orca_config[orca_param] = [v.strip() for v in value.split(',')]
                        else:
                            orca_config[orca_param] = value
                        if ini_type in self.extra_param_map and param in self.extra_param_map[ini_type]:
                            for k, v in self.extra_param_map[ini_type][param].get(value, {}).items():
                                orca_config[k] = v
                        mapped_count += 1
                    #else:
                    #    print(f"[CONVERT]     Unmapped param: {param}={value}", flush=True)
                
                # Save as JSON
                safe_name = "".join(c for c in profile_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                output_file = output_dir / f"{safe_name}.json"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(orca_config, f, indent=4, ensure_ascii=False)
                
                self.log("info", f"  Saved {safe_name}.json ({mapped_count} params mapped)")
            
            self.log("info", "Conversion completed successfully")
            return True
            
        except Exception as e:
            self.log("error", f"Conversion failed: {str(e)}")
            traceback.print_exc()
            return False

class ParameterEditor(tk.Frame):
    """Widget for editing individual parameters with enable/disable checkbox"""
    
    def __init__(self, parent, param_name: str, param_value: str):
        super().__init__(parent)
        self.param_name = param_name
        
        # Convert None/nil/empty values to empty string and disable by default
        if (param_value is None or 
            str(param_value).strip().lower() in ["nil", "null", ""] or 
            str(param_value).strip() == ""):
            param_value = ""
            initial_enabled = False
        else:
            param_value = str(param_value)
            initial_enabled = True
            
        self.original_value = param_value
        
        # Create the checkbox for enable/disable
        self.enabled_var = tk.BooleanVar(value=initial_enabled)
        self.checkbox = ttk.Checkbutton(self, variable=self.enabled_var, command=self.on_toggle)
        self.checkbox.pack(side=tk.LEFT, padx=(0, 5))
        
        # Create label for parameter name
        self.name_label = ttk.Label(self, text=param_name, width=30, anchor="w")
        self.name_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Create the value widget
        self.value_var = tk.StringVar(value=param_value)
        self.value_widget = self.create_value_widget()
        self.value_widget.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Set initial state
        self.on_toggle()
    
    def create_value_widget(self):
        """Create appropriate widget based on parameter value type"""
        value = self.value_var.get().strip().lower()
        
        # Boolean parameters
        if value in ["true", "false", "yes", "no"]:
            combo = ttk.Combobox(self, textvariable=self.value_var, 
                               values=["true", "false"], 
                               state="readonly", width=15)
            combo.set("true" if value in ["true", "1", "yes"] else "false")
            return combo
        
        # Numeric parameters
        if self.is_numeric(self.value_var.get()):
            if "." in self.value_var.get():  # Float
                entry = ttk.Entry(self, textvariable=self.value_var, width=20)
                return entry
            else:  # Integer
                spinbox = ttk.Spinbox(self, textvariable=self.value_var, 
                                    from_=-9999, to=9999, width=15)
                spinbox.set(self.value_var.get())
                return spinbox
        
        # Special cases with predefined options
        if self.param_name in ["fill_pattern", "sparse_infill_pattern"]:
            combo = ttk.Combobox(self, textvariable=self.value_var,
                               values=["rectilinear", "grid", "triangles", "cubic", 
                                      "line", "concentric", "honeycomb", "3dhoneycomb", 
                                      "hilbertcurve"],
                               state="readonly", width=20)
            combo.set(self.value_var.get() if self.value_var.get() in combo["values"] else "rectilinear")
            return combo
        
        if self.param_name in ["support_material", "enable_support"]:
            combo = ttk.Combobox(self, textvariable=self.value_var,
                               values=["true", "false"],
                               state="readonly", width=15)
            combo.set("true" if self.value_var.get().strip().lower() in ["true", "1", "yes"] else "false")
            return combo
        
        if self.param_name in ["filament_type"]:
            combo = ttk.Combobox(self, textvariable=self.value_var,
                               values=["PLA", "ABS", "PETG", "TPU", "ASA", "PC", "PA", "PVA", "HIPS"],
                               state="readonly", width=20)
            combo.set(self.value_var.get() if self.value_var.get() in combo["values"] else "PLA")
            return combo
        
        # Default text entry
        entry = ttk.Entry(self, textvariable=self.value_var, width=40)
        return entry
    
    def is_numeric(self, value: str) -> bool:
        """Check if value is numeric"""
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def on_toggle(self):
        """Handle enable/disable toggle"""
        state = "normal" if self.enabled_var.get() else "disabled"
        if isinstance(self.value_widget, ttk.Combobox):
            self.value_widget.configure(state="readonly" if self.enabled_var.get() else "disabled")
        else:
            self.value_widget.configure(state=state)
        self.name_label.configure(foreground="black" if self.enabled_var.get() else "gray")
    
    def get_value(self):
        """Get the current parameter name and value if enabled"""
        if not self.enabled_var.get():
            return None
        value = self.value_var.get().strip()
        return (self.param_name, value) if value else None

class ConverterApp:
    ABOUT_TEXTS = {
        "en": f"""
{APP_NAME}

Author: {AUTHOR}

This program converts PrusaSlicer configuration files 
to OrcaSlicer compatible format, enabling a smooth 
transition between the two slicers.

Features:
• Conversion of print, filament and printer profiles
• Tabbed interface for parameter editing
• Multi-language support
• Detailed conversion logs
• Proper handling of null values

Supported OrcaSlicer version: {ORCA_SLICER_VERSION}
        """,
        "pt": f"""
{APP_NAME}

Autor: {AUTHOR}

Este programa converte arquivos de configuração do PrusaSlicer 
para o formato compatível com OrcaSlicer, permitindo uma 
transição suave entre os dois slicers.

Funcionalidades:
• Conversão de perfis de impressão, filamento e impressora
• Interface com abas para edição de parâmetros
• Suporte a múltiplos idiomas
• Logs detalhados de conversão
• Tratamento adequado de valores nulos

Versão do OrcaSlicer suportada: {ORCA_SLICER_VERSION}
        """,
        "es": f"""
{APP_NAME}

Autor: {AUTHOR}

Este programa convierte archivos de configuración de PrusaSlicer 
al formato compatible con OrcaSlicer, permitiendo una transición 
suave entre los dos slicers.

Características:
• Conversión de perfiles de impresión, filamento e impresora
• Interfaz con pestañas para edición de parámetros
• Soporte para múltiples idiomas
• Registros detallados de conversión
• Manejo adecuado de valores nulos

Versión de OrcaSlicer soportada: {ORCA_SLICER_VERSION}
        """
    }

    def __init__(self, root, input_file=None, output_dir=None):
        self.root = root
        self.root.title(APP_NAME)
        self.cli_input = input_file
        self.cli_output = output_dir
        self.current_language = "en"  # Default language set to English
        self.log_messages = []
        try:
            self.root.iconbitmap(resource_path("Prusa2Orca.ico"))
        except Exception as e:
            self.add_log_message(self._(f"Icon load error: {e}"))
        self.root.geometry("1200x800")
        self.loaded_parameters = {}
        self.parameter_widgets = {
            "print": {},
            "filament": {},
            "printer": {}
        }
        
        # Create converter instance
        self.converter = PrusaOrcaConverter(log_callback=self.add_log_message)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.main_frame = ttk.Frame(self.notebook)
        self.settings_frame = ttk.Frame(self.notebook)
        self.about_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.main_frame, text=self._("Main"))
        self.notebook.add(self.settings_frame, text=self._("Settings"))
        self.notebook.add(self.about_frame, text=self._("About"))
        
        # Setup tabs
        self.setup_main_tab()
        self.setup_settings_tab()
        self.setup_about_tab()

        # Pre-fill from CLI args if provided
        if self.cli_input:
            self.input_file_entry.insert(0, self.cli_input)
            if os.path.exists(self.cli_input):
                self.load_parameters(self.cli_input)
        if self.cli_output:
            self.output_dir_entry.insert(0, self.cli_output)
    
    def _(self, text: str) -> str:
        """Translation function"""
        return TRANSLATIONS.get(self.current_language, {}).get(text, text)
    
    def add_log_message(self, message: str):
        """Add a message to the log"""
        self.log_messages.append(message)
        if hasattr(self, 'log_text'):
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.see(tk.END)
    
    def setup_main_tab(self):
        """Setup the main conversion tab"""
        # Progress bar and status
        progress_frame = ttk.Frame(self.main_frame)
        progress_frame.pack(fill=tk.X, padx=10, pady=(5, 0))
        
        self.progress_status = ttk.Label(progress_frame, text="", anchor=tk.W)
        self.progress_status.pack(fill=tk.X, pady=(0, 5))
        
        self.progress_var = tk.DoubleVar(value=0.0)
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Input file selection
        input_frame = ttk.Frame(self.main_frame)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_frame, text=self._("Input PrusaSlicer File:")).pack(side=tk.LEFT)
        self.input_file_entry = ttk.Entry(input_frame, width=50)
        self.input_file_entry.pack(side=tk.LEFT, padx=(10, 5), fill=tk.X, expand=True)
        ttk.Button(input_frame, text=self._("Browse..."), command=self.browse_input_file).pack(side=tk.RIGHT)
        
        # Output directory selection
        output_frame = ttk.Frame(self.main_frame)
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(output_frame, text=self._("Output Directory:")).pack(side=tk.LEFT)
        self.output_dir_entry = ttk.Entry(output_frame, width=50)
        self.output_dir_entry.pack(side=tk.LEFT, padx=(10, 5), fill=tk.X, expand=True)
        ttk.Button(output_frame, text=self._("Browse..."), command=self.browse_output_dir).pack(side=tk.RIGHT)
        
        # Configuration tabs
        self.config_notebook = ttk.Notebook(self.main_frame)
        self.config_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create scrollable tabs for each configuration type
        self.printer_settings_frame = self.create_scrollable_frame(self.config_notebook, self._("Printer Settings"))
        self.filaments_frame = self.create_scrollable_frame(self.config_notebook, self._("Filaments"))
        self.printers_frame = self.create_scrollable_frame(self.config_notebook, self._("Printers"))
        
        # Log section
        log_frame = ttk.LabelFrame(self.main_frame, text=self._("Log:"))
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Convert button
        convert_frame = ttk.Frame(self.main_frame)
        convert_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(convert_frame, text=self._("Convert"), command=self.convert).pack(side=tk.RIGHT)
    
    def create_scrollable_frame(self, parent, title):
        """Create a scrollable frame for a notebook tab"""
        frame = ttk.Frame(parent)
        parent.add(frame, text=title)
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to scroll
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        return scrollable_frame
    
    def setup_settings_tab(self):
        """Setup the settings tab"""
        # Language selection
        lang_frame = ttk.LabelFrame(self.settings_frame, text=self._("Language:"))
        lang_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.language_var = tk.StringVar(value=self.current_language)
        for lang_code, lang_name in LANGUAGES.items():
            ttk.Radiobutton(lang_frame, text=lang_name, variable=self.language_var, 
                           value=lang_code).pack(anchor=tk.W, padx=10, pady=2)
        
        # File handling options
        file_frame = ttk.LabelFrame(self.settings_frame, text=self._("On Existing Files:"))
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.file_action_var = tk.StringVar(value="overwrite")
        ttk.Radiobutton(file_frame, text=self._("Skip"), variable=self.file_action_var, 
                       value="skip").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Radiobutton(file_frame, text=self._("Overwrite"), variable=self.file_action_var, 
                       value="overwrite").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Radiobutton(file_frame, text=self._("Merge"), variable=self.file_action_var, 
                       value="merge").pack(anchor=tk.W, padx=10, pady=2)
        
        # Apply button
        ttk.Button(self.settings_frame, text=self._("Apply Settings"), 
                  command=self.apply_settings).pack(pady=20)
    
    def setup_about_tab(self):
        """Setup the about tab"""
        self.about_label = ttk.Label(self.about_frame, justify=tk.CENTER)
        self.about_label.pack(pady=20)
        self.update_about_text()
    
    def update_about_text(self):
        """Update the about tab text based on current language"""
        about_text = self.ABOUT_TEXTS.get(self.current_language, self.ABOUT_TEXTS["en"])
        self.about_label.config(text=about_text.strip())
    
    def browse_input_file(self):
        """Browse for input file"""
        file_path = filedialog.askopenfilename(
            title=self._("Select input file"),
            filetypes=[(self._("PrusaSlicer files"), "*.ini"), (self._("All files"), "*.*")]
        )
        if file_path:
            self.input_file_entry.delete(0, tk.END)
            self.input_file_entry.insert(0, file_path)
            self.load_parameters(file_path)
    
    def browse_output_dir(self):
        """Browse for output directory"""
        dir_path = filedialog.askdirectory(
            title=self._("Select output directory")
        )
        if dir_path:
            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, dir_path)
    
    def load_parameters(self, file_path: str):
        """Load parameters from the input file with progress tracking"""
        # Clear previous parameters
        for widget in self.printer_settings_frame.winfo_children():
            widget.destroy()
        for widget in self.filaments_frame.winfo_children():
            widget.destroy()
        for widget in self.printers_frame.winfo_children():
            widget.destroy()
        
        self.loaded_parameters = {}
        self.parameter_widgets = {
            "print": {},
            "filament": {},
            "printer": {}
        }
        
        try:
            # Read the config file
            self.progress_status.config(text=self._("Reading configuration file..."))
            self.root.update_idletasks()
            
            all_configs = self.converter.read_ini_file(Path(file_path))
            if not all_configs:
                self.add_log_message(self._("Error: No configurations found in file."))
                return
            
            total_sections = len(all_configs)
            section_count = 0
            
            # Log mapping summary once (shared with headless flow)
            self.converter.log_mapping_summary(all_configs)

            # Process each section with progress update
            for section_name, config in all_configs.items():
                section_count += 1
                progress = (section_count / total_sections) * 50
                self.progress_var.set(progress)
                self.progress_status.config(
                    text=self._(f"Processing section {section_count} of {total_sections}: {section_name} ({int(progress)}%)")
                )
                self.root.update_idletasks()
                
                # Determine config type from section name
                if ":" in section_name:
                    ini_type = section_name.split(":")[0].lower()
                else:
                    ini_type = "print"  # Default to print settings
                
                # Get the target frame
                target_frame = None
                if ini_type == "print":
                    target_frame = self.printer_settings_frame
                elif ini_type == "filament":
                    target_frame = self.filaments_frame
                elif ini_type == "printer":
                    target_frame = self.printers_frame
                
                if target_frame:
                    # Store the original parameters
                    self.loaded_parameters[section_name] = config
                    self.parameter_widgets[ini_type][section_name] = []
                    
                    # Add section label
                    section_label = ttk.Label(
                        target_frame, 
                        text=f"--- {section_name} ---", 
                        font=("TkDefaultFont", 10, "bold")
                    )
                    section_label.pack(fill=tk.X, pady=5)
                    
                    # Add parameters with progress update
                    total_params = len(config.items())
                    param_count = 0
                    
                    # Only show parameters that have a mapping in the converter
                    mapped_params = self.converter.parameter_map.get(ini_type, {})
                    filtered = [(p, v) for p, v in config.items() if p in mapped_params]
                    for param, value in filtered:
                        param_count += 1
                        progress = 50 + (param_count / len(filtered)) * 50 * (section_count / total_sections) if filtered else 100
                        self.progress_var.set(progress)
                        self.progress_status.config(
                            text=self._(f"Processing parameter {param_count} of {len(filtered)} in section {section_name} ({int(progress)}%)")
                        )
                        self.root.update_idletasks()
                        
                        try:
                            editor = ParameterEditor(target_frame, param, value)
                            editor.pack(fill=tk.X, padx=5, pady=2)
                            self.parameter_widgets[ini_type][section_name].append(editor)
                        except Exception as e:
                            self.add_log_message(self._(f"Error creating editor for {param}: {str(e)}"))
            
            self.progress_var.set(100)
            self.progress_status.config(text=self._("Loading completed successfully"))
            total_mappable = sum(
                len([p for p in cfg if p in self.converter.parameter_map.get(
                    sec.split(":")[0].lower() if ":" in sec else "print", {}
                )])
                for sec, cfg in self.loaded_parameters.items()
            )
            self.add_log_message(self._(f"Loaded {len(self.loaded_parameters)} sections ({total_mappable} mappable parameters)"))
            
        except Exception as e:
            self.progress_var.set(0)
            self.progress_status.config(text=self._(f"Loading error: {str(e)}"))
            self.add_log_message(self._(f"Error loading parameters: {str(e)}"))
            traceback.print_exc()
            messagebox.showerror(self._("Error"), self._(f"Failed to load parameters: {str(e)}"))
        finally:
            self.root.after(2000, lambda: self.progress_var.set(0))  # Reset progress bar after 2 seconds
            self.root.after(2000, lambda: self.progress_status.config(text=""))
    
    def convert(self):
        """Perform the conversion"""
        input_file = self.input_file_entry.get()
        output_dir = self.output_dir_entry.get()
        
        if not input_file:
            messagebox.showerror(self._("Error"), self._("Please select an input file"))
            return
        
        if not output_dir:
            messagebox.showerror(self._("Error"), self._("Please select an output directory"))
            return
        
        try:
            # Clear log
            
            # Collect parameters from all tabs
            self.progress_status.config(text=self._("Preparing parameters for conversion..."))
            self.root.update_idletasks()
            
            updated_configs = {}
            for ini_type, sections in self.parameter_widgets.items():
                for section_name, widgets in sections.items():
                    updated_configs[section_name] = {}
                    for widget in widgets:
                        if isinstance(widget, ParameterEditor):
                            result = widget.get_value()
                            if result:
                                param, value = result
                                updated_configs[section_name][param] = value
            total_params = sum(len(v) for v in updated_configs.values())
            self.add_log_message(self._(f"Collected {len(updated_configs)} sections ({total_params} enabled parameters)"))
            
            # Perform conversion
            self.add_log_message(self._("Starting conversion..."))
            self.progress_status.config(text=self._("Converting settings..."))
            self.root.update_idletasks()
            
            success = self.converter.convert_config(Path(input_file), Path(output_dir), updated_configs)
            
            if success:
                self.progress_status.config(text=self._("Conversion completed successfully"))
                _main_log("Converted.")
            else:
                self.progress_status.config(text=self._("Conversion failed"))
                messagebox.showerror(self._("Error"), self._("Conversion failed"))
                _main_log("Failed.")
        
        except Exception as e:
            self.progress_status.config(text=self._(f"Conversion error: {str(e)}"))
            traceback.print_exc()
            messagebox.showerror(self._("Error"), self._("An error occurred during conversion:") + f"\n{str(e)}")
    
    def apply_settings(self):
        """Apply settings from the settings tab"""
        try:
            # Update language
            new_language = self.language_var.get()
            if new_language != self.current_language:
                self.current_language = new_language
                self.update_interface_language()
            
            messagebox.showinfo(self._("Success"), self._("Settings applied successfully"))
        
        except Exception as e:
            messagebox.showerror(self._("Error"), f"Failed to apply settings: {str(e)}")
    
    def update_interface_language(self):
        """Update interface language"""
        # Update main tab titles
        self.notebook.tab(0, text=self._("Main"))
        self.notebook.tab(1, text=self._("Settings"))
        self.notebook.tab(2, text=self._("About"))
        
        # Update config tab titles
        self.config_notebook.tab(0, text=self._("Printer Settings"))
        self.config_notebook.tab(1, text=self._("Filaments"))
        self.config_notebook.tab(2, text=self._("Printers"))
        
        # Update about text
        self.update_about_text()

def exception_handler(exc_type, exc_value, exc_traceback):
    """Global exception handler for unhandled exceptions"""
    print(f"\n[FATAL] Unhandled exception: {exc_type.__name__}: {exc_value}", file=sys.stderr, flush=True)
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)

def main():
    sys.excepthook = exception_handler

    parser = argparse.ArgumentParser(description="Convert PrusaSlicer configuration to OrcaSlicer format")
    parser.add_argument("--input", "-i", help="Input PrusaSlicer .ini config file")
    parser.add_argument("--output", "-o", help="Output directory for converted JSON files")
    parser.add_argument("--log-file", help="Save conversion log to this file (plain text)")
    parser.add_argument("--convert", "-c", action="store_true",
                        help="Headless conversion: process immediately and exit (requires --input and --output)")
    args = parser.parse_args()

    print("\n" + "=" * 60, flush=True)
    print(f"  {APP_NAME}", flush=True)
    print(f"  Author: {AUTHOR}", flush=True)
    print(f"  OrcaSlicer target: {ORCA_SLICER_VERSION}", flush=True)
    print("=" * 60 + "\n", flush=True)

    _main_log("Starting application...")

    if args.convert:
        if not args.input or not args.output:
            print("error: --convert requires both --input and --output", file=sys.stderr)
            sys.exit(1)
        from pathlib import Path
        import os
        log_messages = []
        old_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        converter = PrusaOrcaConverter(log_callback=log_messages.append)
        success = False
        try:
            configs = converter.read_ini_file(Path(args.input))
            if configs:
                converter.log_mapping_summary(configs)
                success = converter.convert_config(Path(args.input), Path(args.output), configs)
        finally:
            sys.stdout.close()
            sys.stdout = old_stdout
        _main_log("Converted." if success else "Failed.")
        _main_log("Exiting.")
        if args.log_file:
            try:
                with open(args.log_file, 'w') as f:
                    f.write("\n".join(log_messages) + "\n")
            except Exception as e:
                print(f"warning: failed to write log file: {e}", file=sys.stderr)
        sys.exit(0 if success else 1)


    try:
        root = tk.Tk()
        app = ConverterApp(root, input_file=args.input, output_dir=args.output)
        root.mainloop()
        _main_log("Exiting.")
    except Exception as e:
        _main_fatal(str(e))
        traceback.print_exc()

if __name__ == "__main__":
    main()
