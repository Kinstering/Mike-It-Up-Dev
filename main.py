import subprocess, time

c1 = subprocess.Popen(["python3", "clusters_max.py"])
q1 = subprocess.Popen(["python3", "liq.py"])
r1 = subprocess.Popen(["python3", "_report.py"])

a1 = subprocess.Popen(["python3", "asks_bids_1.py"])
a2 = subprocess.Popen(["python3", "asks_bids_2.py"])
a3 = subprocess.Popen(["python3", "asks_bids_3.py"])
a4 = subprocess.Popen(["python3", "asks_bids_4.py"])
a5 = subprocess.Popen(["python3", "asks_bids_5.py"])
a6 = subprocess.Popen(["python3", "asks_bids_6.py"])
a7 = subprocess.Popen(["python3", "asks_bids_7.py"])

t1 = subprocess.Popen(["python3", "trades_1.py"])
t2 = subprocess.Popen(["python3", "trades_2.py"])
t3 = subprocess.Popen(["python3", "trades_3.py"])
t4 = subprocess.Popen(["python3", "trades_4.py"])
t5 = subprocess.Popen(["python3", "trades_5.py"])
t6 = subprocess.Popen(["python3", "trades_6.py"])
t7 = subprocess.Popen(["python3", "trades_7.py"])


while True:
  time.sleep(30)
  poll = c1.poll()
  if poll is not(None):
    print('Restart the process c1')
    c1 = subprocess.Popen(["python3", "clusters_max.py"])

  poll = q1.poll()
  if poll is not (None):
    print('Restart the process q1')
    q1 = subprocess.Popen(["python3", "liq.py"])

  poll = r1.poll()
  if poll is not(None):
    print('Restart the process r1')
    r1 = subprocess.Popen(["python3", "_report.py"])

  poll = a1.poll()
  if poll is not(None):
    print('Restart the process a1')
    a1 = subprocess.Popen(["python3", "asks_bids_1.py"])
 
  poll = a2.poll()
  if poll is not(None):
    print('Restart the process a2')
    a2 = subprocess.Popen(["python3", "asks_bids_2.py"])

  poll = a3.poll()
  if poll is not(None):
    print('Restart the process a3')
    a3 = subprocess.Popen(["python3", "asks_bids_3.py"])

  poll = a4.poll()
  if poll is not(None):
    print('Restart the process a4')
    a4 = subprocess.Popen(["python3", "asks_bids_4.py"])

  poll = a5.poll()
  if poll is not(None):
    print('Restart the process a5')
    a5 = subprocess.Popen(["python3", "asks_bids_5.py"])

  poll = a6.poll()
  if poll is not(None):
    print('Restart the process a6')
    a6 = subprocess.Popen(["python3", "asks_bids_6.py"])

  poll = a7.poll()
  if poll is not(None):
    print('Restart the process a7')
    a7 = subprocess.Popen(["python3", "asks_bids_7.py"])

  poll = t1.poll()
  if poll is not(None):
    print('Restart the process t1')
    t1 = subprocess.Popen(["python3", "trades_1.py"])

  poll = t2.poll()
  if poll is not(None):
    print('Restart the process t2')
    t2 = subprocess.Popen(["python3", "trades_2.py"])

  poll = t3.poll()
  if poll is not(None):
    print('Restart the process t3')
    t3 = subprocess.Popen(["python3", "trades_3.py"])

  poll = t4.poll()
  if poll is not(None):
    print('Restart the process t4')
    t4 = subprocess.Popen(["python3", "trades_4.py"])

  poll = t5.poll()
  if poll is not(None):
    print('Restart the process t5')
    t5 = subprocess.Popen(["python3", "trades_5.py"])

  poll = t6.poll()
  if poll is not(None):
    print('Restart the process t6')
    t6 = subprocess.Popen(["python3", "trades_6.py"])

  poll = t7.poll()
  if poll is not(None):
    print('Restart the process t7')
    t7 = subprocess.Popen(["python3", "trades_7.py"])