import serial
import webbrowser
import subprocess

BAUD_RATE = 56000

# ask user to sepecify serial port to listen to
serial_port = input("Serial port: ")

# open text file containing action shortcuts
in_file = open("actions.txt")

# read file into a list
buttons = []
for line in in_file:
    if (line[0] != '#'):
        buttons.append(line)

in_file.close


serial_in = serial.Serial(serial_port, BAUD_RATE, timeout = 5)
serial_in.flush()

print("Listening")

#continously check serial interface for incoming data
while(1):    
    # read in one byte
    response = serial_in.read(1)    
    # print out received byte
    print(response)
    
    # b"O" - hearbeat
    # b"A" - button 1
    # b"B" - button 2
    # b"C" - button 3
    # b"D" - button 4
    
    if response == b"O":
        print("Got OK Byte.")
        
    elif response == b"A":
        #check first character of the string assigned to the button
        #letter h implies http therefore a web site
        #for any other character assume a directory
        if (buttons[0][0] == 'h'):
            webbrowser.open(buttons[0]) 
        else:
            subprocess.call([buttons[0]])
            
    elif response == b"B":
        if (buttons[1][0] == 'h'):
            webbrowser.open(buttons[1]) 
        else:
            subprocess.call([buttons[1]])  
            
    elif response == b"C":
        if (buttons[2][0] == 'h'):
            webbrowser.open(buttons[2]) 
        else:
            subprocess.call([buttons[2]])  
            
    elif response == b"D":
        if (buttons[3][0] == 'h'):
            webbrowser.open(buttons[3]) 
        else:
            subprocess.call([buttons[3]])
            
    else:
        print("Got nothing.  Still waiting.")