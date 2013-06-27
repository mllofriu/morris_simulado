# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: robot/protocol/robotProtocol.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='robot/protocol/robotProtocol.proto',
  package='robot.protocol',
  serialized_pb='\n\"robot/protocol/robotProtocol.proto\x12\x0erobot.protocol\"\xb9\x01\n\x07\x43ommand\x12\x30\n\x07\x63ommand\x18\x01 \x02(\x0e\x32\x1f.robot.protocol.Command.CmdType\x12\r\n\x05\x61ngle\x18\x02 \x01(\x05\"m\n\x07\x43mdType\x12\x0c\n\x08\x64oAction\x10\x00\x12\n\n\x06rotate\x10\x01\x12\x12\n\x0egetAffordances\x10\x02\x12\r\n\tgetMarcas\x10\x03\x12\x0e\n\nstartRobot\x10\x04\x12\n\n\x06isFood\x10\x05\x12\t\n\x05\x63lose\x10\x06\"\x16\n\x08Response\x12\n\n\x02ok\x18\x01 \x02(\x08\"!\n\x0b\x41\x66\x66ordances\x12\x12\n\naffordance\x18\x01 \x03(\x08\"@\n\x06Marcas\x12\x0f\n\x07idMarca\x18\x01 \x03(\x05\x12\x12\n\nangleMarca\x18\x02 \x03(\x01\x12\x11\n\tdistMarca\x18\x03 \x03(\x01\"!\n\nIsTherFood\x12\x13\n\x0bisThereFood\x18\x01 \x02(\x08\x42\x1f\n\x0erobot.protocolB\rRobotProtocol')



_COMMAND_CMDTYPE = _descriptor.EnumDescriptor(
  name='CmdType',
  full_name='robot.protocol.Command.CmdType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='doAction', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='rotate', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='getAffordances', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='getMarcas', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='startRobot', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='isFood', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='close', index=6, number=6,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=131,
  serialized_end=240,
)


_COMMAND = _descriptor.Descriptor(
  name='Command',
  full_name='robot.protocol.Command',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='command', full_name='robot.protocol.Command.command', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='angle', full_name='robot.protocol.Command.angle', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _COMMAND_CMDTYPE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=55,
  serialized_end=240,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='robot.protocol.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ok', full_name='robot.protocol.Response.ok', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=242,
  serialized_end=264,
)


_AFFORDANCES = _descriptor.Descriptor(
  name='Affordances',
  full_name='robot.protocol.Affordances',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='affordance', full_name='robot.protocol.Affordances.affordance', index=0,
      number=1, type=8, cpp_type=7, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=266,
  serialized_end=299,
)


_MARCAS = _descriptor.Descriptor(
  name='Marcas',
  full_name='robot.protocol.Marcas',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='idMarca', full_name='robot.protocol.Marcas.idMarca', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='angleMarca', full_name='robot.protocol.Marcas.angleMarca', index=1,
      number=2, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='distMarca', full_name='robot.protocol.Marcas.distMarca', index=2,
      number=3, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=301,
  serialized_end=365,
)


_ISTHERFOOD = _descriptor.Descriptor(
  name='IsTherFood',
  full_name='robot.protocol.IsTherFood',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='isThereFood', full_name='robot.protocol.IsTherFood.isThereFood', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=367,
  serialized_end=400,
)

_COMMAND.fields_by_name['command'].enum_type = _COMMAND_CMDTYPE
_COMMAND_CMDTYPE.containing_type = _COMMAND;
DESCRIPTOR.message_types_by_name['Command'] = _COMMAND
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
DESCRIPTOR.message_types_by_name['Affordances'] = _AFFORDANCES
DESCRIPTOR.message_types_by_name['Marcas'] = _MARCAS
DESCRIPTOR.message_types_by_name['IsTherFood'] = _ISTHERFOOD

class Command(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _COMMAND

  # @@protoc_insertion_point(class_scope:robot.protocol.Command)

class Response(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RESPONSE

  # @@protoc_insertion_point(class_scope:robot.protocol.Response)

class Affordances(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _AFFORDANCES

  # @@protoc_insertion_point(class_scope:robot.protocol.Affordances)

class Marcas(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _MARCAS

  # @@protoc_insertion_point(class_scope:robot.protocol.Marcas)

class IsTherFood(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ISTHERFOOD

  # @@protoc_insertion_point(class_scope:robot.protocol.IsTherFood)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), '\n\016robot.protocolB\rRobotProtocol')
# @@protoc_insertion_point(module_scope)
