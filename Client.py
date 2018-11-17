import sys
sys.path.insert(0, "..")
import time
from opcua import Client
if __name__ == "__main__":
	client = Client("opc.tcp://localhost:4840/freeopcua/server/")
	try:
		client.connect()
		root = client.get_root_node()
		Variables=root.get_children()[0].get_children()[1].get_variables()
		while True:
			time.sleep(1)
			for v in Variables:
				print(v.get_value())
	finally:
		client.disconnect()
