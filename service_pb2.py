# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rservice.proto\"\x1b\n\x0cHelloRequest\x12\x0b\n\x03url\x18\x01 \x01(\t\"4\n\rHelloResponse\x12\x0e\n\x06result\x18\x01 \x01(\t\x12\x13\n\x0bstatus_code\x18\x02 \x01(\x05\x32\x36\n\tMyService\x12)\n\x08webCrawl\x12\r.HelloRequest\x1a\x0e.HelloResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _HELLOREQUEST._serialized_start=17
  _HELLOREQUEST._serialized_end=44
  _HELLORESPONSE._serialized_start=46
  _HELLORESPONSE._serialized_end=98
  _MYSERVICE._serialized_start=100
  _MYSERVICE._serialized_end=154
# @@protoc_insertion_point(module_scope)
