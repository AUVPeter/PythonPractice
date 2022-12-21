# Dealing with MAVLINK in python
MAVLINK allows us to interact with devices running the Ardupilot code base (BlueROVS, AMSL ASVs, etc.)

# Mavlink
Mavlink is the underlying communication standard used by Ardupiplot devices. The [pymavlink](https://github.com/ArduPilot/pymavlink) library allows us to easily connect to and exchange messages with a device running Mavlink using the mavlink module

The available messages and definitions are available [here](https://mavlink.io/en/messages/common.html).

Some examples of using pymavlink can be found [here](https://www.ardusub.com/developers/pymavlink.html).

pymavlink is installed through pip 
~~~python
pip install pymavlink
~~~

Then in our code we simply import 
~~~python
from pymavlink import mavutil
~~~


# Connecting to a device
Our code must first establish a connection to a compatible device, such as a pixhawk or Cube. We need to be aware how the device is connected to our system. In many cases this is either through USB or over Ethernet. To get started will will first look at serial connections. On a windows machine we can use the Device Manager to display what port has been assigned to the connected device, usually this will be the highest number and be labeled as a 'USB to Serial' port. On Linux we look at the /dev folder.

We first create a mavlink_connection to the assigned port (COM23 in this example)
~~~python
mav_conn = mavutil.mavlink_connection('COM23')
~~~

then we wait to ensure that the device is connected by awaiting the reception of a heartbeat message

~~~python
mav_conn.wait_heartbeat()
~~~

To establish a session we send our own heartbeat message to declare what sort of device we are, in this case a GCS (Ground Control Station)

~~~python
mav_conn.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS,mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
~~~

We can now listen for any messages sent from the device over Mavlink. The `recv_msg` function is used to recv the next available message. For this example we will receive and print all messages as they arrive

~~~python
while True:
    msg = mav_conn.recv_msg()
    if msg:
        print(msg)
~~~

If we are only interested in certain messages, we can filter the msg object using its `get_type()` function. For example if we are interested in the `GLOBAL_POSITION_INT` messages we would modify the above block to detect when a message of that type arrives. We also use the `to_dict()` function to convert the raw message object into a python dictionary so we can have access to each data field directly

~~~python
while True:
    msg = mav_conn.recv_msg()
    if msg:
        if msg.get_type() == 'GLOBAL_POSITION_INT':          
            msg_dict = msg.to_dict()
            # Do someting interesting
            print(f"At {msg_dict['time_boot_ms']}ms the position is: {msg_dict['lat']},{msg_dict['lon']}")
~~~

Here is the complete example so far

~~~python
from pymavlink import mavutil

mav_conn = mavutil.mavlink_connection('COM23')
mav_conn.wait_heartbeat()

mav_conn.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS,
                       mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)

while True:
    msg = mav_conn.recv_msg()
    if msg:
        if msg.get_type() == 'GLOBAL_POSITION_INT':
            msg_dict = msg.to_dict()
            # Do someting interesting
            print(f"At {msg_dict['time_boot_ms']}ms the position is: {msg_dict['lat']},{msg_dict['lon']}")
~~~            
