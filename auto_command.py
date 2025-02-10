#!/usr/bin/python3
import rospy
from std_msgs.msg import String
import subprocess
from pynput.keyboard import Controller, Key

keyboard = Controller()

def execute_terminal_command(command):
    subprocess.run(command, shell=True)

def callback(msg):
    command = msg.data.lower()

    if command == "forward":
        keyboard.press(Key.up)
        keyboard.release(Key.up)
    elif command == "left":
        keyboard.press(Key.left)
        keyboard.release(Key.left)
    elif command == "right":
        keyboard.press(Key.right)
        keyboard.release(Key.right)
    elif command == "stop":
        keyboard.press(Key.space)
        keyboard.release(Key.space)

def listener():
    rospy.init_node('keyboard_controller', anonymous=True)
    rospy.Subscriber('/robot_movement', String, callback)
    
    # Keep the script running
    rospy.spin()

if __name__ == "__main__":
    execute_terminal_command("echo 'Listening to /robot_movement topic...'")
    listener()

