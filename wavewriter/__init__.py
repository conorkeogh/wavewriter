__version__ = "0.0.1"

# Import required libraries
import numpy as np
import serial
import serial.tools.list_ports
import time

from matplotlib import pyplot as plt
import seaborn as sns

sns.set()
sns.set_style('ticks')
sns.set_context('talk')

# Import device to main namespace
from wavewriter.device import WaveWriter
from wavewriter.waveforms import *