document.addEventListener("DOMContentLoaded", function () {
  const nameForm = document.getElementById("nameForm");

  if (nameForm) {
    // Check if form exists to avoid errors on office page
    nameForm.addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent default form submission

      const nameInput = document.getElementById("name");
      const name = nameInput.value;
      const appointmentCheckbox = document.getElementById("appointment");
      const appointment = appointmentCheckbox.checked; // Get the checkbox state

      fetch("/submit_name", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `name=${name}&appointment=${appointment}`, // Include appointment data
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            nameInput.value = ""; // Clear the input
            appointmentCheckbox.checked = false; // Uncheck the checkbox
            console.log("Name submitted successfully:", data.name);
          } else {
            console.error("Error submitting name:", data);
          }
        })
        .catch((error) => {
          console.error("Network error:", error);
        });
    });
  }
});
