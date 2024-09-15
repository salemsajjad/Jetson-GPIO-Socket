from Jetson.GPIO import gpio_pin_data
import Jetson.GPIO as GPIO
import socket
import struct
import time

# Set the GPIO mode to BOARD
GPIO.setmode(GPIO.BOARD)
list = [7, 11, 13, 15, 19, 21, 23, 29, 31, 33, 35, 37, 12, 16, 18, 22, 24, 26, 32, 36, 38, 40]
for i in list:
    GPIO_pin_No = i 

    # Set pin 12 as an output
    GPIO.setup(GPIO_pin_No, GPIO.OUT, initial=GPIO.LOW)

    # Set the value of pin 12 to HIGH
    GPIO.output(GPIO_pin_No, GPIO.LOW)

# Define constants for data structure
PACKET_BUFFER_SEND_SIZE = 4 * 3 + 4 * 4 #28 Bytes
PACKET_BUFFER_RECV_SIZE = 3 * 4 + 4 + 4 * 4 #32 Bytes

# Variable Definition
IS_LED_FLASH_ON = [0, 0, 0]
th_isMustSetOutPut = 0,
set_OUTPUT_GPIO_PORT_VALUE = [0, 0, 0, 0]
INPUT_GPIO_PORT_VALUE = [0, 0, 0]
get_OUTPUT_GPIO_PORT_VALUE =[0, 0, 0, 0]

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific port and IP address
server_socket.bind(('127.0.0.1', 14064))  # Replace with your desired IP and port

# Listen for incoming connections
server_socket.listen()

print("Waiting for connections...")

while True:
    try:
        # Accept an incoming connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        while True:
            try:
                # Receive data from the client
                data = client_socket.recv(PACKET_BUFFER_RECV_SIZE)

                # Unpack the received data using struct.unpack
                recv_data = struct.unpack('<8I', data)

                th_isMustSetOutPut = recv_data[3]
                set_OUTPUT_GPIO_PORT_VALUE = recv_data[4:]

                print(f"isMustOutput:{th_isMustSetOutPut}")
                print(f"output1:{set_OUTPUT_GPIO_PORT_VALUE[0]}")
                print(f"output2:{set_OUTPUT_GPIO_PORT_VALUE[1]}")
                print(f"output3:{set_OUTPUT_GPIO_PORT_VALUE[2]}")
                print(f"output4:{set_OUTPUT_GPIO_PORT_VALUE[3]}")

                # Process the data to set GPIOs
                if(th_isMustSetOutPut == 1):
                    GPIO.output(23, set_OUTPUT_GPIO_PORT_VALUE[0])
                    GPIO.output(22, set_OUTPUT_GPIO_PORT_VALUE[1])
                    GPIO.output(21, set_OUTPUT_GPIO_PORT_VALUE[2])
                    GPIO.output(19, set_OUTPUT_GPIO_PORT_VALUE[3])

                get_OUTPUT_GPIO_PORT_VALUE = set_OUTPUT_GPIO_PORT_VALUE[:]
                # Process the received data and send a response
                # ... (your data processing logic here)

                # Prepare the response data
                response_data = struct.pack(
                    "<7I",
                    INPUT_GPIO_PORT_VALUE[0],
                    INPUT_GPIO_PORT_VALUE[1],
                    INPUT_GPIO_PORT_VALUE[2],
                    get_OUTPUT_GPIO_PORT_VALUE[0],
                    get_OUTPUT_GPIO_PORT_VALUE[1],
                    get_OUTPUT_GPIO_PORT_VALUE[2],
                    get_OUTPUT_GPIO_PORT_VALUE[3]
                )

                # Send the response data to the client
                client_socket.sendall(response_data)

                # Add a delay if needed
                time.sleep(0.1)  # Adjust the delay as necessary

            except Exception as e:
                print(f"Error receiving data: {e}")
                break  # Exit the inner loop on socket errors

        client_socket.close()
        print("Client disconnected")

    except Exception() as e:
        print(f"Error accepting connection: {e}")
        time.sleep(5)  # Wait for 5 seconds before retrying

# Close the server socket when finished
server_socket.close()