# pyright: reportMissingImports=false
from pythonosc import dispatcher
import time
import clr
clr.AddReference('./owo/OWO')
from OWOHaptic import OWO, Sensation, Muscle

# Sensations that are predefined
# 'Ball', 'GunRecoil', 'Bleed', 'Insvects', 'Wind', 'Dart', 'MachineGunRecoil', 'Punch', 'DaggerEntry', 'DaggerMovement', 'FastDriving', 'IdleSpeed', 'InsectBites', 'ShotEntry', 'ShotExit', 'Shot', 'Dagger', 'Hug', 'HeartBeat'

# Muscle Properties
# 'Pectoral_R', 'Pectoral_L', 'Abdominal_R', 'Abdominal_L', 'Arm_R', 'Arm_L', 'Dorsal_R', 'Dorsal_L', 'Lumbar_R', 'Lumbar_L', 'AllMuscles', 'BackMuscles', 'FrontMuscles', 'FrontMusclesWithoutArms', 'Arms', 'Dorsals', 'Pectorals', 'Abdominals'

osc_parameters = {
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


def ping_muscles() -> None:
    for address, muscle in osc_parameters.items():
        print(f'Pinging {address}')
        send_sensation(muscle)
        time.sleep(1)


def send_sensation(muscle: Muscle) -> None:
    print(f"Sending Sensation to {muscle}")
    OWO.Send(Sensation.Ball, muscle)


def on_collission_enter(address: str, *args) -> None:
    if not address in osc_parameters:
        return
    muscle = osc_parameters[address]
    send_sensation(muscle)


def map_parameters(dispatcher: dispatcher.Dispatcher) -> None:
    dispatcher.set_default_handler(on_collission_enter)


def connect(owo_ip: str) -> bool:
    if owo_ip != "":
        OWO.Connect(owo_ip)
        if OWO.IsConnected:
            return True
    OWO.AutoConnect()
    return OWO.IsConnected


def init(owo_ip: str) -> None:
    ok = connect(owo_ip)
    while not ok:
        print(
            f'Failed to connect to suit, trying again... IP: {owo_ip or "N/A"}')
        ok = connect(owo_ip)
        time.sleep(1)
    print("Successfully connected to OWO suit!")
