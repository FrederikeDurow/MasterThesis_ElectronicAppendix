// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from proto2ros:msg/AnyProto.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "proto2ros/msg/detail/any_proto__rosidl_typesupport_introspection_c.h"
#include "proto2ros/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "proto2ros/msg/detail/any_proto__functions.h"
#include "proto2ros/msg/detail/any_proto__struct.h"


// Include directives for member types
// Member `type_url`
#include "rosidl_runtime_c/string_functions.h"
// Member `value`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__AnyProto_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  proto2ros__msg__AnyProto__init(message_memory);
}

void proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__AnyProto_fini_function(void * message_memory)
{
  proto2ros__msg__AnyProto__fini(message_memory);
}

size_t proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__size_function__AnyProto__value(
  const void * untyped_member)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return member->size;
}

const void * proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__get_const_function__AnyProto__value(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void * proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__get_function__AnyProto__value(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__fetch_function__AnyProto__value(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__get_const_function__AnyProto__value(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__assign_function__AnyProto__value(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__get_function__AnyProto__value(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

bool proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__resize_function__AnyProto__value(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  rosidl_runtime_c__uint8__Sequence__fini(member);
  return rosidl_runtime_c__uint8__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__AnyProto_message_member_array[2] = {
  {
    "type_url",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(proto2ros__msg__AnyProto, type_url),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "value",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(proto2ros__msg__AnyProto, value),  // bytes offset in struct
    NULL,  // default value
    proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__size_function__AnyProto__value,  // size() function pointer
    proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__get_const_function__AnyProto__value,  // get_const(index) function pointer
    proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__get_function__AnyProto__value,  // get(index) function pointer
    proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__fetch_function__AnyProto__value,  // fetch(index, &value) function pointer
    proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__assign_function__AnyProto__value,  // assign(index, value) function pointer
    proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__resize_function__AnyProto__value  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__AnyProto_message_members = {
  "proto2ros__msg",  // message namespace
  "AnyProto",  // message name
  2,  // number of fields
  sizeof(proto2ros__msg__AnyProto),
  proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__AnyProto_message_member_array,  // message members
  proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__AnyProto_init_function,  // function to initialize message memory (memory has to be allocated)
  proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__AnyProto_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__AnyProto_message_type_support_handle = {
  0,
  &proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__AnyProto_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_proto2ros
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, proto2ros, msg, AnyProto)() {
  if (!proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__AnyProto_message_type_support_handle.typesupport_identifier) {
    proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__AnyProto_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &proto2ros__msg__AnyProto__rosidl_typesupport_introspection_c__AnyProto_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
