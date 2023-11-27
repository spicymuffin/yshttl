import threading
import time

def divbyzero():
    for i in range(10, -1, -1):
        time.sleep(0.5)
        print(1 / i)


exception_thread = threading.Thread(target=divbyzero)
exception_thread.daemon = True
exception_thread.start()

while True:
    time.sleep(0.1)
    print(exception_thread.is_alive())