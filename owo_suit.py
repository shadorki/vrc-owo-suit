# pyright: reportMissingImports=false
from pythonosc import dispatcher
import time
import clr
clr.AddReference('./owo/OWO')
from OWOGame import OWO, Sensation, SensationsFactory, Muscle, MicroSensation, ConnectionState

# Sensations that are predefined
# 'Ball', 'GunRecoil', 'Bleed', 'Insvects', 'Wind', 'Dart', 'MachineGunRecoil', 'Punch', 'DaggerEntry', 'DaggerMovement', 'FastDriving', 'IdleSpeed', 'InsectBites', 'ShotEntry', 'ShotExit', 'Shot', 'Dagger', 'Hug', 'HeartBeat'

# Muscle Properties
# 'Pectoral_R', 'Pectoral_L', 'Abdominal_R', 'Abdominal_L', 'Arm_R', 'Arm_L', 'Dorsal_R', 'Dorsal_L', 'Lumbar_R', 'Lumbar_L', 'AllMuscles', 'BackMuscles', 'FrontMuscles', 'FrontMusclesWithoutArms', 'Arms', 'Dorsals', 'Pectorals', 'Abdominals'


class OWOSuit:
    def __init__(self, owo_ip: str):
        self.owo_ip: str = owo_ip
        self.active_muscles: set = set()
        self.touch_sensation: MicroSensation = SensationsFactory.Create(
            100, 20, 25, 0, 0, 0)
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
            else:
                OWO.Stop()
            time.sleep(.3)

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
        if self.owo_ip != "":
            OWO.Connect(self.owo_ip)
            if OWO.IsConnected:
                return True
        OWO.AutoConnect()
        return OWO.ConnectionState == ConnectionState.Connected

    def init(self) -> None:
        ok = self.connect()
        while not ok:
            print(
                f'Failed to connect to suit, trying again... IP: {self.owo_ip or "N/A"}')
            ok = self.connect()
            time.sleep(1)
        print("Successfully connected to OWO suit!")
