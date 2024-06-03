// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from proto2ros:msg/Value.idl
// generated code does not contain a copyright notice
#include "proto2ros/msg/detail/value__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "proto2ros/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "proto2ros/msg/detail/value__struct.h"
#include "proto2ros/msg/detail/value__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "proto2ros/msg/detail/any__functions.h"  // list_value, struct_value
#include "rosidl_runtime_c/string.h"  // string_value
#include "rosidl_runtime_c/string_functions.h"  // string_value

// forward declare type support functions
size_t get_serialized_size_proto2ros__msg__Any(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_proto2ros__msg__Any(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, proto2ros, msg, Any)();


using _Value__ros_msg_type = proto2ros__msg__Value;

static bool _Value__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _Value__ros_msg_type * ros_message = static_cast<const _Value__ros_msg_type *>(untyped_ros_message);
  // Field name: kind
  {
    cdr << ros_message->kind;
  }

  // Field name: number_value
  {
    cdr << ros_message->number_value;
  }

  // Field name: string_value
  {
    const rosidl_runtime_c__String * str = &ros_message->string_value;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: bool_value
  {
    cdr << (ros_message->bool_value ? true : false);
  }

  // Field name: struct_value
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, proto2ros, msg, Any
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->struct_value, cdr))
    {
      return false;
    }
  }

  // Field name: list_value
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, proto2ros, msg, Any
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->list_value, cdr))
    {
      return false;
    }
  }

  return true;
}

static bool _Value__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _Value__ros_msg_type * ros_message = static_cast<_Value__ros_msg_type *>(untyped_ros_message);
  // Field name: kind
  {
    cdr >> ros_message->kind;
  }

  // Field name: number_value
  {
    cdr >> ros_message->number_value;
  }

  // Field name: string_value
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->string_value.data) {
      rosidl_runtime_c__String__init(&ros_message->string_value);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->string_value,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'string_value'\n");
      return false;
    }
  }

  // Field name: bool_value
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->bool_value = tmp ? true : false;
  }

  // Field name: struct_value
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, proto2ros, msg, Any
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->struct_value))
    {
      return false;
    }
  }

  // Field name: list_value
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, proto2ros, msg, Any
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->list_value))
    {
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_proto2ros
size_t get_serialized_size_proto2ros__msg__Value(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _Value__ros_msg_type * ros_message = static_cast<const _Value__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name kind
  {
    size_t item_size = sizeof(ros_message->kind);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name number_value
  {
    size_t item_size = sizeof(ros_message->number_value);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name string_value
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->string_value.size + 1);
  // field.name bool_value
  {
    size_t item_size = sizeof(ros_message->bool_value);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name struct_value

  current_alignment += get_serialized_size_proto2ros__msg__Any(
    &(ros_message->struct_value), current_alignment);
  // field.name list_value

  current_alignment += get_serialized_size_proto2ros__msg__Any(
    &(ros_message->list_value), current_alignment);

  return current_alignment - initial_alignment;
}

static uint32_t _Value__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_proto2ros__msg__Value(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_proto2ros
size_t max_serialized_size_proto2ros__msg__Value(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: kind
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: number_value
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: string_value
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: bool_value
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: struct_value
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_proto2ros__msg__Any(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // member: list_value
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_proto2ros__msg__Any(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = proto2ros__msg__Value;
    is_plain =
      (
      offsetof(DataType, list_value) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _Value__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_proto2ros__msg__Value(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_Value = {
  "proto2ros::msg",
  "Value",
  _Value__cdr_serialize,
  _Value__cdr_deserialize,
  _Value__get_serialized_size,
  _Value__max_serialized_size
};

static rosidl_message_type_support_t _Value__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_Value,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, proto2ros, msg, Value)() {
  return &_Value__type_support;
}

#if defined(__cplusplus)
}
#endif
