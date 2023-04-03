const {
	createPool
} = require("generic-pool");
const cheerio = require('cheerio');
const puppeteer = require("puppeteer");
const pool = createPool({
	async create() {
		const params = {
			headless: true,
		};
		const isDev = process.env.USER_ENV === "development";
		if (!isDev) {
			params.executablePath = "/usr/bin/chromium";
			params.args = ["--no-sandbox"];
		}
		return await puppeteer.launch(params);
	},
	async destroy(browser) {
		return await browser.close();
	},
}, {
	max: 10,
	min: 2,
});
exports.pupRequest = async function (url) {
	console.log("html2text url =>", url);

	const browser = await pool.acquire();
	const page = await browser.newPage();
	await page.goto(url, {
		waitUntil: "domcontentloaded",
		timeout: 30000
	});
	const content = await page.content();
	await page.close();

	pool.release(browser);

	// return content
	// 加载 HTML 文档
	const $ = cheerio.load(content);

	// 获取 body 内容
	const bodyContent = $('body').html();

	return bodyContent;
}