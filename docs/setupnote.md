# 部署myGPTReader笔记与感想

在twitter上看到大伟老师发布的myGPTReader应用，第一时间就非常想自己搞一套，这正是我想实现的，但苦于不会编程，没法自己实现。

看过大伟老师的readme后，对这个应用充满期待，在slack里也体验了一下，感觉非常适合我的需求。于是迫不及待的开始了自己的部署过程。

一般有安装手册的应用，我大多可以按照步骤自己部署好，但这个程序目前还没有部署手册，一开始挺着急，看不懂如何运行的。

后来通过询问chatGPT，我找到了部署的方法，基本都是通过双向与GPT交互实现的。

## 与chatGPT的交互过程

我把所有文件内容都发给了GPT，让它告诉我每个文件的功能和用途。

突破口在fly.toml文件，GPT告诉我它是fly.io的配置文件，顺藤摸瓜知道了fly应用。

通过env里面的环境变量和几个函数，了解到使用了cloudflare、azure speech、phantomjscloud、fly、slack等应用。

之后我把每一步的部署都发给GPT，只要是有日志输出的情况，基本都能通过几次交互找到正确方法。

## 准备工作

1、申请一个新的openai账号，获取OPENAI_API_KEY

2、申请一个新的slack频道，创建一个slack应用并发布到对应的slack频道，获取SLACK_TOKEN和SLACK_SIGNING_SECRET

以上2步是最先做了，完成后部署了应用，跑通后再继续完善了后面的服务

3、注册fly.io账号，绑定信用卡

4、fork myGPTReader，并clone到本地

5、修改必要的配置文件
	- fly.toml
	- vip_whitelist.txt 增加自己的userid
	- 将/data修改为/tmp （主要是因为不知道如何挂在data）


## 部署过程

### 部署应用slack

1、安装flyctl：

2、运行fly launch，修改配置文件
ps：一步一步配置后，配置文件与fork有了区别，我又把配置覆盖回去了

3、flyctl auth login 终端登录到fly

4、flyctl deploy 部署程序

5、flyctl secrets set OPENAI_API_KEY=...，设置openai和slack的3个api token

6、flyctl status查看状态为started

7、通过https://fly.io/apps/hostname/monitoring可以查看后台日志

8、在fly的overview中，能看到hostname，这个地址+/slack/events就是slack的服务地址

9、在slack中配置上面的服务地址后，再更新下slack的token的授权范围

10、测试slack无响应，在slack中尝试不行，之后通过GPT提示，卸载了应用重新安装，成功了。即可实现slack中@appname得到回复

到此步，基本验证服务流程跑通。

PS：在测试文章抓取功能时，每次都会报out of memey，最后把fly服务升级了下，提高了运行内存，问题得到解决。


### 其他服务配置

1、语音对话通过azure speech实现，需要申请一个账号，并开通speech服务，需要绑定银行卡支付，有一年免费

2、页面抓取分两部分，其中phantomjscloud比较简单，申请账号后直接获取token即可

3、相对有点难度的是cloudflare的抓取服务，主要一开始我没找到代码在哪，看大伟老师代码是自己部署的一个服务

4、后来尝试了让GPT来反向页面抓取那部分代码，知道了是通过cloudflare worker实现的，并让GPT给我实现了一个代码

5、实现的代码多次调试后不太理想，最后还是在大伟老师的github工程里发现了web.scraper.workers.dev工程

6、这个工程有个一键部署，绑定github和cloudflare可实现自动部署，如果不需要access保护，到此就完事了

7、我目前还没把最后的access验证做完，主要是域名验证还没完成


## 其他事项

以上应用的的绝大部分应用，除了github我都没用过，放到以前让我没有手册情况完成部署，真的难以想象，学习成本巨大。

有了chatGPT后，只要知道了具体用的什么服务，通过跟chatGPT的交互，完全可以找到正确的部署过程，这个很厉害。

在问GPT每一步怎么执行时，我都会问如何验证测试，包括申请到的api key，都先测试了一下，这样避免后面不好找问题。

而GPT真的能很好的给出测试方法，只要丢给他反馈，就算第一次给的方法不对，也能很快纠正。

整个部署过程花了不到1天时间，部署了8个版本，我自己还是挺兴奋的。以后可以在此基础上持续的完善了。

最后要非常感谢大伟老师：https://twitter.com/madawei2699

![showgif](https://github.com/nigdaemon/myGPTReader/blob/main/docs/myGPTReader.gif)
