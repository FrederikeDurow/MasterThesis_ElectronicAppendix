// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from proto2ros:msg/Struct.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__STRUCT__STRUCT_H_
#define PROTO2ROS__MSG__DETAIL__STRUCT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'fields'
#include "proto2ros/msg/detail/struct_entry__struct.h"

/// Struct defined in msg/Struct in the package proto2ros.
/**
  * Copyright (c) 2023 Boston Dynamics AI Institute LLC. All rights reserved.
 */
typedef struct proto2ros__msg__Struct
{
  /// A structured data value with dynamically typed fields. Equivalent to the google.protobuf.Struct message.
  /// See https://protobuf.dev/reference/protobuf/google.protobuf/#struct for further reference.
  proto2ros__msg__StructEntry__Sequence fields;
} proto2ros__msg__Struct;

// Struct for a sequence of proto2ros__msg__Struct.
typedef struct proto2ros__msg__Struct__Sequence
{
  proto2ros__msg__Struct * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} proto2ros__msg__Struct__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PROTO2ROS__MSG__DETAIL__STRUCT__STRUCT_H_
