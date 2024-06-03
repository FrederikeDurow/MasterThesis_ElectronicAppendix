// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from proto2ros:msg/List.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__LIST__BUILDER_HPP_
#define PROTO2ROS__MSG__DETAIL__LIST__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "proto2ros/msg/detail/list__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace proto2ros
{

namespace msg
{

namespace builder
{

class Init_List_values
{
public:
  Init_List_values()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::proto2ros::msg::List values(::proto2ros::msg::List::_values_type arg)
  {
    msg_.values = std::move(arg);
    return std::move(msg_);
  }

private:
  ::proto2ros::msg::List msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::proto2ros::msg::List>()
{
  return proto2ros::msg::builder::Init_List_values();
}

}  // namespace proto2ros

#endif  // PROTO2ROS__MSG__DETAIL__LIST__BUILDER_HPP_
