import RPi.GPIO as GPIO
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


# spi bus
spi = busio.SPI( clock = board.SCK, MISO = board.MISO, MOSI = board.MOSI )

# cs (chip select)
cs = digitalio.DigitalInOut( board.D5 )

# mcp object
mcp = MCP.MCP3008( spi, cs )

# analog input channel on pin 0
channel0 = AnalogIn( mcp, MCP.P0 )


# calculates more usable number output by sensor
def _range( x, in_min, in_max, out_min, out_max ):
    return int( ( x - in_min ) * ( out_max - out_min ) / ( in_max - in_min ) + out_min )


# reads and returns the sensor value
def readSensor( spi, cs, mcp, channel0 ):
    sensorValue = _range( channel0.value, 0, 60000, 0, 1023 )
    return sensorValue