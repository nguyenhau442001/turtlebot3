export TURTLEBOT3_MODEL=burger && roslaunch turtlebot3_bringup turtlebot3_robot.launch

export TURTLEBOT3_MODEL=burger && roslaunch turtlebot3_slam turtlebot3_gmapping.launch

View frames can generate a pdf file with a graphical representation of the complete tf tree. It also generates a number of time-related statistics. To run view frames, type:

  $ rosrun tf view_frames

In the current working folder, you should now have a file called "frames.pdf". Open the file:

  $ evince frames.pdf
