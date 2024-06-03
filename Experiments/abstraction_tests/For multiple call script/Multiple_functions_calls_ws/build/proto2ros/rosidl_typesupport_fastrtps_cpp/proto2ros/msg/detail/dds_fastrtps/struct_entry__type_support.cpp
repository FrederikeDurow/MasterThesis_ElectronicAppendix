// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from proto2ros:msg/StructEntry.idl
// generated code does not contain a copyright notice
#include "proto2ros/msg/detail/struct_entry__rosidl_typesupport_fastrtps_cpp.hpp"
#include "proto2ros/msg/detail/struct_entry__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions
namespace proto2ros
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const proto2ros::msg::Value &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  proto2ros::msg::Value &);
size_t get_serialized_size(
  const proto2ros::msg::Value &,
  size_t current_alignment);
size_t
max_serialized_size_Value(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace proto2ros


namespace proto2ros
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_proto2ros
cdr_serialize(
  const proto2ros::msg::StructEntry & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: key
  cdr << ros_message.key;
  // Member: value
  proto2ros::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.value,
    cdr);
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_proto2ros
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  proto2ros::msg::StructEntry & ros_message)
{
  // Member: key
  cdr >> ros_message.key;

  // Member: value
  proto2ros::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.value);

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_proto2ros
get_serialized_size(
  const proto2ros::msg::StructEntry & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: key
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.key.size() + 1);
  // Member: value

  current_alignment +=
    proto2ros::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.value, current_alignment);

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_proto2ros
max_serialized_size_StructEntry(
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


  // Member: key
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

  // Member: value
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        proto2ros::msg::typesupport_fastrtps_cpp::max_serialized_size_Value(
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
    using DataType = proto2ros::msg::StructEntry;
    is_plain =
      (
      offsetof(DataType, value) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _StructEntry__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const proto2ros::msg::StructEntry *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _StructEntry__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<proto2ros::msg::StructEntry *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _StructEntry__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const proto2ros::msg::StructEntry *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _StructEntry__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_StructEntry(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _StructEntry__callbacks = {
  "proto2ros::msg",
  "StructEntry",
  _StructEntry__cdr_serialize,
  _StructEntry__cdr_deserialize,
  _StructEntry__get_serialized_size,
  _StructEntry__max_serialized_size
};

static rosidl_message_type_support_t _StructEntry__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_StructEntry__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace proto2ros

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_proto2ros
const rosidl_message_type_support_t *
get_message_type_support_handle<proto2ros::msg::StructEntry>()
{
  return &proto2ros::msg::typesupport_fastrtps_cpp::_StructEntry__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, proto2ros, msg, StructEntry)() {
  return &proto2ros::msg::typesupport_fastrtps_cpp::_StructEntry__handle;
}

#ifdef __cplusplus
}
#endif
