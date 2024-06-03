// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from proto2ros:msg/List.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__LIST__STRUCT_H_
#define PROTO2ROS__MSG__DETAIL__LIST__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'values'
#include "proto2ros/msg/detail/value__struct.h"

/// Struct defined in msg/List in the package proto2ros.
/**
  * Copyright (c) 2023 Boston Dynamics AI Institute LLC. All rights reserved.
 */
typedef struct proto2ros__msg__List
{
  /// A list of dynamically typed values. Equivalent to the google.protobuf.ListValue message.
  /// See https://protobuf.dev/reference/protobuf/google.protobuf/#list-value for further reference.
  proto2ros__msg__Value__Sequence values;
} proto2ros__msg__List;

// Struct for a sequence of proto2ros__msg__List.
typedef struct proto2ros__msg__List__Sequence
{
  proto2ros__msg__List * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} proto2ros__msg__List__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PROTO2ROS__MSG__DETAIL__LIST__STRUCT_H_
