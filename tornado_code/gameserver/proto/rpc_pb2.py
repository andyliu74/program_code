# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rpc.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import service as _service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='rpc.proto',
  package='protobuf.socketrpc',
  serialized_pb=_b('\n\trpc.proto\x12\x12protobuf.socketrpc\"\x06\n\x04Void\"5\n\x07Request\x12\x13\n\x0bmethod_name\x18\x02 \x02(\t\x12\x15\n\rrequest_proto\x18\x03 \x02(\x0c\x32V\n\x0eIServerService\x12\x44\n\x0b\x63\x61ll_server\x12\x1b.protobuf.socketrpc.Request\x1a\x18.protobuf.socketrpc.VoidB\x06\x80\x01\x01\x90\x01\x01')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_VOID = _descriptor.Descriptor(
  name='Void',
  full_name='protobuf.socketrpc.Void',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=33,
  serialized_end=39,
)


_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='protobuf.socketrpc.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='method_name', full_name='protobuf.socketrpc.Request.method_name', index=0,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='request_proto', full_name='protobuf.socketrpc.Request.request_proto', index=1,
      number=3, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=_b(""),
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
  oneofs=[
  ],
  serialized_start=41,
  serialized_end=94,
)

DESCRIPTOR.message_types_by_name['Void'] = _VOID
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST

Void = _reflection.GeneratedProtocolMessageType('Void', (_message.Message,), dict(
  DESCRIPTOR = _VOID,
  __module__ = 'rpc_pb2'
  # @@protoc_insertion_point(class_scope:protobuf.socketrpc.Void)
  ))
_sym_db.RegisterMessage(Void)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'rpc_pb2'
  # @@protoc_insertion_point(class_scope:protobuf.socketrpc.Request)
  ))
_sym_db.RegisterMessage(Request)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\200\001\001\220\001\001'))

_ISERVERSERVICE = _descriptor.ServiceDescriptor(
  name='IServerService',
  full_name='protobuf.socketrpc.IServerService',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=96,
  serialized_end=182,
  methods=[
  _descriptor.MethodDescriptor(
    name='call_server',
    full_name='protobuf.socketrpc.IServerService.call_server',
    index=0,
    containing_service=None,
    input_type=_REQUEST,
    output_type=_VOID,
    options=None,
  ),
])

IServerService = service_reflection.GeneratedServiceType('IServerService', (_service.Service,), dict(
  DESCRIPTOR = _ISERVERSERVICE,
  __module__ = 'rpc_pb2'
  ))

IServerService_Stub = service_reflection.GeneratedServiceStubType('IServerService_Stub', (IServerService,), dict(
  DESCRIPTOR = _ISERVERSERVICE,
  __module__ = 'rpc_pb2'
  ))


# @@protoc_insertion_point(module_scope)
