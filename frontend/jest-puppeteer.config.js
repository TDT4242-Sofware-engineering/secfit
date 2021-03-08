
module.exports = {
  launch: {
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
    ],
      headless: false,
      slowMo: process.env.SLOWMO ? process.env.SLOWMO : 0,
      devtools: true
  }
}