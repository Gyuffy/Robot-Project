// Copyright (c) 2021, Stogl Robotics Consulting UG (haftungsbeschränkt)
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

//
// Authors: Subhas Das, Denis Stogl
//

#ifndef ROS2_CONTROL_DEMO_EXAMPLE_5__EXTERNAL_RRBOT_FORCE_TORQUE_SENSOR_HPP_
#define ROS2_CONTROL_DEMO_EXAMPLE_5__EXTERNAL_RRBOT_FORCE_TORQUE_SENSOR_HPP_

#include <memory>
#include <string>
#include <vector>

#include "hardware_interface/handle.hpp"
#include "hardware_interface/hardware_info.hpp"
#include "hardware_interface/sensor_interface.hpp"
#include "hardware_interface/types/hardware_interface_return_values.hpp"
#include "rclcpp/clock.hpp"
#include "rclcpp/logger.hpp"
#include "rclcpp/macros.hpp"

namespace ros2_control_demo_example_5
{
class ExternalRRBotForceTorqueSensorHardware : public hardware_interface::SensorInterface
{
public:
  RCLCPP_SHARED_PTR_DEFINITIONS(ExternalRRBotForceTorqueSensorHardware);

  hardware_interface::CallbackReturn on_init(
    const hardware_interface::HardwareInfo & info) override;

  std::vector<hardware_interface::StateInterface> export_state_interfaces() override;

  hardware_interface::CallbackReturn on_activate(
    const rclcpp_lifecycle::State & previous_state) override;

  hardware_interface::CallbackReturn on_deactivate(
    const rclcpp_lifecycle::State & previous_state) override;

  hardware_interface::return_type read(
    const rclcpp::Time & time, const rclcpp::Duration & period) override;

  /// Get the logger of the SensorInterface.
  /**
   * \return logger of the SensorInterface.
   */
  rclcpp::Logger get_logger() const { return *logger_; }

  /// Get the clock of the SensorInterface.
  /**
   * \return clock of the SensorInterface.
   */
  rclcpp::Clock::SharedPtr get_clock() const { return clock_; }

private:
  // Parameters for the RRBot simulation
  double hw_start_sec_;
  double hw_stop_sec_;
  double hw_sensor_change_;

  // Objects for logging
  std::shared_ptr<rclcpp::Logger> logger_;
  rclcpp::Clock::SharedPtr clock_;

  // Store the sensor states for the simulated robot
  std::vector<double> hw_sensor_states_;
};

}  // namespace ros2_control_demo_example_5

#endif  // ROS2_CONTROL_DEMO_EXAMPLE_5__EXTERNAL_RRBOT_FORCE_TORQUE_SENSOR_HPP_
