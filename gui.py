import config
import webbrowser
from event import Event
import dearpygui.dearpygui as dpg
from enum import Enum, auto


class Element(Enum):
    IP_ADDRESS_INPUT = auto()
    DETECT_IP_ADDRESS_CHECKBOX = auto()
    SERVER_PORT_NUMBER_INPUT = auto()
    FREQUENCY_SETTING_SLIDER = auto()
    LEFT_PECTORAL_SETTING_SLIDER = auto()
    RIGHT_PECTORAL_SETTING_SLIDER = auto()
    LEFT_ABDOMINAL_SETTING_SLIDER = auto()
    RIGHT_ABDOMINAL_SETTING_SLIDER = auto()
    LEFT_ARM_SETTING_SLIDER = auto()
    RIGHT_ARM_SETTING_SLIDER = auto()
    LEFT_DORSAL_SETTING_SLIDER = auto()
    RIGHT_DORSAL_SETTING_SLIDER = auto()
    LEFT_LUMBAR_SETTING_SLIDER = auto()
    RIGHT_LUMBAR_SETTING_SLIDER = auto()
    TERMINAL_WINDOW_INPUT = auto()
    CONNECT_BUTTON = auto()
    SAVE_SETTINGS_BUTTON = auto()
    CONNECT_ON_STARTUP_CHECKBOX = auto()
    CONTRIBUTE_BUTTON = auto()


class Gui:
    def __init__(self, config: config.Config, window_width: int, window_height: int, logo_path: str):
        self.config = config
        self.sliders = []
        self.window_width = window_width
        self.window_height = window_height
        self.logo_path = logo_path
        self.on_disconnect_clicked = Event()
        self.on_connect_clicked = Event()
        self.on_save_settings_clicked = Event()
        self.on_intensity_change = Event()
        self.elements = {
            Element.IP_ADDRESS_INPUT: None,
            Element.DETECT_IP_ADDRESS_CHECKBOX: None,
            Element.SERVER_PORT_NUMBER_INPUT: None,
            Element.FREQUENCY_SETTING_SLIDER: None,
            Element.LEFT_PECTORAL_SETTING_SLIDER: None,
            Element.RIGHT_PECTORAL_SETTING_SLIDER: None,
            Element.LEFT_ABDOMINAL_SETTING_SLIDER: None,
            Element.RIGHT_ABDOMINAL_SETTING_SLIDER: None,
            Element.LEFT_ARM_SETTING_SLIDER: None,
            Element.RIGHT_ARM_SETTING_SLIDER: None,
            Element.LEFT_DORSAL_SETTING_SLIDER: None,
            Element.RIGHT_DORSAL_SETTING_SLIDER: None,
            Element.LEFT_LUMBAR_SETTING_SLIDER: None,
            Element.RIGHT_LUMBAR_SETTING_SLIDER: None,
            Element.TERMINAL_WINDOW_INPUT: None,
            Element.CONNECT_BUTTON: None,
            Element.SAVE_SETTINGS_BUTTON: None,
            Element.CONNECT_ON_STARTUP_CHECKBOX: None,
            Element.CONTRIBUTE_BUTTON: None,
        }

    def handle_connect_callback(self, sender, app_data):
        self.on_connect_clicked.dispatch(sender, app_data)

    def handle_disconnect_callback(self, sender, app_data):
        self.on_disconnect_clicked.dispatch(sender, app_data)

    def handle_save_settings_callback(self, sender, app_data):
        self.on_save_settings_clicked.dispatch(sender, app_data)

    def handle_intensity_change(self, sender, app_data):
        parameter = ""
        value = 1
        # figure out how to get these values from sender and app data
        self.on_intensity_change.dispatch(parameter, value)

    def handle_contribute_callback(self, sender, app_data):
        webbrowser.open("https://github.com/uzair-ashraf/vrc-owo-suit")

    def create_centered_image(self, tag: str, path: str):
        image_width, image_height, _, data = dpg.load_image(path)

        with dpg.texture_registry():
            dpg.add_static_texture(
                width=image_width, height=image_height, default_value=data, tag=tag)

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
            handle_centered_image = self.create_centered_image(
                "logo", self.logo_path)
            dpg.add_spacer(height=20)

            dpg.add_text("OWO Suit IP Address")
            self.elements[Element.IP_ADDRESS_INPUT] = dpg.add_input_text(
                width=-1)
            self.elements[Element.DETECT_IP_ADDRESS_CHECKBOX] = dpg.add_checkbox(
                label="Automatically Detect IP Address")
            dpg.add_spacer(height=20)

            dpg.add_text("Server Port Number")
            self.elements[Element.SERVER_PORT_NUMBER_INPUT] = dpg.add_input_int(
                width=-1)
            dpg.add_spacer(height=20)

            # Sliders with labels coming before
            dpg.add_text("Frequency Settings")
            self.elements[Element.FREQUENCY_SETTING_SLIDER] = dpg.add_slider_int(
                min_value=0, max_value=100, width=-1)
            dpg.add_spacer(height=20)

            dpg.add_text("Intensity Settings")
            with dpg.group():
                self.elements[Element.LEFT_PECTORAL_SETTING_SLIDER] = dpg.add_slider_int(min_value=0, width=-120,
                                                                                         max_value=100, label="Left Pectoral")
                self.elements[Element.RIGHT_PECTORAL_SETTING_SLIDER] = dpg.add_slider_int(min_value=0, width=-120,
                                                                                          max_value=100, label="Right Pectoral")
            with dpg.group():
                self.elements[Element.LEFT_ABDOMINAL_SETTING_SLIDER] = dpg.add_slider_int(min_value=0, width=-120,
                                                                                          max_value=100, label="Left Abdominal")
                self.elements[Element.RIGHT_ABDOMINAL_SETTING_SLIDER] = dpg.add_slider_int(min_value=0, width=-120,
                                                                                           max_value=100, label="Right Abdominal")
            with dpg.group():
                self.elements[Element.LEFT_ARM_SETTING_SLIDER] = dpg.add_slider_int(min_value=0, width=-120,
                                                                                    max_value=100, label="Left Arm")
                self.elements[Element.RIGHT_ARM_SETTING_SLIDER] = dpg.add_slider_int(min_value=0, width=-120,
                                                                                     max_value=100, label="Right Arm")
            with dpg.group():
                self.elements[Element.LEFT_DORSAL_SETTING_SLIDER] = dpg.add_slider_int(min_value=0, width=-120,
                                                                                       max_value=100, label="Left Dorsal")
                self.elements[Element.RIGHT_DORSAL_SETTING_SLIDER] = dpg.add_slider_int(min_value=0, width=-120,
                                                                                        max_value=100, label="Right Dorsal")
            with dpg.group():
                self.elements[Element.LEFT_LUMBAR_SETTING_SLIDER] = dpg.add_slider_int(min_value=0, width=-120,
                                                                                       max_value=100, label="Left Lumbar")
                self.elements[Element.RIGHT_LUMBAR_SETTING_SLIDER] = dpg.add_slider_int(min_value=0, width=-120,
                                                                                        max_value=100, label="Right Lumbar")
            dpg.add_spacer(height=20)

            # Terminal-like output
            dpg.add_text("Logs")
            self.elements[Element.TERMINAL_WINDOW_INPUT] = dpg.add_input_text(multiline=True, readonly=True,
                                                                              default_value="...", height=90, width=-1)

            dpg.add_spacer(height=20)

            # Connect button
            with dpg.group(horizontal=True):
                self.elements[Element.CONNECT_BUTTON] = dpg.add_button(label="Connect",
                                                                       callback=self.handle_connect_callback)
                self.elements[Element.SAVE_SETTINGS_BUTTON] = dpg.add_button(label="Save Settings",
                                                                             callback=self.handle_save_settings_callback)
            dpg.add_spacer(height=20)
            self.elements[Element.CONNECT_ON_STARTUP_CHECKBOX] = dpg.add_checkbox(
                label="Automatically Connect on Startup")

            dpg.add_spacer(height=20)

            with dpg.group(width=-1):
                self.elements[Element.CONTRIBUTE_BUTTON] = dpg.add_button(label="\t\t\t\t  Created by Shadoki.\nThis application is not affiliated with VRChat or OWO.\n\t\t\t\t  Want to contribute?",
                                                                          width=-1, callback=self.handle_contribute_callback)

        dpg.create_viewport(title='VRChat OWO Suit',
                            width=self.window_width, height=self.window_height)
        dpg.set_viewport_resize_callback(handle_centered_image)

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("MAIN_WINDOW", True)
        print(self.elements.items())

    def run(self):
        dpg.start_dearpygui()

    def cleanup(self):
        dpg.destroy_context()
