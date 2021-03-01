let deleteProfileButton;
let initiateDeleteButton;
let cancelDeleteButton;

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
        let data = await response.json();
        let alert = createAlert("Could not retrieve profile data!", data);
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

function handleCancelDelete() {
    location.reload();
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

    let modal = document.querySelector("#delete-modal");

    deleteProfileButton.addEventListener("click", (async () => await deleteProfile(user)));
    cancelDeleteButton.addEventListener("click", (() => handleCancelDelete()));
    initiateDeleteButton.addEventListener("click", (() => {
        initiateDeleteButton.classList.add("hide");
        modal.classList.remove("hide");
    }))
});