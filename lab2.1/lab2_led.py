import argparse
import asyncio
import struct

from bleak import BleakClient
from bleak import BleakScanner
from bleak import discover

ARDUINO_LOCAL_NAME = "BLE-AR65"

LED_UUID = "19b10001-e8f2-537e-4f6c-d104768a1214"

on_value = bytearray([0x01])
off_value = bytearray([0x00])

async def find_ble_device(args: argparse.Namespace):
    print("scanning for 5 seconds, please wait...")

    devices = await BleakScanner.discover(
        return_adv=True, cb=dict(use_bdaddr=args.macos_use_bdaddr)
    )

    for d, a in devices.values():
        if d.name == ARDUINO_LOCAL_NAME:
            print(f"Gevonden: {d.name} op adres {d.address}")
            return (d, a)

    return (None, None)



async def runmain(d, a):
    async with BleakClient(d.address) as client:
        svcs = await client.get_services()

        for i in range(10):
            print(f"Aan ({i+1})")
            await client.write_gatt_char(LED_UUID, on_value)
            await asyncio.sleep(1)

            print(f"Uit ({i+1})")
            await client.write_gatt_char(LED_UUID, off_value)
            await asyncio.sleep(1)


# your code here to control the led. 
# use await statements and the bleak read_gatt_char and write_gatt_char
# functions of Bleak 
#flash the LED 10 times with one second in between using an asynchronous sleep 



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--macos-use-bdaddr",
        action="store_true",
        help="when true use Bluetooth address instead of UUID on macOS",
    )


    args = parser.parse_args()
    (d,a) = asyncio.run(find_ble_device(args))
    if (d,a) != (None, None):
      asyncio.run(runmain(d,a))
    else:
        print("arduino not found")
