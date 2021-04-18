async function fetchWorkouts(ordering) {
  let response = await sendRequest(
    "GET",
    `${HOST}/api/workouts/?ordering=${ordering}`
  );

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  } else {
    let data = await response.json();

    let workouts = data.results;
    let container = document.getElementById("div-content");
    workouts.forEach((workout) => {
      let templateWorkout = document.querySelector("#template-workout");
      let cloneWorkout = templateWorkout.content.cloneNode(true);

      let aWorkout = cloneWorkout.querySelector("a");
      aWorkout.href = `workout.html?id=${workout.id}`;

      let h5 = aWorkout.querySelector("h5");
      h5.textContent = workout.name;

      let localDate = new Date(workout.date);

      let table = aWorkout.querySelector("table");
      let rows = table.querySelectorAll("tr");
      rows[0].querySelectorAll(
        "td"
      )[1].textContent = localDate.toLocaleDateString(); // Date
      rows[1].querySelectorAll(
        "td"
      )[1].textContent = localDate.toLocaleTimeString(); // Time
      rows[2].querySelectorAll("td")[1].textContent = workout.owner_username; //Owner
      rows[3].querySelectorAll("td")[1].textContent =
        workout.exercise_instances.length; // Exercises

      container.appendChild(aWorkout);
    });
    return workouts;
  }
}

async function fetchWorkoutInvitations() {
  let templateWorkoutInvitation = document.querySelector(
    "#template-invitation"
  );
  let listWorkoutInvitation = document.querySelector("#list-invitations");
  let response = await sendRequest("GET", `${HOST}/api/workouts/invitations`);

  if (!response.ok) {
    let data = await response.json();
    let alert = createAlert("Could not retrieve Invitations!", data);
    document.body.prepend(alert);
  } else {
    let invitations = await response.json();
    for (let invitation of invitations.results) {
      let cloneInvitation = templateWorkoutInvitation.content.cloneNode(true);
      let li = cloneInvitation.querySelector("li");
      let span = li.querySelector("span");
      span.textContent = `${invitation.owner} has invited you to a workout`;

      let buttons = li.querySelectorAll("button");
      let acceptButton = buttons[0];
      let declineButton = buttons[1];

      acceptButton.addEventListener("click", async (event) =>
        acceptInvitation(event, invitation)
      );

      declineButton.addEventListener("click", async (event) =>
        deleteInvitationAndReload(event, invitation)
      );

      listWorkoutInvitation.appendChild(li);
    }
    if (invitations.results.length == 0) {
      let p = document.createElement("p");
      p.innerText = "You currently have no invitations.";
      listWorkoutInvitation.append(p);
    }
  }
}

async function acceptInvitation(event, invitation) {
  console.log("Accept", invitation);
  let getWorkoutResponse = await sendRequest("GET", invitation.workout);
  if (getWorkoutResponse.ok) {
    let data = await getWorkoutResponse.json();
    console.log("Workout data", data);
    data.participants.push(invitation.participant);
    let putWorkoutResponse = await sendRequest("PUT", invitation.workout, data);
    if (putWorkoutResponse.ok) {
      deleteInvitationAndReload(null, invitation);
      return;
    }
  }
  console.log("Failed to update workout");
}

async function deleteInvitationAndReload(event, invitation) {
  console.log("Delete", invitation);
  let response = await sendRequest("DELETE", invitation.url);
  if (response.ok) {
    console.log("Invitation deleted");
    window.location.replace("workouts.html");
  } else {
    console.log("Failed to delete invitation");
  }
}

function createWorkout() {
  window.location.replace("workout.html");
}

window.addEventListener("DOMContentLoaded", async () => {
  await fetchWorkoutInvitations();
  let createButton = document.querySelector("#btn-create-workout");
  createButton.addEventListener("click", createWorkout);
  let ordering = "-date";

  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has("ordering")) {
    let aSort = null;
    ordering = urlParams.get("ordering");
    if (ordering == "name" || ordering == "owner" || ordering == "date") {
      let aSort = document.querySelector(`a[href="?ordering=${ordering}"`);
      aSort.href = `?ordering=-${ordering}`;
    }
  }

  let currentSort = document.querySelector("#current-sort");
  currentSort.innerHTML =
    (ordering.startsWith("-") ? "Descending" : "Ascending") +
    " " +
    ordering.replace("-", "");

  let currentUser = await getCurrentUser();
  // grab username
  if (ordering.includes("owner")) {
    ordering += "__username";
  }
  let workouts = await fetchWorkouts(ordering);

  let tabEls = document.querySelectorAll('a[data-bs-toggle="list"]');
  for (let i = 0; i < tabEls.length; i++) {
    let tabEl = tabEls[i];
    tabEl.addEventListener("show.bs.tab", function (event) {
      let workoutAnchors = document.querySelectorAll(".workout");
      for (let j = 0; j < workouts.length; j++) {
        // I'm assuming that the order of workout objects matches
        // the other of the workout anchor elements. They should, given
        // that I just created them.
        let workout = workouts[j];
        let workoutAnchor = workoutAnchors[j];

        switch (event.currentTarget.id) {
          case "list-my-workouts-list":
            if (
              workout.owner == currentUser.url ||
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
            if (workout.visibility == "PU") {
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
