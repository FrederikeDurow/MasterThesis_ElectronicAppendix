// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from proto2ros:msg/List.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__LIST__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define PROTO2ROS__MSG__DETAIL__LIST__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "proto2ros/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "proto2ros/msg/detail/list__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace proto2ros
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_proto2ros
cdr_serialize(
  const proto2ros::msg::List & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_proto2ros
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  proto2ros::msg::List & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_proto2ros
get_serialized_size(
  const proto2ros::msg::List & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_proto2ros
max_serialized_size_List(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace proto2ros

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_proto2ros
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, proto2ros, msg, List)();

#ifdef __cplusplus
}
#endif

#endif  // PROTO2ROS__MSG__DETAIL__LIST__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
