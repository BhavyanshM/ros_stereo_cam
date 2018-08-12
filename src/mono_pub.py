#!/usr/bin/env python

import cv2
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


cam = cv2.VideoCapture(0)

bridge = CvBridge()

MONO_FPS = 30

def talker():
    print("Initiating ROS Stereo Cam Driver:")
    pub = rospy.Publisher('image_raw', Image, queue_size=MONO_FPS)

    rospy.init_node('camera', anonymous=True)
    rate = rospy.Rate(MONO_FPS) # 10hz

    while not rospy.is_shutdown():
        hello_str = "Publishing at stereo/image_raw %s" % rospy.get_time()
        #rospy.loginfo(hello_str)
            # Capture frame-by-frame
        ret, frame = cam.read()

        # Our operations on the frame comes here
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        #cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        #pub.publish(hello_str)
	try:
	    pub.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
        except CvBridgeError as e:
            print(e)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
    cam1.release()
    cam2.release()
    cv2.destroyAllWindows()
