// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from proto2ros:msg/Any.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__ANY__STRUCT_H_
#define PROTO2ROS__MSG__DETAIL__ANY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'type_name'
#include "rosidl_runtime_c/string.h"
// Member 'value'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/Any in the package proto2ros.
/**
  * Copyright (c) 2023 Boston Dynamics AI Institute LLC. All rights reserved.
 */
typedef struct proto2ros__msg__Any
{
  /// A dynamically typed ROS 2 message.
  /// ROS 2 message type name
  rosidl_runtime_c__String type_name;
  /// Serialized ROS 2 message instance
  rosidl_runtime_c__uint8__Sequence value;
} proto2ros__msg__Any;

// Struct for a sequence of proto2ros__msg__Any.
typedef struct proto2ros__msg__Any__Sequence
{
  proto2ros__msg__Any * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} proto2ros__msg__Any__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PROTO2ROS__MSG__DETAIL__ANY__STRUCT_H_
