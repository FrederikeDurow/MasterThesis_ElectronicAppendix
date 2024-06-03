// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from proto2ros:msg/StructEntry.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__STRUCT_ENTRY__TRAITS_HPP_
#define PROTO2ROS__MSG__DETAIL__STRUCT_ENTRY__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "proto2ros/msg/detail/struct_entry__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'value'
#include "proto2ros/msg/detail/value__traits.hpp"

namespace proto2ros
{

namespace msg
{

inline void to_flow_style_yaml(
  const StructEntry & msg,
  std::ostream & out)
{
  out << "{";
  // member: key
  {
    out << "key: ";
    rosidl_generator_traits::value_to_yaml(msg.key, out);
    out << ", ";
  }

  // member: value
  {
    out << "value: ";
    to_flow_style_yaml(msg.value, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const StructEntry & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: key
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "key: ";
    rosidl_generator_traits::value_to_yaml(msg.key, out);
    out << "\n";
  }

  // member: value
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "value:\n";
    to_block_style_yaml(msg.value, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const StructEntry & msg, bool use_flow_style = false)
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
  const proto2ros::msg::StructEntry & msg,
  std::ostream & out, size_t indentation = 0)
{
  proto2ros::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use proto2ros::msg::to_yaml() instead")]]
inline std::string to_yaml(const proto2ros::msg::StructEntry & msg)
{
  return proto2ros::msg::to_yaml(msg);
}

template<>
inline const char * data_type<proto2ros::msg::StructEntry>()
{
  return "proto2ros::msg::StructEntry";
}

template<>
inline const char * name<proto2ros::msg::StructEntry>()
{
  return "proto2ros/msg/StructEntry";
}

template<>
struct has_fixed_size<proto2ros::msg::StructEntry>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<proto2ros::msg::StructEntry>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<proto2ros::msg::StructEntry>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // PROTO2ROS__MSG__DETAIL__STRUCT_ENTRY__TRAITS_HPP_
