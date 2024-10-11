import psutil
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys


CONFIG_FILEPATH = "dxvk.conf"
DEFAULT_SETTINGS = {
    "d3d11.maxFeatureLevel": "12_1",
    "dxgi.hideNvidiaGpu": False,
    "dxgi.hideAmdGpu": False,
    "dxgi.hideIntelGpu": False,
    "d3d11.dcSingleUseMode": False,
    "d3d11.zeroWorkgroupMemory": False,
    "dxgi.deferSurfaceCreation": True,
    "dxgi.enableStateCache": True,
    "d3d11.ignoreGraphicsBarriers": True,
    "d3d11.relaxedBarriers": True,
    "dxgi.numBackBuffers": 3,
    "dxvk.enableGraphicsPipelineLibrary": True,
    "dxvk.numCompilerThreads": 4,
    "d3d11.maxDynamicImageBufferSize": -1,
    "d3d11.samplerLodBias": -1.0,
    "dxvk.useRawSsbo": True,
    "dxgi.useMonitorFallback": True,
    "dxgi.maxFrameLatency": 1,
    "dxvk.enableAsync": True,
    "dxvk.gplAsyncCache": True,
    "dxvk.lazyBarrierSkip": True,
    "dxvk.deferPipelineCompilation": True,
    "dxvk.enableAsyncShaderCompilation": True,
    "dxvk.maxQueuedFrames": 2,
    "dxvk.useEarlyDiscard": True,
    "d3d9.floatEmulation": True,
    "d3d9.maxFrameLatency": 1,
    "d3d9.enableMultiThreading": True,
    "d3d9.forceSwapchainMSAA": 0,
    "d3d9.presentInterval": 0,
    "d3d9.useDynamicTextures": True,
    "d3d9.deferSurfaceCreation": True,
    "d3d9.enableStateCache": True,
    "d3d9.ignoreGraphicsBarriers": True,
    "d3d9.relaxedBarriers": True,
    "d3d9.forceNV12": False,
    "d3d9.lowLatencyMode": True,
    "d3d9.maxQueuedFrames": 1,
    "dxvk.fastMemory": True,
    "dxvk.hud": 0,
    "dxvk.disableMemoryTrackers": True,
    "dxvk.vsync": False,
    "dxvk.disableTextureBindingRecycling": True,
    "dxvk.enableGPUQueryOptimization": True,
    "d3d9.fullscreenExclusive": False,
    "d3d9.allowWindowedMode": True,
    "d3d9.disablePostProcessing": True,
    "d3d9.reduceTextureQuality": True,
    "d3d9.disableShadows": True,
    "d3d9.disableParticleEffects": True,
    "d3d9.disableLighting": True,
    "d3d9.reduceResolutionScaling": True,
    "dxvk.enableShaderCache": True,
    "dxvk.enableTextureStreaming": True,
    "dxvk.memoryHeap": 4096,



}


SETTING_DESCRIPTIONS = {
    "d3d11.maxFeatureLevel": "Maximum graphics feature level. (Default recommended.)",
    "dxgi.hideNvidiaGpu": "Hide NVIDIA GPU. (Default recommended.)",
    "dxgi.hideAmdGpu": "Hide AMD GPU. (Default recommended.)",
    "dxgi.hideIntelGpu": "Hide Intel GPU. (Default recommended.)",
    "d3d11.dcSingleUseMode": "Enable/Disable multi-threading support.",
    "d3d11.zeroWorkgroupMemory": "Memory optimization setting.",
    "dxgi.deferSurfaceCreation": "Defer surface creation.",
    "dxgi.enableStateCache": "Enable state caching.",
    "d3d11.ignoreGraphicsBarriers": "Ignore graphics barriers.",
    "d3d11.relaxedBarriers": "More relaxed graphics barriers.",
    "dxgi.numBackBuffers": "Number of back buffers.",
    "dxvk.enableGraphicsPipelineLibrary": "Shorten loading times with pipeline library.",
    "dxvk.numCompilerThreads": "Number of threads for shader compilation.",
    "d3d11.maxDynamicImageBufferSize": "Dynamic image buffer size.",
    "d3d11.samplerLodBias": "LOD bias. Increases result in lower quality.",
    "dxvk.useRawSsbo": "Enable SSBO.",
    "dxgi.useMonitorFallback": "Enable fallback monitor support.",
    "dxgi.maxFrameLatency": "Minimum frame latency.",
    "dxvk.enableAsync": "Enable asynchronous shader compilation.",
    "dxvk.gplAsyncCache": "Asynchronous shader caching.",
    "dxvk.lazyBarrierSkip": "Skip unnecessary barriers.",
    "dxvk.deferPipelineCompilation": "Defer pipeline compilation.",
    "dxvk.enableAsyncShaderCompilation": "Enable asynchronous shader compilation.",
    "dxvk.maxQueuedFrames": "Frame buffering.",
    "dxvk.useEarlyDiscard": "Skip unnecessary pixel calculations.",
    "d3d9.floatEmulation": "Optimize floating-point operations on CPU.",
    "d3d9.maxFrameLatency": "Minimum latency.",
    "d3d9.enableMultiThreading": "Enable multi-threading support.",
    "d3d9.forceSwapchainMSAA": "MSAA disabled.",
    "d3d9.presentInterval": "VSync off 1 enables, 0 disables for DirectX9.",
    "d3d9.useDynamicTextures": "Enable dynamic textures.",
    "d3d9.deferSurfaceCreation": "Defer surface creation.",
    "d3d9.enableStateCache": "Enable state caching.",
    "d3d9.ignoreGraphicsBarriers": "Ignore graphics barriers.",
    "d3d9.relaxedBarriers": "More relaxed barriers.",
    "d3d9.forceNV12": "Does not force NV12 format.",
    "d3d9.lowLatencyMode": "Low latency mode.",
    "d3d9.maxQueuedFrames": "Frame buffering.",
    "d3d9.fullscreenExclusive": "Disables fullscreen exclusive mode.",
    "d3d9.allowWindowedMode": "Supports windowed mode.",
    "d3d9.disablePostProcessing": "Disable post-processing effects (for low-end systems).",
    "d3d9.reduceTextureQuality": "Reduce texture quality (for low-end systems).",
    "d3d9.disableShadows": "Disable shadows (for low-end systems).",
    "d3d9.disableParticleEffects": "Disable particle effects (for low-end systems).",
    "d3d9.disableLighting": "Disable lighting effects (for low-end systems).",
    "d3d9.reduceResolutionScaling": "Dynamically reduce resolution (for low-end systems).",
    "dxvk.fastMemory": "Enable fast memory management.",
    "dxvk.hud": "Keep FPS counter disabled. 1 enables, 0 disables.",
    "dxvk.disableMemoryTrackers": "Disable memory trackers to reduce CPU load.",
    "dxvk.vsync": "VSync off (for maximum FPS) 1 enables, 0 disables.",
    "dxvk.useEarlyDiscard": "Optimize pixel calculations.",
    "dxvk.disableTextureBindingRecycling": "Reduce texture re-binding, optimize memory.",
    "dxvk.enableGPUQueryOptimization": "Speed up query operations by reducing GPU workload.",
    "dxvk.enableShaderCache": "Enable more aggressive shader caching for smoother performance.",
    "dxvk.enableTextureStreaming": "Optimize texture memory usage.",
    "dxvk.memoryHeap": "Optimize how VRAM is used."
}


def detect_system_properties():
    cpu_cores = psutil.cpu_count(logical=True)
    

    total_ram = round(psutil.virtual_memory().total / (1024 ** 3))
    

    gpus = []
    try:
        gpu_info = subprocess.check_output(
            "wmic path win32_videocontroller get name", shell=True).decode()
        gpu_lines = gpu_info.splitlines()
        
        for line in gpu_lines:
            if "NVIDIA" in line:
                gpus.append("NVIDIA")
            elif "AMD" in line:
                gpus.append("AMD")
            elif "Intel" in line:
                gpus.append("Intel")
    except subprocess.SubprocessError as e:
        print(f"Error detecting GPU: {e}")
    
    gpu = ", ".join(gpus) if gpus else "Unknown"
    
    return {"cpu_cores": cpu_cores, "total_ram": total_ram, "gpu": gpu}

def adjust_settings_for_system():
    system_info = detect_system_properties()


    if system_info["cpu_cores"] >= 8:
        DEFAULT_SETTINGS["dxvk.numCompilerThreads"] = 8
    elif system_info["cpu_cores"] >= 4:
        DEFAULT_SETTINGS["dxvk.numCompilerThreads"] = 4
    else:
        DEFAULT_SETTINGS["dxvk.numCompilerThreads"] = 2


    DEFAULT_SETTINGS["dxgi.hideNvidiaGpu"] = True
    DEFAULT_SETTINGS["dxgi.hideAmdGpu"] = True
    DEFAULT_SETTINGS["dxgi.hideIntelGpu"] = True

  
    if "NVIDIA" in system_info["gpu"]:
        DEFAULT_SETTINGS["dxgi.hideNvidiaGpu"] = False
    if "AMD" in system_info["gpu"]:
        DEFAULT_SETTINGS["dxgi.hideAmdGpu"] = False
    if "Intel" in system_info["gpu"]:
        DEFAULT_SETTINGS["dxgi.hideIntelGpu"] = False

 
    if system_info["total_ram"] < 8:
        DEFAULT_SETTINGS["d3d11.maxFeatureLevel"] = "11_0"
        DEFAULT_SETTINGS["dxvk.memoryHeap"] = 2048 
    elif system_info["total_ram"] >= 16:
        DEFAULT_SETTINGS["dxvk.memoryHeap"] = 8192  
    else:
        DEFAULT_SETTINGS["dxvk.memoryHeap"] = 4096 

    return DEFAULT_SETTINGS


class SettingsEditor:
    

    def __init__(self, root):
        self.root = root
        self.root.title("DXVK Settings Editor")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(True, True)


        self.settings = adjust_settings_for_system()

        self.load_settings()
        self.create_styles()
        self.create_menu()
        self.create_widgets()
        self.create_bindings()

    def create_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TButton', font=('Helvetica', 12), padding=6, foreground='white', background='#4CAF50')
        style.map('TButton', foreground=[('active', 'white')], background=[('active', '#45a049')])
        style.configure('TLabel', font=('Helvetica', 12), background="#f0f0f0", foreground="#333333")
        style.configure('TFrame', background="#f0f0f0")
        style.configure('TEntry', font=('Helvetica', 12))
        style.configure('TCheckbutton', background="#f0f0f0")
        style.configure('SearchEntry.TEntry', font=('Helvetica', 12), padding=5)

    def create_menu(self):
        """Create the application menu."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import Settings...", command=self.import_settings)
        file_menu.add_command(label="Export Settings...", command=self.export_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Reset to Default", command=self.reset_to_default)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_widgets(self):
        """Create and layout all widgets."""
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill=tk.X, padx=10, pady=5)

        search_label = ttk.Label(search_frame, text="Search Settings:")
        search_label.pack(side=tk.LEFT, padx=(0, 5))

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, style='SearchEntry.TEntry')
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.bind("<KeyRelease>", self.update_search)


        canvas_frame = ttk.Frame(self.root)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.canvas = tk.Canvas(canvas_frame, bg="#f0f0f0", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.settings_frame = ttk.Frame(self.canvas, padding="20")
        self.canvas.create_window((0, 0), window=self.settings_frame, anchor="nw")

        self.populate_settings()

        self.settings_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))


        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        save_button = ttk.Button(button_frame, text="Save Settings", command=self.save_settings)
        save_button.pack(side=tk.RIGHT, padx=5)

        reset_button = ttk.Button(button_frame, text="Reset to Default", command=self.reset_to_default)
        reset_button.pack(side=tk.RIGHT, padx=5)

        self.status_label = ttk.Label(self.root, text="", background="#f0f0f0")
        self.status_label.pack(fill=tk.X, padx=10, pady=5)

    def create_bindings(self):
        """Bind mouse wheel scrolling for different platforms."""
        if sys.platform.startswith('win') or sys.platform.startswith('darwin'):
            self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        else:
            self.canvas.bind_all("<Button-4>", self.on_mouse_wheel)
            self.canvas.bind_all("<Button-5>", self.on_mouse_wheel)

    def load_settings(self):
        """Load settings from the configuration file."""
        if os.path.exists(CONFIG_FILEPATH):
            try:
                with open(CONFIG_FILEPATH, 'r') as file:
                    for line in file:
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            key = key.strip()
                            value = value.strip().lower()
                            if key in DEFAULT_SETTINGS:
                                if isinstance(DEFAULT_SETTINGS[key], bool):
                                    self.settings[key] = value == 'true'
                                elif isinstance(DEFAULT_SETTINGS[key], int):
                                    self.settings[key] = int(value)
                                elif isinstance(DEFAULT_SETTINGS[key], float):
                                    self.settings[key] = float(value)
                                else:
                                    self.settings[key] = value
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load settings: {e}")
                self.settings = DEFAULT_SETTINGS.copy()
        else:
            self.settings = DEFAULT_SETTINGS.copy()

    def save_settings(self):
        """Save current settings to the configuration file."""
        try:
            with open(CONFIG_FILEPATH, 'w') as file:
                for key, value in self.settings.items():
                    value_str = "true" if isinstance(value, bool) and value else str(value)
                    file.write(f"{key} = {value_str}\n")
            self.status_label.config(text="Settings saved successfully!", foreground="green")
        except OSError as e:
            self.status_label.config(text=f"Error saving settings: {e}", foreground="red")

    def reset_to_default(self):
        """Reset all settings to default values."""
        self.settings = DEFAULT_SETTINGS.copy()
        self.populate_settings()
        self.status_label.config(text="Settings reset to default values.", foreground="blue")

    def populate_settings(self):
        """Populate the settings frame with entries for each setting."""
        for widget in self.settings_frame.winfo_children():
            widget.destroy()

        for key, value in self.settings.items():
            frame = ttk.Frame(self.settings_frame)
            frame.pack(fill=tk.X, pady=5)

            label = ttk.Label(frame, text=SETTING_DESCRIPTIONS.get(key, key))
            label.pack(side=tk.LEFT, padx=(0, 5))

            if isinstance(value, bool):
                var = tk.BooleanVar(value=value)
                check_button = ttk.Checkbutton(frame, variable=var, command=lambda key=key, var=var: self.update_setting(key, var.get()))
                check_button.pack(side=tk.LEFT)
            else:
                var = tk.StringVar(value=str(value))
                entry = ttk.Entry(frame, textvariable=var)
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                entry.bind("<FocusOut>", lambda e, key=key, var=var: self.update_setting(key, var.get()))

    def update_setting(self, key, value):
        """Update the setting value."""
        if key in DEFAULT_SETTINGS:
            if isinstance(DEFAULT_SETTINGS[key], bool):
                self.settings[key] = bool(value)
            elif isinstance(DEFAULT_SETTINGS[key], int):
                self.settings[key] = int(value)
            elif isinstance(DEFAULT_SETTINGS[key], float):
                self.settings[key] = float(value)
            else:
                self.settings[key] = value

    def import_settings(self):
        """Import settings from an external file."""
        file_path = filedialog.askopenfilename(filetypes=[("Configuration Files", "*.conf"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    imported_settings = {}
                    for line in file:
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            key = key.strip()
                            value = value.strip().lower()
                            if key in DEFAULT_SETTINGS:
                                if isinstance(DEFAULT_SETTINGS[key], bool):
                                    imported_settings[key] = value == 'true'
                                elif isinstance(DEFAULT_SETTINGS[key], int):
                                    imported_settings[key] = int(value)
                                elif isinstance(DEFAULT_SETTINGS[key], float):
                                    imported_settings[key] = float(value)
                                else:
                                    imported_settings[key] = value
                    self.settings.update(imported_settings)
                    self.populate_settings()
                    self.status_label.config(text="Settings imported successfully!", foreground="green")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import settings: {e}")

    def export_settings(self):
        """Export current settings to an external file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".conf", filetypes=[("Configuration Files", "*.conf"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    for key, value in self.settings.items():
                        value_str = "true" if isinstance(value, bool) and value else str(value)
                        file.write(f"{key} = {value_str}\n")
                self.status_label.config(text="Settings exported successfully!", foreground="green")
            except OSError as e:
                messagebox.showerror("Error", f"Failed to export settings: {e}")

    def show_about(self):
        """Show the About dialog."""
        messagebox.showinfo("About DXVK Settings Editor", "DXVK Settings Editor\nVersion 1.0\n\nA tool to edit DXVK settings developed by Xnull.")

    def on_mouse_wheel(self, event):
        """Handle mouse wheel scrolling."""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def update_search(self, event=None):
        """Update the visible settings based on the search query."""
        query = self.search_var.get().lower()
        for frame in self.settings_frame.winfo_children():
            label = frame.winfo_children()[0]
            if query in label.cget("text").lower():
                frame.pack(fill=tk.X, pady=5)
            else:
                frame.pack_forget()


if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsEditor(root)
    root.mainloop()