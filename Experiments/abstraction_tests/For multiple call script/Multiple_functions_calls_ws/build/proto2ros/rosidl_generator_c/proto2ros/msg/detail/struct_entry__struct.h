// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from proto2ros:msg/StructEntry.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__STRUCT_ENTRY__STRUCT_H_
#define PROTO2ROS__MSG__DETAIL__STRUCT_ENTRY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'key'
#include "rosidl_runtime_c/string.h"
// Member 'value'
#include "proto2ros/msg/detail/value__struct.h"

/// Struct defined in msg/StructEntry in the package proto2ros.
/**
  * Copyright (c) 2023 Boston Dynamics AI Institute LLC. All rights reserved.
 */
typedef struct proto2ros__msg__StructEntry
{
  /// Key-value entries in the proto2ros/Struct ROS 2 message. Equivalent to
  /// the auxiliary Protobuf message used over-the-wire representation of the
  /// google.protobuf.Struct message.
  rosidl_runtime_c__String key;
  proto2ros__msg__Value value;
} proto2ros__msg__StructEntry;

// Struct for a sequence of proto2ros__msg__StructEntry.
typedef struct proto2ros__msg__StructEntry__Sequence
{
  proto2ros__msg__StructEntry * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} proto2ros__msg__StructEntry__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PROTO2ROS__MSG__DETAIL__STRUCT_ENTRY__STRUCT_H_
