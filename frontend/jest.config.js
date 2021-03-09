module.exports = {
  preset: "jest-puppeteer",
  globals: {
    URL: "http://molde.idi.ntnu.no:22100/"
  },
  verbose: true,
  testTimeout: 10000
}