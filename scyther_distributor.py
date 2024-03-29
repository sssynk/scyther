import subprocess
import threading

print("Welcome to Scyther Distributor")
workers = int(input("Select num of workers (upper max 12):"))

def startWorker(num):
    while True:
        print(f"Worker {num} started")
        subprocess.Popen(["python", "scyther_generate_sync_inf.py"]).wait()
        print(f"Worker {num} completed/died, restarting")


# spawn instances of scyther_generate_sync_inf.py and restart if they die
for i in range(workers - 1):
    threading.Thread(target=startWorker, args=(i,)).start()

# start one worker in main thread
startWorker(workers)
