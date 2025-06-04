import serial
import time


serial = serial.Serial('/dev/ttyACM2', 9600)


def led_on_off(status):
    user_input = input("command > ")
    if user_input =="on":
        print("LED on")
        serial.write(b'N')
        led_on_off("LED on")
    elif user_input =="off":
        print("LED off")
        serial.write(b'F')
        led_on_off("LED off")
    elif user_input =="blink":
        print("LED blink")
        serial.write(b'B')
        led_on_off("LED blink")
    elif user_input =="status":
        print(status)
        led_on_off(status)
    else:
        print("Invalid input. Type on, off, blink or status")
        led_on_off(status)

time.sleep(2)

led_on_off("LED off")