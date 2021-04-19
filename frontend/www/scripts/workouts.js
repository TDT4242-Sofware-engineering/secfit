/* eslint-disable no-shadow, no-plusplus */
async function fetchWorkouts(ordering) {
  const response = await sendRequest(
    "GET",
    `${HOST}/api/workouts/?ordering=${ordering}`
  );

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  } else {
    const data = await response.json();

    const workouts = data.results;
    const container = document.getElementById("div-content");
    workouts.forEach((workout) => {
      const templateWorkout = document.querySelector("#template-workout");
      const cloneWorkout = templateWorkout.content.cloneNode(true);

      const aWorkout = cloneWorkout.querySelector("a");
      aWorkout.href = `workout.html?id=${workout.id}`;

      const h5 = aWorkout.querySelector("h5");
      h5.textContent = workout.name;

      const localDate = new Date(workout.date);

      const table = aWorkout.querySelector("table");
      const rows = table.querySelectorAll("tr");
      rows[0].querySelectorAll(
        "td"
      )[1].textContent = localDate.toLocaleDateString(); // Date
      rows[1].querySelectorAll(
        "td"
      )[1].textContent = localDate.toLocaleTimeString(); // Time
      rows[2].querySelectorAll("td")[1].textContent = workout.owner_username; // Owner
      rows[3].querySelectorAll("td")[1].textContent =
        workout.exercise_instances.length; // Exercises

      container.appendChild(aWorkout);
    });
    return workouts;
  }
}

async function fetchWorkoutInvitations() {
  const templateWorkoutInvitation = document.querySelector(
    "#template-invitation"
  );
  const listWorkoutInvitation = document.querySelector("#list-invitations");
  const response = await sendRequest("GET", `${HOST}/api/workouts/invitations`);

  if (!response.ok) {
    const data = await response.json();
    const alert = createAlert("Could not retrieve Invitations!", data);
    document.body.prepend(alert);
  } else {
    const invitations = await response.json();
    mapInvitationsToHtmlObjects(invitations);

    if (invitations.results.length === 0) {
      displayNoInvitations();
    }
  }

  function displayNoInvitations() {
    const p = document.createElement("p");
    p.innerText = "You currently have no invitations.";
    listWorkoutInvitation.append(p);
  }

  function mapInvitationsToHtmlObjects(invitations) {
    for (const invitation of invitations.results) {
      const cloneInvitation = templateWorkoutInvitation.content.cloneNode(true);
      const li = cloneInvitation.querySelector("li");
      const span = li.querySelector("span");
      span.textContent = `${invitation.owner} has invited you to a workout`;

      const buttons = li.querySelectorAll("button");
      const acceptButton = buttons[0];
      const declineButton = buttons[1];

      acceptButton.addEventListener("click", async (event) =>
        acceptInvitation(event, invitation)
      );

      declineButton.addEventListener("click", async (event) =>
        deleteInvitationAndReload(event, invitation)
      );

      listWorkoutInvitation.appendChild(li);
    }
  }
}

async function acceptInvitation(event, invitation) {
  const getWorkoutResponse = await sendRequest("GET", invitation.workout);
  if (getWorkoutResponse.ok) {
    const workout = await getWorkoutResponse.json();
    workout.participants.push(invitation.participant);
    const putWorkoutResponse = await sendRequest(
      "PUT",
      invitation.workout,
      workout
    );
    if (putWorkoutResponse.ok) {
      deleteInvitationAndReload(null, invitation);
    }
  }
}

async function deleteInvitationAndReload(event, invitation) {
  const response = await sendRequest("DELETE", invitation.url);
  if (response.ok) {
    window.location.replace("workouts.html");
  }
}

function createWorkout() {
  window.location.replace("workout.html");
}

window.addEventListener("DOMContentLoaded", async () => {
  await fetchWorkoutInvitations();
  const createButton = document.querySelector("#btn-create-workout");
  createButton.addEventListener("click", createWorkout);
  let ordering = "-date";

  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has("ordering")) {
    ordering = urlParams.get("ordering");
    if (ordering === "name" || ordering === "owner" || ordering === "date") {
      const aSort = document.querySelector(`a[href="?ordering=${ordering}"`);
      aSort.href = `?ordering=-${ordering}`;
    }
  }

  const currentSort = document.querySelector("#current-sort");
  currentSort.innerHTML = `${
    ordering.startsWith("-") ? "Descending" : "Ascending"
  } ${ordering.replace("-", "")}`;

  const currentUser = await getCurrentUser();
  // grab username
  if (ordering.includes("owner")) {
    ordering += "__username";
  }
  const workouts = await fetchWorkouts(ordering);

  const tabEls = document.querySelectorAll('a[data-bs-toggle="list"]');
  for (let i = 0; i < tabEls.length; i++) {
    const tabEl = tabEls[i];
    tabEl.addEventListener("show.bs.tab", (event) => {
      const workoutAnchors = document.querySelectorAll(".workout");
      for (let j = 0; j < workouts.length; j++) {
        // I'm assuming that the order of workout objects matches
        // the other of the workout anchor elements. They should, given
        // that I just created them.
        const workout = workouts[j];
        const workoutAnchor = workoutAnchors[j];

        switch (event.currentTarget.id) {
          case "list-my-workouts-list":
            if (
              workout.owner === currentUser.url ||
              workout.participants.includes(currentUser.username)
            ) {
              workoutAnchor.classList.remove("hide");
            } else {
              workoutAnchor.classList.add("hide");
            }
            break;
          case "list-athlete-workouts-list":
            if (
              currentUser.athletes &&
              currentUser.athletes.includes(workout.owner)
            ) {
              workoutAnchor.classList.remove("hide");
            } else {
              workoutAnchor.classList.add("hide");
            }
            break;
          case "list-public-workouts-list":
            if (workout.visibility === "PU") {
              workoutAnchor.classList.remove("hide");
            } else {
              workoutAnchor.classList.add("hide");
            }
            break;
          default:
            workoutAnchor.classList.remove("hide");
            break;
        }
      }
    });
  }
});
