const { registerUser, login } = require("./utils")
const user = require("./mock/user.json");


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


// describe("Secfit register", () => {
//    test("Register user", async () => {
//     await registerUser();
//   }, 25000);

// })


describe("Secfit login", () => {
  beforeAll(async () => {
    await page.goto("https://secfit.vassbo.as");
  });


  test("Log in", async () => {
    await page.waitForSelector("#btn-login-nav");

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-login-nav");
    await page.waitForNavigation();


    await login();
  }, 25000);
});



describe("Profile functionality", () => {
  beforeAll(async () => {
    await page.goto("https://secfit.vassbo.as");
  });

  test("access to profile page", async () => {
    await page.waitForSelector("#btn-login-nav");

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-login-nav");
    await page.waitForNavigation();

    await login();

    await page.waitForSelector("#nav-profile");
    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#nav-profile");
    await page.waitForNavigation();

    await page.waitForSelector("#form-profile");
  }, 25000);

  // Read profile info
  test("read profile info", async () => {
    await page.waitForSelector('input[name="username"]');

    await page.waitForSelector('input[name="email"]');
    const username = await page.evaluate(
      (field) => document.querySelector(field).value,
      "#inputUsername"
    );
    expect(username).toEqual(user.username);


    await page.waitForSelector('input[name="email"]');
    const email = await page.evaluate(
      (field) => document.querySelector(field).value,
      'input[name="email"]'
    );
    expect(email).toEqual(user.email);

    await page.waitForSelector('input[name="phone_number"]');
    const phone_number = await page.evaluate(
      (field) => document.querySelector(field).value,
      'input[name="phone_number"]'
    );
    expect(phone_number).toEqual(user.phone_numer);

    await page.waitForSelector('input[name="street_address"]');
    const street_address = await page.evaluate(
      (field) => document.querySelector(field).value,
      'input[name="street_address"]'
    );
    expect(street_address).toEqual(user.street_name);

    await page.waitForSelector('input[name="city"]');
    const city = await page.evaluate(
      (field) => document.querySelector(field).value,
      'input[name="city"]'
    );
    expect(city).toEqual(user.city);

    await page.waitForSelector('input[name="country"]');
    const country = await page.evaluate(
      (field) => document.querySelector(field).value,
      'input[name="country"]'
    );
    expect(country).toEqual(user.country);
  }, 20000);

// Edit profile
  test("edit profile", async () => {

    await page.waitForSelector("#btn-edit-profile");
    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-edit-profile");
    console.log("clicked edit button")


    await page.waitForSelector('input[name="username"]');
    await page.evaluate(
      (field) => document.querySelector(field).value === + "Annika" ,
      "#inputUsername"
    );

    await page.waitForSelector('input[name="email"]');
    await page.evaluate(
      (field) => document.querySelector(field).value === user.email + "1",
      'input[name="email"]'
    );

    await page.waitForSelector('input[name="phone_number"]');
   await page.evaluate(
      (field) => document.querySelector(field).value === user.phone_numer + "1" ,
      'input[name="phone_number"]'
    );

    await page.waitForSelector('input[name="street_address"]');
    await page.evaluate(
      (field) => document.querySelector(field).value === user.street_name + "1", 
      'input[name="street_address"]'
    );

    await page.waitForSelector('input[name="city"]');
    const city = await page.evaluate(
      (field) => document.querySelector(field).value === user.city + "1",
      'input[name="city"]'
    );
    
    await page.waitForSelector('input[name="country"]');
    const country = await page.evaluate(
      (field) => document.querySelector(field).value === user.country + "1", 
      'input[name="country"]'
    );

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-confirm-edit");
    console.log("clicked confirm edit button")


  })


});
