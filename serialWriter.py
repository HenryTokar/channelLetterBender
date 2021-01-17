#this file pushes all of the command information to the arduino

# import serial
# import time
#
#
# #this line is for serial over GPIO
# port = "/dev/ttyS0"
#
# #arduino = serial.Serial(port, 9600, timeout=5)
# arduino = serial.Serial('com3', 9600, timeout=5)
#
#
# def writeDataToArduino(angle, length):
#     arduino.write(str.encode("go"))
#
#
#
#
#
#     return 777
#
# #while (1):
# #    writeDataToArduino(90, 90)
#
#
# writeDataToArduino(90, 90)
import serial, time

def init():
    global arduino
    arduino = serial.Serial('COM4', 9600, timeout=.1)
    time.sleep(1) #give the connection a second to settle
    return arduino


def prompt(arduino):
    while True:
        userPrompt = input("number:")
        arduino.write(userPrompt.encode())

def motorDirection(motor1Direction, motor2Direction, arduino):
    if motor1Direction == "CW":
        arduino.write("0".encode())
    else:
        arduino.write("1".encode())

    if motor2Direction == "CW":
        arduino.write("2".encode())
    else:
        arduino.write("3".encode())



def motorRun(revolutions, arduino):
    pulsesPerRevolution = 400

    numberOfPulsesRequired = revolutions * pulsesPerRevolution

    pulseCounter = 0

    while pulseCounter < numberOfPulsesRequired:
        arduino.write("4".encode())
        time.sleep(0.001)
        arduino.write("5".encode())
        time.sleep(0.001)

        if pulseCounter % 200 == 0:
            motorDirection("CW", "CCW", arduino)
        if pulseCounter % 300 == 0:
            motorDirection("CCW", "CW", arduino)

        pulseCounter = pulseCounter + 1




def motorTest(arduino):
    while True:
        userPrompt = input("number:")

        intNumber = int(userPrompt)
        counter = 0

        while counter < intNumber:
            arduino.write("LOW".encode())
            time.sleep(2)
            arduino.write("3".encode())
            time.sleep(0.025)


            counter = counter + 1

        arduino.write(userPrompt.encode())


# while True:
#     arduino.write(testString.encode('utf-8'))
#     time.sleep(5)
#     data = arduino.readline()
#     if data:
#         time.sleep(2)
#         print(data.decode('utf-8'))

prompt(init())

#motorRun(20, init())