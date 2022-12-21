import time

from pymavlink import mavutil

mav_conn = mavutil.mavlink_connection('COM23')
mav_conn.wait_heartbeat()
print(mav_conn.target_system, mav_conn.target_component)

mav_conn.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS,
                       mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)

while True:
    msg = mav_conn.recv_match()
    if msg:
        print(msg)
        if msg.get_type() == 'HEARTBEAT':
            mav_conn.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS,
                       mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
    time.sleep(.1)