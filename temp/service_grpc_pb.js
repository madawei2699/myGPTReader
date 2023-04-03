// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('grpc');
var src_gpt$reader_service_pb = require('../../src/gpt-reader/service_pb.js');

function serialize_HelloRequest(arg) {
  if (!(arg instanceof src_gpt$reader_service_pb.HelloRequest)) {
    throw new Error('Expected argument of type HelloRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_HelloRequest(buffer_arg) {
  return src_gpt$reader_service_pb.HelloRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_HelloResponse(arg) {
  if (!(arg instanceof src_gpt$reader_service_pb.HelloResponse)) {
    throw new Error('Expected argument of type HelloResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_HelloResponse(buffer_arg) {
  return src_gpt$reader_service_pb.HelloResponse.deserializeBinary(new Uint8Array(buffer_arg));
}


var MyServiceService = exports.MyServiceService = {
  webCrawl: {
    path: '/MyService/webCrawl',
    requestStream: false,
    responseStream: false,
    requestType: src_gpt$reader_service_pb.HelloRequest,
    responseType: src_gpt$reader_service_pb.HelloResponse,
    requestSerialize: serialize_HelloRequest,
    requestDeserialize: deserialize_HelloRequest,
    responseSerialize: serialize_HelloResponse,
    responseDeserialize: deserialize_HelloResponse,
  },
};

exports.MyServiceClient = grpc.makeGenericClientConstructor(MyServiceService);
