const user = require("./mock/user.json");

describe("Secfit", () => {
  beforeAll(async () => {
    await page.goto("https://secfit.vassbo.as");
  });

  it('should be titled "SecFit"', async () => {
    const navTitle = await page.$(".navbar-brand");
    const title = await page.evaluate((title) => title.innerText, navTitle);
    expect(title).toBe("SecFit");
  });
});

describe("Secfit login", () => {
  beforeAll(async () => {
    await page.goto("https://secfit.vassbo.as");
  });

  it("Go to login page", async () => {
    await page.waitForSelector("#btn-login-nav");

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-login-nav");

    await login();

    await page.waitForNavigation();

    const logoutButton = await page.$("#btn-logout");
    const logoutText = await page.evaluate(
      (title) => title.innerText,
      logoutButton
    );
    expect(logoutText).toBe("Log out");
  }, 25000);
});

async function login() {
  await page.waitForNavigation();
  await page.waitForSelector("#form-login");
  await page.waitForSelector('input[name="username"]');
  await page.waitForSelector('input[name="password"]');
  await page.waitForSelector("#btn-login");

  await page.type('input[name="username"]', user.username);
  await page.type('input[name="password"]', user.password);

  await page.evaluate((selector) => {
    document.querySelector(selector).click();
  }, "#btn-login");
}
