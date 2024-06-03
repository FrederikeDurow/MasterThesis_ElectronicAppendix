// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from proto2ros:msg/AnyProto.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__ANY_PROTO__BUILDER_HPP_
#define PROTO2ROS__MSG__DETAIL__ANY_PROTO__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "proto2ros/msg/detail/any_proto__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace proto2ros
{

namespace msg
{

namespace builder
{

class Init_AnyProto_value
{
public:
  explicit Init_AnyProto_value(::proto2ros::msg::AnyProto & msg)
  : msg_(msg)
  {}
  ::proto2ros::msg::AnyProto value(::proto2ros::msg::AnyProto::_value_type arg)
  {
    msg_.value = std::move(arg);
    return std::move(msg_);
  }

private:
  ::proto2ros::msg::AnyProto msg_;
};

class Init_AnyProto_type_url
{
public:
  Init_AnyProto_type_url()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AnyProto_value type_url(::proto2ros::msg::AnyProto::_type_url_type arg)
  {
    msg_.type_url = std::move(arg);
    return Init_AnyProto_value(msg_);
  }

private:
  ::proto2ros::msg::AnyProto msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::proto2ros::msg::AnyProto>()
{
  return proto2ros::msg::builder::Init_AnyProto_type_url();
}

}  // namespace proto2ros

#endif  // PROTO2ROS__MSG__DETAIL__ANY_PROTO__BUILDER_HPP_
