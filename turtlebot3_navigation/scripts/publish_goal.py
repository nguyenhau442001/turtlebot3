#!/usr/bin/env python
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import subprocess
import json
import rospy

from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseActionResult
from std_msgs.msg import String
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped

# Fetch the service account key JSON file contents
cred = credentials.Certificate('/home/amr/catkin_ws/src/turtlebot3/turtlebot3_navigation/scripts/pos-app-for-service-robot-firebase-adminsdk-7et03-c7457f5dcb.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pos-app-for-service-robot-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Get the root reference of the database
ref = db.reference('table')

# Declare name and status of all tables
NameTables         =['Home','T1','T2','T3','T4','T5','T6','T7','T8','T9']
Status_isActivated =[False,False,False,False,False,False,False,False,False,False]
Status_isReached   =[False,False,False,False,False,False,False,False,False,False]


# Read the JSON file
file_path = '/home/amr/catkin_ws/src/turtlebot3/turtlebot3_navigation/scripts/goal.json'
with open(file_path, 'r') as json_file:
    data = json.load(json_file)

def goal_reached_callback(data):
    global current_table
    # Check if MoveBaseActionResult == reached and not to be home, current_table = 0 ~~ HOME
    if "Goal reached." in data.status.text:
        rospy.loginfo("GOAL REACHED")
        users_ref = ref.child(NameTables[current_table])
        users_ref.set({
        'isActivated': False,
        'isReached': True,
        'name':      NameTables[current_table],
        })

        file_path = '/home/amr/catkin_ws/src/turtlebot3/turtlebot3_navigation/scripts/goal.json'
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        if current_table != 0: 

            # Create a PoseStamped message
            rotate_goal_msg = PoseStamped()
            rotate_goal_msg.header.frame_id    = "map"
            rotate_goal_msg.pose.position.x    = data[NameTables[current_table]]["pose"]["position"]["x"]
            rotate_goal_msg.pose.position.y    = data[NameTables[current_table]]["pose"]["position"]["y"]
            rotate_goal_msg.pose.position.z    = 0.0
            rotate_goal_msg.pose.orientation.x = 0.0
            rotate_goal_msg.pose.orientation.y = 0.0
            rotate_goal_msg.pose.orientation.z = 1.0
            rotate_goal_msg.pose.orientation.w = 0.0

            # Publish the goal
            pub.publish(rotate_goal_msg)

            # # Delay for 2 seconds
            rospy.sleep(5.0)

            users_ref = ref.child(NameTables[0])
            users_ref.set({
            'isActivated': True,
            'isReached': False,
            'name':      NameTables[0],
            })
            # Create a PoseStamped message
            # home_goal_msg = PoseStamped()
            # home_goal_msg.header.frame_id    = "map"
            # home_goal_msg.pose.position.x    = -1.5
            # home_goal_msg.pose.position.y    = -0.5
            # home_goal_msg.pose.position.z    = 0.0
            # home_goal_msg.pose.orientation.x = 0.0
            # home_goal_msg.pose.orientation.y = 0.0
            # home_goal_msg.pose.orientation.z = 0.0
            # home_goal_msg.pose.orientation.w = 1.0

            # # Print the goal
            # rospy.loginfo(home_goal_msg)

            # # Publish the goal
            # pub.publish(home_goal_msg)

            # current_table = 0
        
# Set the initial values in the database
for i in range(10):
    users_ref = ref.child(NameTables[i])
    users_ref.set({
        'isActivated':  Status_isActivated[i],
        'isReached':    Status_isReached[i],
        'name':         NameTables[i],
    })

    print(users_ref.get())




# Reset isPublished variable in goal.json file
for i in range(10):
    data[NameTables[i]]["isPublished"] =False
    # Write isPublished status into Json
    with open(file_path, 'w') as json_file:
        # Write the JSON data to the file
        json.dump(data, json_file, indent=4, ensure_ascii=False)
        json_file.write('\n')



# Usage example
command = '''rostopic pub /initialpose geometry_msgs/PoseWithCovarianceStamped "{
    header: {
        frame_id: map
    },
    pose: {
        pose: {
            position: {
                x: -2.0,
                y: -0.5,
                z:  0.0
            },
            orientation: {
                x: 0.0,
                y: 0.0,
                z: 0.0,
                w: 1.0
            }
        }
    }
}"'''


# subprocess.call(command, shell=True)
if __name__ == '__main__':
    try:
        # Connect to ROS
        # Init node publish the goal
        rospy.init_node('goal_publisher', anonymous=True)
        pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
        rospy.sleep(1)  # Delay to allow the publisher to connect
            
        # Subscribe to the result topic
        rospy.Subscriber('/move_base/result', MoveBaseActionResult, goal_reached_callback)
        rate = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            for i in range(10):
                
                # Get the root reference of the database
                ref = db.reference('table')
                users_ref = ref.child(NameTables[i])

                # ((users_ref.get())["isActivated"] == True) and data[NameTables[i]]["isPublished"] ==False
                if users_ref.get()["isActivated"] == True:
                    current_table = i  
                    data[NameTables[i]]["isPublished"] =True

                    # Write isPublished status into Json
                    with open(file_path, 'w') as json_file:
                        # Write the JSON data to the file
                        json.dump(data, json_file, indent=4, ensure_ascii=False)
                        json_file.write('\n')

                    if i == 0:
                        rospy.loginfo("Home is activated")
                    else:
                        rospy.loginfo("Table " + str(i) + " is activated")

                    # Create a PoseStamped message
                    goal_msg = PoseStamped()
                    goal_msg.header.frame_id    = "map"
                    goal_msg.pose.position.x    = data[NameTables[current_table]]["pose"]["position"]["x"]
                    goal_msg.pose.position.y    = data[NameTables[current_table]]["pose"]["position"]["y"]
                    goal_msg.pose.position.z    = data[NameTables[current_table]]["pose"]["position"]["z"]
                    goal_msg.pose.orientation.x = data[NameTables[current_table]]["pose"]["orientation"]["x"]
                    goal_msg.pose.orientation.y = data[NameTables[current_table]]["pose"]["orientation"]["y"]
                    goal_msg.pose.orientation.z = data[NameTables[current_table]]["pose"]["orientation"]["z"]
                    goal_msg.pose.orientation.w = data[NameTables[current_table]]["pose"]["orientation"]["w"]

                    # Print the goal
                    print(goal_msg)

                    # Publish the goal
                    pub.publish(goal_msg)

                    rate.sleep()
                        # Keep the node running
                # rospy.spin()
            # Sleep to maintain the desired frequency

    except rospy.ROSInterruptException:
        pass
