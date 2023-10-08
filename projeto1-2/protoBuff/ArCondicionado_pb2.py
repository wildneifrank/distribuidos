# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protoBuff/ArCondicionado.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protoBuff/ArCondicionado.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1eprotoBuff/ArCondicionado.proto\"\x1c\n\x08\x43ontrole\x12\x10\n\x08operacao\x18\x01 \x01(\t\"F\n\nattributes\x12\x12\n\x05state\x18\x01 \x01(\x08H\x00\x88\x01\x01\x12\x11\n\x04temp\x18\x02 \x01(\x05H\x01\x88\x01\x01\x42\x08\n\x06_stateB\x07\n\x05_tempb\x06proto3'
)




_CONTROLE = _descriptor.Descriptor(
  name='Controle',
  full_name='Controle',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='operacao', full_name='Controle.operacao', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=34,
  serialized_end=62,
)


_ATTRIBUTES = _descriptor.Descriptor(
  name='attributes',
  full_name='attributes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='state', full_name='attributes.state', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='temp', full_name='attributes.temp', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='_state', full_name='attributes._state',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_temp', full_name='attributes._temp',
      index=1, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=64,
  serialized_end=134,
)

_ATTRIBUTES.oneofs_by_name['_state'].fields.append(
  _ATTRIBUTES.fields_by_name['state'])
_ATTRIBUTES.fields_by_name['state'].containing_oneof = _ATTRIBUTES.oneofs_by_name['_state']
_ATTRIBUTES.oneofs_by_name['_temp'].fields.append(
  _ATTRIBUTES.fields_by_name['temp'])
_ATTRIBUTES.fields_by_name['temp'].containing_oneof = _ATTRIBUTES.oneofs_by_name['_temp']
DESCRIPTOR.message_types_by_name['Controle'] = _CONTROLE
DESCRIPTOR.message_types_by_name['attributes'] = _ATTRIBUTES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Controle = _reflection.GeneratedProtocolMessageType('Controle', (_message.Message,), {
  'DESCRIPTOR' : _CONTROLE,
  '__module__' : 'protoBuff.ArCondicionado_pb2'
  # @@protoc_insertion_point(class_scope:Controle)
  })
_sym_db.RegisterMessage(Controle)

attributes = _reflection.GeneratedProtocolMessageType('attributes', (_message.Message,), {
  'DESCRIPTOR' : _ATTRIBUTES,
  '__module__' : 'protoBuff.ArCondicionado_pb2'
  # @@protoc_insertion_point(class_scope:attributes)
  })
_sym_db.RegisterMessage(attributes)


# @@protoc_insertion_point(module_scope)