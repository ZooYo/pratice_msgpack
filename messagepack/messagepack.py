import sys

class TypeString:
    def __init__(self, string_data):
        self.string_data = string_data
        if len(string_data) < 32:
            self.data_description = int('10100000', 2)
            self.description_length_space = 0
        elif len(string_data) < 256:
            self.data_description = int('0xd9', 16).to_bytes(1, byteorder="big")
            self.description_length_space = 1
        elif len(string_data) < 65536:
            self.data_description = int('0xda', 16).to_bytes(1, byteorder="big")
            self.description_length_space = 2
        elif len(string_data) < 4294967295:
            self.data_description = int('0xdb', 16).to_bytes(1, byteorder="big")
            self.description_length_space = 4
        else:
            raise Exception("too large string")

    def pack(self):
        if self.description_length_space == 0:
            byte_description = (self.data_description + len(self.string_data)).to_bytes(1, byteorder="big")
        else:
            byte_description = self.data_description + len(self.string_data).to_bytes(self.description_length_space, byteorder="big")
        packed_data = byte_description + (bytes(self.string_data, "utf-8"))
        return packed_data

    @staticmethod
    def unpack(byte_string):
        if len(byte_string) > 4294967295:
            raise Exception("too large string")

        if hex(byte_string[0]) == "0xd9":
            string_length = byte_string[1]
            string = byte_string[2:]
        elif hex(byte_string[0]) == "0xda":
            string_length = int.from_bytes(byte_string[1:3], byteorder="big")
            string = byte_string[3:]
        elif hex(byte_string[0]) == "0xdb":
            string_length = int.from_bytes(byte_string[1:5], byteorder="big")
            string = byte_string[5:]
        else:
            string_length = byte_string[0]-160
            string = byte_string[1:]

        if len(string) == string_length:
            return string.decode('utf-8')
        else:
            raise Exception("invalid length")
