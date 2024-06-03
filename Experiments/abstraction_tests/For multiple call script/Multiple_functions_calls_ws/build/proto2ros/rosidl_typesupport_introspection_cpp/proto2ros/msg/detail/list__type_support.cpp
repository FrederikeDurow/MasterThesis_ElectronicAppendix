// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from proto2ros:msg/List.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "proto2ros/msg/detail/list__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace proto2ros
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void List_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) proto2ros::msg::List(_init);
}

void List_fini_function(void * message_memory)
{
  auto typed_message = static_cast<proto2ros::msg::List *>(message_memory);
  typed_message->~List();
}

size_t size_function__List__values(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<proto2ros::msg::Value> *>(untyped_member);
  return member->size();
}

const void * get_const_function__List__values(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<proto2ros::msg::Value> *>(untyped_member);
  return &member[index];
}

void * get_function__List__values(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<proto2ros::msg::Value> *>(untyped_member);
  return &member[index];
}

void fetch_function__List__values(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const proto2ros::msg::Value *>(
    get_const_function__List__values(untyped_member, index));
  auto & value = *reinterpret_cast<proto2ros::msg::Value *>(untyped_value);
  value = item;
}

void assign_function__List__values(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<proto2ros::msg::Value *>(
    get_function__List__values(untyped_member, index));
  const auto & value = *reinterpret_cast<const proto2ros::msg::Value *>(untyped_value);
  item = value;
}

void resize_function__List__values(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<proto2ros::msg::Value> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember List_message_member_array[1] = {
  {
    "values",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<proto2ros::msg::Value>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(proto2ros::msg::List, values),  // bytes offset in struct
    nullptr,  // default value
    size_function__List__values,  // size() function pointer
    get_const_function__List__values,  // get_const(index) function pointer
    get_function__List__values,  // get(index) function pointer
    fetch_function__List__values,  // fetch(index, &value) function pointer
    assign_function__List__values,  // assign(index, value) function pointer
    resize_function__List__values  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers List_message_members = {
  "proto2ros::msg",  // message namespace
  "List",  // message name
  1,  // number of fields
  sizeof(proto2ros::msg::List),
  List_message_member_array,  // message members
  List_init_function,  // function to initialize message memory (memory has to be allocated)
  List_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t List_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &List_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace proto2ros


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<proto2ros::msg::List>()
{
  return &::proto2ros::msg::rosidl_typesupport_introspection_cpp::List_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, proto2ros, msg, List)() {
  return &::proto2ros::msg::rosidl_typesupport_introspection_cpp::List_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
