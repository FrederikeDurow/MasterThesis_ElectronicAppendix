// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from proto2ros:msg/Value.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "proto2ros/msg/detail/value__rosidl_typesupport_introspection_c.h"
#include "proto2ros/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "proto2ros/msg/detail/value__functions.h"
#include "proto2ros/msg/detail/value__struct.h"


// Include directives for member types
// Member `string_value`
#include "rosidl_runtime_c/string_functions.h"
// Member `struct_value`
// Member `list_value`
#include "proto2ros/msg/any.h"
// Member `struct_value`
// Member `list_value`
#include "proto2ros/msg/detail/any__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void proto2ros__msg__Value__rosidl_typesupport_introspection_c__Value_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  proto2ros__msg__Value__init(message_memory);
}

void proto2ros__msg__Value__rosidl_typesupport_introspection_c__Value_fini_function(void * message_memory)
{
  proto2ros__msg__Value__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember proto2ros__msg__Value__rosidl_typesupport_introspection_c__Value_message_member_array[6] = {
  {
    "kind",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(proto2ros__msg__Value, kind),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "number_value",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(proto2ros__msg__Value, number_value),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "string_value",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(proto2ros__msg__Value, string_value),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "bool_value",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(proto2ros__msg__Value, bool_value),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "struct_value",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(proto2ros__msg__Value, struct_value),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "list_value",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(proto2ros__msg__Value, list_value),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers proto2ros__msg__Value__rosidl_typesupport_introspection_c__Value_message_members = {
  "proto2ros__msg",  // message namespace
  "Value",  // message name
  6,  // number of fields
  sizeof(proto2ros__msg__Value),
  proto2ros__msg__Value__rosidl_typesupport_introspection_c__Value_message_member_array,  // message members
  proto2ros__msg__Value__rosidl_typesupport_introspection_c__Value_init_function,  // function to initialize message memory (memory has to be allocated)
  proto2ros__msg__Value__rosidl_typesupport_introspection_c__Value_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t proto2ros__msg__Value__rosidl_typesupport_introspection_c__Value_message_type_support_handle = {
  0,
  &proto2ros__msg__Value__rosidl_typesupport_introspection_c__Value_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_proto2ros
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, proto2ros, msg, Value)() {
  proto2ros__msg__Value__rosidl_typesupport_introspection_c__Value_message_member_array[4].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, proto2ros, msg, Any)();
  proto2ros__msg__Value__rosidl_typesupport_introspection_c__Value_message_member_array[5].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, proto2ros, msg, Any)();
  if (!proto2ros__msg__Value__rosidl_typesupport_introspection_c__Value_message_type_support_handle.typesupport_identifier) {
    proto2ros__msg__Value__rosidl_typesupport_introspection_c__Value_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &proto2ros__msg__Value__rosidl_typesupport_introspection_c__Value_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
