# Quickly develop a bot

> ⚠️ In order to facilitate the implementation of this tutorial, a reverse proxy tool (ngrok) is used. This tool is only suitable for the development and testing phase and cannot be used in the production environment. Before using it, you need to confirm whether it complies with the company's network security policy.

This example shows how to use the Open Platform's bot function to have a bot receive user messages and make replies. You
can extend the event processing functions of bot based on this example.

## Runtime environment

- [Python 3](https://www.python.org/)
- [ngrok](https://ngrok.com/download) (intranet penetration tool)

## Prep work

1. In [Developer Console](https://open.feishu.cn/app/), click **Create custom app**, then click the app name to go to
   the app details page.
2. Go to **Credentials & Basic Info** to obtain the `App ID` and `App Secret`, and then go to **Event Subscriptions** to
   obtain the
   `Encrypt Key` and `Verification Token`.
3. Pull the latest code to local and enter the corresponding directory.

   ```
   git clone https://github.com/larksuite/lark-samples.git
   cd lark-samples/robot_quick_start/python
   ```

4. Edit environment variables

   Edit the app credential data in the `.env` file to real data.

   ```
   APP_ID=cli_9fxxxx00b
   APP_SECRET=EX6xxxxOF
   APP_VERIFICATION_TOKEN=cq3xxxxxxkUS
   ENCRYPT_KEY=
   ```

   The above parameters can be viewed in [Developer Console](https://open.feishu.cn/app/). Encrypt Key can be empty.

5. 音频转换工具
   > openai 支持的音频格式如下：['m4a', 'mp3', 'webm', 'mp4', 'mpga', 'wav', 'mpeg']。但是飞书语音的格式是 OGG 的。要将 OGG 文件转换为受支持的格式（如 MP3），您可以使用 Python 的 pydub 库。首先，您需要安装 pydub 库，以及处理音频文件所需的 ffmpeg 工具。

## server rpc

- change service.proto

```
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto
```

- 这将生成 service_pb2.py 和 service_pb2_grpc.py 文件。

```
npm install -g grpc-tools
grpc_tools_node_protoc --js_out=import_style=commonjs,binary:. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_tools_node_protoc_plugin` service.proto
```

- 这将生成 service_pb.js 和 service_grpc_pb.js 文件。

## Running with Docker

Ensure that [Docker](https://www.docker.com/) has been installed before running. You can choose to run your code either
with Docker or locally.

**Mac/Linux**

```
sh exec.sh
```

**Windows**

```
.\exec.ps1
```

## Running Locally

1. Create and activate a new virtual environment.

   **Mac/Linux**

   ```
   python3 -m venv venv
   . venv/bin/activate
   ```

   **Windows**

   ```
   python3 -m venv venv
   venv\Scripts\activate
   ```

   Once activated, the terminal will display the virtual environment's name.

   ```
   (venv) **** python %
   ```

2. Install dependencies

   ```
   pip install -r requirements.txt
   ```

3. Run

   ```
   python3 server.py
   ```

# Feature & bugfix

- [x] myGptReader 网页爬取能力
- [ ] 支持和 pdf 对话能力
- [ ] 支持提取视频主要内容
- [ ] 用 ChatGPT 编写儿童故事
- [ ] 拍照，ocr 提起文字，翻译功能
- [x] chatgpt 保存回话的上下文信息，统一加入到一个数组中
- [x] 增加会话超时能力
- [ ] 需要根据 userId，当前是根据时间戳无脑的去重了，单独跟机器人私聊没有问题，但是如果加入群聊就有问题了
- [x] 支持群聊能力

bugfix：

- [x] 解决发一条消息，收到多条回复的问题

# 历程

- 阿里云弹性服务收费很高，使用了一周服务基本就消耗 100 元左右了，所以专项更便宜的 fly.io
- 用 docker 容器部署，希望 python 服务调用 node 服务，能够通过 rpc，这样稳定性和性能都更好，因此考虑到部署的方便性，把 node 代码和 python 代码放置到同一个仓库。
- 支持 gpt goken 计数能力，需要升级 llama-index 到 0.5.4，但是此版本依赖 python 3.9。因为我需要 在 node 镜像上单独安装 3.9 的 python。但是安装 python 3.9 有很多前置依赖，导致在 docker 容器构建阶段失败率非常高。因此就不增加计数功能了，降级到 llama-index@0.4.26
- 使用 fly.io 部署仓库代码,nodejs 服务切换为 python 服务.
