import subprocess
import time

processes = {
    "c1": "clusters_max.py",
    "q1": "liq.py",
    "r1": "_report.py",
    "a1": "asks_bids_1.py",
    "a2": "asks_bids_2.py",
    "a3": "asks_bids_3.py",
    "a4": "asks_bids_4.py",
    "a5": "asks_bids_5.py",
    "a6": "asks_bids_6.py",
    "a7": "asks_bids_7.py",
    "t1": "trades_1.py",
    "t2": "trades_2.py",
    "t3": "trades_3.py",
    "t4": "trades_4.py",
    "t5": "trades_5.py",
    "t6": "trades_6.py",
    "t7": "trades_7.py",
}

running_processes = {}

def start_process(key, command):
    running_processes[key] = subprocess.Popen(["python3", command])

def restart_process(key, command):
    print(f"Restart the process {key}")
    running_processes[key].terminate()
    start_process(key, command)

for key, command in processes.items():
    start_process(key, command)

while True:
    time.sleep(30)

    for key, process in running_processes.items():
        poll = process.poll()
        if poll is not None:
            restart_process(key, processes[key])