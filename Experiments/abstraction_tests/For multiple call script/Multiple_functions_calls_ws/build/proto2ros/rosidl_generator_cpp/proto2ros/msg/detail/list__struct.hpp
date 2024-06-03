// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from proto2ros:msg/List.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__LIST__STRUCT_HPP_
#define PROTO2ROS__MSG__DETAIL__LIST__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'values'
#include "proto2ros/msg/detail/value__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__proto2ros__msg__List __attribute__((deprecated))
#else
# define DEPRECATED__proto2ros__msg__List __declspec(deprecated)
#endif

namespace proto2ros
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct List_
{
  using Type = List_<ContainerAllocator>;

  explicit List_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit List_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _values_type =
    std::vector<proto2ros::msg::Value_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<proto2ros::msg::Value_<ContainerAllocator>>>;
  _values_type values;

  // setters for named parameter idiom
  Type & set__values(
    const std::vector<proto2ros::msg::Value_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<proto2ros::msg::Value_<ContainerAllocator>>> & _arg)
  {
    this->values = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    proto2ros::msg::List_<ContainerAllocator> *;
  using ConstRawPtr =
    const proto2ros::msg::List_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<proto2ros::msg::List_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<proto2ros::msg::List_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      proto2ros::msg::List_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<proto2ros::msg::List_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      proto2ros::msg::List_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<proto2ros::msg::List_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<proto2ros::msg::List_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<proto2ros::msg::List_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__proto2ros__msg__List
    std::shared_ptr<proto2ros::msg::List_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__proto2ros__msg__List
    std::shared_ptr<proto2ros::msg::List_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const List_ & other) const
  {
    if (this->values != other.values) {
      return false;
    }
    return true;
  }
  bool operator!=(const List_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct List_

// alias to use template instance with default allocator
using List =
  proto2ros::msg::List_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace proto2ros

#endif  // PROTO2ROS__MSG__DETAIL__LIST__STRUCT_HPP_
