from smbus2 import SMBus
from mlx90614 import MLX90614
# import random


def readoC():
    bus = SMBus(1)

    sensor = MLX90614(bus, address=0x5A)

    amb = sensor.get_ambient()
    obj = sensor.get_object_2()

    print(amb)
    print(obj)

    bus.close()

    return amb, obj
