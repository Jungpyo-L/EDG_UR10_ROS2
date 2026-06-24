# EDG UR10 ROS 2 Package

This package contains the ROS 2 version of the EDG UR10 experiment tools. It is used for UR10 robot control, TCP pose publishing, ATI force/torque streaming, live PlotJuggler visualization, and experiment data logging.

## Supported Platform

- Ubuntu 24.04
- ROS 2 Jazzy Jalisco
- Universal Robots ROS 2 driver stack
- ATI NetFT sensor support through the ROS 2 `edg_netft_ros2` package

The ROS package name is `edg_ur10`. This is an `ament_cmake` package that installs Python nodes as ROS 2 executables.

## Workspace Dependencies

This package depends on the separate EDG NetFT ROS 2 package for ATI force/torque sensor streaming:

```text
https://github.com/Jungpyo-L/edg_netft_ros2.git
```

Clone both packages into the same ROS 2 workspace:

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/Jungpyo-L/EDG_UR10_ROS2.git
git clone https://github.com/Jungpyo-L/edg_netft_ros2.git
```

The `edg_ur10` experiment launch file starts `edg_netft_ros2`'s `netft_node` automatically. Without `edg_netft_ros2` in the workspace, `ur_experiment.launch.py` will not be able to start the NetFT sensor node.

## Build

From the workspace root:

```bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select edg_ur10 edg_netft_ros2
source install/setup.bash
```

If launch files or config files were recently changed, rebuild `edg_ur10` and source the workspace again:

```bash
colcon build --packages-select edg_ur10
source install/setup.bash
```

## Launch Files

This package uses two main launch files. Run them from separate terminals when both robot control and experiment logging are needed.

### Robot Control, MoveIt, and RViz

`ur_control.launch.py` starts the Universal Robots ROS 2 driver and MoveIt. RViz is enabled by default.

```bash
ros2 launch edg_ur10 ur_control.launch.py
```

Default arguments:

```text
robot_ip:=10.0.0.1
ur_type:=ur10
launch_rviz:=true
headless_mode:=true
```

Example with a custom robot IP:

```bash
ros2 launch edg_ur10 ur_control.launch.py robot_ip:=10.0.0.1
```

`headless_mode:=true` tells the UR ROS 2 driver to send the External Control program to the robot automatically. If this does not work with the robot controller version, run the External Control program manually on the teach pendant.

### Experiment, NetFT, Data Logger, and PlotJuggler

`ur_experiment.launch.py` starts:

- `robotStatePublisher.py`
- `netft_node`
- `data_logger.py`
- PlotJuggler

```bash
ros2 launch edg_ur10 ur_experiment.launch.py
```

Default arguments:

```text
ati_ip:=192.168.1.42
robot_ip:=10.0.0.1
launch_plot:=true
plotjuggler_layout:=<edg_ur10 share>/config/PlotJuggler_default_layout.xml
```

Example with a custom ATI sensor IP:

```bash
ros2 launch edg_ur10 ur_experiment.launch.py ati_ip:=192.168.1.42
```

To disable PlotJuggler:

```bash
ros2 launch edg_ur10 ur_experiment.launch.py launch_plot:=false
```

To load a different PlotJuggler layout:

```bash
ros2 launch edg_ur10 ur_experiment.launch.py plotjuggler_layout:=/path/to/my_preset.xml
```

## Important Topics

`robotStatePublisher.py` publishes the robot TCP pose:

```text
/endEffectorPose
```

`netft_node` publishes ATI force/torque data:

```text
/netft_data
/netft_ready
/diagnostics
```

Check that the NetFT node is alive with:

```bash
ros2 node list | grep netft
ros2 topic list | grep netft
```

The default NetFT data topic is `/netft_data`, published as `geometry_msgs/msg/WrenchStamped`.

## PlotJuggler

PlotJuggler is launched automatically by `ur_experiment.launch.py` when `launch_plot:=true`. The default layout is:

```text
config/PlotJuggler_default_layout.xml
```

You can also open the layout manually:

```bash
ros2 run plotjuggler plotjuggler --layout ~/ros2_ws/src/EDG_UR10_ROS2/config/PlotJuggler_default_layout.xml
```

For live ROS 2 data, use the ROS 2 data streamer in PlotJuggler and select topics such as `/netft_data`.

## Data Logging

`data_logger.py` records the topics listed in:

```text
config/TopicsList.txt
```

The current default list is:

```text
/endEffectorPose
/netft_data
/sync
```

Add topic names to `TopicsList.txt` if additional experiment topics should be logged. The helper code can save experiment output as `.mat` files for later analysis.

For ROS 2 bag recording, use `ros2 bag` separately, for example:

```bash
ros2 bag record /endEffectorPose /netft_data /sync
```

## Example Nodes

Run installed Python examples with `ros2 run`:

```bash
ros2 run edg_ur10 simple_robot_control.py
ros2 run edg_ur10 simple_data_log.py
ros2 run edg_ur10 simple_experiment.py
```

Before running robot motion examples, make sure `ur_control.launch.py` is running and the UR driver controller is active.

## Helper Modules

The helper modules are installed from `src/helperFunction`.

- `rtde_helper.py` contains UR RTDE helper functions for robot motion and TCP pose access.
- `FT_callback_helper.py` subscribes to `/netft_data` and provides force/torque filtering and offset handling.
- `transformation_matrix.py` contains pose and transformation matrix helpers.
- `fileSaveHelper.py` contains experiment file saving helpers, including `.mat` export.
- `utils.py` contains math utilities used by the robot control scripts.

## Troubleshooting

If `netft_node` does not publish `/netft_data`, check that the node is still running and that the ATI sensor IP is correct:

```bash
ros2 node list
ros2 topic list | grep netft
```

If ROS cannot write logs because of permissions, use a workspace log directory:

```bash
export ROS_LOG_DIR=~/ros2_ws/log/ros
```

If deleted packages still appear after tab completion or in the install folder, remove that package's `build/`, `install/`, and `log/` artifacts, then rebuild and source the workspace again.

## Author

Please contact the author with questions.

Jungpyo Lee

- Email: jungpyolee@berkeley.edu
- GitHub: [@Jungpyo-L](https://github.com/Jungpyo-L)
