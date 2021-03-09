const { registerUser, login } = require("./utils")

describe("SecFit", () => {
  beforeAll(async () => {
    await page.goto("https://secfit.vassbo.as");
  });

  it('should be titled "SecFit"', async () => {
    const navTitle = await page.$(".navbar-brand");
    const title = await page.evaluate((title) => title.innerText, navTitle);
    expect(title).toBe("SecFit");
  });
});


describe("Secfit register", () => {
   test("Register user", async () => {
    await registerUser();
  }, 25000);

})


describe("Secfit login", () => {
  beforeAll(async () => {
    await page.goto("https://secfit.vassbo.as");
  });

  
  test("Log in", async () => {
    await page.waitForSelector("#btn-login-nav");

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-login-nav");

    await login();
  }, 25000);
});


