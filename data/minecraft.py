from mcrcon import MCRcon

mc = MCRcon("192.168.0.186", "12345a", 25575)


def add_player(name):
    mc.connect()
    mc.command(f"/whitelist add {name}")
    mc.disconnect()
    print(f"ok - for {name} ")

