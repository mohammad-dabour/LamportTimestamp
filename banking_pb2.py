# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: banking.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='banking.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\rbanking.proto\"_\n\x0e\x42\x61nkingRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x11\n\tinterface\x18\x02 \x01(\t\x12\r\n\x05money\x18\x03 \x01(\x02\x12\x10\n\x08writeset\x18\x04 \x01(\x05\x12\r\n\x05reset\x18\x05 \x01(\x08\"^\n\x0c\x42\x61nkingReply\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x11\n\tinterface\x18\x02 \x01(\t\x12\x0e\n\x06result\x18\x03 \x01(\t\x12\r\n\x05money\x18\x04 \x01(\x02\x12\x10\n\x08writeset\x18\x05 \x01(\x05\x32:\n\x07\x42\x61nking\x12/\n\x0bMsgDelivery\x12\x0f.BankingRequest\x1a\r.BankingReply\"\x00\x62\x06proto3'
)




_BANKINGREQUEST = _descriptor.Descriptor(
  name='BankingRequest',
  full_name='BankingRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='BankingRequest.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='interface', full_name='BankingRequest.interface', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='money', full_name='BankingRequest.money', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='writeset', full_name='BankingRequest.writeset', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='reset', full_name='BankingRequest.reset', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=17,
  serialized_end=112,
)


_BANKINGREPLY = _descriptor.Descriptor(
  name='BankingReply',
  full_name='BankingReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='BankingReply.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='interface', full_name='BankingReply.interface', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='result', full_name='BankingReply.result', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='money', full_name='BankingReply.money', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='writeset', full_name='BankingReply.writeset', index=4,
      number=5, type=5, cpp_type=1, label=1,
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
  ],
  serialized_start=114,
  serialized_end=208,
)

DESCRIPTOR.message_types_by_name['BankingRequest'] = _BANKINGREQUEST
DESCRIPTOR.message_types_by_name['BankingReply'] = _BANKINGREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BankingRequest = _reflection.GeneratedProtocolMessageType('BankingRequest', (_message.Message,), {
  'DESCRIPTOR' : _BANKINGREQUEST,
  '__module__' : 'banking_pb2'
  # @@protoc_insertion_point(class_scope:BankingRequest)
  })
_sym_db.RegisterMessage(BankingRequest)

BankingReply = _reflection.GeneratedProtocolMessageType('BankingReply', (_message.Message,), {
  'DESCRIPTOR' : _BANKINGREPLY,
  '__module__' : 'banking_pb2'
  # @@protoc_insertion_point(class_scope:BankingReply)
  })
_sym_db.RegisterMessage(BankingReply)



_BANKING = _descriptor.ServiceDescriptor(
  name='Banking',
  full_name='Banking',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=210,
  serialized_end=268,
  methods=[
  _descriptor.MethodDescriptor(
    name='MsgDelivery',
    full_name='Banking.MsgDelivery',
    index=0,
    containing_service=None,
    input_type=_BANKINGREQUEST,
    output_type=_BANKINGREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_BANKING)

DESCRIPTOR.services_by_name['Banking'] = _BANKING

# @@protoc_insertion_point(module_scope)
