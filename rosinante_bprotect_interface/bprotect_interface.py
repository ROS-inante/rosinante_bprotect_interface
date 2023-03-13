import time

import rclpy
import rclpy.node

import requests

from rosinante_bprotect_interfaces.msg import Bprotectstatus

class BatteryNode(rclpy.node.Node):

    period_ms = 250

    commands_ = {}
    values_   = {}

    publisher_ = None

    ip_addr_ = '';


    def __init__(self):
        super().__init__('battery_node')

        self.declare_parameter('ip', '')
        self.ip_addr_ = self.get_parameter('ip').get_parameter_value().string_value

        self.add_command('BAT_PWR')
        self.add_command('BAT_VOLTAGE')
        self.add_command('BAT_CURRENT')
        self.add_command('BAT_SWITCH')
        self.add_command('BAT_OK')
        
        self.publisher_ = self.create_publisher(Bprotectstatus, f'{self.get_name()}/status', 10)


        self.timer = self.create_timer(self.period_ms/1000, self.timer_callback)

        self.get_logger().info("battery_node successfully started.")

    def timer_callback(self):
        ## Request data from BProtect
        for key, value in self.commands_.items():
            r = requests.get(f'http://{self.ip_addr_}/cm?cmnd={key}')
            for k, v in r.json().items():
                self.values_[k] = v 

        msg = Bprotectstatus()

        msg.header.stamp = self.get_clock().now().to_msg()

        msg.power = float(self.values_['BAT_PWR'])
        msg.voltage = float(self.values_['BAT_VOLTAGE'])
        msg.current = float(self.values_['BAT_CURRENT'])
        msg.switch_state = int(self.values_['BAT_SWITCH'])
        msg.ok = int(self.values_['BAT_OK'])


        ## Publish data to ROS

        self.publisher_.publish(msg)

    def add_command(self, cmd_str):
        self.commands_[cmd_str] = f'http://{self.ip_addr_}/cm?cmnd={cmd_str}'
        self.values_[cmd_str] = 0.0


def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

