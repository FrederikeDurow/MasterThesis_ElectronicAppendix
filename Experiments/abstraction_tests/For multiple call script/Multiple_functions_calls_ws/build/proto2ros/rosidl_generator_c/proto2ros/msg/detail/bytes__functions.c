// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from proto2ros:msg/Bytes.idl
// generated code does not contain a copyright notice
#include "proto2ros/msg/detail/bytes__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `data`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
proto2ros__msg__Bytes__init(proto2ros__msg__Bytes * msg)
{
  if (!msg) {
    return false;
  }
  // data
  if (!rosidl_runtime_c__uint8__Sequence__init(&msg->data, 0)) {
    proto2ros__msg__Bytes__fini(msg);
    return false;
  }
  return true;
}

void
proto2ros__msg__Bytes__fini(proto2ros__msg__Bytes * msg)
{
  if (!msg) {
    return;
  }
  // data
  rosidl_runtime_c__uint8__Sequence__fini(&msg->data);
}

bool
proto2ros__msg__Bytes__are_equal(const proto2ros__msg__Bytes * lhs, const proto2ros__msg__Bytes * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // data
  if (!rosidl_runtime_c__uint8__Sequence__are_equal(
      &(lhs->data), &(rhs->data)))
  {
    return false;
  }
  return true;
}

bool
proto2ros__msg__Bytes__copy(
  const proto2ros__msg__Bytes * input,
  proto2ros__msg__Bytes * output)
{
  if (!input || !output) {
    return false;
  }
  // data
  if (!rosidl_runtime_c__uint8__Sequence__copy(
      &(input->data), &(output->data)))
  {
    return false;
  }
  return true;
}

proto2ros__msg__Bytes *
proto2ros__msg__Bytes__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  proto2ros__msg__Bytes * msg = (proto2ros__msg__Bytes *)allocator.allocate(sizeof(proto2ros__msg__Bytes), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(proto2ros__msg__Bytes));
  bool success = proto2ros__msg__Bytes__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
proto2ros__msg__Bytes__destroy(proto2ros__msg__Bytes * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    proto2ros__msg__Bytes__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
proto2ros__msg__Bytes__Sequence__init(proto2ros__msg__Bytes__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  proto2ros__msg__Bytes * data = NULL;

  if (size) {
    data = (proto2ros__msg__Bytes *)allocator.zero_allocate(size, sizeof(proto2ros__msg__Bytes), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = proto2ros__msg__Bytes__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        proto2ros__msg__Bytes__fini(&data[i - 1]);
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
proto2ros__msg__Bytes__Sequence__fini(proto2ros__msg__Bytes__Sequence * array)
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
      proto2ros__msg__Bytes__fini(&array->data[i]);
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

proto2ros__msg__Bytes__Sequence *
proto2ros__msg__Bytes__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  proto2ros__msg__Bytes__Sequence * array = (proto2ros__msg__Bytes__Sequence *)allocator.allocate(sizeof(proto2ros__msg__Bytes__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = proto2ros__msg__Bytes__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
proto2ros__msg__Bytes__Sequence__destroy(proto2ros__msg__Bytes__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    proto2ros__msg__Bytes__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
proto2ros__msg__Bytes__Sequence__are_equal(const proto2ros__msg__Bytes__Sequence * lhs, const proto2ros__msg__Bytes__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!proto2ros__msg__Bytes__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
proto2ros__msg__Bytes__Sequence__copy(
  const proto2ros__msg__Bytes__Sequence * input,
  proto2ros__msg__Bytes__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(proto2ros__msg__Bytes);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    proto2ros__msg__Bytes * data =
      (proto2ros__msg__Bytes *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!proto2ros__msg__Bytes__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          proto2ros__msg__Bytes__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!proto2ros__msg__Bytes__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
