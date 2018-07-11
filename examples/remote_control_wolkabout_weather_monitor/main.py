#######################################################
# This example sends BME280 data to the wolkAbout cloud.
# PCA9536 outputs can also be controlled from within the
# wolkAbout dashboard.
#
# Upload the manifest to the wolkAbout platform. 
########################################################

# imports
import streams
from texas.pca9536 import pca9536 as OC01
from wolkabout.iot import iot
from wireless import wifi
from bosch.bme280 import bme280
from espressif.esp32net import esp32wifi as wifi_driver

# wifi details
wifi_ssid = "WiFi Username"
wifi_pass = "WiFi Password"
wifi_secu = wifi.WIFI_WPA2

# rgb pins
RED = D25
GREEN = D26
BLUE = D27

# enable console
streams.serial()

# wolkabout project details
device_key = "wolkabout device key"
device_password = "wolkabout device password"
actuator_references = ["0", "1", "2", "3"]

# rgb pins set as output
pinMode(RED, OUTPUT)
pinMode(GREEN, OUTPUT)
pinMode(BLUE, OUTPUT)

# xChip instances
OC01 = OC01.PCA9536(I2C0)
SW01 = bme280.BME280(I2C0)

# initialize sensors
SW01.start()
OC01.init()

# OC01 pins
OUT0 = OC01.OUT0
OUT1 = OC01.OUT1
OUT2 = OC01.OUT2
OUT3 = OC01.OUT3

# init the wifi driver
wifi_driver.auto_init()


# method that establishes a wifi connection
def wifi_connect():
    for retry in range(10):
        try:
            print("Establishing Link...")
            wifi.link(wifi_ssid, wifi_secu, wifi_pass)
            print("Link Established")
            digitalWrite(GREEN, HIGH)
            break
        except Exception as e:
            print("ooops, something wrong while linking :(", e)
            digitalWrite(GREEN, LOW)
            digitalWrite(RED, HIGH)
            sleep(1000)
            digitalWrite(RED, LOW)
            sleep(1000)


# connect to wifi
wifi_connect()

# establish a connection between device and wolkabout iot platform
try:
    device = iot.Device(device_key, device_password, actuator_references)
except Exception as e:
    print("Something went wrong while creating the device: ", e)


# Provide implementation of a way to read actuator status if your device has actuators
class ActuatorStatusProviderImpl(iot.ActuatorStatusProvider):

    def get_actuator_status(reference):
        if reference == actuator_references[0]:
            value = OC01.getStatus() & 0x01
            print(value)
            if value == 0x01:
                return iot.ACTUATOR_STATE_READY, "true"
            else:
                return iot.ACTUATOR_STATE_READY, "false"
        if reference == actuator_references[1]:
            value = OC01.getStatus() & 0x02
            print(value)
            if value == 0x02:
                return iot.ACTUATOR_STATE_READY, "true"
            else:
                return iot.ACTUATOR_STATE_READY, "false"
        if reference == actuator_references[2]:
            value = OC01.getStatus() & 0x04
            print(value)
            if value == 0x04:
                return iot.ACTUATOR_STATE_READY, "true"
            else:
                return iot.ACTUATOR_STATE_READY, "false"
        if reference == actuator_references[3]:
            value = OC01.getStatus() & 0x08
            print(value)
            if value == 0x08:
                return iot.ACTUATOR_STATE_READY, "true"
            else:
                return iot.ACTUATOR_STATE_READY, "false"


class ActuationHandlerImpl(iot.ActuationHandler):

    def handle_actuation(reference, value):
        print("Setting actuator " + reference + " to value: " + value)
        if reference == actuator_references[0]:
            if value == "false":
                OC01.writePin(OUT0, False)
            else:
                if value == "true":
                    OC01.writePin(OUT0, True)
        if reference == actuator_references[1]:
            if value == "false":
                OC01.writePin(OUT1, False)
            else:
                if value == "true":
                    OC01.writePin(OUT1, True)
        if reference == actuator_references[2]:
            if value == "false":
                OC01.writePin(OUT2, False)
            else:
                if value == "true":
                    OC01.writePin(OUT2, True)
        if reference == actuator_references[3]:
            if value == "false":
                OC01.writePin(OUT3, False)
            else:
                if value == "true":
                    OC01.writePin(OUT3, True)


try:
    wolk = iot.Wolk(device, ActuationHandlerImpl, ActuatorStatusProviderImpl)
except Exception as e:
    print("Something went wrong while creating the Wolk instance: ", e)

# Establish a connection to the WolkAbout IoT Platform
try:
    print("Connecting to WolkAbout IoT Platform")
    wolk.connect()
    print("Done")
except Exception as e:
    print("Something went wrong while connecting: ", e)

publish_period = 5000

try:
    while True:
        if not wifi.is_linked():
            wifi_connect()

        sleep(publish_period)

        print("Publishing sensor readings and actuator statuses")
        temperature = SW01.get_temp()
        humidity = SW01.get_hum()
        pressure = SW01.get_press()
        print("T", temperature, "H", humidity, "P", pressure)
        wolk.add_sensor_reading("T", temperature)
        wolk.add_sensor_reading("H", humidity)
        wolk.add_sensor_reading("P", pressure)

        wolk.publish()
except Exception as e:
    print("Something went wrong: ", e)
