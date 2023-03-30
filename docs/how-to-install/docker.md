# 如何使用 Docker 安装本项目

fly.io 需要绑定信用卡才能发布项目，而且应该比较多小伙伴想要自己部署一套，docker 部署应该是比较好的选择。

## 安装前准备

项目使用了比较多其他服务，比如 Cloudflare， PHANTOMJSCLOUD， slack, speech 等。

因为本人比较感兴趣的是基于电子书的功能，所以本着最小化原则，只配置电子书相关的设置。如果其他服务也需要介绍可以继续提 issue。

本文旨在帮助小白在自己服务器中部署，对已经了解的内容，可以直接跳过。

### OpenAI API key

OpenAI 的 API key 是必须的。获取 key 的方式也比较简单。如果已经拥有了，可以直接忽略次步骤。

步骤如下：

- 打开并登录：https://platform.openai.com/account/api-keys
- 点击 Create new secret key 即可。

### 创建和配置 Slack 应用

Slack 应用可能大家比较少创建，因此本文将通过详细的图片过程讲解如何快速创建一个 slack bot。具体步骤如下：

1、登录 https://api.slack.com/apps

2、 点击 Create New App 按钮，在弹出菜单中，选择 From scratch

![Slack](../assets/images/slack_1.png?raw=true "Slack")

3、输入 App 名称，选择你的工作空间，点击右下角创建即可。

![Slack](../assets/images/slack_2.png?raw=true "Slack")

4、进入页面后，点击 Add features and functionality 下的 Bot

![Slack](../assets/images/slack_3.png?raw=true "Slack")

5、进入页面后，点击 Review Scopes to Add

![Slack](../assets/images/slack_4.png?raw=true "Slack")

6、下拉到 Scopes 部分，点击 Add an OAuth Scope，添加下图所示的 Scope

![Slack](../assets/images/slack_5.png?raw=true "Slack")

7、回到当前页面上方，点击 install to Workspace 按钮，按照提示安装。

![Slack](../assets/images/slack_6.png?raw=true "Slack")

8、安装完成后，这个页面就会出现如图所示的 OAuth Tokens for Your Workspace。记录下 Bot User OAuth token。这个将用于后面的配置。

![Slack](../assets/images/slack_7.png?raw=true "Slack")

9、进入到 Basic Information 页面。在 App Credentials 中找到 Signing Secret。这个也是后面配置需要用到的。

![Slack](../assets/images/slack_8.png?raw=true "Slack")

![Slack](../assets/images/slack_9.png?raw=true "Slack")

最后向大家推荐一个视频，视频里有非常详细的讲解，如何创建一个 slack bot。

https://www.youtube.com/watch?v=nyyXTIL3Hkw&t=617s&ab_channel=TraversyMedia

## Dockerfile

以下是 docker 文件内容。这里有个小插曲。一开始想通过 ChatGPT 就 fly.toml 直接转换成 Docker 文件，但发觉并没有什么用。

以下是可以跑起来的 Dockerfile

```Dockerfile
FROM python:3.9-slim

ENV PORT=8080

USER root

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /data && mkdir /data/myGPTReader

EXPOSE 8080

CMD ["gunicorn", "app.server:app"]
```

## 部署

因为有比较多的环境变量，所以使用 dokcer compose 部署。具体步骤如下：

1、克隆本项目代码:

```shell
git clone https://github.com/madawei2699/myGPTReader.git
```

2、增加 Dockerfile。将上面的 Dockerfile 内容复制在本项目的根目录中。

3、构建项目

```shell
docker build -t gptreader:lastest .
```

4、在服务器的任意目录新建一个文件夹，文件夹中将包含两个文件。

```
.env
docker-compose.yaml
```

以下是 `docker-compose.yaml` 内容。

```docker
services:
  web:
    image: gptreader:lastest
    environment:
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      SLACK_TOKEN: ${SLACK_TOKEN}
      SLACK_SIGNING_SECRET: ${SLACK_SIGNING_SECRET}
    ports:
      - ${PORT}:8080
```

以下是 `.env` 内容。

```env
CF_ACCESS_CLIENT_ID='your_client_id'
CF_ACCESS_CLIENT_SECRET='your_client_secret'
PHANTOMJSCLOUD_API_KEY='your_api_key'
OPENAI_API_KEY='输入你的 OpenAI API key'
SLACK_TOKEN='输入你的 Slack Bot User OAuth token'
SLACK_SIGNING_SECRET='输入你的 Slack Signing Secret'
SPEECH_KEY='your_azure_speech_key'
SPEECH_REGION='your_azure_speech_region'
PORT=8080
```

其中，`OPENAI_API_KEY` 是我们之前获取到的 OpenAI API key, `SLACK_TOKEN` 是 Slack Bot User OAuth token，`SLACK_SIGNING_SECRET` 是上述的 Slack Signing Secret。 Port 端口可以任意指定，这里使用的是 8080 端口。

5、执行如下命令启动服务。

```
docker-compose up -d
```

6、配置 slack 的事件订阅。

最后一步，就是需要让 slack 知道通过那个 url 可以访问到你的服务器。如果你没有配置域名，通常这个地址是：

```
http://你的ip:端口/slack/events
```

如

```
http://192.168.1.2:8080/slack/events
```

## 总结

自此，通过 docker 部署本项目已经完成。可以到 slack 中 @ 你所创建的机器人即可。

最后的最后，你需要配置一下 pdf 的执行白名单。在 `app/server.py` 代码里找到 `temp_whitelist_channle_id`。需要到 slack 里面，右键点击你的 channel，找到对应的 channel 名称，替换一下即可。

另外，上传限制也是。找到同一个文件的 `max_file_size` 参数，修改一下。

修改代码后，需要重新 build 一下 docker image， 即执行

```shell
docker build -t gptreader:lastest .
```
