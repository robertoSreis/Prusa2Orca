import os
import sys
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import configparser
import datetime
from typing import Dict, List, Optional

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

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class PrusaOrcaConverter:
    def __init__(self, log_callback=None):
        
        """Initialize the converter with optional log callback"""
        self.log_callback = log_callback
        self.initialize_parameter_mappings()
        
    def initialize_parameter_mappings(self):
        """Initialize parameter mappings between Prusa and Orca"""
        self.parameter_map = {
            'print': {
                'bottom_solid_layers': 'bottom_shell_layers',
                'fill_pattern': 'sparse_infill_pattern',
                'fill_density': 'sparse_infill_density',
                'layer_height': 'layer_height',
                'perimeters': 'wall_loops',
                'top_solid_layers': 'top_shell_layers',
                'infill_speed': 'sparse_infill_speed',
                'perimeter_speed': 'outer_wall_speed',
                'first_layer_speed': 'initial_layer_speed',
                'support_material': 'enable_support',
                'brim_width': 'brim_width',
                'skirts': 'skirt_loops',
                'skirt_distance': 'skirt_distance'
            },
            'filament': {
                'bed_temperature': 'hot_plate_temp',
                'temperature': 'nozzle_temperature',
                'first_layer_temperature': 'nozzle_temperature_initial_layer',
                'filament_type': 'filament_type',
                'filament_density': 'filament_density',
                'filament_diameter': 'filament_diameter'
            },
            'printer': {
                'bed_shape': 'printable_area',
                'nozzle_diameter': 'nozzle_diameter',
                'extruder_offset': 'extruder_offset'
            }
        }
    
    def log(self, level: str, message: str):
        """Log a message with timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {level.upper()}: {message}"
        if self.log_callback:
            self.log_callback(log_message)
        else:
            print(log_message)
    
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
                self.log("debug", f"Section {section} has {len(parsed_config[section])} parameters")
            
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
                
                # Create Orca config structure
                orca_config = {
                    f"{ini_type}_settings_id": profile_name,
                    "name": profile_name,
                    "from": "User",
                    "version": ORCA_SLICER_VERSION
                }
                
                # Convert parameters
                for param, value in config.items():
                    if param in self.parameter_map[ini_type]:
                        orca_param = self.parameter_map[ini_type][param]
                        orca_config[orca_param] = value
                
                # Save as JSON
                safe_name = "".join(c for c in profile_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                output_file = output_dir / f"{safe_name}.json"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(orca_config, f, indent=4, ensure_ascii=False)
                
                self.log("info", f"Saved config to {output_file}")
            
            self.log("info", "Conversion completed successfully")
            return True
            
        except Exception as e:
            self.log("error", f"Conversion failed: {str(e)}")
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
        if value in ["true", "false", "1", "0", "yes", "no"]:
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
            combo.set("true" if self.value_var.get().lower() in ["true", "1", "yes"] else "false")
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

    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        try:
            self.root.iconbitmap(resource_path("Prusa2Orca.ico"))
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")  # Isso ajudará no debug
        self.root.geometry("1200x800")
        
        # Initialize variables
        self.log_messages = []
        self.current_language = "en"  # Default language set to English
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
                    
                    for param, value in config.items():
                        param_count += 1
                        progress = 50 + (param_count / total_params) * 50 * (section_count / total_sections)
                        self.progress_var.set(progress)
                        self.progress_status.config(
                            text=self._(f"Processing parameter {param_count} of {total_params} in section {section_name} ({int(progress)}%)")
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
            self.add_log_message(self._("Parameters loaded successfully"))
            
        except Exception as e:
            self.progress_var.set(0)
            self.progress_status.config(text=self._(f"Loading error: {str(e)}"))
            self.add_log_message(self._(f"Error loading parameters: {str(e)}"))
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
            self.log_text.delete(1.0, tk.END)
            
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
            
            # Perform conversion
            self.add_log_message(self._("Starting conversion..."))
            self.progress_status.config(text=self._("Converting settings..."))
            self.root.update_idletasks()
            
            success = self.converter.convert_config(Path(input_file), Path(output_dir), updated_configs)
            
            if success:
                self.progress_status.config(text=self._("Conversion completed successfully"))
                messagebox.showinfo(self._("Success"), self._("Conversion completed successfully"))
            else:
                self.progress_status.config(text=self._("Conversion failed"))
                messagebox.showerror(self._("Error"), self._("Conversion failed"))
        
        except Exception as e:
            self.progress_status.config(text=self._(f"Conversion error: {str(e)}"))
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

def main():
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
