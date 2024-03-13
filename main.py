import asyncio
import threading
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from owo_suit import OWOSuit
from config import Config
from gui import Gui, GuiLogger
import os
import logging

log = logging.getLogger("vrc-owo-suit")
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
console_handler.setLevel(logging.WARNING)
log.addHandler(console_handler)
cfg = Config(log.getChild("Config"))
logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './img/logo.png'))
gui = Gui(config=cfg, window_width=550, window_height=1000, logo_path=logo_path, log=log.getChild("GUI"))
gui_logger = GuiLogger(gui)
gui_logger.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
log.addHandler(gui_logger)
try:
    cfg.init()
    gui.init()
    owo_suit = OWOSuit(config=cfg, gui=gui)
    owo_suit.init()
    dispatcher = Dispatcher()
    owo_suit.map_parameters(dispatcher)

    server_port = cfg.get_by_key("server_port")

    osc_server = ThreadingOSCUDPServer(
        ("127.0.0.1", server_port), dispatcher, asyncio.new_event_loop())
    threading.Thread(target=lambda: osc_server.serve_forever(2),
                     daemon=True).start()
    threading.Thread(target=owo_suit.watch,
                     daemon=True).start()
    gui.run()
except KeyboardInterrupt:
    log.warning("Shutting Down...\n")
except OSError as e:
    log.error("The OSC port (UDP) is already taken. Please change the port or close the other application listening to "
              "that port. If you want to run multiple OSC applications, consider running VOR "
              "(https://github.com/SutekhVRC/VOR/tree/main)")
    log.error("Got OSError during startup: %s" % e.strerror)
    gui.init()  # Make sure the GUI is initialized, even if it had an error before starting the GUI
    gui.run()
finally:
    if gui is not None:
        gui.cleanup()
