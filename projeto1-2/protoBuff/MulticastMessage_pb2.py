# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protoBuff/MulticastMessage.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protoBuff/MulticastMessage.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n protoBuff/MulticastMessage.proto\"0\n\x10MulticastMessage\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\tb\x06proto3'
)




_MULTICASTMESSAGE = _descriptor.Descriptor(
  name='MulticastMessage',
  full_name='MulticastMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='sender', full_name='MulticastMessage.sender', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='MulticastMessage.type', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=36,
  serialized_end=84,
)

DESCRIPTOR.message_types_by_name['MulticastMessage'] = _MULTICASTMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MulticastMessage = _reflection.GeneratedProtocolMessageType('MulticastMessage', (_message.Message,), {
  'DESCRIPTOR' : _MULTICASTMESSAGE,
  '__module__' : 'protoBuff.MulticastMessage_pb2'
  # @@protoc_insertion_point(class_scope:MulticastMessage)
  })
_sym_db.RegisterMessage(MulticastMessage)


# @@protoc_insertion_point(module_scope)