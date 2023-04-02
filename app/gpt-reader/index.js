const express = require("express");
const bodyParser = require("body-parser");
const {
  pupRequest
} = require('./puppeteer');

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: false
}));

async function processRequest(req, res) {
  try {
    const {
      url
    } = req.body;

    const content = await pupRequest(url);

    console.log('获取网站内容成功');
    res.send("Data Received: " + JSON.stringify(content));
  } catch (err) {
    res.send(`puppeteer 服务出现异常: ${err.message}`);
  }
}

app.post("/web-crawler", (req, res) => {
  processRequest(req, res);
});

const port = 4000;
app.listen(port, () => {
  console.log(`Example app listening on port ${port}!`);
});