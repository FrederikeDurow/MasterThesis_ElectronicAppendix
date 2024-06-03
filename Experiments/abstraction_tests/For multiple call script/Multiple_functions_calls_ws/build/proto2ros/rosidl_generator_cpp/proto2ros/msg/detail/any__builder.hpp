// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from proto2ros:msg/Any.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__ANY__BUILDER_HPP_
#define PROTO2ROS__MSG__DETAIL__ANY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "proto2ros/msg/detail/any__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace proto2ros
{

namespace msg
{

namespace builder
{

class Init_Any_value
{
public:
  explicit Init_Any_value(::proto2ros::msg::Any & msg)
  : msg_(msg)
  {}
  ::proto2ros::msg::Any value(::proto2ros::msg::Any::_value_type arg)
  {
    msg_.value = std::move(arg);
    return std::move(msg_);
  }

private:
  ::proto2ros::msg::Any msg_;
};

class Init_Any_type_name
{
public:
  Init_Any_type_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Any_value type_name(::proto2ros::msg::Any::_type_name_type arg)
  {
    msg_.type_name = std::move(arg);
    return Init_Any_value(msg_);
  }

private:
  ::proto2ros::msg::Any msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::proto2ros::msg::Any>()
{
  return proto2ros::msg::builder::Init_Any_type_name();
}

}  // namespace proto2ros

#endif  // PROTO2ROS__MSG__DETAIL__ANY__BUILDER_HPP_
