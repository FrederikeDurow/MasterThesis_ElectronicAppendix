// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from proto2ros:msg/Any.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__ANY__TRAITS_HPP_
#define PROTO2ROS__MSG__DETAIL__ANY__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "proto2ros/msg/detail/any__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace proto2ros
{

namespace msg
{

inline void to_flow_style_yaml(
  const Any & msg,
  std::ostream & out)
{
  out << "{";
  // member: type_name
  {
    out << "type_name: ";
    rosidl_generator_traits::value_to_yaml(msg.type_name, out);
    out << ", ";
  }

  // member: value
  {
    if (msg.value.size() == 0) {
      out << "value: []";
    } else {
      out << "value: [";
      size_t pending_items = msg.value.size();
      for (auto item : msg.value) {
        rosidl_generator_traits::value_to_yaml(item, out);
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
  const Any & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: type_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "type_name: ";
    rosidl_generator_traits::value_to_yaml(msg.type_name, out);
    out << "\n";
  }

  // member: value
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.value.size() == 0) {
      out << "value: []\n";
    } else {
      out << "value:\n";
      for (auto item : msg.value) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Any & msg, bool use_flow_style = false)
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
  const proto2ros::msg::Any & msg,
  std::ostream & out, size_t indentation = 0)
{
  proto2ros::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use proto2ros::msg::to_yaml() instead")]]
inline std::string to_yaml(const proto2ros::msg::Any & msg)
{
  return proto2ros::msg::to_yaml(msg);
}

template<>
inline const char * data_type<proto2ros::msg::Any>()
{
  return "proto2ros::msg::Any";
}

template<>
inline const char * name<proto2ros::msg::Any>()
{
  return "proto2ros/msg/Any";
}

template<>
struct has_fixed_size<proto2ros::msg::Any>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<proto2ros::msg::Any>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<proto2ros::msg::Any>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // PROTO2ROS__MSG__DETAIL__ANY__TRAITS_HPP_
