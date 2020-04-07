"""A local performance test to see how memory usage for the app changes.

Run this from the home directory of the application `python ./test/load/simple_perf.py`

1. Run the application
2. Run psrecord with the PID of the application
3. Send 3 requests
4. Kill the application and psrecord should shut down of it's own accord and save the plot
5. Open the graph
"""
import os
import requests
import subprocess
import time

run_app = subprocess.Popen(["python", "main.py"])

# Wait for the app to start
time.sleep(5)

print(f"started application with pid {run_app.pid}")

plot_file = f"{run_app.pid}.png"

ps_record = subprocess.Popen(["psrecord", str(run_app.pid), f"--plot={plot_file}"])

print("started psrecord")

for text_input in ['holla at the DJ', 'Kim what are you saying', 'jesus runs this']:
    print(f"sending {text_input} to application")
    requests.post(url="http://localhost:5000", data={'text_input': text_input})

run_app.terminate()

# Wait for the file to be created by psrecord then open it to have a look
time.sleep(5)
os.system(f"open {plot_file}")
