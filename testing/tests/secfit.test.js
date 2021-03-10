const { registerUser, login } = require("./utils")
const user = require("./mock/user.json");
const exercise = require("./mock/exercise.json")
const url = "https://secfit.vassbo.as/index.html"


// describe("SecFit", () => {
//   beforeAll(async () => {
//     await page.goto(url);
//   });

//   it('should be titled "SecFit"', async () => {
//     const navTitle = await page.$(".navbar-brand");
//     const title = await page.evaluate((title) => title.innerText, navTitle);
//     expect(title).toBe("SecFit");
//   });
// });


// describe("Secfit register", () => {
//    test("Register user", async () => {
//     await registerUser();
//   }, 25000);

// })


// describe("Secfit login", () => {
//   beforeAll(async () => {
//     await page.goto(url);
//   });


//   test("Log in", async () => {
//     await page.waitForSelector("#btn-login-nav");

//     await page.evaluate((selector) => {
//       document.querySelector(selector).click();
//     }, "#btn-login-nav");
//     await page.waitForNavigation();


//     await login();
//   }, 25000);
// });



// describe("Profile functionality", () => {
//   beforeAll(async () => {
//     await page.goto(url);
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

  // // Read profile info
  // test("read profile info", async () => {


  //   await page.waitForSelector('input[name="username"]');
  //   const username = await page.evaluate(
  //     (field) => document.querySelector(field).value,
  //     "#inputUsername"
  //   );
  //   expect(username).toEqual(user.username);


  //   await page.waitForSelector('input[name="email"]');
  //   const email = await page.evaluate(
  //     (field) => document.querySelector(field).value,
  //     'input[name="email"]'
  //   );
  //   expect(email).toEqual(user.email);

  //   await page.waitForSelector('input[name="phone_number"]');
  //   const phone_number = await page.evaluate(
  //     (field) => document.querySelector(field).value,
  //     'input[name="phone_number"]'
  //   );
  //   expect(phone_number).toEqual(user.phone_numer);

  //   await page.waitForSelector('input[name="street_address"]');
  //   const street_address = await page.evaluate(
  //     (field) => document.querySelector(field).value,
  //     'input[name="street_address"]'
  //   );
  //   expect(street_address).toEqual(user.street_name);

  //   await page.waitForSelector('input[name="city"]');
  //   const city = await page.evaluate(
  //     (field) => document.querySelector(field).value,
  //     'input[name="city"]'
  //   );
  //   expect(city).toEqual(user.city);

  //   await page.waitForSelector('input[name="country"]');
  //   const country = await page.evaluate(
  //     (field) => document.querySelector(field).value,
  //     'input[name="country"]'
  //   );
  //   expect(country).toEqual(user.country);
  // }, 20000);


  // // Cancel edit profile
  // test("cancel edit email", async () => {

  //   await page.waitForSelector("#btn-edit-profile");

  //   await page.evaluate((selector) => {
  //     document.querySelector(selector).click();
  //   }, "#btn-edit-profile");
  //   console.log("clicked edit button")

  //   await page.waitForSelector("#btn-cancel-edit");

  //   await page.evaluate((selector) => {
  //     document.querySelector(selector).click();
  //   }, "#btn-cancel-edit");
  //   console.log("clicked cancel edit button")

  //   await page.waitForSelector("#btn-edit-profile");
  //   console.log("cancelled edit")

  // })

  // // Edit profile
  // test("edit profile", async () => {

  //   await page.waitForSelector("#btn-edit-profile");

  //   await page.evaluate((selector) => {
  //     document.querySelector(selector).click();
  //   }, "#btn-edit-profile");
  //   console.log("clicked edit button")


  //   await page.waitForSelector('input[name="username"]');
  //   await page.evaluate(
  //     (field) => document.querySelector(field).value = "Annika",
  //     "#inputUsername"
  //   );

  //   await page.waitForSelector('input[name="email"]');
  //   await page.evaluate(
  //     (field) => document.querySelector(field).value = "new@email.com",
  //     'input[name="email"]'
  //   );

  //   await page.waitForSelector('input[name="phone_number"]');
  //   await page.evaluate(
  //     (field) => document.querySelector(field).value = "123",
  //     'input[name="phone_number"]'
  //   );

  //   await page.waitForSelector('input[name="street_address"]');
  //   await page.evaluate(
  //     (field) => document.querySelector(field).value = "munkegata 36",
  //     'input[name="street_address"]'
  //   );

  //   await page.waitForSelector('input[name="city"]');
  //   const city = await page.evaluate(
  //     (field) => document.querySelector(field).value = "Trondheim",
  //     'input[name="city"]'
  //   );

  //   await page.waitForSelector('input[name="country"]');
  //   const country = await page.evaluate(
  //     (field) => document.querySelector(field).value = "Sweden",
  //     'input[name="country"]'
  //   );

  //   await page.evaluate((selector) => {
  //     document.querySelector(selector).click();
  //   }, "#btn-confirm-edit");
  //   console.log("clicked confirm edit button")

  //   await page.waitForSelector('input[name="username"]');
  //   const username = await page.evaluate(
  //     (field) => document.querySelector(field).value,
  //     "#inputUsername"
  //   );
  //   expect(username).toEqual("Annika");


  // })


  // // cancel delete profile
  // test("cancel delete profile", async () => {

  //   await page.waitForSelector("#btn-edit-profile");

  //   await page.evaluate((selector) => {
  //     document.querySelector(selector).click();
  //   }, "#btn-edit-profile");
  //   console.log("clicked edit profile button")

  //   await page.waitForSelector("#btn-initiate-delete");
  //   await page.evaluate((selector) => {
  //     document.querySelector(selector).click();
  //   }, "#btn-initiate-delete");
  //   console.log("clicked delete profile button")

  //   await page.waitForSelector("#btn-cancel-delete");
  //   await page.evaluate((selector) => {
  //     document.querySelector(selector).click();
  //   }, "#btn-cancel-delete");
  //   console.log("clicked cancel delete profile button")

  //   await page.waitForSelector('input[name="username"]');

  // })

  // delete profile
  // test("delete profile", async () => {

  //   await page.waitForSelector("#btn-edit-profile");

  //   await page.evaluate((selector) => {
  //     document.querySelector(selector).click();
  //   }, "#btn-edit-profile");
  //   console.log("clicked edit profile button")

  //   await page.waitForSelector("#btn-initiate-delete");
  //   await page.evaluate((selector) => {
  //     document.querySelector(selector).click();
  //   }, "#btn-initiate-delete");

  //   console.log("clicked delete profile button")

  //   await page.waitForSelector("#btn-delete-user");
  //   await page.evaluate((selector) => {
  //     document.querySelector(selector).click();
  //   }, "#btn-delete-user");

  //   console.log("clicked confirm delete profile button")

  //   await page.waitForNavigation();

  //   await page.waitForSelector("#btn-login-nav");
  //   console.log("user deleted")

  // })

// });

describe("exercise page", async () => {
  beforeAll(async () => {
    await page.goto(url)
  })

  //access exercise page
  test("access exercise page", async () =>{
    await page.waitForSelector("#btn-login-nav");

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-login-nav");
    await page.waitForNavigation();

    await login();

    await page.waitForSelector("#nav-exercises");
    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#nav-exercises");
    await page.waitForNavigation();

    await page.waitForSelector("#btn-create-exercise");
  })

  // new exercise
  test("create exercise", async () =>{
    await page.waitForSelector("#btn-create-exercise");

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-create-exercise");
    await page.waitForNavigation();

    await page.waitForSelector("#inputName");
    await page.type("#inputName", exercise.name)

    await page.waitForSelector("#inputDescription");
    await page.type("#inputDescription", exercise.description)

    await page.waitForSelector("#inputUnit");
    await page.type("#inputUnit", exercise.unit)

    // await page.waitForSelector("#customFile");
    // await page.evaluate((selector) => {
    //   document.querySelector(selector).click();
    // }, "#customFile");
    // const uploadHandle = await page.$('input[type="file"]')
    // uploadHandle.uploadFile("./mock/image.jpg");

    await page.waitForSelector("#btn-ok-exercise");
    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-ok-exercise");

    await page.waitForNavigation();

    await page.waitForSelector("#btn-create-exercise");
    
  }, 25000)

  // read exercise
  test("look at exercise", async () =>{
    await page.waitForSelector("#div-content");

    const exercises = await page.$$("a");
    await page.evaluate((field) => field.click(), exercises[exercises.length -1]);
    
    await page.waitForSelector("#inputName");
    const name = await page.evaluate(
      (field) => document.querySelector(field).value,
      "#inputName"
    );
    expect(name).toEqual(exercise.name);

    await page.waitForSelector("#inputDescription");
    const desc = await page.evaluate(
      (field) => document.querySelector(field).value,
      "#inputDescription"
    );
    expect(desc).toEqual(exercise.description);

    await page.waitForSelector("#inputUnit");
    const unit = await page.evaluate(
      (field) => document.querySelector(field).value,
      "#inputUnit"
    );
    expect(unit).toEqual(exercise.unit);

  }, 25000)

  // edit exercise
  test("edit exercise", async () =>{

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-edit-exercise");
    
    await page.waitForSelector("#inputName");
    await page.evaluate(
      (field) => document.querySelector(field).value = "sit-ups",
      '#inputName'
    );

    await page.waitForSelector("#inputDescription");
    await page.evaluate(
      (field) => document.querySelector(field).value = "sit up and down",
      '#inputDescription'
    );
    
    await page.waitForSelector("#inputUnit");
    await page.evaluate(
      (field) => document.querySelector(field).value = "num",
      '#inputUnit'
    );

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-ok-exercise");

    await page.waitForSelector("#btn-edit-exercise");

  }, 25000)

  // delete exercise
  test("delete exercise", async () =>{

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-edit-exercise");
    
    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-delete-exercise");

    await page.waitForSelector("#btn-create-exercise");

  }, 25000)

})


