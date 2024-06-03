// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from proto2ros:msg/Bytes.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__BYTES__STRUCT_H_
#define PROTO2ROS__MSG__DETAIL__BYTES__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'data'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/Bytes in the package proto2ros.
/**
  * Copyright (c) 2023 Boston Dynamics AI Institute LLC. All rights reserved.
 */
typedef struct proto2ros__msg__Bytes
{
  /// A binary blob. Equivalent to the google.protobuf.BytesValue message, also used to map repeated bytes fields to
  /// the ROS 2 domain. See https://protobuf.dev/reference/protobuf/google.protobuf/#bytes-value for further reference.
  rosidl_runtime_c__uint8__Sequence data;
} proto2ros__msg__Bytes;

// Struct for a sequence of proto2ros__msg__Bytes.
typedef struct proto2ros__msg__Bytes__Sequence
{
  proto2ros__msg__Bytes * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} proto2ros__msg__Bytes__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PROTO2ROS__MSG__DETAIL__BYTES__STRUCT_H_
