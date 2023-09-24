import json


class Config:
    def __init__(self):
        self.server_port = 9001
        self.owo_ip = ""
        self.intensity = 10
        self.frequency = 100
    
    def init(self):
        try:
            f = open('./vrc-owo-suit.config.json')
            data = json.load(f)
            f.close()
            if ("server_port" in data and type(data['server_port']) is int):
                print(f"Using server_port {data['server_port']}.")
                self.server_port = data['server_port']
            if ("owo_ip" in data and type(data['owo_ip']) is str):
                print(f"Using owo_ip {data['owo_ip']}.")
                self.owo_ip = data['owo_ip']
            if ("intensity" in data and type(data['intensity']) is int):
                print(f"Using intensity {data['intensity']}.")
                self.intensity = data['intensity']
            if ("frequency" in data and type(data['frequency']) is int):
                print(f"Using frequency {data['frequency']}.")
                self.frequency = data['frequency']
        except:
            print("Config file not found, using default settings")