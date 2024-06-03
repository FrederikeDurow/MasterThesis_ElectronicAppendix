// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from proto2ros:msg/Value.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__VALUE__BUILDER_HPP_
#define PROTO2ROS__MSG__DETAIL__VALUE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "proto2ros/msg/detail/value__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace proto2ros
{

namespace msg
{

namespace builder
{

class Init_Value_list_value
{
public:
  explicit Init_Value_list_value(::proto2ros::msg::Value & msg)
  : msg_(msg)
  {}
  ::proto2ros::msg::Value list_value(::proto2ros::msg::Value::_list_value_type arg)
  {
    msg_.list_value = std::move(arg);
    return std::move(msg_);
  }

private:
  ::proto2ros::msg::Value msg_;
};

class Init_Value_struct_value
{
public:
  explicit Init_Value_struct_value(::proto2ros::msg::Value & msg)
  : msg_(msg)
  {}
  Init_Value_list_value struct_value(::proto2ros::msg::Value::_struct_value_type arg)
  {
    msg_.struct_value = std::move(arg);
    return Init_Value_list_value(msg_);
  }

private:
  ::proto2ros::msg::Value msg_;
};

class Init_Value_bool_value
{
public:
  explicit Init_Value_bool_value(::proto2ros::msg::Value & msg)
  : msg_(msg)
  {}
  Init_Value_struct_value bool_value(::proto2ros::msg::Value::_bool_value_type arg)
  {
    msg_.bool_value = std::move(arg);
    return Init_Value_struct_value(msg_);
  }

private:
  ::proto2ros::msg::Value msg_;
};

class Init_Value_string_value
{
public:
  explicit Init_Value_string_value(::proto2ros::msg::Value & msg)
  : msg_(msg)
  {}
  Init_Value_bool_value string_value(::proto2ros::msg::Value::_string_value_type arg)
  {
    msg_.string_value = std::move(arg);
    return Init_Value_bool_value(msg_);
  }

private:
  ::proto2ros::msg::Value msg_;
};

class Init_Value_number_value
{
public:
  explicit Init_Value_number_value(::proto2ros::msg::Value & msg)
  : msg_(msg)
  {}
  Init_Value_string_value number_value(::proto2ros::msg::Value::_number_value_type arg)
  {
    msg_.number_value = std::move(arg);
    return Init_Value_string_value(msg_);
  }

private:
  ::proto2ros::msg::Value msg_;
};

class Init_Value_kind
{
public:
  Init_Value_kind()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Value_number_value kind(::proto2ros::msg::Value::_kind_type arg)
  {
    msg_.kind = std::move(arg);
    return Init_Value_number_value(msg_);
  }

private:
  ::proto2ros::msg::Value msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::proto2ros::msg::Value>()
{
  return proto2ros::msg::builder::Init_Value_kind();
}

}  // namespace proto2ros

#endif  // PROTO2ROS__MSG__DETAIL__VALUE__BUILDER_HPP_
