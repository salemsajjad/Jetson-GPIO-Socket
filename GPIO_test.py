import Jetson.GPIO as GPIO
from Jetson.GPIO import gpio_pin_data
import time

# Set the GPIO mode to BOARD
GPIO.setmode(GPIO.BOARD)
list = [7, 11, 13, 15, 19, 21, 23, 29, 31, 33, 35, 37, 12, 16, 18, 22, 24, 26, 32, 36, 38, 40]
for i in list:
    GPIO_pin_No = i # 11th pin on the developer board.

    # Set pin 12 as an output
    GPIO.setup(GPIO_pin_No, GPIO.OUT, initial=GPIO.LOW)

    # Set the value of pin 12 to HIGH
    GPIO.output(GPIO_pin_No, GPIO.LOW)

while True:
    # for i in list:
    #     GPIO_pin_No = i
    #     GPIO.output(GPIO_pin_No, GPIO.HIGH)
    # print("GPIO is High")
    # time.sleep(5)
    # for i in list:
    #     GPIO_pin_No = i
    #     GPIO.output(GPIO_pin_No, GPIO.LOW)
    # print("GPIO is LOW")
    # time.sleep(5)
    GPIO.output(22, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(22, GPIO.LOW)
    time.sleep(5)


