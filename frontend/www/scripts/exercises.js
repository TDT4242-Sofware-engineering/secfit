async function fetchExerciseTypes(request) {
  const response = await sendRequest("GET", `${HOST}/api/exercises/`);

  if (response.ok) {
    const data = await response.json();

    const exercises = data.results;
    const container = document.getElementById("div-content");
    const exerciseTemplate = document.querySelector("#template-exercise");
    exercises.forEach((exercise) => {
      const exerciseAnchor = exerciseTemplate.content.firstElementChild.cloneNode(
        true
      );
      exerciseAnchor.href = `exercise.html?id=${exercise.id}`;

      const h5 = exerciseAnchor.querySelector("h5");
      h5.textContent = exercise.name;

      const p = exerciseAnchor.querySelector("p");
      p.textContent = exercise.description;

      container.appendChild(exerciseAnchor);
    });
  }

  return response;
}

function createExercise() {
  window.location.replace("exercise.html");
}

window.addEventListener("DOMContentLoaded", async () => {
  const createButton = document.querySelector("#btn-create-exercise");
  createButton.addEventListener("click", createExercise);

  const response = await fetchExerciseTypes();

  if (!response.ok) {
    const data = await response.json();
    const alert = createAlert("Could not retrieve exercise types!", data);
    document.body.prepend(alert);
  }
});
