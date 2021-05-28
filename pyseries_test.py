import serial

serialPort = serial.Serial(
    port="/dev/ttyACM0", baudrate=9600, bytesize=8, timeout=2)

print(serialPort.readline())