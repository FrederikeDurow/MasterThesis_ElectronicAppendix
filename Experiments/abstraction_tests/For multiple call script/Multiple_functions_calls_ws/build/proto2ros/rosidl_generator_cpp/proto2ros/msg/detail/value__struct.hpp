// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from proto2ros:msg/Value.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__VALUE__STRUCT_HPP_
#define PROTO2ROS__MSG__DETAIL__VALUE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'struct_value'
// Member 'list_value'
#include "proto2ros/msg/detail/any__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__proto2ros__msg__Value __attribute__((deprecated))
#else
# define DEPRECATED__proto2ros__msg__Value __declspec(deprecated)
#endif

namespace proto2ros
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Value_
{
  using Type = Value_<ContainerAllocator>;

  explicit Value_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : struct_value(_init),
    list_value(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::DEFAULTS_ONLY == _init)
    {
      this->kind = 0;
    } else if (rosidl_runtime_cpp::MessageInitialization::ZERO == _init) {
      this->kind = 0;
      this->number_value = 0.0;
      this->string_value = "";
      this->bool_value = false;
    }
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->number_value = 0.0;
      this->string_value = "";
      this->bool_value = false;
    }
  }

  explicit Value_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : string_value(_alloc),
    struct_value(_alloc, _init),
    list_value(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::DEFAULTS_ONLY == _init)
    {
      this->kind = 0;
    } else if (rosidl_runtime_cpp::MessageInitialization::ZERO == _init) {
      this->kind = 0;
      this->number_value = 0.0;
      this->string_value = "";
      this->bool_value = false;
    }
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->number_value = 0.0;
      this->string_value = "";
      this->bool_value = false;
    }
  }

  // field types and members
  using _kind_type =
    int8_t;
  _kind_type kind;
  using _number_value_type =
    double;
  _number_value_type number_value;
  using _string_value_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _string_value_type string_value;
  using _bool_value_type =
    bool;
  _bool_value_type bool_value;
  using _struct_value_type =
    proto2ros::msg::Any_<ContainerAllocator>;
  _struct_value_type struct_value;
  using _list_value_type =
    proto2ros::msg::Any_<ContainerAllocator>;
  _list_value_type list_value;

  // setters for named parameter idiom
  Type & set__kind(
    const int8_t & _arg)
  {
    this->kind = _arg;
    return *this;
  }
  Type & set__number_value(
    const double & _arg)
  {
    this->number_value = _arg;
    return *this;
  }
  Type & set__string_value(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->string_value = _arg;
    return *this;
  }
  Type & set__bool_value(
    const bool & _arg)
  {
    this->bool_value = _arg;
    return *this;
  }
  Type & set__struct_value(
    const proto2ros::msg::Any_<ContainerAllocator> & _arg)
  {
    this->struct_value = _arg;
    return *this;
  }
  Type & set__list_value(
    const proto2ros::msg::Any_<ContainerAllocator> & _arg)
  {
    this->list_value = _arg;
    return *this;
  }

  // constant declarations
  static constexpr int8_t NO_VALUE_SET =
    0;
  static constexpr int8_t NUMBER_VALUE_SET =
    1;
  static constexpr int8_t STRING_VALUE_SET =
    2;
  static constexpr int8_t BOOL_VALUE_SET =
    3;
  static constexpr int8_t STRUCT_VALUE_SET =
    4;
  static constexpr int8_t LIST_VALUE_SET =
    5;

  // pointer types
  using RawPtr =
    proto2ros::msg::Value_<ContainerAllocator> *;
  using ConstRawPtr =
    const proto2ros::msg::Value_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<proto2ros::msg::Value_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<proto2ros::msg::Value_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      proto2ros::msg::Value_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<proto2ros::msg::Value_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      proto2ros::msg::Value_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<proto2ros::msg::Value_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<proto2ros::msg::Value_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<proto2ros::msg::Value_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__proto2ros__msg__Value
    std::shared_ptr<proto2ros::msg::Value_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__proto2ros__msg__Value
    std::shared_ptr<proto2ros::msg::Value_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Value_ & other) const
  {
    if (this->kind != other.kind) {
      return false;
    }
    if (this->number_value != other.number_value) {
      return false;
    }
    if (this->string_value != other.string_value) {
      return false;
    }
    if (this->bool_value != other.bool_value) {
      return false;
    }
    if (this->struct_value != other.struct_value) {
      return false;
    }
    if (this->list_value != other.list_value) {
      return false;
    }
    return true;
  }
  bool operator!=(const Value_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Value_

// alias to use template instance with default allocator
using Value =
  proto2ros::msg::Value_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr int8_t Value_<ContainerAllocator>::NO_VALUE_SET;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr int8_t Value_<ContainerAllocator>::NUMBER_VALUE_SET;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr int8_t Value_<ContainerAllocator>::STRING_VALUE_SET;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr int8_t Value_<ContainerAllocator>::BOOL_VALUE_SET;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr int8_t Value_<ContainerAllocator>::STRUCT_VALUE_SET;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr int8_t Value_<ContainerAllocator>::LIST_VALUE_SET;
#endif  // __cplusplus < 201703L

}  // namespace msg

}  // namespace proto2ros

#endif  // PROTO2ROS__MSG__DETAIL__VALUE__STRUCT_HPP_
