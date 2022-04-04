import os
import time

def dotsleep(sec: int, sep: str='.'):
  end = time.time() + sec
  while time.time() < end:
    print(sep, end='', flush=True)
    time.sleep(1)
  print(os.linesep)


