const { registerUser, login } = require("./utils")
const user = require("./mock/user.json");
const exercise = require("./mock/exercise.json")
const workout = require("./mock/workout.json")
const url = "https://secfit.vassbo.as/index.html"


// Initial test
describe("SecFit", () => {
  beforeAll(async () => {
    await page.goto(url);
  });

  it('should be titled "SecFit"', async () => {
    const navTitle = await page.$(".navbar-brand");
    const title = await page.evaluate((title) => title.innerText, navTitle);
    expect(title).toBe("SecFit");
  });
});

// Register user
describe("Secfit register", () => {
   test("Register user", async () => {
    await registerUser();
  }, 25000);

})

// Login user
describe("Secfit login", () => {
  beforeAll(async () => {
    await page.goto(url);
  });
 // log in
  test("Log in", async () => {
    await page.waitForSelector("#btn-login-nav");

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-login-nav");
    await page.waitForNavigation();


    await login();
  }, 25000);
});


// Exercises
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

// Workouts
describe("workout page", async () => {
  beforeAll(async () => {
    await page.goto(url)
  })

  //access workout page
  test("access workout page", async () =>{
    await page.waitForSelector("#btn-login-nav");

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-login-nav");
    await page.waitForNavigation();

    await login();

    await page.waitForSelector("#btn-create-workout");
  })

  // new workout
  test("create workout", async () =>{
    await page.waitForSelector("#btn-create-workout");

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-create-workout");
    await page.waitForNavigation();

    await page.waitForSelector("#inputName");
    await page.type("#inputName", workout.name)

    await page.waitForSelector("#inputDateTime");
    await page.type("#inputDateTime", String.fromCharCode(32));
    await page.type("#inputDateTime", String.fromCharCode(13));

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-add-athelte");

    await page.waitForSelector("#inputSearchForUser");
    await page.type("#inputSearchForUser", "Annika");

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, '[value="Annika"]');

    await page.select('#inputVisibility', 'PU')

    await page.waitForSelector("#inputNotes");
    await page.type("#inputNotes", workout.notes);

    // await page.waitForSelector("#customFile");
    // await page.evaluate((selector) => {
    //   document.querySelector(selector).click();
    // }, "#customFile");
    // const uploadHandle = await page.$('input[type="file"]')
    // uploadHandle.uploadFile("./mock/image.jpg");

    await page.select('select[name=type]', '4')

  
    await page.waitForSelector('input[name=sets]');
    await page.type('input[name=sets]', "1");

    await page.waitForSelector('[name=number]');
    await page.type('input[name=number]', "1");


    await page.waitForSelector("#btn-ok-workout");
    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-ok-workout");

    await page.waitForNavigation();

    await page.waitForSelector("#btn-create-workout");
    
  }, 25000)

  // read workout
  test("look at workout", async () =>{
    await page.waitForSelector("#div-content");

    const workouts = await page.$$(".workout");
    await page.evaluate((field) => field.click(), workouts[0]);
    
    await page.waitForSelector("#inputName");
    const name = await page.evaluate(
      (field) => document.querySelector(field).value,
      "#inputName"
    );
    expect(name).toEqual(workout.name);

    await page.waitForSelector("#inputNotes");
    const notes = await page.evaluate(
      (field) => document.querySelector(field).value,
      "#inputNotes"
    );
    expect(notes).toEqual(workout.notes);

    await page.waitForSelector("#inputOwner");
    const owner = await page.evaluate(
      (field) => document.querySelector(field).value,
      "#inputOwner"
    );
    expect(owner).toEqual("Anna");

  }, 25000)

  // edit workout
  test("edit workout", async () =>{

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-edit-workout");
    
    await page.waitForSelector("#inputName");
    await page.evaluate(
      (field) => document.querySelector(field).value = "lame workout",
      '#inputName'
    );

    await page.waitForSelector("#inputDateTime");
    await page.type("#inputDateTime", String.fromCharCode(32));
    await page.type("#inputDateTime", String.fromCharCode(13));

    await page.select('#inputVisibility', 'PR')

    await page.waitForSelector("#inputNotes");
    await page.evaluate(
      (field) => document.querySelector(field).value = "new notes",
      '#inputNotes'
    );

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-ok-workout");

    await page.waitForSelector("#btn-edit-workout");

  }, 25000)

  // delete workout
  test("delete workout", async () =>{

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-edit-workout");
    
    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-delete-workout");

    await page.waitForSelector("#btn-create-workout");

  }, 25000)

})

// Athlete page
describe("athlete page", async () => {
  beforeAll(async () => {
    await page.goto(url)
  })

  //access athlete page
  test("access athlete page", async () =>{
    await page.waitForSelector("#btn-login-nav");

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-login-nav");
    await page.waitForNavigation();

    await login();

    await page.waitForSelector("#nav-myathletes");
    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#nav-myathletes");
    await page.waitForNavigation();

    await page.waitForSelector("#button-submit-roster");
  })

  // new athlete
  test("add athlete", async () =>{
    await page.waitForSelector("#button-submit-roster");

    await page.waitForSelector("input[name='athlete']");
    await page.type("input[name='athlete']", "Annika")

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, '.btn-success');

    await page.waitForSelector(".btn-danger");

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, '#button-submit-roster');

    await page.waitForSelector("#controls");

  }, 25000)

})


// Coach page
describe("coach page", async () => {
  beforeAll(async () => {
    await page.goto(url)
  })

  //access coach page
  test("access coach page", async () =>{
    await page.waitForSelector("#btn-login-nav");

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-login-nav");
    await page.waitForNavigation();

    await login();

    await page.waitForSelector("#nav-mycoach");
    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#nav-mycoach");
    await page.waitForNavigation();

    await page.waitForSelector("#button-edit-coach");
  }, 25000)

  // new athlete
  test("add athlete", async () =>{
    await page.waitForSelector("#button-edit-coach");

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, '#button-edit-coach');

    await page.waitForSelector("input[name='coach']");
    await page.type("input[name='coach']", "Annika")

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, '#button-set-coach');

    await page.waitForSelector("#button-edit-coach");

    const coach = await page.evaluate(
          (field) => document.querySelector(field).value,
          'input[name="coach"]'
        );
    expect(coach).toEqual("Annika");

  }, 25000)

})

describe("Profile functionality", () => {
  beforeAll(async () => {
    await page.goto(url);
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


  // Cancel edit profile
  test("cancel edit email", async () => {

    await page.waitForSelector("#btn-edit-profile");

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-edit-profile");
    console.log("clicked edit button")

    await page.waitForSelector("#btn-cancel-edit");

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-cancel-edit");
    console.log("clicked cancel edit button")

    await page.waitForSelector("#btn-edit-profile");
    console.log("cancelled edit")

  })

  // Edit profile
  test("edit profile", async () => {

    await page.waitForSelector("#btn-edit-profile");

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-edit-profile");
    console.log("clicked edit button")


    await page.waitForSelector('input[name="username"]');
    await page.evaluate(
      (field) => document.querySelector(field).value = "Anita",
      "#inputUsername"
    );

    await page.waitForSelector('input[name="email"]');
    await page.evaluate(
      (field) => document.querySelector(field).value = "new@email.com",
      'input[name="email"]'
    );

    await page.waitForSelector('input[name="phone_number"]');
    await page.evaluate(
      (field) => document.querySelector(field).value = "123",
      'input[name="phone_number"]'
    );

    await page.waitForSelector('input[name="street_address"]');
    await page.evaluate(
      (field) => document.querySelector(field).value = "munkegata 36",
      'input[name="street_address"]'
    );

    await page.waitForSelector('input[name="city"]');
    const city = await page.evaluate(
      (field) => document.querySelector(field).value = "Trondheim",
      'input[name="city"]'
    );

    await page.waitForSelector('input[name="country"]');
    const country = await page.evaluate(
      (field) => document.querySelector(field).value = "Sweden",
      'input[name="country"]'
    );

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-confirm-edit");
    console.log("clicked confirm edit button")

    await page.waitForSelector('input[name="username"]');
    const username = await page.evaluate(
      (field) => document.querySelector(field).value,
      "#inputUsername"
    );
    expect(username).toEqual("Anita");


  })


  // cancel delete profile
  test("cancel delete profile", async () => {

    await page.waitForSelector("#btn-edit-profile");

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-edit-profile");
    console.log("clicked edit profile button")

    await page.waitForSelector("#btn-initiate-delete");
    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-initiate-delete");
    console.log("clicked delete profile button")

    await page.waitForSelector("#btn-cancel-delete");
    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-cancel-delete");
    console.log("clicked cancel delete profile button")

    await page.waitForSelector('input[name="username"]');

  })

  //delete profile
  test("delete profile", async () => {

    await page.waitForSelector("#btn-edit-profile");

    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-edit-profile");
    console.log("clicked edit profile button")

    await page.waitForSelector("#btn-initiate-delete");
    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-initiate-delete");

    console.log("clicked delete profile button")

    await page.waitForSelector("#btn-delete-user");
    await page.evaluate((selector) => {
      document.querySelector(selector).click();
    }, "#btn-delete-user");

    console.log("clicked confirm delete profile button")

    await page.waitForNavigation();

    await page.waitForSelector("#btn-login-nav");
    console.log("user deleted")

  })

});