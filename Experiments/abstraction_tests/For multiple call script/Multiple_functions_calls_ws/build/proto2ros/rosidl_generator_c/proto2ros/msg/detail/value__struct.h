// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from proto2ros:msg/Value.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__VALUE__STRUCT_H_
#define PROTO2ROS__MSG__DETAIL__VALUE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Constant 'NO_VALUE_SET'.
/**
  * A dynamically typed (scalar or composite) value. Equivalent to the google.protobuf.Value message.
  * See https://protobuf.dev/reference/protobuf/google.protobuf/#value for further reference.
 */
enum
{
  proto2ros__msg__Value__NO_VALUE_SET = 0
};

/// Constant 'NUMBER_VALUE_SET'.
enum
{
  proto2ros__msg__Value__NUMBER_VALUE_SET = 1
};

/// Constant 'STRING_VALUE_SET'.
enum
{
  proto2ros__msg__Value__STRING_VALUE_SET = 2
};

/// Constant 'BOOL_VALUE_SET'.
enum
{
  proto2ros__msg__Value__BOOL_VALUE_SET = 3
};

/// Constant 'STRUCT_VALUE_SET'.
enum
{
  proto2ros__msg__Value__STRUCT_VALUE_SET = 4
};

/// Constant 'LIST_VALUE_SET'.
enum
{
  proto2ros__msg__Value__LIST_VALUE_SET = 5
};

// Include directives for member types
// Member 'string_value'
#include "rosidl_runtime_c/string.h"
// Member 'struct_value'
// Member 'list_value'
#include "proto2ros/msg/detail/any__struct.h"

/// Struct defined in msg/Value in the package proto2ros.
/**
  * Copyright (c) 2023 Boston Dynamics AI Institute LLC. All rights reserved.
 */
typedef struct proto2ros__msg__Value
{
  int8_t kind;
  double number_value;
  rosidl_runtime_c__String string_value;
  bool bool_value;
  /// is proto2ros/Struct
  proto2ros__msg__Any struct_value;
  /// is proto2ros/List
  proto2ros__msg__Any list_value;
} proto2ros__msg__Value;

// Struct for a sequence of proto2ros__msg__Value.
typedef struct proto2ros__msg__Value__Sequence
{
  proto2ros__msg__Value * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} proto2ros__msg__Value__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PROTO2ROS__MSG__DETAIL__VALUE__STRUCT_H_
