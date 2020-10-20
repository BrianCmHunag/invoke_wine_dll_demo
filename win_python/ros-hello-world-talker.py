import time

import roslibpy # ROS bridge https://roslibpy.readthedocs.io/en/latest/
import ctypes # Load DLL into memory. #https://docs.python.org/2/library/ctypes.html

myDll = ctypes.WinDLL ("Dll_example.dll")

client = roslibpy.Ros(host='localhost', port=9090)
client.run()

talker = roslibpy.Topic(client, '/chatter', 'std_msgs/String')


accumulator = 0

while client.is_connected:

    double_accumulator = myDll.add(accumulator,accumulator)
    talker.publish(roslibpy.Message({'data': str(double_accumulator)}))
    print('Sending message...')
    time.sleep(1)
    accumulator = accumulator + 1

talker.unadvertise()

client.terminate()
