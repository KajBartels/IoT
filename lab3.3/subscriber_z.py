import zmq
import numpy as np

url = "tcp://127.0.0.1:5555"

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect(url)
socket.setsockopt(zmq.SUBSCRIBE, b"")

print("Waiting for arrays...")

while True:
    md = socket.recv_json()
    array = socket.recv(copy=True)
    arr = np.frombuffer(array, dtype=md['dtype']).reshape(md['shape'])
    print("Received array:", arr[2])
