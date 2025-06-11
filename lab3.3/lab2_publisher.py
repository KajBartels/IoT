import argparse
import asyncio
import logging
import struct
import zmq
import numpy
from bleak import BleakClient, BleakScanner

BLE_UUID_ACCEL_SENSOR_DATA = "4664E7A1-5A13-BFFF-4636-7D0A4B16496C"
exit_flag = False

logger = logging.getLogger(__name__)

def send_array(socket: zmq.Socket, array: numpy.ndarray, flags=0, copy=True, track=False):
    md = {
        "shape": array.shape,
        "dtype": str(array.dtype),
    }
    socket.send_json(md, flags | zmq.SNDMORE)
    return socket.send(array, flags, copy=copy, track=track)

def notification_handler_factory(socket):
    def notification_handler(sender, data):
        x, y, z = struct.unpack("fff", data)
        # Round to 2 decimal places
        arr = numpy.array([round(x, 2), round(y, 2), round(z, 2)], dtype=numpy.float32)
        send_array(socket, arr)
    return notification_handler

async def main(args: argparse.Namespace):
    device = await BleakScanner.find_device_by_name(
        args.name, cb=dict(use_bdaddr=args.macos_use_bdaddr))
    if device is None:
        logger.error("could not find device with name '%s'", args.name)
        return

    ctx = zmq.Context()
    s = ctx.socket(zmq.XPUB)
    s.bind(args.url)
    print("Waiting for subscriber")
    s.recv()
    print("Sending arrays...")

    async with BleakClient(
        device,
        services=args.services,
    ) as client:
        logger.info("connected")
        await client.start_notify(
            BLE_UUID_ACCEL_SENSOR_DATA,
            notification_handler_factory(s)
        )
        while not exit_flag:
            await asyncio.sleep(1.0)
            print(".")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    device_group = parser.add_mutually_exclusive_group(required=True)
    device_group.add_argument("--name", metavar="<name>", help="the name of the bluetooth device to connect to")
    device_group.add_argument("--address", metavar="<address>", help="the address of the bluetooth device to connect to")

    parser.add_argument("--macos-use-bdaddr", action="store_true", help="when true use Bluetooth address instead of UUID on macOS")
    parser.add_argument("--services", nargs="+", metavar="<uuid>", help="if provided, only enumerate matching service(s)")
    parser.add_argument("-d", "--debug", action="store_true", help="sets the log level to debug")
    parser.add_argument("--url", default="tcp://127.0.0.1:5555", help="ZeroMQ URL to bind to")

    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

    asyncio.run(main(args))
