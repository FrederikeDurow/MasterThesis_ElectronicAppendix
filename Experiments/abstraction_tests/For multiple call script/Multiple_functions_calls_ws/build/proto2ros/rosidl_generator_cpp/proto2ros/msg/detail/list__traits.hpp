// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from proto2ros:msg/List.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__LIST__TRAITS_HPP_
#define PROTO2ROS__MSG__DETAIL__LIST__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "proto2ros/msg/detail/list__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'values'
#include "proto2ros/msg/detail/value__traits.hpp"

namespace proto2ros
{

namespace msg
{

inline void to_flow_style_yaml(
  const List & msg,
  std::ostream & out)
{
  out << "{";
  // member: values
  {
    if (msg.values.size() == 0) {
      out << "values: []";
    } else {
      out << "values: [";
      size_t pending_items = msg.values.size();
      for (auto item : msg.values) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const List & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: values
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.values.size() == 0) {
      out << "values: []\n";
    } else {
      out << "values:\n";
      for (auto item : msg.values) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const List & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace proto2ros

namespace rosidl_generator_traits
{

[[deprecated("use proto2ros::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const proto2ros::msg::List & msg,
  std::ostream & out, size_t indentation = 0)
{
  proto2ros::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use proto2ros::msg::to_yaml() instead")]]
inline std::string to_yaml(const proto2ros::msg::List & msg)
{
  return proto2ros::msg::to_yaml(msg);
}

template<>
inline const char * data_type<proto2ros::msg::List>()
{
  return "proto2ros::msg::List";
}

template<>
inline const char * name<proto2ros::msg::List>()
{
  return "proto2ros/msg/List";
}

template<>
struct has_fixed_size<proto2ros::msg::List>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<proto2ros::msg::List>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<proto2ros::msg::List>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // PROTO2ROS__MSG__DETAIL__LIST__TRAITS_HPP_
