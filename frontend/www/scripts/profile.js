let deleteProfileButton;
let initiateDeleteButton;
let cancelDeleteButton;
let editProfileButton;
let confirmButton;
let cancelEditButton;

async function getCurrentUser() {
    let user = null;
    let response = await sendRequest("GET", `${HOST}/api/users/?user=current`)
    if (!response.ok) {
        console.log("COULD NOT RETRIEVE CURRENTLY LOGGED IN USER");
    } else {
        let data = await response.json();
        user = data.results[0];
    }
    return user;
}

async function retrieveProfile() {
    let user = null;
    let response = await sendRequest("GET", `${HOST}/api/users/?user=current`);
    if (!response.ok) {
        let alert = createAlert("Could not retrieve profile data!");
        document.body.prepend(alert);
    } else {
        let data = await response.json();
        user = data.results[0];
        let form = document.querySelector("#form-profile");
        let formData = new FormData(form);

        for (let key of formData.keys()) {
            let selector = `input[name="${key}"], textarea[name="${key}"]`;
            let input = form.querySelector(selector);
            let newVal = user[key];
            input.value = newVal;
        }
    }
    return user;
}

function handleEditProfile() {
    confirmButton = document.querySelector("#btn-confirm-edit");
    cancelEditButton = document.querySelector("#btn-cancel-edit");
    
    setReadOnly(false, "#form-profile");

    editProfileButton.classList.add("hide");
    confirmButton.classList.remove("hide");
    cancelEditButton.classList.remove("hide");
    initiateDeleteButton.classList.remove("hide");

    cancelEditButton.addEventListener("click", handleCancel);
}

async function updateProfile(user) {
    let submitForm = generateProfileForm();

    let response = await sendRequest("PATCH", `${HOST}/api/users/${user.id}/`, submitForm, "");
    if (!response.ok) {
        let alert = createAlert("Could not update profile!");
        document.body.prepend(alert);
    } else {
        location.reload();
    }
}

function handleCancel() {
    location.reload();
}

function generateProfileForm() {
    let form = document.querySelector("#form-profile");

    let formData = new FormData(form);
    let submitForm = new FormData();

    submitForm.append("username", formData.get('username'));
    submitForm.append("email", formData.get('email'));
    submitForm.append("phone_number", formData.get('phone_number'));
    submitForm.append("street_address", formData.get('street_address'));
    submitForm.append("city", formData.get('city'));
    submitForm.append("country", formData.get('country'));

    return submitForm;
}


async function deleteProfile(user) {
    let response = await sendRequest("DELETE", `${HOST}/api/users/${user.id}/`);
    if (!response.ok) {
        let data = await response.json();
        let alert = createAlert(`Could not delete profile ${id}!`, data);
        document.body.prepend(alert);
    } else {
        window.location.replace("logout.html");
    }
}


window.addEventListener("DOMContentLoaded", async () => {
    let user = await retrieveProfile();
    deleteProfileButton = document.querySelector("#btn-delete-user");
    cancelDeleteButton = document.querySelector("#btn-cancel-delete");
    initiateDeleteButton = document.querySelector("#btn-initiate-delete");
    editProfileButton = document.querySelector("#btn-edit-profile");
    confirmButton = document.querySelector("#btn-confirm-edit");


    let modal = document.querySelector("#delete-modal");

    confirmButton.addEventListener("click", (() => updateProfile(user)))
    editProfileButton.addEventListener("click", (() => handleEditProfile()));
    deleteProfileButton.addEventListener("click", (async () => deleteProfile(user)));
    cancelDeleteButton.addEventListener("click", (() => handleCancel()));
    initiateDeleteButton.addEventListener("click", (() => {
        initiateDeleteButton.classList.add("hide");
        modal.classList.remove("hide");
    }))
});