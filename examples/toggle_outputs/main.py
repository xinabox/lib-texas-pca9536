##############################################
#   This is example for the pca9536 library
#
#   Each output is toggled at 500ms
##############################################

# imports
from texas.pca9536 import pca9536 as OC01

# sleep time
DELAY = 500

# create an instance of PCA9536 class
OC01 = OC01.PCA9536(I2C0)

# OC01 pins
OUT0 = OC01.OUT0
OUT1 = OC01.OUT1
OUT2 = OC01.OUT2
OUT3 = OC01.OUT3

# initialize OC01
OC01.init()

# infinite loop
while True:
    # Switch OUT0 On
    OC01.writePin(OUT0, True)
    sleep(DELAY)

    # Switch OUT1 On
    OC01.writePin(OUT1, True)
    sleep(DELAY)

    # Switch OUT2 On
    OC01.writePin(OUT2, True)
    sleep(DELAY)

    # Switch OUT3 On
    OC01.writePin(OUT3, True)
    sleep(DELAY)

    # Switch OUT0 off
    OC01.writePin(OUT0, False)
    sleep(DELAY)

    # Switch OUT1 off
    OC01.writePin(OUT1, False)
    sleep(DELAY)

    # Switch OUT2 off
    OC01.writePin(OUT2, False)
    sleep(DELAY)

    # Switch OUT3 off
    OC01.writePin(OUT3, False)
    sleep(DELAY)
