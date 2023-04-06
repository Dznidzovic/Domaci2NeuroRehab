import serial
import time



class SerialComunication:
    
    def populateByteArrayWithAscii(self,messageString):
        byteMessage = bytearray()
        for i in messageString:
            byteMessage.append(ord(i))
        return byteMessage


    def activate_channel(self, value):
        message_string = ">SC;xyz<"
        bytemessage = self.populateByteArrayWithAscii(message_string)
        bytemessage[4] = value
        bytemessage[5] = value
        bytemessage[6] = value
        self.port.write(bytemessage)
        time.sleep(1)

    def turn_simulator_on(self):
        message_string = '>ON<'
        bytemessage = self.populateByteArrayWithAscii(message_string)
        self.port.write(bytemessage)
        time.sleep(1)

    def turn_simulator_off(self):
        message_string = '>OFF<'
        bytemessage = self.populateByteArrayWithAscii(message_string)
        self.port.write(bytemessage)
        time.sleep(1)

    def convert_to_signed_int32(self, b1, b2, b3):
        vref = 4.5
        gain = 24

        uint32val = (b1<<16)+(b2<<8)+b3

        if uint32val >= (1 << 23):
            int32val = uint32val - (1<<24)
        else:
            int32val = uint32val

        scaleFactor = (vref/(2**23 - 1))/gain
        to_microV = 10**(6)
        return int32val*scaleFactor*to_microV
    
    def convert_gyro_x(self, b1, b2):
        return (b1 << 8) + b2

    def convert_data(self, row):
        converted_row = []

        for i in range(0, 72):
            if(i%3 == 0):
                converted_row.append(self.convert_to_signed_int32(row[i], row[i+1], row[i+2]))

        converted_row.append(self.convert_gyro_x(row[73], row[74]))

        return converted_row

    def read_line(self):
        row = []
        if self.port.read() == b'>':
            data = self.port.read()
            while data != b'<':
                row.append(ord(data))
                data = self.port.read()
                
            if len(row) == 81:
                return self.convert_data(row)


    def __init__(self) -> None:
        self.port = serial.Serial("COM3", 921600, timeout=1, parity=serial.PARITY_EVEN, rtscts=1)
        self.data_history = []

    def __del__(self):
        self.turn_simulator_off()
        self.port.close()

