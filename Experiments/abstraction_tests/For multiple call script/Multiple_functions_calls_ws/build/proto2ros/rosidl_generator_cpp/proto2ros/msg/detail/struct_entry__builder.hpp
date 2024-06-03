// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from proto2ros:msg/StructEntry.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__STRUCT_ENTRY__BUILDER_HPP_
#define PROTO2ROS__MSG__DETAIL__STRUCT_ENTRY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "proto2ros/msg/detail/struct_entry__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace proto2ros
{

namespace msg
{

namespace builder
{

class Init_StructEntry_value
{
public:
  explicit Init_StructEntry_value(::proto2ros::msg::StructEntry & msg)
  : msg_(msg)
  {}
  ::proto2ros::msg::StructEntry value(::proto2ros::msg::StructEntry::_value_type arg)
  {
    msg_.value = std::move(arg);
    return std::move(msg_);
  }

private:
  ::proto2ros::msg::StructEntry msg_;
};

class Init_StructEntry_key
{
public:
  Init_StructEntry_key()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_StructEntry_value key(::proto2ros::msg::StructEntry::_key_type arg)
  {
    msg_.key = std::move(arg);
    return Init_StructEntry_value(msg_);
  }

private:
  ::proto2ros::msg::StructEntry msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::proto2ros::msg::StructEntry>()
{
  return proto2ros::msg::builder::Init_StructEntry_key();
}

}  // namespace proto2ros

#endif  // PROTO2ROS__MSG__DETAIL__STRUCT_ENTRY__BUILDER_HPP_
