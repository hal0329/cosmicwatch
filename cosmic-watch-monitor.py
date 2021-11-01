#
# cosmic-watch-console
#
#  using for data acquisition from Cosmic Watch 
#  generate exe file: pyinstaller .\cosmic-watch-console.spec --onefile
#

import serial
import serial.tools.list_ports
import datetime
from time import sleep
import matplotlib.pyplot as plt

#search avilable COM ports
def search_com_port():
    coms = serial.tools.list_ports.comports()
    comlist = []
    for com in coms:
        comlist.append(com.device)
    print('Connected COM ports: ' + str(comlist))
    return comlist

#select COM port
def select_com_port(comlist):
    if len(comlist) == 1:
        print('connected to '+comlist[0])
        return comlist[0]
    elif len(comlist) > 1:
        print('select from available ports:')
        i = 0
        for com in comlist:
            print(str(i) + ': ' + com)
            i += 1
        use_port_num = input()
        print('connected to '+comlist[int(use_port_num)])
        return comlist[int(use_port_num)]
    else:
        exit

#ready serial com.
comlist = search_com_port()        # Search COM Ports
use_port = select_com_port(comlist)
ser = serial.Serial(use_port,9600)    # Init Serial Port Setting


# prepare plotting
data ={
    'time':[],
    'adc':[],
    'vol':[],
    'deadtime':[]
}
fig, ax = plt.subplots(2, 1, figsize=(12, 8))

#ready csv file
today = datetime.datetime.now()
f = open(today.strftime('%Y-%m-%d-%H-%M-%S')+'.dat', 'w')

#read lines
try:
    while True: #loop until ctrl+C
        try:
            line = ser.readline().decode('utf-8').split() #read lines
        except UnicodeDecodeError:
            continue
        if (len(line) > 2 and line[0] != '###'):
            line.insert(1, (today+datetime.timedelta(milliseconds = int(line[1]))).strftime('%Y-%m-%d-%H-%M-%S.%f'))
            print(line)    #read lines
            f.write('\t'.join(line)+'\n')   #write lines
            data['time'].append(float(line[2]))
            data['adc'].append(float(line[3]))
            data['vol'].append(float(line[4]))
            data['deadtime'].append(float(line[5]))

            ax[0].cla()
            ax[0].set_title('ADC')
            ax[0].hist(data['adc'],bins=30,color="skyblue")

            ax[1].cla()
            ax[1].set_title('Flux')
            ax[1].hist(data['time'],bins=30,color="lightcoral")
            plt.pause(.001)
except KeyboardInterrupt:   #terminate with ctrl+C
    exit
