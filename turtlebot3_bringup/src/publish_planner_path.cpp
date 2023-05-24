#include <ros/ros.h>
#include <nav_msgs/Odometry.h>
#include <nav_msgs/Path.h>
#include <geometry_msgs/Point.h>
#include <geometry_msgs/PoseStamped.h>

class PathTracer
{
public:
    PathTracer()
    {
        path_pub_ = nh_.advertise<nav_msgs::Path>("/path", 10);
        path_.header.frame_id = "odom";
        last_time_ = ros::Time::now();
        odom_sub_ = nh_.subscribe("/odom", 1, &PathTracer::odom_callback, this);
    }

    void odom_callback(const nav_msgs::Odometry::ConstPtr& msg)
    {
        if ((ros::Time::now() - last_time_).toSec() >= 0.001)
        {
            last_time_ = ros::Time::now();

            geometry_msgs::PoseStamped pose;
            pose.header = msg->header;
            pose.pose.position = msg->pose.pose.position;
            path_.poses.push_back(pose);
            path_pub_.publish(path_);
        }
    }

private:
    ros::NodeHandle nh_;
    ros::Publisher path_pub_;
    ros::Subscriber odom_sub_;
    nav_msgs::Path path_;
    ros::Time last_time_;
};

int main(int argc, char** argv)
{
    ros::init(argc, argv, "path_tracer");
    PathTracer tracer;
    ros::spin();
    return 0;
}

