async function createNewUser() {
  const form = document.querySelector("#form-register-user");
  const formData = new FormData(form);

  let response = await sendRequest("POST", `${HOST}/api/users/`, formData, "");

  if (!response.ok) {
    const data = await response.json();
    const alert = createAlert("Registration failed!", data);
    document.body.prepend(alert);
  } else {
    const body = {
      username: formData.get("username"),
      password: formData.get("password"),
      phone_number: formData.get("phone_number"),
      country: formData.get("country"),
      city: formData.get("city"),
      street_address: formData.get("street_address"),
    };
    response = await sendRequest("POST", `${HOST}/api/token/`, body);
    if (response.ok) {
      const data = await response.json();
      setCookie("access", data.access, 86400, "/");
      setCookie("refresh", data.refresh, 86400, "/");
      sessionStorage.setItem("username", formData.get("username"));
    } else {
      const data = await response.json();
      const alert = createAlert(
        "Registration could not complete. Try again!",
        data
      );
      document.body.prepend(alert);
    }
    form.reset();
    window.location.replace("workouts.html");
  }
}

document
  .querySelector("#btn-create-account")
  .addEventListener("click", async (event) => {
    await createNewUser(event);
  });
