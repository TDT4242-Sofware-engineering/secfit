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

const registerUser = async () => {
  await page.waitForSelector("#btn-register");
    await page.evaluate(
      (selector) => document.querySelector(selector).click(),
      "#btn-register"
    );
    console.log("Register button clicked");

    await page.waitForNavigation();

    await page.waitForSelector('input[name="username"]');
    await page.type('input[name="username"]', "testUser");
    await page.waitForSelector('input[name="email"]');
    await page.type('input[name="email"]', "test@test.no");
    await page.waitForSelector('input[name="password"]');
    await page.type('input[name="password"]', "test");
    await page.waitForSelector('input[name="password1"]');
    await page.type('input[name="password1"]', "test");
    await page.waitForSelector('input[name="phone_number"]');
    await page.type('input[name="phone_number"]', "95837412");
    await page.waitForSelector('input[name="country"]');
    await page.type('input[name="country"]', "Norway");
    await page.waitForSelector('input[name="city"]');
    await page.type('input[name="city"]', "Oslo");
    await page.waitForSelector('input[name="street_address"]');
    await page.type('input[name="street_address"]', "Munkegata 36");
    
    await page.evaluate(
      (selector) => document.querySelector(selector).click(),
      "#btn-create-account"
    );
    console.log("Create account button clicked");

    await page.waitForNavigation();

    const logoutButton = await page.$("#btn-logout");
    const logoutText = await page.evaluate((title) => title.innerText, logoutButton);
    expect(logoutText).toBe("Log out");




}