// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from proto2ros:msg/StructEntry.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__STRUCT_ENTRY__STRUCT_HPP_
#define PROTO2ROS__MSG__DETAIL__STRUCT_ENTRY__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'value'
#include "proto2ros/msg/detail/value__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__proto2ros__msg__StructEntry __attribute__((deprecated))
#else
# define DEPRECATED__proto2ros__msg__StructEntry __declspec(deprecated)
#endif

namespace proto2ros
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct StructEntry_
{
  using Type = StructEntry_<ContainerAllocator>;

  explicit StructEntry_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : value(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->key = "";
    }
  }

  explicit StructEntry_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : key(_alloc),
    value(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->key = "";
    }
  }

  // field types and members
  using _key_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _key_type key;
  using _value_type =
    proto2ros::msg::Value_<ContainerAllocator>;
  _value_type value;

  // setters for named parameter idiom
  Type & set__key(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->key = _arg;
    return *this;
  }
  Type & set__value(
    const proto2ros::msg::Value_<ContainerAllocator> & _arg)
  {
    this->value = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    proto2ros::msg::StructEntry_<ContainerAllocator> *;
  using ConstRawPtr =
    const proto2ros::msg::StructEntry_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<proto2ros::msg::StructEntry_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<proto2ros::msg::StructEntry_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      proto2ros::msg::StructEntry_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<proto2ros::msg::StructEntry_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      proto2ros::msg::StructEntry_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<proto2ros::msg::StructEntry_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<proto2ros::msg::StructEntry_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<proto2ros::msg::StructEntry_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__proto2ros__msg__StructEntry
    std::shared_ptr<proto2ros::msg::StructEntry_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__proto2ros__msg__StructEntry
    std::shared_ptr<proto2ros::msg::StructEntry_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const StructEntry_ & other) const
  {
    if (this->key != other.key) {
      return false;
    }
    if (this->value != other.value) {
      return false;
    }
    return true;
  }
  bool operator!=(const StructEntry_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct StructEntry_

// alias to use template instance with default allocator
using StructEntry =
  proto2ros::msg::StructEntry_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace proto2ros

#endif  // PROTO2ROS__MSG__DETAIL__STRUCT_ENTRY__STRUCT_HPP_
