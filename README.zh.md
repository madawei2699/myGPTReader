# 快速开发机器人

> ⚠️ 本教程为了方便实现，使用了反向代理工具（ngrok），该工具仅适用于开发测试阶段，不可用于生产环境。使用前需要确认是否符合所在公司网络安全政策。


本示例介绍如何使用开放平台机器人能力，完成机器人接收用户消息，并且回复消息的处理。可以基于此示例扩展机器人事件处理能力。

## 运行环境

- [Python 3](https://www.python.org/)
- [ngrok](https://ngrok.com/download) （内网穿透工具）

## 准备工作

1、在[开发者后台](https://open.feishu.cn/app/) **新建企业自建应用**，点击应用名称进入应用详情页。

2、点击**凭证与基础信息**切换页面，拿到 `App ID` 和 `App Secret`值，点击**事件订阅**切换页面：拿到 `Encrypt Key` 和 `Verification Token` 值。

3、拉取最新代码到本地，并进入对应目录。

  ```commandline
  git clone https://github.com/larksuite/lark-samples.git
  cd lark-samples/robot_quick_start/python
  ```

4、修改环境值

修改`.env`文件中应用凭证数据为真实数据。

  ```text
  APP_ID=cli_9fxxxx00b
  APP_SECRET=EX6xxxxOF
  APP_VERIFICATION_TOKEN=cq3xxxxxxkUS
  ENCRYPT_KEY=
  ```

以上参数可以在 [开发者后台](https://open.feishu.cn/app) 查看，其中 Encrypt Key 可以为空。

## docker运行

运行之前需要确保 [Docker](https://www.docker.com/) 已经安装。docker运行与下方本地运行二选一即可。

**mac/linux**

```commandline
sh exec.sh
```

**windows**

```
.\exec.ps1
```

## 本地运行

1、创建并激活一个新的虚拟环境

**mac/linux**

```commandline
python3 -m venv venv
. venv/bin/activate
```

**windows**

```commandline
python3 -m venv venv
venv\Scripts\activate
```

激活后，终端会显示虚拟环境的名称

```
(venv) **** python %
```

2、安装依赖

```
pip install -r requirements.txt
```     

3、运行

```
python3 server.py
```

## 完成配置，体验机器人

机器人接收的消息都会以回调事件请求形式，通过 POST 请求方式，送达到服务端处理。所以本地服务端启动之后，回调事件无法请求到内网，需要配置公网请求 URL。

配置分为如下两步：使用工具完成内网穿透、在应用的**事件订阅**页面配置公网请求 URL。

1、使用工具暴露本地服务的公网访问入口，此处给出 ngrok 使用示例，若本地未安装可以访问 [ngrok](https://ngrok.com/download) ，按照教程完成安装。

- 使用以下命令获得公网 URL

  **注意**：使用反向代理工具（ngrok）之前需要确定是否符合公司网络安全策略。

  **注意**：需要提前在 [ngrok](https://dashboard.ngrok.com/signup) 获取token值。

  ```
  ngrok authtoken <token> // <token>需要替换
  ngrok http 3000
  ```

2、点击**机器人**切换页面>打开**启用机器人**开关。

3、在**事件订阅**页面：配置**请求网址 URL**。

使用工具生成的域名，填写请求网址 URL，如下图所示。
![image.png](https://sf3-cn.feishucdn.com/obj/open-platform-opendoc/336d89fde0b7a5313ce9f90951cce581_nupZP6M8bb.png)

**注意**：配置请求网址URL和发送消息给机器人，都会有请求到后端服务，请求期间需要保证服务为启动状态。

4、为机器人选择监听事件。

在**事件订阅**页面，点击**添加事件**，选择`接收消息`事件并订阅。

5、申请权限

在**权限管理**页面，搜索需要的**权限配置**，并开通权限。

- 依赖权限清单
    - 获取与发送单聊、群组消息
    - 获取用户发给机器人的单聊消息

**注意**：`获取用户发给机器人的单聊消息`权限未展示在**已添加事件**中，必须切换到**权限管理**页面开通。

6、在**版本管理与发布**页面：**创建版本**>**申请发布**。

注意：本次涉及需要审核的权限，可以利用 [测试企业与人员功能](https://open.feishu.cn/document/home/introduction-to-custom-app-development/testing-enterprise-and-personnel-functions)
，生成测试版应用（无需发布，配置直接生效），完成测试。

**注意**：成功发布后，可以根据是否能搜到机器人，判断用户是否在机器人可用性范围内。

7、打开**飞书**，搜索**机器人名称**并开始体验机器人自动回复。
