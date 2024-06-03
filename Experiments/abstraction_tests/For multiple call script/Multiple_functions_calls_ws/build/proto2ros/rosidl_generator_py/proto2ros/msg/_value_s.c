// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from proto2ros:msg/Value.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "proto2ros/msg/detail/value__struct.h"
#include "proto2ros/msg/detail/value__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"

bool proto2ros__msg__any__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * proto2ros__msg__any__convert_to_py(void * raw_ros_message);
bool proto2ros__msg__any__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * proto2ros__msg__any__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool proto2ros__msg__value__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[27];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("proto2ros.msg._value.Value", full_classname_dest, 26) == 0);
  }
  proto2ros__msg__Value * ros_message = _ros_message;
  {  // kind
    PyObject * field = PyObject_GetAttrString(_pymsg, "kind");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->kind = (int8_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // number_value
    PyObject * field = PyObject_GetAttrString(_pymsg, "number_value");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->number_value = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // string_value
    PyObject * field = PyObject_GetAttrString(_pymsg, "string_value");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->string_value, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // bool_value
    PyObject * field = PyObject_GetAttrString(_pymsg, "bool_value");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->bool_value = (Py_True == field);
    Py_DECREF(field);
  }
  {  // struct_value
    PyObject * field = PyObject_GetAttrString(_pymsg, "struct_value");
    if (!field) {
      return false;
    }
    if (!proto2ros__msg__any__convert_from_py(field, &ros_message->struct_value)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // list_value
    PyObject * field = PyObject_GetAttrString(_pymsg, "list_value");
    if (!field) {
      return false;
    }
    if (!proto2ros__msg__any__convert_from_py(field, &ros_message->list_value)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * proto2ros__msg__value__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of Value */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("proto2ros.msg._value");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "Value");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  proto2ros__msg__Value * ros_message = (proto2ros__msg__Value *)raw_ros_message;
  {  // kind
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->kind);
    {
      int rc = PyObject_SetAttrString(_pymessage, "kind", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // number_value
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->number_value);
    {
      int rc = PyObject_SetAttrString(_pymessage, "number_value", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // string_value
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->string_value.data,
      strlen(ros_message->string_value.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "string_value", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // bool_value
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->bool_value ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "bool_value", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // struct_value
    PyObject * field = NULL;
    field = proto2ros__msg__any__convert_to_py(&ros_message->struct_value);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "struct_value", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // list_value
    PyObject * field = NULL;
    field = proto2ros__msg__any__convert_to_py(&ros_message->list_value);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "list_value", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
