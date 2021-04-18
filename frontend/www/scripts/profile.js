async function getCurrentUser() {
  let user = null;
  const response = await sendRequest("GET", `${HOST}/api/users/?user=current`);
  if (!response.ok) {
    const alert = createAlert("Could not retrieve profile data!");
    document.body.prepend(alert);
  } else {
    const data = await response.json();
    user = data.results[0];
  }
  return user;
}

async function retrieveProfile() {
  let user = null;
  const response = await sendRequest("GET", `${HOST}/api/users/?user=current`);
  if (!response.ok) {
    const alert = createAlert("Could not retrieve profile data!");
    document.body.prepend(alert);
  } else {
    const data = await response.json();
    user = data.results[0];
    const form = document.querySelector("#form-profile");
    const formData = new FormData(form);

    for (const key of formData.keys()) {
      const selector = `input[name="${key}"], textarea[name="${key}"]`;
      const input = form.querySelector(selector);
      const newVal = user[key];
      input.value = newVal;
    }
  }
  return user;
}

function handleEditProfile(
  confirmButton,
  cancelEditButton,
  editProfileButton,
  initiateDeleteButton,
  cancelEditButton
) {
  confirmButton = document.querySelector("#btn-confirm-edit");
  cancelEditButton = document.querySelector("#btn-cancel-edit");

  setReadOnly(false, "#form-profile");

  setReadOnly(false, "#form-profile");

  editProfileButton.classList.add("hide");
  confirmButton.classList.remove("hide");
  cancelEditButton.classList.remove("hide");
  initiateDeleteButton.classList.remove("hide");

  cancelEditButton.addEventListener("click", handleCancel);
}

async function updateProfile(user) {
  const submitForm = generateProfileForm();

  const response = await sendRequest(
    "PATCH",
    `${HOST}/api/users/${user.id}/`,
    submitForm,
    ""
  );
  if (!response.ok) {
    const alert = createAlert("Could not update profile!");
    document.body.prepend(alert);
  } else {
    location.reload();
  }
}

function handleCancel() {
  location.reload();
}

function generateProfileForm() {
  const form = document.querySelector("#form-profile");

  const formData = new FormData(form);
  const submitForm = new FormData();

  submitForm.append("username", formData.get("username"));
  submitForm.append("email", formData.get("email"));
  submitForm.append("phone_number", formData.get("phone_number"));
  submitForm.append("street_address", formData.get("street_address"));
  submitForm.append("city", formData.get("city"));
  submitForm.append("country", formData.get("country"));

  return submitForm;
}

async function deleteProfile(user) {
  const response = await sendRequest("DELETE", `${HOST}/api/users/${user.id}/`);
  if (!response.ok) {
    const data = await response.json();
    const alert = createAlert(`Could not delete profile ${id}!`, data);
    document.body.prepend(alert);
  } else {
    window.location.replace("logout.html");
  }
}

window.addEventListener("DOMContentLoaded", async () => {
  const user = await retrieveProfile();
  const deleteProfileButton = document.querySelector("#btn-delete-user");
  const cancelDeleteButton = document.querySelector("#btn-cancel-delete");
  const initiateDeleteButton = document.querySelector("#btn-initiate-delete");
  const editProfileButton = document.querySelector("#btn-edit-profile");
  const confirmButton = document.querySelector("#btn-confirm-edit");
  const cancelEditButton = document.querySelector("#btn-cancel-edit");

  const modal = document.querySelector("#delete-modal");

  confirmButton.addEventListener("click", () => updateProfile(user));
  editProfileButton.addEventListener("click", () =>
    handleEditProfile(
      confirmButton,
      cancelEditButton,
      editProfileButton,
      initiateDeleteButton,
      cancelEditButton
    )
  );
  deleteProfileButton.addEventListener("click", async () =>
    deleteProfile(user)
  );
  cancelDeleteButton.addEventListener("click", () => handleCancel());
  initiateDeleteButton.addEventListener("click", () => {
    initiateDeleteButton.classList.add("hide");
    modal.classList.remove("hide");
  });
});
