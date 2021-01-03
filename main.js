require('dotenv').config();
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
  });
  const page = await browser.newPage();

  await page.setViewport({ width: 1280, height: 800})
  await page.goto('https://gmail.com');
   
  const navigationPromise = page.waitForNavigation()


  //-  Acessa a página de login
  await page.waitForSelector('input[type="email"]')
  await page.type('input[type="email"]', process.env.GMAIL_EMAIL)
  await page.click('button[type="button"]')

  await navigationPromise

  
  await page.waitForSelector('[name="password"]')
  await page.type('[name="password"]', process.env.GMAIL_SENHA)

  //await browser.close();


})();