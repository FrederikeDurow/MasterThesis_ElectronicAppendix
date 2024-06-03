// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from proto2ros:msg/Bytes.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__BYTES__STRUCT_HPP_
#define PROTO2ROS__MSG__DETAIL__BYTES__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__proto2ros__msg__Bytes __attribute__((deprecated))
#else
# define DEPRECATED__proto2ros__msg__Bytes __declspec(deprecated)
#endif

namespace proto2ros
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Bytes_
{
  using Type = Bytes_<ContainerAllocator>;

  explicit Bytes_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit Bytes_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _data_type =
    std::vector<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>>;
  _data_type data;

  // setters for named parameter idiom
  Type & set__data(
    const std::vector<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>> & _arg)
  {
    this->data = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    proto2ros::msg::Bytes_<ContainerAllocator> *;
  using ConstRawPtr =
    const proto2ros::msg::Bytes_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<proto2ros::msg::Bytes_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<proto2ros::msg::Bytes_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      proto2ros::msg::Bytes_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<proto2ros::msg::Bytes_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      proto2ros::msg::Bytes_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<proto2ros::msg::Bytes_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<proto2ros::msg::Bytes_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<proto2ros::msg::Bytes_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__proto2ros__msg__Bytes
    std::shared_ptr<proto2ros::msg::Bytes_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__proto2ros__msg__Bytes
    std::shared_ptr<proto2ros::msg::Bytes_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Bytes_ & other) const
  {
    if (this->data != other.data) {
      return false;
    }
    return true;
  }
  bool operator!=(const Bytes_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Bytes_

// alias to use template instance with default allocator
using Bytes =
  proto2ros::msg::Bytes_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace proto2ros

#endif  // PROTO2ROS__MSG__DETAIL__BYTES__STRUCT_HPP_
