// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from proto2ros:msg/Value.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__VALUE__TRAITS_HPP_
#define PROTO2ROS__MSG__DETAIL__VALUE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "proto2ros/msg/detail/value__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'struct_value'
// Member 'list_value'
#include "proto2ros/msg/detail/any__traits.hpp"

namespace proto2ros
{

namespace msg
{

inline void to_flow_style_yaml(
  const Value & msg,
  std::ostream & out)
{
  out << "{";
  // member: kind
  {
    out << "kind: ";
    rosidl_generator_traits::value_to_yaml(msg.kind, out);
    out << ", ";
  }

  // member: number_value
  {
    out << "number_value: ";
    rosidl_generator_traits::value_to_yaml(msg.number_value, out);
    out << ", ";
  }

  // member: string_value
  {
    out << "string_value: ";
    rosidl_generator_traits::value_to_yaml(msg.string_value, out);
    out << ", ";
  }

  // member: bool_value
  {
    out << "bool_value: ";
    rosidl_generator_traits::value_to_yaml(msg.bool_value, out);
    out << ", ";
  }

  // member: struct_value
  {
    out << "struct_value: ";
    to_flow_style_yaml(msg.struct_value, out);
    out << ", ";
  }

  // member: list_value
  {
    out << "list_value: ";
    to_flow_style_yaml(msg.list_value, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Value & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: kind
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "kind: ";
    rosidl_generator_traits::value_to_yaml(msg.kind, out);
    out << "\n";
  }

  // member: number_value
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "number_value: ";
    rosidl_generator_traits::value_to_yaml(msg.number_value, out);
    out << "\n";
  }

  // member: string_value
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "string_value: ";
    rosidl_generator_traits::value_to_yaml(msg.string_value, out);
    out << "\n";
  }

  // member: bool_value
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "bool_value: ";
    rosidl_generator_traits::value_to_yaml(msg.bool_value, out);
    out << "\n";
  }

  // member: struct_value
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "struct_value:\n";
    to_block_style_yaml(msg.struct_value, out, indentation + 2);
  }

  // member: list_value
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "list_value:\n";
    to_block_style_yaml(msg.list_value, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Value & msg, bool use_flow_style = false)
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
  const proto2ros::msg::Value & msg,
  std::ostream & out, size_t indentation = 0)
{
  proto2ros::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use proto2ros::msg::to_yaml() instead")]]
inline std::string to_yaml(const proto2ros::msg::Value & msg)
{
  return proto2ros::msg::to_yaml(msg);
}

template<>
inline const char * data_type<proto2ros::msg::Value>()
{
  return "proto2ros::msg::Value";
}

template<>
inline const char * name<proto2ros::msg::Value>()
{
  return "proto2ros/msg/Value";
}

template<>
struct has_fixed_size<proto2ros::msg::Value>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<proto2ros::msg::Value>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<proto2ros::msg::Value>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // PROTO2ROS__MSG__DETAIL__VALUE__TRAITS_HPP_
