# pyright: reportMissingImports=false
from pythonosc import dispatcher
import time
import clr
from System.Reflection import Assembly
Assembly.UnsafeLoadFrom('./owo/OWO.dll')
from OWOGame import OWO, Sensation, SensationsFactory, Muscle, MicroSensation, ConnectionState

# Sensations that are predefined
# 'Ball', 'GunRecoil', 'Bleed', 'Insvects', 'Wind', 'Dart', 'MachineGunRecoil', 'Punch', 'DaggerEntry', 'DaggerMovement', 'FastDriving', 'IdleSpeed', 'InsectBites', 'ShotEntry', 'ShotExit', 'Shot', 'Dagger', 'Hug', 'HeartBeat'

# Muscle Properties
# 'Pectoral_R', 'Pectoral_L', 'Abdominal_R', 'Abdominal_L', 'Arm_R', 'Arm_L', 'Dorsal_R', 'Dorsal_L', 'Lumbar_R', 'Lumbar_L', 'AllMuscles', 'BackMuscles', 'FrontMuscles', 'FrontMusclesWithoutArms', 'Arms', 'Dorsals', 'Pectorals', 'Abdominals'


class OWOSuit:
    def __init__(self, owo_ip: str, frequency: int, intensity: int):
        self.owo_ip: str = owo_ip
        self.intensity: int = intensity
        self.frequency: int = frequency
        self.active_muscles: set = set()
        self.touch_sensation: MicroSensation = SensationsFactory.Create(
            self.frequency, .1, self.intensity, 0, 0, 0)
        self.osc_parameters: dict[str, Muscle] = {
            "/avatar/parameters/owo_suit_Pectoral_R": Muscle.Pectoral_R,
            "/avatar/parameters/owo_suit_Pectoral_L": Muscle.Pectoral_L,
            "/avatar/parameters/owo_suit_Abdominal_R": Muscle.Abdominal_R,
            "/avatar/parameters/owo_suit_Abdominal_L": Muscle.Abdominal_L,
            "/avatar/parameters/owo_suit_Arm_R": Muscle.Arm_R,
            "/avatar/parameters/owo_suit_Arm_L": Muscle.Arm_L,
            "/avatar/parameters/owo_suit_Dorsal_R": Muscle.Dorsal_R,
            "/avatar/parameters/owo_suit_Dorsal_L": Muscle.Dorsal_L,
            "/avatar/parameters/owo_suit_Lumbar_R": Muscle.Lumbar_R,
            "/avatar/parameters/owo_suit_Lumbar_L": Muscle.Lumbar_L,
        }

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

    def retry_connect(self) -> None:
        ok = self.connect()
        while not ok:
            print(
                f'Failed to connect to suit, trying again... IP: {self.owo_ip or "N/A"}')
            ok = self.connect()
            time.sleep(1)