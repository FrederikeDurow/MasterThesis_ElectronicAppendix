// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from proto2ros:msg/Any.idl
// generated code does not contain a copyright notice

#ifndef PROTO2ROS__MSG__DETAIL__ANY__FUNCTIONS_H_
#define PROTO2ROS__MSG__DETAIL__ANY__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "proto2ros/msg/rosidl_generator_c__visibility_control.h"

#include "proto2ros/msg/detail/any__struct.h"

/// Initialize msg/Any message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * proto2ros__msg__Any
 * )) before or use
 * proto2ros__msg__Any__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_proto2ros
bool
proto2ros__msg__Any__init(proto2ros__msg__Any * msg);

/// Finalize msg/Any message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_proto2ros
void
proto2ros__msg__Any__fini(proto2ros__msg__Any * msg);

/// Create msg/Any message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * proto2ros__msg__Any__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_proto2ros
proto2ros__msg__Any *
proto2ros__msg__Any__create();

/// Destroy msg/Any message.
/**
 * It calls
 * proto2ros__msg__Any__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_proto2ros
void
proto2ros__msg__Any__destroy(proto2ros__msg__Any * msg);

/// Check for msg/Any message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_proto2ros
bool
proto2ros__msg__Any__are_equal(const proto2ros__msg__Any * lhs, const proto2ros__msg__Any * rhs);

/// Copy a msg/Any message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_proto2ros
bool
proto2ros__msg__Any__copy(
  const proto2ros__msg__Any * input,
  proto2ros__msg__Any * output);

/// Initialize array of msg/Any messages.
/**
 * It allocates the memory for the number of elements and calls
 * proto2ros__msg__Any__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_proto2ros
bool
proto2ros__msg__Any__Sequence__init(proto2ros__msg__Any__Sequence * array, size_t size);

/// Finalize array of msg/Any messages.
/**
 * It calls
 * proto2ros__msg__Any__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_proto2ros
void
proto2ros__msg__Any__Sequence__fini(proto2ros__msg__Any__Sequence * array);

/// Create array of msg/Any messages.
/**
 * It allocates the memory for the array and calls
 * proto2ros__msg__Any__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_proto2ros
proto2ros__msg__Any__Sequence *
proto2ros__msg__Any__Sequence__create(size_t size);

/// Destroy array of msg/Any messages.
/**
 * It calls
 * proto2ros__msg__Any__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_proto2ros
void
proto2ros__msg__Any__Sequence__destroy(proto2ros__msg__Any__Sequence * array);

/// Check for msg/Any message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_proto2ros
bool
proto2ros__msg__Any__Sequence__are_equal(const proto2ros__msg__Any__Sequence * lhs, const proto2ros__msg__Any__Sequence * rhs);

/// Copy an array of msg/Any messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_proto2ros
bool
proto2ros__msg__Any__Sequence__copy(
  const proto2ros__msg__Any__Sequence * input,
  proto2ros__msg__Any__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // PROTO2ROS__MSG__DETAIL__ANY__FUNCTIONS_H_
