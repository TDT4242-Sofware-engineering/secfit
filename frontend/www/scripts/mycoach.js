/* eslint-disable no-await-in-loop, no-shadow, no-param-reassign */

async function displayCurrentCoach() {
  const user = await getCurrentUser();

  if (user.coach) {
    const response = await sendRequest("GET", user.coach);
    if (!response.ok) {
      const data = await response.json();
      const alert = createAlert("Could not retrieve coach!", data);
      document.body.prepend(alert);
    }
    const coach = await response.json();
    const input = document.querySelector("#input-coach");

    input.value = coach.username;
  } else {
    console.log("NO USER.COACH"); // eslint-disable-line
  }
}

async function displayOffers() {
  const templateOffer = document.querySelector("#template-offer");
  const listOffers = document.querySelector("#list-offers");

  const status = "p"; // pending
  const category = "received";
  const response = await sendRequest(
    "GET",
    `${HOST}/api/offers/?status=${status}&category=${category}`
  );
  if (!response.ok) {
    const data = await response.json();
    const alert = createAlert("Could not retrieve offers!", data);
    document.body.prepend(alert);
  } else {
    const offers = await response.json();
    for (const offer of offers.results) {
      const cloneOffer = templateOffer.content.cloneNode(true);
      const li = cloneOffer.querySelector("li");
      const span = li.querySelector("span");
      span.textContent = `${offer.owner} wants to be your coach`;

      const buttons = li.querySelectorAll("button");
      const acceptButton = buttons[0];
      const declineButton = buttons[1];

      acceptButton.addEventListener("click", async () => {
        await acceptOffer(offer.url, offer.owner);
      });

      declineButton.addEventListener("click", async () => {
        await declineOffer(offer.url);
      });

      listOffers.appendChild(li);
    }
    if (offers.results.length === 0) {
      const offersDiv = document.querySelector("#offers-div");
      const p = document.createElement("p");
      p.innerText = "You currently have no offers.";
      offersDiv.append(p);
    }
  }
}

async function acceptOffer(offerUrl, ownerUsername) {
  const body = { status: "d" };

  const response = await sendRequest("PATCH", offerUrl, body);
  if (!response.ok) {
    const data = await response.json();
    const alert = createAlert("Could not accept offer!", data);
    document.body.prepend(alert);
  } else {
    let response = await sendRequest(
      "GET",
      `${HOST}/api/users/${ownerUsername}/`
    );
    const owner = await response.json();
    const user = await getCurrentUser();

    const body = { coach: owner.url };
    response = await sendRequest("PATCH", user.url, body);

    if (!response.ok) {
      const data = await response.json();
      const alert = createAlert("Could not update coach!", data);
      document.body.prepend(alert);
    } else {
      location.reload();
      return false;
    }
  }
}

async function declineOffer(offerUrl) {
  const body = { status: "d" };

  const response = await sendRequest("PATCH", offerUrl, body);
  if (!response.ok) {
    const data = await response.json();
    const alert = createAlert("Could not decline offer!", data);
    document.body.prepend(alert);
  } else {
    location.reload();
    return false;
  }
}

async function displayFiles() {
  const user = await getCurrentUser();

  const templateOwner = document.querySelector("#template-owner-tab");
  const templateFiles = document.querySelector("#template-files");
  const templateFile = document.querySelector("#template-file");
  const listTab = document.querySelector("#list-tab");
  const navTabContent = document.querySelector("#nav-tabContent");

  for (const fileUrl of user.coach_files) {
    const response = await sendRequest("GET", fileUrl);
    const file = await response.json();
    let divFiles = null;

    if (!document.querySelector(`#list-${file.owner}-list`)) {
      const cloneOwner = templateOwner.content.cloneNode(true);
      const a = cloneOwner.querySelector("a");
      a.id = `list-${file.owner}-list`;
      a.href = `#list-${file.owner}`;
      a.text = file.owner;
      listTab.appendChild(a);

      const cloneFiles = templateFiles.content.cloneNode(true);
      divFiles = cloneFiles.querySelector("div");
      divFiles.id = `list-${file.owner}`;
      navTabContent.appendChild(divFiles);
    } else {
      divFiles = document.querySelector(`#list-${file.owner}`);
    }

    const cloneFile = templateFile.content.cloneNode(true);
    const aFile = cloneFile.querySelector("a");
    aFile.href = file.file;
    const pathArray = file.file.split("/");
    aFile.text = pathArray[pathArray.length - 1];

    divFiles.appendChild(aFile);
  }

  if (listTab.childElementCount > 0) {
    listTab.firstElementChild.click();
  }

  if (user.coach_files.length === 0) {
    const p = document.createElement("p");
    p.innerText = "There are currently no files uploaded for this user.";
    document.querySelector("#list-files-div").append(p);
  }
}

function editCoach(event) {
  const buttonEditCoach = event.currentTarget;
  const buttonSetCoach = document.querySelector("#button-set-coach");
  const buttonCancelCoach = document.querySelector("#button-cancel-coach");

  setReadOnly(false, "#form-coach");

  buttonEditCoach.className += " hide";
  buttonSetCoach.className = buttonSetCoach.className.replace(" hide", "");
  buttonCancelCoach.className = buttonCancelCoach.className.replace(
    " hide",
    ""
  );
}

function cancelCoach() {
  location.reload();
  return false;
}

async function setCoach() {
  // get current user
  const user = await getCurrentUser();
  const newCoach = document.querySelector("#input-coach").value;
  const body = {};
  if (!newCoach) {
    body.coach = null;
  } else {
    const response = await sendRequest("GET", `${HOST}/api/users/${newCoach}/`);
    if (!response.ok) {
      const data = await response.json();
      const alert = createAlert(`Could not retrieve user ${newCoach}`, data);
      document.body.prepend(alert);
    }
    const newCoachObject = await response.json();
    body.coach = newCoachObject.url;
  }

  if ("coach" in body) {
    const response = await sendRequest("PATCH", user.url, body);
    if (!response.ok) {
      const data = await response.json();
      const alert = createAlert("Could not update coach!", data);
      document.body.prepend(alert);
    } else {
      location.reload();
      return false;
    }
  }
}

window.addEventListener("DOMContentLoaded", async () => {
  await displayCurrentCoach();
  await displayOffers();
  await displayFiles();

  const buttonSetCoach = document.querySelector("#button-set-coach");
  const buttonEditCoach = document.querySelector("#button-edit-coach");
  const buttonCancelCoach = document.querySelector("#button-cancel-coach");

  buttonSetCoach.addEventListener(
    "click",
    async (event) => await setCoach(event)
  );
  buttonEditCoach.addEventListener("click", editCoach);
  buttonCancelCoach.addEventListener("click", cancelCoach);
});
