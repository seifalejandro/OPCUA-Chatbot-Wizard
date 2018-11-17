import sys
sys.path.insert(0, "..")
import time
from opcua import ua, Server
if __name__ == "__main__":
	# setup our server
	server = Server()
	server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
	# setup our own namespace, not really necessary but should as spec
	uri = "http://examples.freeopcua.github.io"
	idx = server.register_namespace(uri)
	# get Objects node, this is where we should put our nodes
	objects = server.get_objects_node()
	myobj = objects.add_object(idx, "MyObject")
	myvars = []
	myvars.append(myobj.add_variable(idx, "PEOR", 0))
	myvars.append(myobj.add_variable(idx, "TERO", 0))
	myvars.append(myobj.add_variable(idx, "asfasfasfasfsf", 0))
	server.start()
	try:
		count = 0
		while True:
			time.sleep(0.5)
			count += 0.1
			myvars[0].set_value(count)
			myvars[1].set_value(count)
			myvars[2].set_value(count)
	finally:
		server.stop()
