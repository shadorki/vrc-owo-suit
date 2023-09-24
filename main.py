import asyncio
import threading
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from owo_suit import OWOSuit
from config import Config
from gui import Gui

gui = None
try:
    cfg = Config()
    cfg.init()
    gui = Gui(config=cfg, window_width = 550, window_height = 1000, logo_path="./img/logo.png")
    gui.init()
    owo_suit = OWOSuit(cfg.owo_ip, cfg.frequency, cfg.intensity, gui=gui)
    owo_suit.init()
    dispatcher = Dispatcher()
    owo_suit.map_parameters(dispatcher)
    osc_server = ThreadingOSCUDPServer(
        ("127.0.0.1", cfg.server_port), dispatcher, asyncio.new_event_loop())
    threading.Thread(target=lambda: osc_server.serve_forever(2),
                     daemon=True).start()
    threading.Thread(target=owo_suit.watch,
                     daemon=True).start()
    gui.run()
except KeyboardInterrupt:
    print("Shutting Down...\n")
except OSError:
    pass
finally:
    if gui is not None:
        gui.cleanup()

