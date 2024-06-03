// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from proto2ros:msg/StructEntry.idl
// generated code does not contain a copyright notice
#include "proto2ros/msg/detail/struct_entry__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `key`
#include "rosidl_runtime_c/string_functions.h"
// Member `value`
#include "proto2ros/msg/detail/value__functions.h"

bool
proto2ros__msg__StructEntry__init(proto2ros__msg__StructEntry * msg)
{
  if (!msg) {
    return false;
  }
  // key
  if (!rosidl_runtime_c__String__init(&msg->key)) {
    proto2ros__msg__StructEntry__fini(msg);
    return false;
  }
  // value
  if (!proto2ros__msg__Value__init(&msg->value)) {
    proto2ros__msg__StructEntry__fini(msg);
    return false;
  }
  return true;
}

void
proto2ros__msg__StructEntry__fini(proto2ros__msg__StructEntry * msg)
{
  if (!msg) {
    return;
  }
  // key
  rosidl_runtime_c__String__fini(&msg->key);
  // value
  proto2ros__msg__Value__fini(&msg->value);
}

bool
proto2ros__msg__StructEntry__are_equal(const proto2ros__msg__StructEntry * lhs, const proto2ros__msg__StructEntry * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // key
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->key), &(rhs->key)))
  {
    return false;
  }
  // value
  if (!proto2ros__msg__Value__are_equal(
      &(lhs->value), &(rhs->value)))
  {
    return false;
  }
  return true;
}

bool
proto2ros__msg__StructEntry__copy(
  const proto2ros__msg__StructEntry * input,
  proto2ros__msg__StructEntry * output)
{
  if (!input || !output) {
    return false;
  }
  // key
  if (!rosidl_runtime_c__String__copy(
      &(input->key), &(output->key)))
  {
    return false;
  }
  // value
  if (!proto2ros__msg__Value__copy(
      &(input->value), &(output->value)))
  {
    return false;
  }
  return true;
}

proto2ros__msg__StructEntry *
proto2ros__msg__StructEntry__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  proto2ros__msg__StructEntry * msg = (proto2ros__msg__StructEntry *)allocator.allocate(sizeof(proto2ros__msg__StructEntry), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(proto2ros__msg__StructEntry));
  bool success = proto2ros__msg__StructEntry__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
proto2ros__msg__StructEntry__destroy(proto2ros__msg__StructEntry * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    proto2ros__msg__StructEntry__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
proto2ros__msg__StructEntry__Sequence__init(proto2ros__msg__StructEntry__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  proto2ros__msg__StructEntry * data = NULL;

  if (size) {
    data = (proto2ros__msg__StructEntry *)allocator.zero_allocate(size, sizeof(proto2ros__msg__StructEntry), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = proto2ros__msg__StructEntry__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        proto2ros__msg__StructEntry__fini(&data[i - 1]);
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
proto2ros__msg__StructEntry__Sequence__fini(proto2ros__msg__StructEntry__Sequence * array)
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
      proto2ros__msg__StructEntry__fini(&array->data[i]);
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

proto2ros__msg__StructEntry__Sequence *
proto2ros__msg__StructEntry__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  proto2ros__msg__StructEntry__Sequence * array = (proto2ros__msg__StructEntry__Sequence *)allocator.allocate(sizeof(proto2ros__msg__StructEntry__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = proto2ros__msg__StructEntry__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
proto2ros__msg__StructEntry__Sequence__destroy(proto2ros__msg__StructEntry__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    proto2ros__msg__StructEntry__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
proto2ros__msg__StructEntry__Sequence__are_equal(const proto2ros__msg__StructEntry__Sequence * lhs, const proto2ros__msg__StructEntry__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!proto2ros__msg__StructEntry__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
proto2ros__msg__StructEntry__Sequence__copy(
  const proto2ros__msg__StructEntry__Sequence * input,
  proto2ros__msg__StructEntry__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(proto2ros__msg__StructEntry);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    proto2ros__msg__StructEntry * data =
      (proto2ros__msg__StructEntry *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!proto2ros__msg__StructEntry__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          proto2ros__msg__StructEntry__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!proto2ros__msg__StructEntry__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}