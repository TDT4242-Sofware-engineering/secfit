/* eslint-disable no-await-in-loop, no-shadow, no-param-reassign, no-plusplus */

let cancelWorkoutButton;
let okWorkoutButton;
let deleteWorkoutButton;
let editWorkoutButton;
let participants = [];
let currentUser;

async function retrieveWorkout(id) {
  let workoutData = null;
  const response = await sendRequest("GET", `${HOST}/api/workouts/${id}/`);
  if (!response.ok) {
    const data = await response.json();
    const alert = createAlert("Could not retrieve workout data!", data);
    document.body.prepend(alert);
  } else {
    workoutData = await response.json();
    const form = document.querySelector("#form-workout");
    const formData = new FormData(form);

    fillWorkoutForm(formData, form);

    const input = form.querySelector("select:disabled");
    input.value = workoutData.visibility;
    // files
    mapWorkoutFilesToHrefObjects();

    // create exercises

    // fetch exercise types
    const exerciseTypeResponse = await sendRequest(
      "GET",
      `${HOST}/api/exercises/`
    );
    const exerciseTypes = await exerciseTypeResponse.json();

    // handleRetrievedExercises(workoutData, exerciseTypes);
    //TODO: This should be in its own method.
    handleRetrievedExercises(exerciseTypes);
  }
  return workoutData;

  function handleRetrievedExercises(exerciseTypes) {
    for (let i = 0; i < workoutData.exercise_instances.length; i++) {
      const templateExercise = document.querySelector("#template-exercise");
      const divExerciseContainer = templateExercise.content.firstElementChild.cloneNode(
        true
      );

      const exerciseTypeLabel = divExerciseContainer.querySelector(
        ".exercise-type"
      );
      exerciseTypeLabel.for = `inputExerciseType${i}`;

      const exerciseTypeSelect = divExerciseContainer.querySelector("select");
      exerciseTypeSelect.id = `inputExerciseType${i}`;
      exerciseTypeSelect.disabled = true;

      const splitUrl = workoutData.exercise_instances[i].exercise.split("/");
      const currentExerciseTypeId = splitUrl[splitUrl.length - 2];
      let currentExerciseType = "";

      for (let j = 0; j < exerciseTypes.count; j++) {
        const option = document.createElement("option");
        option.value = exerciseTypes.results[j].id;
        if (currentExerciseTypeId == exerciseTypes.results[j].id) {
          currentExerciseType = exerciseTypes.results[j];
        }
        option.innerText = exerciseTypes.results[j].name;
        exerciseTypeSelect.append(option);
      }

      exerciseTypeSelect.value = currentExerciseType.id;

      const exerciseSetLabel = divExerciseContainer.querySelector(
        ".exercise-sets"
      );
      exerciseSetLabel.for = `inputSets${i}`;

      const exerciseSetInput = divExerciseContainer.querySelector(
        "input[name='sets']"
      );
      exerciseSetInput.id = `inputSets${i}`;
      exerciseSetInput.value = workoutData.exercise_instances[i].sets;
      exerciseSetInput.readOnly = true;

      const exerciseNumberLabel = divExerciseContainer.querySelector(
        ".exercise-number"
      );
      (exerciseNumberLabel.for = "for"), `inputNumber${i}`;
      exerciseNumberLabel.innerText = currentExerciseType.unit;

      const exerciseNumberInput = divExerciseContainer.querySelector(
        "input[name='number']"
      );
      exerciseNumberInput.id = `inputNumber${i}`;
      exerciseNumberInput.value = workoutData.exercise_instances[i].number;
      exerciseNumberInput.readOnly = true;

      const exercisesDiv = document.querySelector("#div-exercises");
      exercisesDiv.appendChild(divExerciseContainer);
    }
  }

  function mapWorkoutFilesToHrefObjects() {
    const filesDiv = document.querySelector("#uploaded-files");
    for (const file of workoutData.files) {
      const a = document.createElement("a");
      a.href = file.file;
      const pathArray = file.file.split("/");
      a.text = pathArray[pathArray.length - 1];
      a.className = "me-2";
      filesDiv.appendChild(a);
    }
  }

  function fillWorkoutForm(formData, form) {
    for (const key of formData.keys()) {
      const selector = `input[name="${key}"], textarea[name="${key}"]`;
      const inputFromForm = form.querySelector(selector);
      let newVal = workoutData[key];
      if (key === "date") {
        // Creating a valid datetime-local string with the correct local time
        let date = new Date(newVal);
        date = new Date(
          date.getTime() - date.getTimezoneOffset() * 60 * 1000
        ).toISOString(); // get ISO format for local time
        newVal = date.substring(0, newVal.length - 1); // remove Z (since this is a local time, not UTC)
      }
      if (key !== "files") {
        inputFromForm.value = newVal;
      }
    }
  }
}

function handleCancelDuringWorkoutEdit() {
  window.location.reload();
}

function handleEditWorkoutButtonClick() {
  const addExerciseButton = document.querySelector("#btn-add-exercise");
  const removeExerciseButton = document.querySelector("#btn-remove-exercise");

  setReadOnly(false, "#form-workout");
  document.querySelector("#inputOwner").readOnly = true; // owner field should still be readonly

  editWorkoutButton.className += " hide";
  okWorkoutButton.className = okWorkoutButton.className.replace(" hide", "");
  cancelWorkoutButton.className = cancelWorkoutButton.className.replace(
    " hide",
    ""
  );
  deleteWorkoutButton.className = deleteWorkoutButton.className.replace(
    " hide",
    ""
  );
  addExerciseButton.className = addExerciseButton.className.replace(
    " hide",
    ""
  );
  removeExerciseButton.className = removeExerciseButton.className.replace(
    " hide",
    ""
  );

  cancelWorkoutButton.addEventListener("click", handleCancelDuringWorkoutEdit);
}

async function deleteWorkout(id) {
  const response = await sendRequest("DELETE", `${HOST}/api/workouts/${id}/`);
  if (!response.ok) {
    const data = await response.json();
    const alert = createAlert(`Could not delete workout ${id}!`, data);
    document.body.prepend(alert);
  } else {
    window.location.replace("workouts.html");
  }
}

async function updateWorkout(id) {
  const submitForm = generateWorkoutForm();

  const response = await sendRequest(
    "PUT",
    `${HOST}/api/workouts/${id}/`,
    submitForm,
    ""
  );
  if (!response.ok) {
    const data = await response.json();
    const alert = createAlert("Could not update workout!", data);
    document.body.prepend(alert);
  } else {
    window.location.reload();
  }
}

function generateWorkoutForm() {
  const form = document.querySelector("#form-workout");

  const formData = new FormData(form);
  const submitForm = new FormData();

  submitForm.append("name", formData.get("name"));
  const date = new Date(formData.get("date")).toISOString();
  submitForm.append("date", date);
  submitForm.append("notes", formData.get("notes"));
  submitForm.append("visibility", formData.get("visibility"));
  submitForm.append("participants", JSON.stringify([]));

  // adding exercise instances
  const exerciseInstances = [];
  const exerciseInstancesTypes = formData.getAll("type");
  const exerciseInstancesSets = formData.getAll("sets");
  const exerciseInstancesNumbers = formData.getAll("number");
  for (let i = 0; i < exerciseInstancesTypes.length; i++) {
    exerciseInstances.push({
      exercise: `${HOST}/api/exercises/${exerciseInstancesTypes[i]}/`,
      number: exerciseInstancesNumbers[i],
      sets: exerciseInstancesSets[i],
    });
  }

  submitForm.append("exercise_instances", JSON.stringify(exerciseInstances));
  // adding files
  addWorkoutFiles();

  return submitForm;

  function addWorkoutFiles() {
    for (const file of formData.getAll("files")) {
      submitForm.append("files", file);
    }
  }
}

async function createWorkout() {
  const submitForm = generateWorkoutForm();

  const response = await sendRequest(
    "POST",
    `${HOST}/api/workouts/`,
    submitForm,
    ""
  );

  if (response.ok) {
    const data = await response.json();
    sendWorkoutInvitations(data);

    participants = [];
    window.location.replace("workouts.html");
  } else {
    const data = await response.json();
    const alert = createAlert("Could not create new workout!", data);
    document.body.prepend(alert);
  }

  function sendWorkoutInvitations(data) {
    participants.forEach(async (participant) => {
      const invitation = {
        owner: currentUser.username,
        participant,
        workout: data.url,
      };
      const invResponse = await sendRequest(
        "POST",
        `${HOST}/api/workouts/invitations`,
        invitation
      );
      console.log(invResponse);
    });
  }
}

function handleCancelDuringWorkoutCreate() {
  window.location.replace("workouts.html");
}

async function createBlankExercise() {
  const exerciseTypeResponse = await sendRequest(
    "GET",
    `${HOST}/api/exercises/`
  );
  const exerciseTypes = await exerciseTypeResponse.json();

  const exerciseTemplate = document.querySelector("#template-exercise");
  const divExerciseContainer = exerciseTemplate.content.firstElementChild.cloneNode(
    true
  );
  const exerciseTypeSelect = divExerciseContainer.querySelector("select");

  for (let i = 0; i < exerciseTypes.count; i++) {
    const option = document.createElement("option");
    option.value = exerciseTypes.results[i].id;
    option.innerText = exerciseTypes.results[i].name;
    exerciseTypeSelect.append(option);
  }

  const currentExerciseType = exerciseTypes.results[0];
  exerciseTypeSelect.value = currentExerciseType.name;

  const divExercises = document.querySelector("#div-exercises");
  divExercises.appendChild(divExerciseContainer);
}

function removeExercise() {
  const divExerciseContainers = document.querySelectorAll(
    ".div-exercise-container"
  );
  if (divExerciseContainers && divExerciseContainers.length > 0) {
    divExerciseContainers[divExerciseContainers.length - 1].remove();
  }
}

function addComment(author, text, date, append) {
  /* Taken from https://www.bootdey.com/snippets/view/Simple-Comment-panel#css */
  const commentList = document.querySelector("#comment-list");
  const listElement = document.createElement("li");
  listElement.className = "media";
  const commentBody = document.createElement("div");
  commentBody.className = "media-body";
  const dateSpan = document.createElement("span");
  dateSpan.className = "text-muted pull-right me-1";
  const smallText = document.createElement("small");
  smallText.className = "text-muted";

  if (date !== "Now") {
    const localDate = new Date(date);
    smallText.innerText = localDate.toLocaleString();
  } else {
    smallText.innerText = date;
  }

  dateSpan.appendChild(smallText);
  commentBody.appendChild(dateSpan);

  const strong = document.createElement("strong");
  strong.className = "text-success";
  strong.innerText = author;
  commentBody.appendChild(strong);
  const p = document.createElement("p");
  p.innerHTML = text;

  commentBody.appendChild(strong);
  commentBody.appendChild(p);
  listElement.appendChild(commentBody);

  if (append) {
    commentList.append(listElement);
  } else {
    commentList.prepend(listElement);
  }
}

async function createComment(workoutid) {
  const commentArea = document.querySelector("#comment-area");
  const content = commentArea.value;
  const body = {
    workout: `${HOST}/api/workouts/${workoutid}/`,
    content,
  };

  const response = await sendRequest("POST", `${HOST}/api/comments/`, body);
  if (response.ok) {
    addComment(sessionStorage.getItem("username"), content, "Now", false);
  } else {
    const data = await response.json();
    const alert = createAlert("Failed to create comment!", data);
    document.body.prepend(alert);
  }
}

async function retrieveComments(workoutid) {
  const response = await sendRequest("GET", `${HOST}/api/comments/`);
  if (!response.ok) {
    const data = await response.json();
    const alert = createAlert("Could not retrieve comments!", data);
    document.body.prepend(alert);
  } else {
    const data = await response.json();
    const comments = data.results;
    for (const comment of comments) {
      const splitArray = comment.workout.split("/");
      if (splitArray[splitArray.length - 2] === workoutid) {
        addComment(comment.owner, comment.content, comment.timestamp, true);
      }
    }
  }
}

window.addEventListener("DOMContentLoaded", async () => {
  cancelWorkoutButton = document.querySelector("#btn-cancel-workout");
  okWorkoutButton = document.querySelector("#btn-ok-workout");
  deleteWorkoutButton = document.querySelector("#btn-delete-workout");
  editWorkoutButton = document.querySelector("#btn-edit-workout");
  const postCommentButton = document.querySelector("#post-comment");
  const divCommentRow = document.querySelector("#div-comment-row");
  const buttonAddExercise = document.querySelector("#btn-add-exercise");
  const buttonRemoveExercise = document.querySelector("#btn-remove-exercise");

  buttonAddExercise.addEventListener("click", createBlankExercise);
  buttonRemoveExercise.addEventListener("click", removeExercise);

  const urlParams = new URLSearchParams(window.location.search);
  currentUser = await getCurrentUser();

  if (urlParams.has("id")) {
    const id = urlParams.get("id");
    const workoutData = await retrieveWorkout(id);
    await retrieveComments(id);

    if (workoutData.owner === currentUser.url) {
      editWorkoutButton.classList.remove("hide");
      editWorkoutButton.addEventListener("click", handleEditWorkoutButtonClick);
      deleteWorkoutButton.addEventListener(
        "click",
        (async (id) => deleteWorkout(id)).bind(undefined, id)
      );
      okWorkoutButton.addEventListener(
        "click",
        (async (id) => updateWorkout(id)).bind(undefined, id)
      );
      postCommentButton.addEventListener(
        "click",
        (async (id) => createComment(id)).bind(undefined, id)
      );
      divCommentRow.className = divCommentRow.className.replace(" hide", "");
    }
  } else {
    await createBlankExercise();
    const ownerInput = document.querySelector("#inputOwner");
    const usersContainer = document.getElementById(
      "users-search-result-container"
    );

    const inputSearchForUser = document.querySelector("#inputSearchForUser");
    inputSearchForUser.style.display = "none";
    inputSearchForUser.addEventListener("input", async (e) =>
      onSearchForInputChange(e, usersContainer, currentUser.username)
    );
    const addAthelteButton = document.querySelector("#btn-add-athelte");
    addAthelteButton.addEventListener("click", () =>
      toggleHideById("#inputSearchForUser")
    );

    ownerInput.value = currentUser.username;
    setReadOnly(false, "#form-workout");
    ownerInput.readOnly = !ownerInput.readOnly;

    okWorkoutButton.className = okWorkoutButton.className.replace(" hide", "");
    cancelWorkoutButton.className = cancelWorkoutButton.className.replace(
      " hide",
      ""
    );
    buttonAddExercise.className = buttonAddExercise.className.replace(
      " hide",
      ""
    );
    buttonRemoveExercise.className = buttonRemoveExercise.className.replace(
      " hide",
      ""
    );
    inputSearchForUser.className = inputSearchForUser.className.replace(
      " hide",
      ""
    );
    addAthelteButton.className = addAthelteButton.className.replace(
      " hide",
      ""
    );

    okWorkoutButton.addEventListener("click", async () => createWorkout());
    cancelWorkoutButton.addEventListener(
      "click",
      handleCancelDuringWorkoutCreate
    );
    divCommentRow.className += " hide";
  }
});

function toggleHideById(id) {
  const element = document.querySelector(id);
  // eslint-disable-next-line
  console.log(`Hide${id} style: ${element.style.display}`);
  if (element.style.display === "block") {
    element.style.display = "none";
  } else {
    element.style.display = "block";
  }
}

async function onSearchForInputChange(e, container, currentUserUsername) {
  container.innerHTML = "";
  container.className = "col-lg-6";
  const input = e.target.value;
  if (input === undefined || input === null || input === "") {
    return;
  }
  const users = await sendRequest("GET", `${HOST}/api/users/?search=${input}`);
  const data = await users.json();
  mapUsersToButtons();

  function mapUsersToButtons() {
    data.results.forEach((user) => {
      const button = document.createElement("input");
      button.value = user.username;
      button.type = "button";
      button.className = "btn btn-primary";
      button.addEventListener("click", () =>
        toggleParticipant(user.username, currentUserUsername)
      );
      container.appendChild(button);
    });
  }
}

function toggleParticipant(username, currentUserUsername) {
  const ownerInput = document.querySelector("#inputOwner");
  if (participants.indexOf(username) < 0) {
    participants.push(username);
    ownerInput.value = `${currentUserUsername}, ${participants.join(", ")}`;
  } else {
    participants = participants.filter((f) => f !== username);
    const temp = participants.length > 0 ? `, ${participants.join(", ")}` : "";
    ownerInput.value = currentUserUsername + temp;
  }
}
