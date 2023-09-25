import params
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
    CLEAR_CONSOLE_BUTTON = auto()
    TOGGLES_INTERACTIONS_BUTTON = auto()
    CONNECT_ON_STARTUP_CHECKBOX = auto()
    CONTRIBUTE_BUTTON = auto()


class Gui:
    def __init__(self, config: config.Config, window_width: int, window_height: int, logo_path: str):
        self.config = config
        self.sliders = []
        self.window_width = window_width
        self.window_height = window_height
        self.logo_path = logo_path
        self.on_connect_clicked = Event()
        self.on_save_settings_clicked = Event()
        self.on_clear_console_clicked = Event()
        self.on_toggle_interaction_clicked = Event()
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
            Element.CLEAR_CONSOLE_BUTTON: None,
            Element.TOGGLES_INTERACTIONS_BUTTON: None,
            Element.CONNECT_ON_STARTUP_CHECKBOX: None,
            Element.CONTRIBUTE_BUTTON: None,
        }
        self.element_to_config_key = {
            Element.SERVER_PORT_NUMBER_INPUT: "server_port",
            Element.IP_ADDRESS_INPUT: "owo_ip",
            Element.DETECT_IP_ADDRESS_CHECKBOX: "should_detect_ip",
            Element.CONNECT_ON_STARTUP_CHECKBOX: "should_connect_on_startup",
            Element.FREQUENCY_SETTING_SLIDER: "frequency",
            "intensities": {
                Element.LEFT_PECTORAL_SETTING_SLIDER: params.owo_suit_Pectoral_L,
                Element.RIGHT_PECTORAL_SETTING_SLIDER: params.owo_suit_Pectoral_R,
                Element.LEFT_ABDOMINAL_SETTING_SLIDER: params.owo_suit_Abdominal_L,
                Element.RIGHT_ABDOMINAL_SETTING_SLIDER: params.owo_suit_Abdominal_R,
                Element.LEFT_ARM_SETTING_SLIDER: params.owo_suit_Arm_L,
                Element.RIGHT_ARM_SETTING_SLIDER: params.owo_suit_Arm_R,
                Element.LEFT_DORSAL_SETTING_SLIDER: params.owo_suit_Dorsal_L,
                Element.RIGHT_DORSAL_SETTING_SLIDER: params.owo_suit_Dorsal_R,
                Element.LEFT_LUMBAR_SETTING_SLIDER: params.owo_suit_Lumbar_L,
                Element.RIGHT_LUMBAR_SETTING_SLIDER: params.owo_suit_Lumbar_R,
            }
        }
        self.parameter_to_muscle_element = {
            value: key for key, value in self.element_to_config_key.get('intensities').items()
        }
        self.element_labels = {
            Element.LEFT_PECTORAL_SETTING_SLIDER: "Left Pectoral",
            Element.RIGHT_PECTORAL_SETTING_SLIDER: "Right Pectoral",
            Element.LEFT_ABDOMINAL_SETTING_SLIDER: "Left Abdominal",
            Element.RIGHT_ABDOMINAL_SETTING_SLIDER: "Right Abdominal",
            Element.LEFT_ARM_SETTING_SLIDER: "Left Arm",
            Element.RIGHT_ARM_SETTING_SLIDER: "Right Arm",
            Element.LEFT_DORSAL_SETTING_SLIDER: "Left Dorsal",
            Element.RIGHT_DORSAL_SETTING_SLIDER: "Right Dorsal",
            Element.LEFT_LUMBAR_SETTING_SLIDER: "Left Lumbar",
            Element.RIGHT_LUMBAR_SETTING_SLIDER: "Right Lumbar",
        }
        self.ids_to_elements = None

    def handle_connect_callback(self, sender, app_data):
        self.on_connect_clicked.dispatch(sender, app_data)

    def handle_save_settings_callback(self):
        self.config.write_config_to_disk()
        self.print_terminal("Settings Saved!")

    def handle_clear_console_callback(self, sender, app_data):
        self.on_clear_console_clicked.dispatch(sender, app_data)

    def handle_active_muscle_update(self, parameter):
        element_name = self.parameter_to_muscle_element.get(parameter)
        element_id = self.elements[element_name]
        existing_element_label = self.element_labels[element_name]
        result = "[" + existing_element_label + "]"
        dpg.configure_item(
            element_id, label=result
        )

    def handle_active_muscle_reset(self):
        for element_name in self.parameter_to_muscle_element.values():
            element_id = self.elements[element_name]
            label = self.element_labels[element_name]
            dpg.configure_item(
                element_id, label=label
            )

    def handle_toggle_interactions_callback(self, sender, app_data):
        self.on_toggle_interaction_clicked.dispatch()

    def handle_input_change(self, sender, app_data):
        element = self.ids_to_elements.get(sender)
        config_key = self.element_to_config_key.get(element)
        # this implies its an intensity
        if config_key is None:
            intensities_map = self.element_to_config_key.get("intensities")
            config_key = intensities_map.get(element)
            intensities = self.config.get_by_key("intensities")
            intensities[config_key] = app_data
            self.config.update("intensities", intensities)
            return
        self.config.update(config_key, app_data)

    def handle_contribute_callback(self, sender, app_data):
        webbrowser.open("https://github.com/uzair-ashraf/vrc-owo-suit")

    def handle_connecting_state_change(self, next_state):
        if next_state == "CONNECTING":
            dpg.configure_item(
                self.elements[Element.CONNECT_BUTTON], label="Connecting...", enabled=False)
            return
        elif next_state == "CONNECTED":
            dpg.configure_item(
                self.elements[Element.CONNECT_BUTTON], label="Connected!", enabled=False)
            return
        elif next_state == "DISCONNECTED":
            dpg.configure_item(
                self.elements[Element.CONNECT_BUTTON], label="Connect", enabled=True)
            return

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

    def print_terminal(self, text: str) -> None:
        value = dpg.get_value(self.elements[Element.TERMINAL_WINDOW_INPUT])
        dpg.set_value(
            self.elements[Element.TERMINAL_WINDOW_INPUT], text + '\n' + value)

    def on_clear_console(self, *args) -> None:
        dpg.set_value(
            self.elements[Element.TERMINAL_WINDOW_INPUT], "Cleared.")

    def add_listeners(self) -> None:
        self.on_clear_console_clicked.add_listener(self.on_clear_console)

    def create_owo_suit_ip_address_input(self):
        owo_ip = self.config.get_by_key("owo_ip") or ""
        dpg.add_text("OWO Suit IP Address")
        self.elements[Element.IP_ADDRESS_INPUT] = dpg.add_input_text(default_value=owo_ip,
                                                                     width=-1, callback=self.handle_input_change)

    def create_detect_address_checkbox(self):
        should_detect_ip = self.config.get_by_key("should_detect_ip")
        self.elements[Element.DETECT_IP_ADDRESS_CHECKBOX] = dpg.add_checkbox(
            label="Automatically Detect IP Address", default_value=should_detect_ip, callback=self.handle_input_change)

    def create_server_port_input(self):
        server_port = self.config.get_by_key("server_port") or 9001
        dpg.add_text("Server Port Number")
        self.elements[Element.SERVER_PORT_NUMBER_INPUT] = dpg.add_input_int(default_value=server_port,
                                                                            width=-1, callback=self.handle_input_change)

    def create_frequency_slider(self):
        frequency = self.config.get_by_key("frequency")
        dpg.add_text("Frequency Settings")
        self.elements[Element.FREQUENCY_SETTING_SLIDER] = dpg.add_slider_int(
            min_value=0,
            max_value=100,
            width=-1,
            default_value=frequency,
            callback=self.handle_input_change
        )

    def create_intensity_settings(self):
        dpg.add_text("Intensity Settings")
        for element, label in self.element_labels.items():
            self.create_intensity_slider(element, label)

    def create_intensity_slider(self, element: Element, label: str):
        intensities_map = self.element_to_config_key.get("intensities")
        config_key = intensities_map.get(element)
        intensities = self.config.get_by_key("intensities")
        default_value = intensities.get(config_key) or 0
        self.elements[element] = dpg.add_slider_int(default_value=default_value, min_value=0, width=-120,
                                                    max_value=100, label=label, callback=self.handle_input_change)

    def create_logs_output(self):
        dpg.add_text("Logs")
        self.elements[Element.TERMINAL_WINDOW_INPUT] = dpg.add_input_text(
            multiline=True, readonly=True, height=90, width=-1)

    def create_button_group(self):
        with dpg.group(horizontal=True):
            self.elements[Element.CONNECT_BUTTON] = dpg.add_button(label="Connect",
                                                                   callback=self.handle_connect_callback)
            self.elements[Element.SAVE_SETTINGS_BUTTON] = dpg.add_button(label="Save Settings",
                                                                         callback=self.handle_save_settings_callback)
            self.elements[Element.CLEAR_CONSOLE_BUTTON] = dpg.add_button(label="Clear Console",
                                                                         callback=self.handle_clear_console_callback)
            self.elements[Element.TOGGLES_INTERACTIONS_BUTTON] = dpg.add_button(label="Toggle Interactions",
                                                                                callback=self.handle_toggle_interactions_callback)

    def create_connect_startup_checkbox(self):
        should_connect_on_startup = self.config.get_by_key(
            "should_connect_on_startup"
        )
        self.elements[Element.CONNECT_ON_STARTUP_CHECKBOX] = dpg.add_checkbox(
            default_value=should_connect_on_startup,
            label="Automatically Connect on Startup",
            callback=self.handle_input_change
        )

    def create_footer(self):
        with dpg.group(width=-1):
            self.elements[Element.CONTRIBUTE_BUTTON] = dpg.add_button(
                label="\t\t\t\t  Created by Shadoki.\nThis application is not affiliated with VRChat or OWO.\n\t\t\t\t  Want to contribute?",
                width=-1,
                callback=self.handle_contribute_callback
            )

    def validate_connect_on_startup(self):
        should_connect_on_startup = self.config.get_by_key(
            "should_connect_on_startup"
        )
        if should_connect_on_startup:
            self.handle_connect_callback(Element.CONNECT_BUTTON, None)

    def init(self):
        dpg.create_context()
        with dpg.window(tag="MAIN_WINDOW"):
            dpg.add_spacer(height=20)
            handle_centered_image = self.create_centered_image(
                "logo", self.logo_path)
            dpg.add_spacer(height=20)
            self.create_owo_suit_ip_address_input()
            self.create_detect_address_checkbox()
            dpg.add_spacer(height=20)
            self.create_server_port_input()
            dpg.add_spacer(height=20)
            self.create_frequency_slider()
            dpg.add_spacer(height=20)
            self.create_intensity_settings()
            dpg.add_spacer(height=20)
            self.create_logs_output()
            dpg.add_spacer(height=20)
            self.create_button_group()
            dpg.add_spacer(height=20)
            self.create_connect_startup_checkbox()
            dpg.add_spacer(height=20)
            self.create_footer()

        self.add_listeners()
        dpg.create_viewport(title='VRChat OWO Suit',
                            width=self.window_width, height=self.window_height)
        dpg.set_viewport_resize_callback(handle_centered_image)
        self.ids_to_elements = {
            value: key for key, value in self.elements.items()}
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("MAIN_WINDOW", True)

    def run(self):
        self.validate_connect_on_startup()
        dpg.start_dearpygui()

    def cleanup(self):
        dpg.destroy_context()
