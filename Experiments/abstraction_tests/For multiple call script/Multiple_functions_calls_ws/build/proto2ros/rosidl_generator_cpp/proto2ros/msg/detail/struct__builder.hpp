// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from proto2ros:msg/Struct.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__STRUCT__BUILDER_HPP_
#define PROTO2ROS__MSG__DETAIL__STRUCT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "proto2ros/msg/detail/struct__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace proto2ros
{

namespace msg
{

namespace builder
{

class Init_Struct_fields
{
public:
  Init_Struct_fields()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::proto2ros::msg::Struct fields(::proto2ros::msg::Struct::_fields_type arg)
  {
    msg_.fields = std::move(arg);
    return std::move(msg_);
  }

private:
  ::proto2ros::msg::Struct msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::proto2ros::msg::Struct>()
{
  return proto2ros::msg::builder::Init_Struct_fields();
}

}  // namespace proto2ros

#endif  // PROTO2ROS__MSG__DETAIL__STRUCT__BUILDER_HPP_
