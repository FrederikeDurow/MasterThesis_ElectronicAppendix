// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from proto2ros:msg/Value.idl
// generated code does not contain a copyright notice
#include "proto2ros/msg/detail/value__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `string_value`
#include "rosidl_runtime_c/string_functions.h"
// Member `struct_value`
// Member `list_value`
#include "proto2ros/msg/detail/any__functions.h"

bool
proto2ros__msg__Value__init(proto2ros__msg__Value * msg)
{
  if (!msg) {
    return false;
  }
  // kind
  msg->kind = 0;
  // number_value
  // string_value
  if (!rosidl_runtime_c__String__init(&msg->string_value)) {
    proto2ros__msg__Value__fini(msg);
    return false;
  }
  // bool_value
  // struct_value
  if (!proto2ros__msg__Any__init(&msg->struct_value)) {
    proto2ros__msg__Value__fini(msg);
    return false;
  }
  // list_value
  if (!proto2ros__msg__Any__init(&msg->list_value)) {
    proto2ros__msg__Value__fini(msg);
    return false;
  }
  return true;
}

void
proto2ros__msg__Value__fini(proto2ros__msg__Value * msg)
{
  if (!msg) {
    return;
  }
  // kind
  // number_value
  // string_value
  rosidl_runtime_c__String__fini(&msg->string_value);
  // bool_value
  // struct_value
  proto2ros__msg__Any__fini(&msg->struct_value);
  // list_value
  proto2ros__msg__Any__fini(&msg->list_value);
}

bool
proto2ros__msg__Value__are_equal(const proto2ros__msg__Value * lhs, const proto2ros__msg__Value * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // kind
  if (lhs->kind != rhs->kind) {
    return false;
  }
  // number_value
  if (lhs->number_value != rhs->number_value) {
    return false;
  }
  // string_value
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->string_value), &(rhs->string_value)))
  {
    return false;
  }
  // bool_value
  if (lhs->bool_value != rhs->bool_value) {
    return false;
  }
  // struct_value
  if (!proto2ros__msg__Any__are_equal(
      &(lhs->struct_value), &(rhs->struct_value)))
  {
    return false;
  }
  // list_value
  if (!proto2ros__msg__Any__are_equal(
      &(lhs->list_value), &(rhs->list_value)))
  {
    return false;
  }
  return true;
}

bool
proto2ros__msg__Value__copy(
  const proto2ros__msg__Value * input,
  proto2ros__msg__Value * output)
{
  if (!input || !output) {
    return false;
  }
  // kind
  output->kind = input->kind;
  // number_value
  output->number_value = input->number_value;
  // string_value
  if (!rosidl_runtime_c__String__copy(
      &(input->string_value), &(output->string_value)))
  {
    return false;
  }
  // bool_value
  output->bool_value = input->bool_value;
  // struct_value
  if (!proto2ros__msg__Any__copy(
      &(input->struct_value), &(output->struct_value)))
  {
    return false;
  }
  // list_value
  if (!proto2ros__msg__Any__copy(
      &(input->list_value), &(output->list_value)))
  {
    return false;
  }
  return true;
}

proto2ros__msg__Value *
proto2ros__msg__Value__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  proto2ros__msg__Value * msg = (proto2ros__msg__Value *)allocator.allocate(sizeof(proto2ros__msg__Value), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(proto2ros__msg__Value));
  bool success = proto2ros__msg__Value__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
proto2ros__msg__Value__destroy(proto2ros__msg__Value * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    proto2ros__msg__Value__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
proto2ros__msg__Value__Sequence__init(proto2ros__msg__Value__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  proto2ros__msg__Value * data = NULL;

  if (size) {
    data = (proto2ros__msg__Value *)allocator.zero_allocate(size, sizeof(proto2ros__msg__Value), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = proto2ros__msg__Value__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        proto2ros__msg__Value__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
proto2ros__msg__Value__Sequence__fini(proto2ros__msg__Value__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      proto2ros__msg__Value__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

proto2ros__msg__Value__Sequence *
proto2ros__msg__Value__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  proto2ros__msg__Value__Sequence * array = (proto2ros__msg__Value__Sequence *)allocator.allocate(sizeof(proto2ros__msg__Value__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = proto2ros__msg__Value__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
proto2ros__msg__Value__Sequence__destroy(proto2ros__msg__Value__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    proto2ros__msg__Value__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
proto2ros__msg__Value__Sequence__are_equal(const proto2ros__msg__Value__Sequence * lhs, const proto2ros__msg__Value__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!proto2ros__msg__Value__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
proto2ros__msg__Value__Sequence__copy(
  const proto2ros__msg__Value__Sequence * input,
  proto2ros__msg__Value__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(proto2ros__msg__Value);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    proto2ros__msg__Value * data =
      (proto2ros__msg__Value *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!proto2ros__msg__Value__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          proto2ros__msg__Value__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!proto2ros__msg__Value__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
