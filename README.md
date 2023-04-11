# PART I. OVERVIEW ESSENTIAL PART COMMUNICATE
1.Introduction

In order to communicate with ROS, the first step we need do is install the rosserial package. But you need to determine what is the package fit your microcontroller, I use STM32DUINO so I will install rosserial package for arduino.

![image](https://user-images.githubusercontent.com/105471622/196738444-9dd84fe6-eab7-49eb-9ac8-48d59ac44471.png)

Next step, we need determine how many topic neccesary for this application.

Publisher node (buffer size is 1024 bytes)
1.	sensor_state [turtlebot3_msgs/SensorState]  (may be need)
2.	version_info [turtlebot3_msgs/VersionInfo] (optional)
3.	imu [sensor_msgs/Imu] (compulsory)
4.	odom [nav_msgs/Odometry] (compulsory)
5.	battery_state [sensor_msgs/BatteryState] (optional)
6.	joint_states [sensor_msgs/JointState] (compulsory)
7.	magnetic_field [sensor_msgs/MagneticField] (compulsory)
8.	/tf [tf/tfMessage] (compulsory)

Subscribe node (buffer size is 1024 bytes)
1.	cmd_vel [geometry_msgs/Twist] (compulsory)
2.	reset [std_msgs/Empty] (compulsory)

Set up TF (Transformation) 
1.	 Setup TF on Odometry [odom]
2.	 Setup TF on IMU [imu_link]
3.	 Setup TF on MagneticField [mag_link]
4.	 Setup TF on JointState [base_link]


# PART 2: KINETIC DIFFERENTIAL DRIVE MOBILE BOT

The common method to get kinetic mobile robot, we consider as the picture it illustrate for basic model kinetic differential drive robot:

![image](https://user-images.githubusercontent.com/105471622/196739775-1a44c4a5-01c2-4700-9e5d-425551a7759b.png)

We assumed the robot rotate around any point, in instantaneous time we can consider motion is linear, so the linear velocity of the center has the formula:
                                                           
![image](https://user-images.githubusercontent.com/105471622/196741436-15c1fd77-d795-4a25-a4a0-d9e12acdfa1e.png)    
  
                                                           
Where v_l,v_r, v is left linear velocity of left,right,center of robot corresponding.

Have again

![image](https://user-images.githubusercontent.com/105471622/196741249-5b3fbe59-4a76-44c8-aabf-4c947f89cb83.png)

       
We do some projection velocity vector into flat plane, we obtain the velocity of x-axis and y-axis corresponding

![image](https://user-images.githubusercontent.com/105471622/196741322-f6b99628-0699-491f-a43b-45fbad0ea03c.png)

![image](https://user-images.githubusercontent.com/105471622/196741718-e606f7e6-6795-4b15-957f-ffa9e9ec9aac.png)

![image](https://user-images.githubusercontent.com/105471622/196741850-9b6f7e35-a65c-4105-bda0-21b122a5f165.png)

We can rewrite motion as below matrix form:

![image](https://user-images.githubusercontent.com/105471622/196741958-2b4bbf91-5204-40cc-ba7b-d752b0125322.png)
 
 
From the (3) and (8) equations, we extract:

![image](https://user-images.githubusercontent.com/105471622/196742093-a1ed9284-a8a0-402f-8e99-ec90b3971ee9.png)

![image](https://user-images.githubusercontent.com/105471622/196742140-82b8dacb-5b20-4bc0-bb91-6ab5284957ba.png)

I introduce the algorithm powerful and popular name DEAD RECKONING.

In navigation, dead reckoning is the process of calculating the current position of a moving object using a previously determined or fixed position and then combining estimates of speed, direction, and distance, time past. A corresponding term in biology is used to describe the processes by which animals update their estimate of their position or orientation. Inertial navigation systems, which provide directional information, use dead reckoning and are very widely used.
Similarly, we also apply dead reckoning to the kinetic model of the robot, and it is described as follows:

![image](https://user-images.githubusercontent.com/105471622/196742559-bfeab541-b302-47aa-b34a-11964c2cefc3.png)

Figure 1 Kinetic model of the robot

(Source: Authors: Kooktae Lee, Changbae Jung and Woojin Chung, Article “Accurate calibration of kinematic parameters for two wheel differential mobile robots”)

From the figure above we get the following equations:

![image](https://user-images.githubusercontent.com/105471622/196742675-031d5c8e-f262-4da4-b9b3-64daa166e8aa.png)

![image](https://user-images.githubusercontent.com/105471622/196742932-7de7ea88-3c02-42c7-a5be-5f41f2c4b845.png)

![image](https://user-images.githubusercontent.com/105471622/196742962-79cd54a2-f0b2-42af-8469-8f661ff43faf.png)

Wheel Encoder

An encoder is a mechanical motion sensor that generates a digital signal in response to the motion. An electromechanical device capable of converting motion into a digital signal or pulse. Thanks to the encoder, we can know the exact position of the rotation angle of the motor shaft, thereby calculating the displacement of the center of gravity of the robot. More specifically, to calculate equations (13), (14) we need to know the number of pulses reads, and ticks.
Assuming we have the right and left motor with a resolution , to know how much the wheel has rotated, we need to know how much an angle the wheel rotates according to 1 pulse (tick). For example, the motor uses a resolution of 4000 (pulses/rev), through the transmission ratio of 1:3, this means that the motor turns 3 revolutions the wheel only turns one revolution. Then 1 tick will be calculated as follows:

![image](https://user-images.githubusercontent.com/105471622/196743383-fd141aac-da01-450d-b8fb-a0bbd2de20ec.png)

The angular displacement of each wheel will be calculated as follows:

![image](https://user-images.githubusercontent.com/105471622/196743448-f78aeeca-92b7-4f52-9693-2a5647183bc3.png)

The workflow of control mobile base
![image](https://user-images.githubusercontent.com/105471622/196743528-ea7499db-eb1f-446d-af67-6e7ae8fc3f8e.png)

Keep in mind that the velocity pair sent down by Navigation stack is not constant in continuous time but it is discrete, i.e. every time delta T, this velocity pair value it will be different, it is still constant, but only for a period of delta T. So to control the robot base, we update the velocity value, but because the time is very small (select 0.001s), it can be considered as continuous.

# PART3 MAGNETOMETER CALIBRATION

MPU9250 is actually an IMU (Inertial Measurement Unit) sensor and a Magnetometer, the task of the IMU will measure inertia (including angular velocity and linear acceleration), while the Magnetometer will measure the local magnetic field. around the sensor.
The MPU9250 helps to give an exact orientation of an object with respect to its environment. It plays an important role in navigating aircraft and spacecraft. Similar in applications of self-propelled robots, we can use MPU9250 to determine the direction and coordinates of the robot. From quantities such as acceleration, angular velocity, magnetic field of the robot then converted to rotation angle of the robot.
Currently, I still not yet using Madgwick for some reason such as : error due to integral, drift. I compute yaw angle base on magnetic field. Unfortunely, hard ion and soft ion cause distortion for magnetic field. So before use it, we need to calibrate it!!!!!!!

![image](https://user-images.githubusercontent.com/105471622/196747454-4ccb4b54-f55b-4860-8dbc-64c5a87708be.png)
![image](https://user-images.githubusercontent.com/105471622/196747463-0b68a5cc-1d76-4ce3-bcfa-af1b18e30b0a.png)
![image](https://user-images.githubusercontent.com/105471622/196747485-adc2ecc4-9105-45e3-84cf-9c7852b76c33.png)

We can completely edit the magnetic field with the formula below:

![image](https://user-images.githubusercontent.com/105471622/196747610-597e5c3b-2191-46ae-8653-e50d8d5e3e98.png)

Where h_hat: calibration magnetic matrix, h_m magnetic sensor magnetic matrix, b: offset matrix, M: hard and soft iron matrix system.

The result after calibrated:

![image](https://user-images.githubusercontent.com/105471622/196747814-774c0011-895e-46ed-9a9d-c82106091522.png)

The yaw angle equal atan(my,mx).


 
PART 4: TRANSFORMATION IN ROBOTIC

This section very importance for the autonomous robot system. If you already learn about robot engineering subject, you heard about "transformation" and "frame". In ROS, we dont use "frame", we use "link", it has the same meaning.
So in mobile robot, how many link was used? The answer is it depend on your own robot, the ROBOTIS's open source contain a lot of link, but to me, it is not neccessary to use all of it. 

To me, I used "map", "odom", "base_link", "laser", "wheel_right_link", "wheel_left_link" and "imu_link". It is all about I need.
You still work well at SLAM section, but when getting NAVIGATION STACK section, you will encounter some error if dont understanding fully. 

The consecutive transformation will be map -> odom -> base_link -> laser/wheel_right_link/wheel_left_link/imu_link
In default, the transformation between map and odom frame wasn't defined automatically,  you need to do it.

So in amcl.launch file, you need to add   
node pkg="tf" type="static_transform_publisher" name="map_odom_broadcaster"
      args="0 0 0 0 0 0 map odom 100"
      
cd ~/catkin_ws/src && git clone https://github.com/Slamtec/rplidar_ros.git && cd .. && catkin_make

export TURTLEBOT3_MODEL=burger && roslaunch turtlebot3_bringup turtlebot3_robot.launch

export TURTLEBOT3_MODEL=burger && roslaunch turtlebot3_slam turtlebot3_slam.launch

export TURTLEBOT3_MODEL=burger && roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/map.yaml

View frames can generate a pdf file with a graphical representation of the complete tf tree. It also generates a number of time-related statistics. To run view frames, type:

  $ rosrun tf view_frames

In the current working folder, you should now have a file called "frames.pdf". Open the file:

  $ evince frames.pdf
  
 
 PART 5: EXPLORE_LITE (SIMULATION)
 
 1. export TURTLEBOT3_MODEL=burger && roslaunch turtlebot3_gazebo turtlebot3_world.launch
 2. export TURTLEBOT3_MODEL=burger && roslaunch turtlebot3_slam turtlebot3_slam.launch slam_methods:=gmapping
 3. export TURTLEBOT3_MODEL=burger && roslaunch turtlebot3_navigation move_base.launch
 4. roslaunch explore_lite explore.launch
 5. roslaunch error_calculator error_calculator.launch
