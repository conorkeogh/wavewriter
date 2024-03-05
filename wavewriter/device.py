# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_initialisation.ipynb.

# %% auto 0
__all__ = ['WaveWriter']

# %% ../nbs/02_initialisation.ipynb 10
'''
    WaveWriter device drivers

    Oxford Neural Interfacing
    Written by Conor Keogh
    conor.keogh@nds.ox.ac.uk
    04/03/2024

    Provides functions for interacting with WaveWriter device
'''

'''
WaveWriter device class
Provide functions to interact with device
Finds device and confirms presence
Sends messages to device to specify waveforms and start/stop stimulation
'''
import serial
import serial.tools.list_ports
import time
import numpy as np

class WaveWriter:

    def __init__(self):
        '''
        Device object for controlling synchronisation
        '''

        '''
        Define constants for device configuration
        '''
        # Define messages
        self.GREETING = b'Hello'
        self.RESPONSE = 'Hi there'
        
        self.prep1_command = 'prep1'    # Prepare buffer 1 (V)
        self.prep2_command = 'prep2'    # Prepare buffer 2 (t)
        self.start_command = 'start'    # Start stimulation
        self.stop_command = 'stop'      # Stop stimulation
    
        # Define COM port settings
        self.BAUDRATE = 115200
        
        # Empty arrays for waveform
        self.v = np.array([])
        self.t = np.array([])
        
        # Get all serial ports
        ports = serial.tools.list_ports.comports()

        # For each port: try accessing and checking for acknowledge message
        port_found = False
        for port in ports:
            try:
                # Connect to serial port
                self.ser = serial.Serial(port.device, self.BAUDRATE, timeout=1, write_timeout=1)

                # Send test message and read response; repeat 3 times and keep third
                for _ in range(3):
                    self.ser.write(self.GREETING)
                    response = self.ser.readline()

                # Check if response is appropriate
                if response.decode().rstrip('\x00') == self.RESPONSE:
                    self.target_port = port.device
                    port_found = True

                # Close port
                self.ser.close()

            except Exception as e:
                # Do nothing - just ignore failed ports
                pass

        # If port found: connect to port
        if port_found:
            self.ser = serial.Serial(self.target_port, self.BAUDRATE, timeout=5)

        # If port not found: raise error
        else:
            raise Exception("Device not found")
            #print("Device not found")

    ''' Send required messages over serial '''
    # Send message via serial port
    def sendMessage(self, message):
        '''
        Send message over serial port
        Takes message to send
        '''
        self.ser.write(message.encode())
        
    # Check inputs are appropriate
    def check_inputs(self, v, t):
        # Check types
        if type(v) is not np.ndarray:
            raise Exception("V is not an array")
            
        if type(t) is not np.ndarray:
            raise Exception("t is not an array")
            
        # Check dimensions
        v = np.squeeze(v)
        t = np.squeeze(t)
        
        if v.ndim > 1:
            raise Exception("V is not one-dimensional")
            
        if t.ndim > 1:
            raise Exception("t is not one dimensional")
            
        # Check lengths are equal
        if v.size != t.size:
            raise Exception("V and t are not of equal lengths")
            
        # If appropriate: save V and t to object
        self.v = v
        self.t = t
        
    def convert_buffer(self, x):
        ''' Convert array to buffer to send '''
        # Create emoty string
        x_buffer = ''
        
        # Iterate through array
        for value in x[:-1]:
            x_buffer += str(value)    # Add to buffer
            x_buffer += ','           # Add delimiter
        x_buffer += str(x[-1])        # Add last value without delimiter
        
        return x_buffer
            
    def send_waveform(self, v, t):
        ''' Send waveform data to device '''
        # Check inputs are appropriate
        self.check_inputs(v, t)
        
        # Convert to string buffers to send
        v_buffer = self.convert_buffer(v)
        t_buffer = self.convert_buffer(t)
        
        # Prepare to send first buffer
        self.sendMessage(self.prep1_command)
        
        # Send V to buffer 1
        self.sendMessage(v_buffer)
        
        # Prepare to send second buffer
        self.sendMessage(self.prep2_command)
        
        # Send t to buffer 2
        self.sendMessage(t_buffer)
        
    def start(self):
        ''' Send start signal '''
        self.sendMessage(self.start_command)

    def stop(self):
        ''' Send end signal '''
        self.sendMessage(self.stop_command)

    # Close channel
    def close(self):
        '''
        Closes device connection
        '''
        self.ser.close()
