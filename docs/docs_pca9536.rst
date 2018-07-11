.. module:: pca9536

***************
 PCA9536 Module
***************

This is a Module for the PCA9536 I/O expander by Texas Instruments.
The Module implements the PCA9536 as an output device utilizing the `OC01 xChip <https://wiki.xinabox.cc/OC01_-_High_Current_DC_Switch>`_.
The board uses I2C for communication.


Data Sheets: `PCA9536 <http://www.ti.com/lit/ds/symlink/pca9536.pdf>`_
    
===============
PCA9536 class
===============

.. class:: PCA9536(self, drvname, addr = PCA9536_I2C_ADDRESS , clk = 100000)

    Create an instance of the PCA9536 class.

    :param drvname: I2C Bus used '( I2C0, ... )'
    :param addr: Slave address, default 0x41
    :param clk: Clock speed, default 100kHz

    
.. method:: init(self, pins = PCA9536_ALL_OUTPUTS_OFF)

        Configures PCA9536 and sets all outputs False by default

        :param pins: gives the pins an initial state

        
.. method:: writePin(self, pin, state)

        Determines the status of the output

        :param pin: accepts one of four output pins on PCA9536 (1, 2, 4, 8)
        :param state: accepts the state at which selected pin should be (True or False)

        
.. method:: getStatus(self)

        Reads the status of the output port. To read a single bit/pin mask the return value with the pin number.
        Eg. getStatus() & OUT0

        returns the status of the output port
