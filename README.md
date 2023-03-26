# myGPTReader

myGPTReader is a slack bot that can read any webpage, ebook, video(YouTube) or document and summarize it with chatGPT. It can also talk to you via voice using the content in the channel.

> The exciting part is that the development of this project is also paired with chatGPT. I document the development process in this [CDDR](docs/chatGPT/CDDR.md) file.

## Main Features

- Stay updated with the latest news summaries daily with chatGPT.
  ![my-gpt-reader-read-hot-news-1-s-min](https://user-images.githubusercontent.com/2446612/227771698-961cf6ee-c28a-44a0-811d-22b28578e8a9.gif)
- Use chatGPT to read and provide a summary of any webpage include the video(YouTube).
  ![my-gpt-reader-read-web-page-1](https://user-images.githubusercontent.com/2446612/227771860-1a6182d4-1e12-49a4-9adc-f170a338f1ce.gif)
  ![](https://img.bmpi.dev/my-gpt-reader-read-web-page-2.gif)
- Use chatGPT to read and provide a summary of any document include the eBook.
  ![my-gpt-reader-read-pdf-1-s-min](https://user-images.githubusercontent.com/2446612/227771769-96b3ee60-232f-4992-bf50-c57ff1b0ffe4.gif)
  ![](https://img.bmpi.dev/my-gpt-reader-read-epub-1.gif)
- Enjoy customizable prompt templates that use context from previous conversations with chatGPT.
  ![](https://img.bmpi.dev/my-gpt-reader-prompt-template-1.gif)
- Practice speaking languages by conversing with chatGPT using your voice.
  ![](https://img.bmpi.dev/my-gpt-reader-voice-1.gif)
  ![](https://img.bmpi.dev/my-gpt-reader-voice-2.gif)

Please join this [slack channel](https://slack-redirect.i365.tech/) to experience all these features for free.

![](https://img.bmpi.dev/my-gpt-reader-showcase.gif)

## TODO List

- [x] Integrated with slack bot
  - [x] Bot replies messages in the same thread
- [x] Support web page reading with chatGPT
  - [x] Consider to use cloudflare worker to scrape the html content
    - [x] Self-hosting [Web Scraper](https://github.com/adamschwartz/web.scraper.workers.dev)
    - [x] Restrict to access the web scraper, only allow the API server to access it by [Cloudflare Access](https://www.cloudflare.com/products/zero-trust/access/)
  - [x] Consider to use a headless browser to scrape the web page content like twitter thread
    - ~~https://www.browserless.io/~~
    - https://phantomjscloud.com/
    - https://scrapfly.io/
  - [ ] Consider to use OCR to scrape the web page content (Web crawler to get the screenshot, then OCR to get the text)
    - ~~[Azure OCR](https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/overview-ocr)~~
    - [Google Vision](https://cloud.google.com/vision)
    - may use GPT4
- [x] Support RSS reading with chatGPT
  - RSS is a bunch of links, so it is equivalent to reading a web page to get the content.
- [x] ~~Support newsletter reading with chatGPT~~
  - Most newsletters are public and can be accessed online, so we can just give the url to the slack bot.
- Prompt fine-tue
  - [x] Support for custom `prompt`
  - [x] Show `prompt` templates by slack app slash commands
  - [ ] Auto collect the good `prompt` to `#gpt-prompt` channel by message shortcut
- Cost saving
  - [x] by caching the web page llama index
    - ~~Consider to use [sqlite-vss](https://github.com/asg017/sqlite-vss) to store and search the text embeddings~~
    - ~~Use [chromadb](https://github.com/chroma-core/chroma) to store and search the text embeddings~~
    - Use the llama index file to restore the index
  - [x] Consider to use [sentence-transformers](https://github.com/UKPLab/sentence-transformers) or [txtai](https://github.com/neuml/txtai) to generate [embeddings](https://github.com/asg017/sqlite-vss/blob/main/examples/headlines/build/add_embeddings.py) (vectors)
    - Not good as the embeddings of OpenAI, rollback to use the OpenAI embeddings, and if enable to use the custom embeddings, the minimum of server's memory is 2GB which still increase the cost.
  - [ ] Consider to fine-tue the chunk size of index node and prompt to save the cost
    - If the chunk size is too big, it will cause the index node to be too large and the cost will be high.
- [x] Bot can read historical messages from the same thread, thus providing context to chatGPT
  - [x] [Changing the number of output tokens](https://github.com/jerryjliu/llama_index/issues/778#issuecomment-1478303173)
- Index fine-tune
  - [x] Use the [GPTListIndex](https://github.com/jerryjliu/llama_index/issues/753#issuecomment-1472387421) to summarize multiple URLs
  - [ ] Use the `GPTTreeIndex` with `summarize` mode to summarize a single web page
    - Use [response_mode](https://gist.github.com/ninehills/ecf7107574c83016e8b68965bf9a51c4) to change the summary mode
- Bot regularly send hot ~~summarizes(expensive cost)~~ news in the slack channel (`#daily-news`)
  - [x] Use chatGPT to summarize the hot news
  - ~~Refer to [this](https://github.com/SkywalkerDarren/chatWeb/blob/c2ad05a97aecbe1bc0c846476ea003640f2a0f2e/main.py#L144-L175) approach~~
    - World News
      - [x] Zhihu daily hot answers
      - [x] V2EX daily hot topics
      - [x] 1point3acres daily hot topics
      - [x] Reddit world hot news
    - Dev News
      - [x] Hacker News daily hot topics
      - [x] Product Hunt daily hot topics
    - Invest News
      - [x] Xueqiu daily hot topics
      - [x] Jisilu daily hot topics
- Support file reading and analysis 💥
  - Considering the expensive billing, it needs to use the slack userID whitelist to restrict the access this feature
  - Need to cache the file Documents to save extract cost
  - [x] EPUB
  - [x] DOCX
  - [x] MD
  - [x] TEXT
  - [x] PDF
    - Use [Google Vision](https://cloud.google.com/vision/docs/pdf) to handle the PDF reading
  - [ ] Image
    - may use GPT4
- [x] Support voice reading ~~with self-hosting [whisper](https://github.com/aarnphm/whispercpp)~~
  - (whisper -> chatGPT -> azure text2speech) to play language speaking practices 💥
  - Support language
    - Chinese
    - English
      - 🇺🇸
      - 🇬🇧
      - 🇦🇺
      - 🇮🇳
    - Japanese
    - German
- Support video summarization
  - [x] YouTube
- [x] User access limit
  - Limit the number of requests to bot per user per day to save the cost
- IM Support
  - [x] Slack bot
  - [ ] Discord bot
  - [ ] Telegram bot
- Bot landing page 🚩
  - [ ] Use [earlybird](https://earlybird.im/) to build the landing page
  - [ ] SEO optimization
  - [ ] Traffic analysis
    - [mixpanel](https://mixpanel.com/get-demo/free-plan/)
    - [beamanalytics](https://beamanalytics.io/)
  - [ ] [Screen recordings](https://www.screen.studio/) to show how to use the bot
- [ ] Integrated with Azure OpenAI Service
- [ ] Rewrite the code in Typescript ❓
- [ ] Upgrade chat model (gpt-3.5-turbo) to GPT4 (gpt-4-0314) 💥
- Publish bot to make it can be used in other workspaces
  - [ ] Slack marketplace

## Documentation

Currently, if you want to know this repo quickly, you can refer to the following YouTube video:

[![myGPTReader Live Share](http://img.youtube.com/vi/XZIogwFU7jE/0.jpg)](https://www.youtube.com/live/XZIogwFU7jE?feature=share "myGPTReader Live Share")

## Post

- [我的AI阅读助手](https://www.bmpi.dev/self/my-gpt-reader/)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=madawei2699/myGPTReader&type=Date)](https://star-history.com/#madawei2699/myGPTReader&Date)
