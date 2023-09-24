import config
from event import Event
import dearpygui.dearpygui as dpg

class Gui:
    def __init__(self, config: config.Config, window_width: int, window_height: int, logo_path: str):
        self.config = config
        self.sliders = []
        # self.window_width = 550
        # self.window_height = 1040
        self.window_width = window_width
        self.window_height = window_height
        self.logo_path = logo_path
        self.on_disconnect_clicked = Event()
        self.on_connect_clicked = Event()
        self.on_save_settings_clicked = Event()

    def handle_connect_callback(self, sender, app_data):
        self.on_connect_clicked.dispatch(sender, app_data)

    def handle_disconnect_callback(self, sender, app_data):
        self.on_disconnect_clicked.dispatch(sender, app_data)

    def handle_save_settings_callback(self, sender, app_data):
        self.on_save_settings_clicked.dispatch(sender, app_data)

    def create_centered_image(self, tag: str, path: str):
        image_width, image_height, _, data = dpg.load_image(path)

        with dpg.texture_registry():
            dpg.add_static_texture(width=image_width, height=image_height, default_value=data, tag=tag)

        spacer_width = (self.window_width - image_width) / 2
        with dpg.group(horizontal=True):
            width_spacer_id = dpg.add_spacer(width=int(spacer_width) - 25)
            dpg.add_image(tag)
            width_spacer_id_2 = dpg.add_spacer(width=int(spacer_width))

        def resize_callback():
            current_window_width = dpg.get_viewport_width()
            spacer_width = (current_window_width - image_width) / 2
            dpg.configure_item(width_spacer_id, width=int(spacer_width) - 25)
            dpg.configure_item(width_spacer_id_2, width=int(spacer_width))

        return resize_callback
    
    def init(self):
        dpg.create_context()
        with dpg.window(tag="MAIN_WINDOW"):
            dpg.add_spacer(height=20)
            # handle_centered_image = self.create_centered_image("logo", "./img/logo.png")
            handle_centered_image = self.create_centered_image("logo", self.logo_path)
            dpg.add_spacer(height=20)

            dpg.add_text("OWO Suit IP Address")
            dpg.add_input_text(width=-1)
            dpg.add_checkbox(label="Automatically Detect IP Address")
            dpg.add_spacer(height=20)
            
            dpg.add_text("Server Port Number")
            dpg.add_input_int(width=-1)
            dpg.add_spacer(height=20)

            # Sliders with labels coming before
            dpg.add_text("Frequency Settings")
            dpg.add_slider_int(min_value=0, max_value=100, width=-1)
            dpg.add_spacer(height=20)

            dpg.add_text("Intensity Settings")
            with dpg.group():
                dpg.add_slider_int(min_value=0, width=-120,
                                max_value=100, label="Left Pectoral")
                dpg.add_slider_int(min_value=0, width=-120,
                                max_value=100, label="Right Pectoral")
            with dpg.group():
                dpg.add_slider_int(min_value=0, width=-120,
                                max_value=100, label="Left Abdominal")
                dpg.add_slider_int(min_value=0, width=-120,
                                max_value=100, label="Right Abdominal")
            with dpg.group():
                dpg.add_slider_int(min_value=0, width=-120,
                                max_value=100, label="Left Arm")
                dpg.add_slider_int(min_value=0, width=-120,
                                max_value=100, label="Right Arm")
            with dpg.group():
                dpg.add_slider_int(min_value=0, width=-120,
                                max_value=100, label="Left Dorsal")
                dpg.add_slider_int(min_value=0, width=-120,
                                max_value=100, label="Right Dorsal")
            with dpg.group():
                dpg.add_slider_int(min_value=0, width=-120,
                                max_value=100, label="Left Lumbar")
                dpg.add_slider_int(min_value=0, width=-120,
                                max_value=100, label="Right Lumbar")
            dpg.add_spacer(height=20)

            # Terminal-like output
            dpg.add_text("Terminal Information")
            dpg.add_input_text(multiline=True, readonly=True,
                            default_value="Terminal Information...", height=90, width=-1)

            dpg.add_spacer(height=20)

            # Connect button
            with dpg.group(horizontal=True):
                dpg.add_button(label="Connect", callback=self.handle_connect_callback)
                dpg.add_button(label="Save Settings", callback=self.handle_save_settings_callback)
            dpg.add_spacer(height=20)
            dpg.add_checkbox(label="Automatically Connect on Startup")

            dpg.add_spacer(height=20)

            
            with dpg.group(width=-1):
                dpg.add_text("Created by Shadoki.", indent=185)
                dpg.add_text("This application is not affiliated with VRChat or OWO.", indent=75)
                dpg.add_text("Want to contribute?", indent=185, color=(51, 102, 204))

        dpg.create_viewport(title='VRChat OWO Suit', width=self.window_width, height=self.window_height)
        dpg.set_viewport_resize_callback(handle_centered_image)

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("MAIN_WINDOW", True)

    def run(self):
        dpg.start_dearpygui()

    def cleanup(self):
        dpg.destroy_context()
