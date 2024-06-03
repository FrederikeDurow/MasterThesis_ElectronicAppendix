# generated from rosidl_generator_py/resource/_idl.py.em
# with input from proto2ros:msg/Value.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_Value(type):
    """Metaclass of message 'Value'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
        'NO_VALUE_SET': 0,
        'NUMBER_VALUE_SET': 1,
        'STRING_VALUE_SET': 2,
        'BOOL_VALUE_SET': 3,
        'STRUCT_VALUE_SET': 4,
        'LIST_VALUE_SET': 5,
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('proto2ros')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'proto2ros.msg.Value')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__value
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__value
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__value
            cls._TYPE_SUPPORT = module.type_support_msg__msg__value
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__value

            from proto2ros.msg import Any
            if Any.__class__._TYPE_SUPPORT is None:
                Any.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
            'NO_VALUE_SET': cls.__constants['NO_VALUE_SET'],
            'NUMBER_VALUE_SET': cls.__constants['NUMBER_VALUE_SET'],
            'STRING_VALUE_SET': cls.__constants['STRING_VALUE_SET'],
            'BOOL_VALUE_SET': cls.__constants['BOOL_VALUE_SET'],
            'STRUCT_VALUE_SET': cls.__constants['STRUCT_VALUE_SET'],
            'LIST_VALUE_SET': cls.__constants['LIST_VALUE_SET'],
            'KIND__DEFAULT': 0,
        }

    @property
    def NO_VALUE_SET(self):
        """Message constant 'NO_VALUE_SET'."""
        return Metaclass_Value.__constants['NO_VALUE_SET']

    @property
    def NUMBER_VALUE_SET(self):
        """Message constant 'NUMBER_VALUE_SET'."""
        return Metaclass_Value.__constants['NUMBER_VALUE_SET']

    @property
    def STRING_VALUE_SET(self):
        """Message constant 'STRING_VALUE_SET'."""
        return Metaclass_Value.__constants['STRING_VALUE_SET']

    @property
    def BOOL_VALUE_SET(self):
        """Message constant 'BOOL_VALUE_SET'."""
        return Metaclass_Value.__constants['BOOL_VALUE_SET']

    @property
    def STRUCT_VALUE_SET(self):
        """Message constant 'STRUCT_VALUE_SET'."""
        return Metaclass_Value.__constants['STRUCT_VALUE_SET']

    @property
    def LIST_VALUE_SET(self):
        """Message constant 'LIST_VALUE_SET'."""
        return Metaclass_Value.__constants['LIST_VALUE_SET']

    @property
    def KIND__DEFAULT(cls):
        """Return default value for message field 'kind'."""
        return 0


class Value(metaclass=Metaclass_Value):
    """
    Message class 'Value'.

    Constants:
      NO_VALUE_SET
      NUMBER_VALUE_SET
      STRING_VALUE_SET
      BOOL_VALUE_SET
      STRUCT_VALUE_SET
      LIST_VALUE_SET
    """

    __slots__ = [
        '_kind',
        '_number_value',
        '_string_value',
        '_bool_value',
        '_struct_value',
        '_list_value',
    ]

    _fields_and_field_types = {
        'kind': 'int8',
        'number_value': 'double',
        'string_value': 'string',
        'bool_value': 'boolean',
        'struct_value': 'proto2ros/Any',
        'list_value': 'proto2ros/Any',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['proto2ros', 'msg'], 'Any'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['proto2ros', 'msg'], 'Any'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.kind = kwargs.get(
            'kind', Value.KIND__DEFAULT)
        self.number_value = kwargs.get('number_value', float())
        self.string_value = kwargs.get('string_value', str())
        self.bool_value = kwargs.get('bool_value', bool())
        from proto2ros.msg import Any
        self.struct_value = kwargs.get('struct_value', Any())
        from proto2ros.msg import Any
        self.list_value = kwargs.get('list_value', Any())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.kind != other.kind:
            return False
        if self.number_value != other.number_value:
            return False
        if self.string_value != other.string_value:
            return False
        if self.bool_value != other.bool_value:
            return False
        if self.struct_value != other.struct_value:
            return False
        if self.list_value != other.list_value:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def kind(self):
        """Message field 'kind'."""
        return self._kind

    @kind.setter
    def kind(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'kind' field must be of type 'int'"
            assert value >= -128 and value < 128, \
                "The 'kind' field must be an integer in [-128, 127]"
        self._kind = value

    @builtins.property
    def number_value(self):
        """Message field 'number_value'."""
        return self._number_value

    @number_value.setter
    def number_value(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'number_value' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'number_value' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._number_value = value

    @builtins.property
    def string_value(self):
        """Message field 'string_value'."""
        return self._string_value

    @string_value.setter
    def string_value(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'string_value' field must be of type 'str'"
        self._string_value = value

    @builtins.property
    def bool_value(self):
        """Message field 'bool_value'."""
        return self._bool_value

    @bool_value.setter
    def bool_value(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'bool_value' field must be of type 'bool'"
        self._bool_value = value

    @builtins.property
    def struct_value(self):
        """Message field 'struct_value'."""
        return self._struct_value

    @struct_value.setter
    def struct_value(self, value):
        if __debug__:
            from proto2ros.msg import Any
            assert \
                isinstance(value, Any), \
                "The 'struct_value' field must be a sub message of type 'Any'"
        self._struct_value = value

    @builtins.property
    def list_value(self):
        """Message field 'list_value'."""
        return self._list_value

    @list_value.setter
    def list_value(self, value):
        if __debug__:
            from proto2ros.msg import Any
            assert \
                isinstance(value, Any), \
                "The 'list_value' field must be a sub message of type 'Any'"
        self._list_value = value
