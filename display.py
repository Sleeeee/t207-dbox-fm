from machine import Pin, Timer

class Display:
    def __init__(self, decoder_pins=[12, 13, 14, 15], transistor_pins=[20, 21, 22, 26], dot_pin=27):
        self.decoder_pins = [Pin(p, Pin.OUT) for p in decoder_pins]
        self.transistor_pins = [Pin(p, Pin.OUT) for p in transistor_pins]
        self.dot_pin = Pin(dot_pin, Pin.OUT)
        self.count = len(transistor_pins)

        self._digits = None
        self.i = 0
        self.dot_pin.value(1)
        self.timer = Timer()
        self.timer.init(mode=Timer.PERIODIC, freq=200, callback=self.display_next_digit)

    @property
    def digits(self):
        return self._digits

    @digits.setter
    def digits(self, number):
        number_as_str = str(number)
        if len(number_as_str) != self.count:
            self._digits = None
            raise ValueError("This number does not match the amount of seven-segment displays you initialized :", self.count)
        self._digits = [int(d) for d in number_as_str]

    def activate_display(self, i):
        for j in range(len(self.transistor_pins)):
            if i == j:
                self.transistor_pins[j].value(1)
            else:
                self.transistor_pins[j].value(0)

    def display_digit(self, digit):
        for i in range(4):
            self.decoder_pins[i].value((digit >> (3-i)) & 1)
        self.activate_display(self.i)

    def display_next_digit(self, timer):
        if self.digits is not None:
            self.display_digit(self.digits[self.i])
            self.i = (self.i + 1) % self.count

    def deinit(self):
        self.timer.deinit()
        for pin in self.decoder_pins:
            pin.value(0)
        for pin in self.transistor_pins:
            pin.value(0)
        self.dot_pin.value(0)
