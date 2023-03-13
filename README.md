This node connects to a Tasmota-based BProtect board.
It gathers data about its operating conditions such as switch status, current and power and exports them as ros2-topics.

# rosinante_bprotect_interface

ROS2 node for gathering data from BProtect boards.

## Overview
The provided node connects to the interface of a Tasmota-based BProtect board via http.
The IP address of the board has to be set via the apropriate parameter.

The node publishes messages to *<node_name>/status*.
The appropriate message type ('Bprotectstatus') is defined in *rosinante_protect_interfaces*.

## ROS2 Parameters

| Parameter |  Type  | Description |
|:-----|:--------:|:---|
| `ip` | string | IP address of the BProtect board to connect to. |

