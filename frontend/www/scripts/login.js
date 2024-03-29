async function login() {
  const form = document.querySelector("#form-login");
  const formData = new FormData(form);
  const body = {
    username: formData.get("username"),
    password: formData.get("password"),
  };

  const response = await sendRequest("POST", `${HOST}/api/token/`, body);
  if (response.ok) {
    const data = await response.json();
    // access and refresh cookies each have a max age of 24 hours
    setCookie("access", data.access, 86400, "/");
    setCookie("refresh", data.refresh, 86400, "/");
    sessionStorage.setItem("username", formData.get("username"));

    window.location.replace("workouts.html");
  } else {
    const data = await response.json();
    const alert = createAlert("Login failed!", data);
    document.body.prepend(alert);
  }

  /* eslint-disable no-shadow */
  // Sets cookie if remember me checked
  const rememberMe = document.getElementById("rememberMe").checked;
  if (rememberMe) {
    const response = await sendRequest("GET", `${HOST}/api/remember_me/`);
    if (response.ok) {
      const data = await response.json();
      setCookie("remember_me", data.remember_me, 3000000000, "/");
    }
  }
  /* eslint-enable */
}

// Used for login if remember me cookie exists
async function rememberMe() {
  const response = await sendRequest("POST", `${HOST}/api/remember_me/`);
  if (response.ok) {
    const data = await response.json();
    // access and refresh cookies each have a max age of 24 hours
    setCookie("access", data.access, 86400, "/");
    setCookie("refresh", data.refresh, 86400, "/");

    window.location.replace("workouts.html");
  } else {
    const data = await response.json();
    const alert = createAlert("Login failed!", data);
    document.body.prepend(alert);
  }
}

/* eslint-disable func-names */
window.onload = function () {
  if (getCookieValue("remember_me")) {
    rememberMe();
  }
};
/* eslint-enable */

document.querySelector("#btn-login").addEventListener("click", async () => {
  await login();
});
