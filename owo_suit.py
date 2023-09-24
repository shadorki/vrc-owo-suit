# pyright: reportMissingImports=false
from pythonosc import dispatcher
from event import Event
from gui import Gui
import params
import time
import clr
from System.Reflection import Assembly
Assembly.UnsafeLoadFrom('./owo/OWO.dll')
from OWOGame import OWO, Sensation, SensationsFactory, Muscle, MicroSensation, ConnectionState


class OWOSuit:
    def __init__(self, owo_ip: str, frequency: int, intensity: int, gui: Gui):
        self.owo_ip: str = owo_ip
        self.intensity: int = intensity
        self.frequency: int = frequency
        self.gui = gui
        self.active_muscles: set = set()
        self.touch_sensation: MicroSensation = SensationsFactory.Create(
            self.frequency, .1, self.intensity, 0, 0, 0)
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
        self.is_connecting = False
        self.on_connection_state_change = Event()

    def ping_muscles(self) -> None:
        for address, muscle in self.osc_parameters.items():
            print(f'Pinging {address}')
            self.send_sensation(muscle)
            time.sleep(.1)

    def watch(self) -> None:
        while True:
            if len(self.active_muscles) > 0:
                OWO.Send(self.touch_sensation, list(self.active_muscles))
                print("\033[SSending sensation to: ", self.active_muscles)
            time.sleep(.1)

    def on_collission_enter(self, address: str, *args) -> None:
        if address == "/avatar/parameters/owo_intensity":
            self.intensity = int(args[0]*100)
            print("Set intensity to: "+str(self.intensity))
            self.touch_sensation = SensationsFactory.Create(
                self.frequency, 10, self.intensity, 0, 0, 0)
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
        if self.owo_ip != "":
            OWO.Connect(self.owo_ip)
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
                f'Failed to connect to suit, trying again... IP: {self.owo_ip or "N/A"}')
            print(
                f'Failed to connect to suit, trying again... IP: {self.owo_ip or "N/A"}')
            ok = self.connect()
            time.sleep(1)
        self.is_connecting = False
        self.dispatch_connection_state_change()

    def init(self) -> None:
        self.gui.on_connect_clicked.add_listener(self.retry_connect)
        self.on_connection_state_change.add_listener(self.gui.handle_connecting_state_change)
