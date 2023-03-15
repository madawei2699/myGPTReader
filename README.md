# myGPTReader

myGPTReader is a slack bot that reads web pages and summarizes them with chatGPT. You can use it to read news and summarize them in your slack channel.

For now it is in development, but you can try it out by join this [channel](https://join.slack.com/t/bmpidev/shared_invite/zt-1r38f90n5-bOp~RZqoMYiYMOtmKZsbcw).

> The exciting part is that the development of this project is also paired with chatGPT. I document the development process in this [CDDR](docs/chatGPT/CDDR.md) file.

## Features

- [x] Integrate with slack bot
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
- Prompt fine-tue 🚩
  - [ ] Support for custom `prompt`
  - [ ] Auto collect the good `prompt` from the slack channel by emoji reactions
- Cost saving 🚩
  - [ ] by caching the web page llama index
- [ ] Bot can read historical messages from the same thread, thus providing context to chatGPT 🚩
- [ ] Bot regularly summarizes news in the slack channel 🚩
- Support file reading and analysis
  - [ ] PDF
  - [ ] epub
  - [ ] image
    - may use GPT4
  - [ ] docx
  - [ ] txt
- [ ] Support voice reading with self-hosting [whisper](https://github.com/aarnphm/whispercpp)❓
- [ ] Support discord bot ❓
- [ ] Rewrite the code in Typescript ❓
- [ ] Upgrade chat model (gpt-3.5-turbo) to GPT4 (gpt-4-0314) 💥
- [ ] Documentation
- Publish bot to make it can be used in other workspaces
  - [ ] Slack marketplace
