
async function registerUser(user) {
  await page.waitForSelector("#btn-register");
    await page.evaluate(
      (selector) => document.querySelector(selector).click(),
      "#btn-register"
    );
    console.log("Register button clicked");

    await page.waitForNavigation();

    console.log("Using user: ", user)

    await page.waitForSelector('input[name="username"]');
    await page.type('input[name="username"]', user.username);
    await page.waitForSelector('input[name="email"]');
    await page.type('input[name="email"]', user.email);
    await page.waitForSelector('input[name="password"]');
    await page.type('input[name="password"]', user.password);
    await page.waitForSelector('input[name="password1"]');
    await page.type('input[name="password1"]', user.password);
    await page.waitForSelector('input[name="phone_number"]');
    await page.type('input[name="phone_number"]', user.phone_numer);
    await page.waitForSelector('input[name="country"]');
    await page.type('input[name="country"]', user.country);
    await page.waitForSelector('input[name="city"]');
    await page.type('input[name="city"]', user.city);
    await page.waitForSelector('input[name="street_address"]');
    await page.type('input[name="street_address"]', user.street_name);
    
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

async function login(user) {
  console.log("Login as user: ", user)
  await page.waitForSelector("#form-login");
  await page.waitForSelector('input[name="username"]');
  await page.waitForSelector('input[name="password"]');
  await page.waitForSelector("#btn-login");

  await page.type('input[name="username"]', user.username);
  await page.type('input[name="password"]', user.password);

  await page.evaluate((selector) => {
    document.querySelector(selector).click();
  }, "#btn-login");

  await page.waitForNavigation();

    const logoutButton = await page.$("#btn-logout");
    const logoutText = await page.evaluate(
      (title) => title.innerText,
      logoutButton
    );
    expect(logoutText).toBe("Log out");
}

module.exports = {
    registerUser, 
    login
}