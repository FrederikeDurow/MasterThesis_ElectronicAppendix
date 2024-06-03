// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from proto2ros:msg/StructEntry.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "proto2ros/msg/detail/struct_entry__struct.hpp"
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

void StructEntry_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) proto2ros::msg::StructEntry(_init);
}

void StructEntry_fini_function(void * message_memory)
{
  auto typed_message = static_cast<proto2ros::msg::StructEntry *>(message_memory);
  typed_message->~StructEntry();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember StructEntry_message_member_array[2] = {
  {
    "key",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(proto2ros::msg::StructEntry, key),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "value",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<proto2ros::msg::Value>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(proto2ros::msg::StructEntry, value),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers StructEntry_message_members = {
  "proto2ros::msg",  // message namespace
  "StructEntry",  // message name
  2,  // number of fields
  sizeof(proto2ros::msg::StructEntry),
  StructEntry_message_member_array,  // message members
  StructEntry_init_function,  // function to initialize message memory (memory has to be allocated)
  StructEntry_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t StructEntry_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &StructEntry_message_members,
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
get_message_type_support_handle<proto2ros::msg::StructEntry>()
{
  return &::proto2ros::msg::rosidl_typesupport_introspection_cpp::StructEntry_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, proto2ros, msg, StructEntry)() {
  return &::proto2ros::msg::rosidl_typesupport_introspection_cpp::StructEntry_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif