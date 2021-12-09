from gpiozero import LED
import sys
import time
import datetime
import subprocess as sub
import numpy as np
import starcoder42 as s
from pathlib import Path

start = time.time()
s.iprint(f"[{start:12.0f}] HiFiBerry Muter started", 0)

try:
    state = sys.argv[1]
except IndexError as e:
    raise IndexError('Please provide an "on", "off", or "daemon" argument. "on'
                     '  means you want to turn the mute on (ie. no sound)')

state_file = Path(__file__).parent / 'mute_state.txt'
if state == 'daemon':

    procs = sub.Popen("ps auxf", stdout=sub.PIPE, shell=True)
    lines = np.array(procs.stdout.readlines())
    is_fan = np.array([(sys.argv[0] in str(proc))
                         for proc in lines])
    to_kill = lines[is_fan]
    
    for proc in to_kill:
        parts = proc.split()
        pid = parts[1]
        dt = parts[9]
        m, sec = dt.split(b':')
        dt = datetime.timedelta(minutes=int(m), seconds=int(sec))
        if dt > datetime.timedelta(hours=23):
            sub.call(['kill', pid])
        
    muter = LED(4, initial_value=state=='off')
    while True:
        with state_file.open('r') as fil:
            state = fil.read()
        if state == 'off':
            muter.on()
        elif state == 'on':
            muter.off()
        time.sleep(1)

else:
    if state=='off':
        s.iprint(f'[{time.time():12.0f}] Unmuting', 1)
    elif state=='on':
        s.iprint(f'[{time.time():12.0f}] Muting', 1)
    with state_file.open('w') as fil:
        fil.write(state)

