import serial
import webbrowser
import subprocess

BAUD_RATE = 56000

# map buttons to ascii codes sent from microcontroller
# b"A" - button 0
# b"B" - button 1
# b"C" - button 2
# b"D" - button 3
buttons = {b"A":0, b"B":1, b"C":2, b"D":4}

# ask user to sepecify serial port to listen to
serial_port = input("Serial port: ")

# open text file containing action shortcuts
in_file = open("shortcuts.txt")

# read file into a list
shortcuts = []
for line in in_file:
    if (line[0] != '#'):
        shortcuts.append(line)

in_file.close

# set up serial interface
serial_in = serial.Serial(serial_port, BAUD_RATE, timeout = 10)
serial_in.flush()

print("Listening")

def action(code):
    try:
        # if first character in the shortcut string is an 'h' 
        # then it probably stands for http://somethin...   
        if (shortcuts[code][0] == 'h'):
            webbrowser.open(shortcuts[code]) 
        # otherwise it's probably a directory
        else:
            subprocess.call([shortcuts[code]]) 
    except:
        print("Error. Button probably unassigned.")

#continously check serial interface for incoming data
while(1):    
    # read in one byte
    ascii_code = serial_in.read(1)    
    
    # b"O" - hearbeat
    if ascii_code == b"O":
        print("Got OK Byte.")
        
    # if code representing one of the buttons comes in then
    # pass assigned button number to the function
    elif ascii_code in buttons:
        action(buttons[ascii_code])
            
    else:
        print("Got nothing.  Still waiting.")