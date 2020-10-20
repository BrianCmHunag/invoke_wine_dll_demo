
# Liunx ROS invoke Windows libraries.

We use ROS as main control process program, but sometimes we have Windows proprietaty softwares and libraries. 
Both of them are not compatible with each other. Either two machine or virtual machine can handle this problem, but they are not good methods.

I use [Wine](https://www.winehq.org/) and [Rosbridge](http://wiki.ros.org/rosbridge_suite) to deal with it. 
Wine is a compatibility layer capable of running Windows applications on POSIX-compliant (Ubuntu) operating systems. It translates Windows API calls into POSIX calls on-the-fly.
Rosbridge provides [python APIs](https://roslibpy.readthedocs.io/en/latest/readme.html#installation) to ROS functionality for non-ROS programs. So we can communicate with ROS master without installing ROS on our computer.


## Environment Setup:
1. Install ROS and Wine according to the official websites:
	<br>ROS:  [Ubuntu install of ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu)
	<br>Wine:  [Installing WineHQ packages](https://wiki.winehq.org/Ubuntu)
	<br> I installed ros-kinetic-desktop-full for ROS and stable branch for Wine. I also pushed this image [iles88039/ubuntu_ros_wine](https://hub.docker.com/repository/docker/iles88039/ubuntu_ros_wine) on my dockerhub for reference.
 
2. Install ROS package rosbridge_suite:
	<br>`$ sudo apt-get install ros-kinetic-rosbridge-suite`
	
3. Setup Wine environment:
	<br>`$ winecfg`
	<br>Click 'install' or 'agree' when Wine pops up any windows. Finally, choose Windows 10 for Windows verion in Wine configuration.
	By the way, a virtual C disk would be created at ~/.wine/C_drive after installation. This is because Windows need C disk to execute programs.
	> note: Wine command need normal user priviledge (root uesr is not allowed) to run it. So don't add sudo when type the command.
	
4. Install Windows Python2.7 in Wine.
	Download msi installer from official website: [Python 2.7 Release](https://www.python.org/download/releases/2.7/)
	<br>I chose 'Windows x86 MSI Installer' because my Windows dll is x86 (32bits). Use the command to install Python in Wine:
	<br>`$ wine msiexec /i python-2.7.14.msi`
	<br>It would pop up a installer window, click agree to install python.  
	
5. Install roslibpy:
	Roslibpy is a python library. We use its API as a interface and wrap our Window dll to communicate with ROS master without installing ROS on our computer. It uses WebSockets to connect to rosbridge_suite and provides publishing, subscribing, service calls, actionlib, TF, and other essential ROS functionality.
	<br> Use python package manager pip to install it:
	<br>`$ Wine pip roslibpy`
	
So far, We have already installed Wine, ROS and ROS package rosbridge_suite on Linux computer. And We also have configured Wine and install Window python and roslibpy in Wine.

optional:
If you want to test this repo in docker container, please note the priviledge problem. Because docker use root user as default, you may face problem when use Wine.
So after pulling the image iles88039/ubuntu_ros_wine, create a container and install rosbridge_suite as above. Then, we need to change the priviledge. 
Commit this container as a new image and create another new container based on this new image. Log in this new container as a normal user instead of root user.
By doing this, you can run wine command in container.

## Demo

Clone this repo in your ROS workspace. Remember to **source setup.bash**. 

### ROS command:

terminal1:
 <br>`$ roslaunch rosbridge_server rosbridge_websocket.launch`
 <br>Rosbridge_server provides a WebSocket connection so other programs can talk to ROS master via rosbridge.
 
terminal2:
 <br>`$ rosrun invoke_wine_dll_demo sub.py`
 <br>Run a ROS subscriber. Remember to make file executable.(chmod +x) 

### Wine command:

terminal3:
 <br>`$ wine python ros-hello-world-talker.py`
 <br>Run a roslibpy publisher which is executed in Wine.

	