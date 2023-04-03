const grpc = require("grpc");
const protoLoader = require("@grpc/proto-loader");
const path = require('path');
const {
	pupRequest
} = require('./puppeteer');

// const PROTO_PATH = "./service.proto";
const PROTO_PATH = path.join(process.cwd(), 'service.proto');

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
	keepCase: true,
	longs: String,
	enums: String,
	defaults: true,
	oneofs: true
});
const service = grpc.loadPackageDefinition(packageDefinition).MyService;

async function processEvent(call, callback) {
	const content = call.request.url;
	let status_code = 200,
		webContent = "";
	console.log("Received event:", content);
	try {
		webContent = await pupRequest(content)
	} catch (e) {
		status_code = 500;
		webContent = e.message;
	}
	const response = {
		result: JSON.stringify(webContent),
		status_code
	};
	callback(null, response);
}

function main() {
	const server = new grpc.Server();
	server.addService(service.service, {
		webCrawl: processEvent
	});
	server.bind("0.0.0.0:50051", grpc.ServerCredentials.createInsecure());
	server.start();
	console.log("Node.js server started on port 50051");
}

main();