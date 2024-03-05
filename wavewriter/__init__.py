__version__ = "0.0.1"

# Import required libraries
import numpy as np
import serial
import serial.tools.list_ports
import time

# Import device to main namespace
from wavewriter.device import WaveWriter