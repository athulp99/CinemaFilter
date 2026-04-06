const statusButton = document.getElementById("status-button");
const statusText = document.getElementById("status-text");

if (statusButton && statusText) {
  statusButton.addEventListener("click", () => {
    statusText.textContent = "Project status: starter is working and ready to publish.";
  });
}
