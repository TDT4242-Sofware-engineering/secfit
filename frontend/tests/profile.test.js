// describe("Profile functionality", () => {
//   beforeAll(async () => {
//     await page.goto("https://secfit.vassbo.as");
//   });

//   test("access to profile page", async () => {
//     await page.waitForSelector("#btn-login-nav");

//     await page.evaluate((selector) => {
//       document.querySelector(selector).click();
//     }, "#btn-login-nav");
//     await page.waitForNavigation();

//     await login();

//     await page.waitForSelector("#nav-profile");
//     await page.evaluate((selector) => {
//       document.querySelector(selector).click();
//     }, "#nav-profile");
//     await page.waitForNavigation();

//     await page.waitForSelector("#form-profile");
//   }, 25000);

//   test("read profile info", async () => {
//     await page.waitForSelector('input[name="username"]');

//     await page.waitForSelector('input[name="email"]');
//     const username = await page.evaluate(
//       (field) => document.querySelector(field).value,
//       "#inputUsername"
//     );
//     expect(username).toEqual(user.username);


//     await page.waitForSelector('input[name="email"]');
//     const email = await page.evaluate(
//       (field) => document.querySelector(field).value,
//       'input[name="email"]'
//     );
//     expect(email).toEqual(user.email);

//     await page.waitForSelector('input[name="phone_number"]');
//     const phone_number = await page.evaluate(
//       (field) => document.querySelector(field).value,
//       'input[name="phone_number"]'
//     );
//     expect(phone_number).toEqual(user.phone_number);

//     await page.waitForSelector('input[name="street_address"]');
//     const street_address = await page.evaluate(
//       (field) => document.querySelector(field).value,
//       'input[name="street_address"]'
//     );
//     expect(street_address).toEqual(user.street_address);

//     await page.waitForSelector('input[name="city"]');
//     const city = await page.evaluate(
//       (field) => document.querySelector(field).value,
//       'input[name="city"]'
//     );
//     expect(city).toEqual(user.city);

//     await page.waitForSelector('input[name="country"]');
//     const country = await page.evaluate(
//       (field) => document.querySelector(field).value,
//       'input[name="country"]'
//     );
//     expect(country).toEqual(user.country);
//   }, 20000);
// });
