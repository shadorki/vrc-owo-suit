import json


class Config:
    def __init__(self, server_port: int, owo_ip: str):
        self.server_port = server_port
        self.owo_ip = owo_ip


def get() -> Config:
    server_port = 9001
    owo_ip = ""
    try:
        f = open('./vrc-owo-suit.config.json')
        data = json.load(f)
        f.close()
        if ("server_port" in data and type(data['server_port']) is int):
            print(f"Using server_port {data['server_port']}.")
            server_port = data['server_port']
        if ("owo_ip" in data and type(data['owo_ip']) is str):
            print(f"Using owo_ip {data['owo_ip']}.")
            owo_ip = data['owo_ip']
    except:
        print("Config file not found, using default settings")
    finally:
        return Config(server_port, owo_ip)
