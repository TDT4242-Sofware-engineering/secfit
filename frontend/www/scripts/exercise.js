let cancelButton;
let okButton;
let deleteButton;
let editButton;
let oldFormData;
let currentUser;

function handleCancelButtonDuringEdit() {
  setReadOnly(true, "#form-exercise");
  okButton.className += " hide";
  deleteButton.className += " hide";
  cancelButton.className += " hide";
  editButton.className = editButton.className.replace(" hide", "");

  cancelButton.removeEventListener("click", handleCancelButtonDuringEdit);

  let form = document.querySelector("#form-exercise");
  if (oldFormData.has("name")) form.name.value = oldFormData.get("name");
  if (oldFormData.has("description"))
    form.description.value = oldFormData.get("description");
  if (oldFormData.has("unit")) form.unit.value = oldFormData.get("unit");

  oldFormData.delete("name");
  oldFormData.delete("description");
  oldFormData.delete("unit");
}

function handleCancelButtonDuringCreate() {
  window.location.replace("exercises.html");
}

function validateFile() {
  const errorMsg = document.querySelector("#errorMsg");
  errorMsg.innerHTML = "";
  const validatedFiles = Array.from(customFile.files).filter((file, i) => {
    if (file.size < 1024 * 1024) {
      return file;
    }
    const errorNode = document.createElement("p");
    errorNode.classList.add("text-danger");
    const text = document.createTextNode(
      `File ${file.name} is too big. Max size 1MB`
    );
    errorNode.appendChild(text);
    errorMsg.appendChild(errorNode);
  });

  const newFileList = new DataTransfer();
  validatedFiles.forEach((file) => newFileList.items.add(file));

  customFile.files = newFileList.files;
}

function exerciseForm() {
  let form = document.querySelector("#form-exercise");
  let formData = new FormData(form);
  const submitForm = new FormData();
  submitForm.append("name", formData.get("name"));
  submitForm.append("description", formData.get("description"));
  submitForm.append("unit", formData.get("unit"));

  for (let file of formData.getAll("files")) {
    submitForm.append("files", file);
  }

  return submitForm;
}

async function createExercise() {
  const submitForm = exerciseForm();

  let response = await sendRequest(
    "POST",
    `${HOST}/api/exercises/`,
    submitForm,
    ""
  );

  if (response.ok) {
    window.location.replace("exercises.html");
  } else {
    let data = await response.json();
    let msg = "";
    if (data.files) {
      data.files.forEach((file) => (msg += `${file.file}`));
    }
    let alert = createAlert("Could not create new exercise!", data, msg);
    document.body.prepend(alert);
  }
}

function handleEditExerciseButtonClick() {
  setReadOnly(false, "#form-exercise");

  editButton.className += " hide";
  okButton.className = okButton.className.replace(" hide", "");
  cancelButton.className = cancelButton.className.replace(" hide", "");
  deleteButton.className = deleteButton.className.replace(" hide", "");

  cancelButton.addEventListener("click", handleCancelButtonDuringEdit);

  let form = document.querySelector("#form-exercise");
  oldFormData = new FormData(form);
}

async function deleteExercise(id) {
  let response = await sendRequest("DELETE", `${HOST}/api/exercises/${id}/`);
  if (!response.ok) {
    let data = await response.json();
    let alert = createAlert(`Could not delete exercise ${id}`, data);
    document.body.prepend(alert);
  } else {
    window.location.replace("exercises.html");
  }
}

async function retrieveExercise(id) {
  let response = await sendRequest("GET", `${HOST}/api/exercises/${id}/`);
  if (!response.ok) {
    let data = await response.json();
    let alert = createAlert("Could not retrieve exercise data!", data);
    document.body.prepend(alert);
  } else {
    let exerciseData = await response.json();
    let form = document.querySelector("#form-exercise");
    let formData = new FormData(form);
    if (currentUser.username === exerciseData["owner_username"]) {
      const customFile = document.querySelector("#customFile");
      customFile.classList.remove("hide");
    }

    for (let key of formData.keys()) {
      let selector = `input[name="${key}"], textarea[name="${key}"]`;
      let input = form.querySelector(selector);
      let newVal = exerciseData[key];
      input.value = newVal;
    }

    handleExerciseFiles(exerciseData);
  }
}

function handleExerciseFiles(exerciseData) {
  if (exerciseData.files && exerciseData.files.length > 0) {
    const mediaCarousel = document.querySelector("#mediaCarousel");
    mediaCarousel.classList.remove("hide");

    exerciseData.files.forEach((file, i) => {
      // Indicator button
      const btn = document.createElement("button");
      btn.setAttribute("type", "button");
      btn.setAttribute("data-bs-target", "#mediaCarousel");
      btn.setAttribute("data-bs-slide-to", i);
      btn.setAttribute("aria-label", `Slide ${i}`);
      if (i === 0) {
        btn.setAttribute("class", "active");
        btn.setAttribute("aria-current", "true");
      }
      const carouselIndicator = document.querySelector(".carousel-indicators");
      carouselIndicator.appendChild(btn);

      // Carousel item
      const carouselItem = document.createElement("div");
      carouselItem.classList.add("carousel-item");
      carouselItem.setAttribute("style", "height:400px");
      if (i === 0) {
        carouselItem.classList.add("active");
      }
      const media = document.createElement("img");
      media.classList.add("d-block");
      media.classList.add("w-75");
      media.classList.add("h-100");
      media.classList.add("mx-auto");
      media.classList.add("pb-4");
      media.setAttribute("style", "object-fit: contain");
      media.src = file.file;
      carouselItem.appendChild(media);

      const carouselInner = document.querySelector(".carousel-inner");
      carouselInner.appendChild(carouselItem);
    });
  }
}

async function updateExercise(id) {
  const submitForm = exerciseForm();

  let response = await sendRequest(
    "PUT",
    `${HOST}/api/exercises/${id}/`,
    submitForm,
    ""
  );

  if (!response.ok) {
    let data = await response.json();
    let msg = "";
    if (data.files) {
      data.files.forEach((file) => (msg += `${file.file}`));
    }
    let alert = createAlert(`Could not update exercise ${id}`, data, msg);
    document.body.prepend(alert);
  } else {
    // duplicate code from handleCancelButtonDuringEdit
    // you should refactor this
    setReadOnly(true, "#form-exercise");
    okButton.className += " hide";
    deleteButton.className += " hide";
    cancelButton.className += " hide";
    editButton.className = editButton.className.replace(" hide", "");

    cancelButton.removeEventListener("click", handleCancelButtonDuringEdit);

    oldFormData.delete("name");
    oldFormData.delete("description");
    oldFormData.delete("unit");
  }
}

window.addEventListener("DOMContentLoaded", async () => {
  cancelButton = document.querySelector("#btn-cancel-exercise");
  okButton = document.querySelector("#btn-ok-exercise");
  deleteButton = document.querySelector("#btn-delete-exercise");
  editButton = document.querySelector("#btn-edit-exercise");
  oldFormData = null;
  currentUser = await getCurrentUser();

  const urlParams = new URLSearchParams(window.location.search);

  const cstmFile = document.querySelector("#customFile");
  console.log("custom inputfile: ", cstmFile);
  cstmFile.addEventListener("input", validateFile);

  // view/edit
  if (urlParams.has("id")) {
    const exerciseId = urlParams.get("id");
    await retrieveExercise(exerciseId);

    editButton.addEventListener("click", handleEditExerciseButtonClick);
    deleteButton.addEventListener(
      "click",
      (async (id) => deleteExercise(id)).bind(undefined, exerciseId)
    );
    okButton.addEventListener("click", async () => {
      await updateExercise(exerciseId);
    });
  }
  //create
  else {
    setReadOnly(false, "#form-exercise");

    editButton.className += " hide";
    okButton.className = okButton.className.replace(" hide", "");
    cancelButton.className = cancelButton.className.replace(" hide", "");
    customFile.classList.remove("hide");

    okButton.addEventListener("click", async () => createExercise());
    cancelButton.addEventListener("click", handleCancelButtonDuringCreate);
  }
});
