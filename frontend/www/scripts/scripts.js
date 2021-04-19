function makeNavLinkActive(id) {
  const link = document.getElementById(id);
  link.classList.add("active");
  link.setAttribute("aria-current", "page");
}

function isUserAuthenticated() {
  return getCookieValue("access") != null || getCookieValue("refresh") != null;
}

function updateNavBar() {
  // Emphasize link to current page
  if (
    window.location.pathname === "/" ||
    window.location.pathname === "/index.html"
  ) {
    makeNavLinkActive("nav-index");
  } else if (window.location.pathname === "/workouts.html") {
    makeNavLinkActive("nav-workouts");
  } else if (window.location.pathname === "/exercises.html") {
    makeNavLinkActive("nav-exercises");
  } else if (window.location.pathname === "/mycoach.html") {
    makeNavLinkActive("nav-mycoach");
  } else if (window.location.pathname === "/myathletes.html") {
    makeNavLinkActive("nav-myathletes");
  }

  if (isUserAuthenticated()) {
    document.getElementById("btn-logout").classList.remove("hide");

    document.querySelector('a[href="logout.html"').classList.remove("hide");
    document.querySelector('a[href="workouts.html"').classList.remove("hide");
    document.querySelector('a[href="mycoach.html"').classList.remove("hide");
    document.querySelector('a[href="exercises.html"').classList.remove("hide");
    document.querySelector('a[href="myathletes.html"').classList.remove("hide");
    document.querySelector('a[href="profile.html"').classList.remove("hide");
  } else {
    document.getElementById("btn-login-nav").classList.remove("hide");
    document.getElementById("btn-register").classList.remove("hide");
  }
}

function setCookie(name, value, maxage, path = "") {
  document.cookie = `${name}=${value}; max-age=${maxage}; path=${path}`;
}

// eslint-disable-next-line no-unused-vars
function deleteCookie(name) {
  setCookie(name, "", 0, "/");
}

function getCookieValue(name) {
  let cookieValue = null;
  const cookieByName = document.cookie
    .split("; ")
    .find((row) => row.startsWith(name));

  if (cookieByName) {
    // eslint-disable-next-line
    cookieValue = cookieByName.split("=")[1];
  }

  return cookieValue;
}

/* eslint-disable */
async function sendRequest(
  method,
  url,
  body,
  contentType = "application/json; charset=UTF-8"
) {
  if (url.includes("secfit.vassbo.as")) {
    url = url.replace("http://", "https://");
  }
  if (body && contentType.includes("json")) {
    body = JSON.stringify(body);
  }

  let myHeaders = new Headers();

  if (contentType) myHeaders.set("Content-Type", contentType);
  if (getCookieValue("access"))
    myHeaders.set("Authorization", `Bearer ${getCookieValue("access")}`);
  let myInit = { headers: myHeaders, method, body };
  let myRequest = new Request(url, myInit);

  let response = await fetch(myRequest);
  if (response.status == 401 && getCookieValue("refresh")) {
    // access token not accepted. getting refresh token
    myHeaders = new Headers({
      "Content-Type": "application/json; charset=UTF-8",
    });
    const tokenBody = JSON.stringify({ refresh: getCookieValue("refresh") });
    myInit = { headers: myHeaders, method: "POST", body: tokenBody };
    myRequest = new Request(`${HOST}/api/token/refresh/`, myInit);
    response = await fetch(myRequest);

    if (response.ok) {
      // refresh successful, received new access token
      const data = await response.json();
      setCookie("access", data.access, 86400, "/");

      const myHeaders = new Headers({
        Authorization: `Bearer ${getCookieValue("access")}`,
        "Content-Type": contentType,
      });
      const myInit = { headers: myHeaders, method, body };
      const myRequest = new Request(url, myInit);
      response = await fetch(myRequest);

      if (!response.ok) window.location.replace("logout.html");
    }
  }

  return response;
}

// eslint-disable-next-line no-unused-vars
function setReadOnly(readOnly, selector) {
  const form = document.querySelector(selector);
  const formData = new FormData(form);

  for (const key of formData.keys()) {
    let selector = `input[name="${key}"], textarea[name="${key}"]`;
    for (const input of form.querySelectorAll(selector)) {
      if (!readOnly && input.hasAttribute("readonly")) {
        input.readOnly = false;
      } else if (readOnly && !input.hasAttribute("readonly")) {
        input.readOnly = true;
      }
    }

    selector = `input[type="file"], select[name="${key}`;
    for (const input of form.querySelectorAll(selector)) {
      if (!readOnly && input.hasAttribute("disabled")) {
        input.disabled = false;
      } else if (readOnly && !input.hasAttribute("disabled")) {
        input.disabled = true;
      }
    }
  }

  for (const input of document.querySelectorAll(
    "input:disabled, select:disabled"
  )) {
    if (
      (!readOnly && input.hasAttribute("disabled")) ||
      (readOnly && !input.hasAttribute("disabled"))
    ) {
      input.disabled = !input.disabled;
    }
  }
}
/* eslint-enable  */

// eslint-disable-next-line no-unused-vars
async function getCurrentUser() {
  let user = null;
  const response = await sendRequest("GET", `${HOST}/api/users/?user=current`);
  if (!response.ok) {
    console.log("COULD NOT RETRIEVE CURRENTLY LOGGED IN USER");
  } else {
    const data = await response.json();
    user = data.results[0];
  }

  return user;
}

// eslint-disable-next-line no-unused-vars
function createAlert(header, data, msg) {
  const alertDiv = document.createElement("div");
  alertDiv.className = "alert alert-warning alert-dismissible fade show";
  alertDiv.setAttribute("role", "alert");

  const strong = document.createElement("strong");
  strong.innerText = header;
  alertDiv.appendChild(strong);

  const button = document.createElement("button");
  button.type = "button";
  button.className = "btn-close";
  button.setAttribute("data-bs-dismiss", "alert");
  button.setAttribute("aria-label", "Close");
  alertDiv.appendChild(button);

  const ul = document.createElement("ul");
  if ("detail" in data) {
    const li = document.createElement("li");
    li.innerText = data.detail;
    ul.appendChild(li);
  } else {
    for (const key in data) {
      const li = document.createElement("li");
      li.innerText = key;

      const innerUl = document.createElement("ul");
      for (const message of data[key]) {
        const innerLi = document.createElement("li");
        innerLi.innerText = message;
        innerUl.appendChild(innerLi);
      }
      li.appendChild(innerUl);
      ul.appendChild(li);

      if (msg) {
        const li = document.createElement("li");
        const text = document.createTextNode(msg);
        li.appendChild(text), ul.appendChild(li);
      }
    }
  }
  alertDiv.appendChild(ul);

  return alertDiv;
}

window.addEventListener("DOMContentLoaded", updateNavBar);
