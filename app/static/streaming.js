const form = document.getElementById("mood-form");
const output = document.getElementById("output");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  output.textContent = "";

  const formData = new FormData(form);
  const input = formData.get("input");

  const evtSource = new EventSource("/stream?input=" + encodeURIComponent(input));
  evtSource.onmessage = function(event) {
    let eventData = JSON.parse(event.data);
    output.textContent += eventData.response;
  };
  evtSource.onerror = function() {
    evtSource.close();
  };
});