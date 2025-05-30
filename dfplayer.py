from machine import Pin, UART

class DFPlayer:
    def __init__(self, pin_rx=1, pin_tx=0):
        self.uart = UART(0, 9600, rx=pin_rx, tx=pin_tx)

    def command(self, cmd, param=0x00):
        bytes_to_send = bytes([0x7e, 0xff, 0x06, cmd, 0x00, 0x00, param, 0xef])
        self.uart.write(bytes_to_send)

    def resume(self):
        self.command(0x0d)

    def previous(self):
        self.command(0x02)

    def next(self):
        self.command(0x01)

    def play(self, number):
        self.command(0x03, number)

    def pause(self):
        self.command(0x0e)

    def reset(self):
        self.command(0x0c)
