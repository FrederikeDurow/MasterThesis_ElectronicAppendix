// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from proto2ros:msg/Any.idl
// generated code does not contain a copyright notice
#include "proto2ros/msg/detail/any__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "proto2ros/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "proto2ros/msg/detail/any__struct.h"
#include "proto2ros/msg/detail/any__functions.h"
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

#include "rosidl_runtime_c/primitives_sequence.h"  // value
#include "rosidl_runtime_c/primitives_sequence_functions.h"  // value
#include "rosidl_runtime_c/string.h"  // type_name
#include "rosidl_runtime_c/string_functions.h"  // type_name

// forward declare type support functions


using _Any__ros_msg_type = proto2ros__msg__Any;

static bool _Any__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _Any__ros_msg_type * ros_message = static_cast<const _Any__ros_msg_type *>(untyped_ros_message);
  // Field name: type_name
  {
    const rosidl_runtime_c__String * str = &ros_message->type_name;
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

  // Field name: value
  {
    size_t size = ros_message->value.size;
    auto array_ptr = ros_message->value.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  return true;
}

static bool _Any__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _Any__ros_msg_type * ros_message = static_cast<_Any__ros_msg_type *>(untyped_ros_message);
  // Field name: type_name
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->type_name.data) {
      rosidl_runtime_c__String__init(&ros_message->type_name);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->type_name,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'type_name'\n");
      return false;
    }
  }

  // Field name: value
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->value.data) {
      rosidl_runtime_c__uint8__Sequence__fini(&ros_message->value);
    }
    if (!rosidl_runtime_c__uint8__Sequence__init(&ros_message->value, size)) {
      fprintf(stderr, "failed to create array for field 'value'");
      return false;
    }
    auto array_ptr = ros_message->value.data;
    cdr.deserializeArray(array_ptr, size);
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_proto2ros
size_t get_serialized_size_proto2ros__msg__Any(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _Any__ros_msg_type * ros_message = static_cast<const _Any__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name type_name
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->type_name.size + 1);
  // field.name value
  {
    size_t array_size = ros_message->value.size;
    auto array_ptr = ros_message->value.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _Any__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_proto2ros__msg__Any(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_proto2ros
size_t max_serialized_size_proto2ros__msg__Any(
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

  // member: type_name
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
  // member: value
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = proto2ros__msg__Any;
    is_plain =
      (
      offsetof(DataType, value) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _Any__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_proto2ros__msg__Any(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_Any = {
  "proto2ros::msg",
  "Any",
  _Any__cdr_serialize,
  _Any__cdr_deserialize,
  _Any__get_serialized_size,
  _Any__max_serialized_size
};

static rosidl_message_type_support_t _Any__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_Any,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, proto2ros, msg, Any)() {
  return &_Any__type_support;
}

#if defined(__cplusplus)
}
#endif
