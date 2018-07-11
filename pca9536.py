"""
.. module:: pca9536

***************
 PCA9536 Module
***************

This is a Module for the PCA9536 I/O expander by Texas Instruments.
The Module implements the PCA9536 as an output device utilizing the `OC01 xChip <https://wiki.xinabox.cc/OC01_-_High_Current_DC_Switch>`_.
The board uses I2C for communication.


Data Sheets: `PCA9536 <http://www.ti.com/lit/ds/symlink/pca9536.pdf>`_

	"""

import i2c

PCA9536_I2C_ADDRESS         = 0x41

PCA9536_REG_INPUT_PORT      = 0x00
PCA9536_REG_OUTPUT_PORT     = 0x01  
PCA9536_REG_POL_INVERSION   = 0x02
PCA9536_REG_CONFIG          = 0x03

PCA9536_CONF_OUTPUT         = 0x00
PCA9536_CONF_INPUT          = 0x0F

PCA9536_ALL_OUTPUTS_OFF     = 0x00

PCA9536_PIN0_OUTPUT         = 0x00
PCA9536_PIN0_INPUT          = 0x01

PCA9536_PIN1_OUTPUT         = 0x00
PCA9536_PIN1_INPUT          = 0x02

PCA9536_PIN2_OUTPUT         = 0x00
PCA9536_PIN2_INPUT          = 0x04

PCA9536_PIN3_OUTPUT         = 0x00
PCA9536_PIN3_INTPUT         = 0x08


class PCA9536(i2c.I2C):
    '''

===============
PCA9536 class
===============

.. class:: PCA9536(self, drvname, addr = 0x41, clk = 100000)

        Create an instance of the PCA9536 class.

        :param drvname: I2C Bus used '( I2C0, ... )'
        :param addr: Slave address, default 0x41
        :param clk: Clock speed, default 100kHz

    '''

    # pca9536 pin numbers. Correlates OC01 xChip

    OUT0 = 0x01
    OUT1 = 0x02
    OUT2 = 0x04
    OUT3 = 0x08

    def __init__(self, drvname, addr = PCA9536_I2C_ADDRESS , clk = 100000):
        i2c.I2C.__init__(self, drvname, addr, clk)
        self._addr = addr
        self.start()

    def init(self, pins = PCA9536_ALL_OUTPUTS_OFF):
        '''
.. method:: init(self, pins = PCA9536_ALL_OUTPUTS_OFF)

        Configures PCA9536 and sets all outputs False by default

        :param pins: gives the pins an initial state

        '''

        self.write_bytes(PCA9536_REG_OUTPUT_PORT, pins)
        self.write_bytes(PCA9536_REG_CONFIG, PCA9536_CONF_OUTPUT)


    def writePin(self, pin, state):
        '''
.. method:: writePin(self, pin, state)

        Determines the status of the output

        :param pin: accepts one of four output pins on PCA9536 (1, 2, 4, 8)
        :param state: accepts the state at which selected pin should be (True or False)

        '''
        pin_state = self.write_read(PCA9536_REG_OUTPUT_PORT, 1)[0]
        if state is True:
            pin_state |= (pin_state | pin)
            self.write_bytes(PCA9536_REG_OUTPUT_PORT, pin_state)
        elif state is False:
            pin_state &= ~(1 << pin_state|pin)
            self.write_bytes(PCA9536_REG_OUTPUT_PORT, pin_state)
    

    def getStatus(self):
        '''
.. method:: getStatus(self)

        Reads the status of the output port. To read a single bit/pin mask the return value with the pin number.
        | Eg. getStatus()& OUT0

        returns the status of the output port

        '''
        pin_state = self.write_read(PCA9536_REG_OUTPUT_PORT, 1)[0]
        return pin_state

