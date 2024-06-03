// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from proto2ros:msg/Bytes.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__BYTES__BUILDER_HPP_
#define PROTO2ROS__MSG__DETAIL__BYTES__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "proto2ros/msg/detail/bytes__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace proto2ros
{

namespace msg
{

namespace builder
{

class Init_Bytes_data
{
public:
  Init_Bytes_data()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::proto2ros::msg::Bytes data(::proto2ros::msg::Bytes::_data_type arg)
  {
    msg_.data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::proto2ros::msg::Bytes msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::proto2ros::msg::Bytes>()
{
  return proto2ros::msg::builder::Init_Bytes_data();
}

}  // namespace proto2ros

#endif  // PROTO2ROS__MSG__DETAIL__BYTES__BUILDER_HPP_
