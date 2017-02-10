import unittest
import smbus


class I2C:
    """
    I2C class used as parent class for modules communicating with I2C.
    This class stores the adress of the I2C module it represents and
    connects to the I2C bus using smbus. It also provides a couple
    of convenience methods.
    """

    def __init__(self, address):
        """Takes the I2C adress of the module it represents"""
        self.bus = smbus.SMBus(1)
        self.address = address

    # Can handle numbers aswell as lists
    def send(self, data):
        """Send data to the module it represents"""
        if isinstance(data, list):
            for byte in data:
                self.bus.write_byte(self.address, byte)
        elif isinstance(data, int):
            self.bus.write_byte(self.address, data)

    # read_i2c_block_data can't process more than 32 bytes, so num_bytes should
    # not be greater than 32 !!
    def receive(self, num_bytes=1):
        """Receive a specific amount of data from the module it represents"""
        data = self.bus.read_i2c_block_data(self.address, 0x00, num_bytes)
        if len(data) == 1:
            return data[0]
        else:
            return data

    def pack8(high, low):
        """Takes two 4 bit variables and packs them together into 8 bits"""
        # Use  bitwise AND to retain only the first 4 bits
        # of high and low, shift the four bits from high to the left
        # and do a bitwise OR with the four bits of low
        # to get a 8 bit value of the form: hhhh llll
        return (high & 0b1111) << 4 | (low & 0b1111)

    def pack16(high, low):
        """Takes two bytes and packs them together into a 16 bits variable"""
        # Use  bitwise AND to retain only the first 8 bits
        # of high and low, shift the 8 bits from high to the left
        # and do a bitwise OR with the 8 bits of low
        # to get a 16 bit value of the form: hhhh hhhh llll llll
        return (high & 0xFF) << 8 | (low & 0xFF)


class TestPack(unittest.TestCase):

    def test_pack8(self):
        self.assertEqual(I2C.pack8(0b0011, 0b0010), 0b00110010)
        self.assertEqual(I2C.pack8(0b11000011, 0b0010), 0b00110010)
        self.assertEqual(I2C.pack8(0b1111, 0b0000), 0b11110000)

    def test_pack16(self):
        self.assertEqual(I2C.pack16(0xF3, 0xAB), 0xF3AB)
        self.assertEqual(I2C.pack16(0x2, 0xFF), 0x02FF)


if __name__ == '__main__':
    unittest.main()
