# pyright: reportMissingImports=false
from pythonosc import dispatcher
from event import Event
from config import Config
from gui import Gui
import params
import time
import clr
from System.Reflection import Assembly
Assembly.UnsafeLoadFrom('./owo/OWO.dll')
from OWOGame import OWO, SensationsFactory, Muscle, ConnectionState


class OWOSuit:
    def __init__(self, config: Config, gui: Gui):
        self.config = config
        self.gui = gui
        self.active_muscles: set = set()
        self.osc_parameters: dict[str, Muscle] = {
            params.owo_suit_Pectoral_R: Muscle.Pectoral_R,
            params.owo_suit_Pectoral_L: Muscle.Pectoral_L,
            params.owo_suit_Abdominal_R: Muscle.Abdominal_R,
            params.owo_suit_Abdominal_L: Muscle.Abdominal_L,
            params.owo_suit_Arm_R: Muscle.Arm_R,
            params.owo_suit_Arm_L: Muscle.Arm_L,
            params.owo_suit_Dorsal_R: Muscle.Dorsal_R,
            params.owo_suit_Dorsal_L: Muscle.Dorsal_L,
            params.owo_suit_Lumbar_R: Muscle.Lumbar_R,
            params.owo_suit_Lumbar_L: Muscle.Lumbar_L,
        }
        self.muscles_to_parameters: dict[Muscle, str] = {
            value: key for key, value in self.osc_parameters.items()}
        self.is_connecting = False
        self.on_connection_state_change = Event()

    def create_sensation(self, parameter: str):
        frequency = self.config.get_by_key("frequency") or 50
        intensities = self.config.get_by_key("intensities")
        intensity = getattr(intensities, parameter, 0)
        return SensationsFactory.Create(
            frequency, .1, intensity, 0, 0, 0)

    def watch(self) -> None:
        while True:
            if len(self.active_muscles) > 0:
                for muscle in self.active_muscles:
                    parameter = self.muscles_to_parameters.get(muscle)
                    sensation = self.create_sensation(parameter)
                    OWO.Send(sensation, muscle)
                    print("\033[SSending sensation to: ", parameter)
            time.sleep(.1)

    def on_collission_enter(self, address: str, *args) -> None:
        if not address in self.osc_parameters:
            return
        if len(args) != 1:
            return
        was_entered: bool = args[0]
        if type(was_entered) != bool:
            return
        muscle = self.osc_parameters[address]
        if was_entered:
            self.active_muscles.add(muscle)
        else:
            self.active_muscles.remove(muscle)

    def map_parameters(self, dispatcher: dispatcher.Dispatcher) -> None:
        dispatcher.set_default_handler(self.on_collission_enter)

    def connect(self) -> bool:
        owo_ip = self.config.get_by_key("owo_ip")
        if type(owo_ip) is str and owo_ip != "":
            OWO.Connect(owo_ip)
            if self.is_connected():
                return True
        OWO.AutoConnect()
        return self.is_connected()

    def is_connected(self) -> bool:
        return OWO.ConnectionState == ConnectionState.Connected

    def dispatch_connection_state_change(self) -> None:
        if self.is_connecting:
            self.on_connection_state_change.dispatch('CONNECTING')
            return
        if self.is_connected():
            self.on_connection_state_change.dispatch('CONNECTED')
            return
        self.on_connection_state_change.dispatch('DISCONNECTED')

    def retry_connect(self, *args) -> None:
        if self.is_connecting:
            return
        self.is_connecting = True
        self.dispatch_connection_state_change()
        ok = self.connect()
        while not ok:
            self.gui.print_terminal(
                "Failed to connect to suit, trying again...")
            print(
                "Failed to connect to suit, trying again...")
            ok = self.connect()
            time.sleep(1)
        self.is_connecting = False
        self.dispatch_connection_state_change()

    def init(self) -> None:
        self.gui.on_connect_clicked.add_listener(self.retry_connect)
        self.on_connection_state_change.add_listener(
            self.gui.handle_connecting_state_change)
