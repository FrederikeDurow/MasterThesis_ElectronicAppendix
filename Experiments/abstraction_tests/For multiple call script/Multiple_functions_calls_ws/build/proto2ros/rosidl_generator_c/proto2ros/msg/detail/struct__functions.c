// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from proto2ros:msg/Struct.idl
// generated code does not contain a copyright notice
#include "proto2ros/msg/detail/struct__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `fields`
#include "proto2ros/msg/detail/struct_entry__functions.h"

bool
proto2ros__msg__Struct__init(proto2ros__msg__Struct * msg)
{
  if (!msg) {
    return false;
  }
  // fields
  if (!proto2ros__msg__StructEntry__Sequence__init(&msg->fields, 0)) {
    proto2ros__msg__Struct__fini(msg);
    return false;
  }
  return true;
}

void
proto2ros__msg__Struct__fini(proto2ros__msg__Struct * msg)
{
  if (!msg) {
    return;
  }
  // fields
  proto2ros__msg__StructEntry__Sequence__fini(&msg->fields);
}

bool
proto2ros__msg__Struct__are_equal(const proto2ros__msg__Struct * lhs, const proto2ros__msg__Struct * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // fields
  if (!proto2ros__msg__StructEntry__Sequence__are_equal(
      &(lhs->fields), &(rhs->fields)))
  {
    return false;
  }
  return true;
}

bool
proto2ros__msg__Struct__copy(
  const proto2ros__msg__Struct * input,
  proto2ros__msg__Struct * output)
{
  if (!input || !output) {
    return false;
  }
  // fields
  if (!proto2ros__msg__StructEntry__Sequence__copy(
      &(input->fields), &(output->fields)))
  {
    return false;
  }
  return true;
}

proto2ros__msg__Struct *
proto2ros__msg__Struct__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  proto2ros__msg__Struct * msg = (proto2ros__msg__Struct *)allocator.allocate(sizeof(proto2ros__msg__Struct), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(proto2ros__msg__Struct));
  bool success = proto2ros__msg__Struct__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
proto2ros__msg__Struct__destroy(proto2ros__msg__Struct * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    proto2ros__msg__Struct__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
proto2ros__msg__Struct__Sequence__init(proto2ros__msg__Struct__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  proto2ros__msg__Struct * data = NULL;

  if (size) {
    data = (proto2ros__msg__Struct *)allocator.zero_allocate(size, sizeof(proto2ros__msg__Struct), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = proto2ros__msg__Struct__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        proto2ros__msg__Struct__fini(&data[i - 1]);
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
proto2ros__msg__Struct__Sequence__fini(proto2ros__msg__Struct__Sequence * array)
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
      proto2ros__msg__Struct__fini(&array->data[i]);
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

proto2ros__msg__Struct__Sequence *
proto2ros__msg__Struct__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  proto2ros__msg__Struct__Sequence * array = (proto2ros__msg__Struct__Sequence *)allocator.allocate(sizeof(proto2ros__msg__Struct__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = proto2ros__msg__Struct__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
proto2ros__msg__Struct__Sequence__destroy(proto2ros__msg__Struct__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    proto2ros__msg__Struct__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
proto2ros__msg__Struct__Sequence__are_equal(const proto2ros__msg__Struct__Sequence * lhs, const proto2ros__msg__Struct__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!proto2ros__msg__Struct__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
proto2ros__msg__Struct__Sequence__copy(
  const proto2ros__msg__Struct__Sequence * input,
  proto2ros__msg__Struct__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(proto2ros__msg__Struct);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    proto2ros__msg__Struct * data =
      (proto2ros__msg__Struct *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!proto2ros__msg__Struct__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          proto2ros__msg__Struct__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!proto2ros__msg__Struct__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
