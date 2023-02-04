import asyncio
import threading
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from owo_suit import OWOSuit
import config

try:
    print("Starting OWO Suit...")
    c = config.get()
    owo_suit = OWOSuit(c.owo_ip)
    owo_suit.init()
    dispatcher = Dispatcher()
    owo_suit.map_parameters(dispatcher)
    osc_server = ThreadingOSCUDPServer(
        ("127.0.0.1", c.server_port), dispatcher, asyncio.new_event_loop())

    threading.Thread(target=lambda: osc_server.serve_forever(2),
                     daemon=True).start()
    threading.Thread(target=owo_suit.watch,
                     daemon=True).start()
    input("Press any key to exit\n")
except KeyboardInterrupt:
    print("Shutting Down...\n")
except OSError:
    pass
