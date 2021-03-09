const { registerUser } = require("./utils")

describe("SecFit", () => {
  beforeAll(async () => {
    await page.goto("https://secfit.vassbo.as");
  });

  it('should be titled "SecFit"', async () => {
    const navTitle = await page.$(".navbar-brand");
    const title = await page.evaluate((title) => title.innerText, navTitle);
    expect(title).toBe("SecFit");
  });

  test("Register user", async () => {
    await registerUser();
  }, 25000);
});

