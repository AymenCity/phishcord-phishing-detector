const modelSelectAuto = document.getElementById('model-select');
modelSelectAuto.addEventListener('change', async () => {
  const selectedModel = modelSelectAuto.value;

  try {
    await fetch('http://127.0.0.1:5000/set-model', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ model: selectedModel }),
    });
  } catch (err) {
    console.error('Failed to set model for auto detection:', err);
  }
});


// https://www.youtube.com/watch?v=Jxj_jfh4IDk
// manual detection - predict
const form = document.getElementById("email-form");
form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const input = document.getElementById("email-text").value;

  try {
    const modelSelect = document.getElementById("model-select").value;
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: input, model: modelSelect }),
    });

    if (response.ok) {
      const data = await response.json();
      const prediction = data.prediction;
      const explanation = data.explanation;

      const resultDiv = document.getElementById("prediction-result");
      resultDiv.innerText = prediction === 0 ? "REGULAR" : "PHISHING";

      const explanationDiv = document.getElementById("lime-explanation");
      explanationDiv.innerHTML = explanation
        .map(
          ([word, weight]) =>
            `${word}: <span style="color:${
              weight > 0 ? "red" : "green"
            }">${weight.toFixed(3)}</span>`
        )
        .join("<br>");
    } else {
      console.error("Request failed:", response.status);
    }
  } catch (error) {
    console.error("Request failed:", error);
  }
});

// start / stop
let scriptRunning = false;
const toggleButton = document.getElementById("toggle-script");

toggleButton.addEventListener("click", async () => {
  const endpoint = scriptRunning ? "stop" : "start";

  try {
    const response = await fetch(`http://127.0.0.1:5000/${endpoint}`, {
      method: "POST",
    });

    if (response.ok) {
      scriptRunning = !scriptRunning;
      toggleButton.innerHTML = scriptRunning
        ? '<i class="fa fa-stop" aria-hidden="true"></i> STOP'
        : '<i class="fa fa-play" aria-hidden="true"></i> START';
    } else {
      console.error(await response.text());
    }
  } catch (error) {
    console.error("Failed to connect to Python server:", error);
  }
});

// changes icon of sound
let isMuted = false;
document.getElementById("volumeIcon").addEventListener("click", () => {
  isMuted = !isMuted;
  document
    .getElementById("volumeIcon")
    .classList.toggle("fa-volume-up", !isMuted);
  document
    .getElementById("volumeIcon")
    .classList.toggle("fa-volume-off", isMuted);
});

// auto detection - stream
  const stream = new EventSource('http://127.0.0.1:5000/stream');

  stream.onmessage = function(event) {
    const data = JSON.parse(event.data);
  
    // Only update if there's actually a subject and from field
    if (data.subject && data.from) {
      const resultDiv = document.getElementById('prediction-result-auto');
      const resultDiv_extra = document.getElementById('prediction-result-auto-extra');
  
      const summary = `
        ${data.prediction === 0 ? "REGULAR" : "PHISHING"}
      `;
      const summary_extra = `
      New Email Detected!
      Subject: ${data.subject}
      From: ${data.from}
    `;
  
      resultDiv.innerText = summary;
      resultDiv_extra.innerText = summary_extra;
  
      // Display LIME explanation if present
      const autoExplainDiv = document.getElementById('lime-explanation-auto');
      if (data.explanation) {
        autoExplainDiv.innerHTML = data.explanation
          .map(([word, weight]) => `${word}: <span style="color:${weight > 0 ? 'red' : 'green'}">${weight.toFixed(3)}</span>`)
          .join('<br>');
      }
  
      // Optional: play sound only when real data arrives
      if (!isMuted) {
        var myAudio = new Audio(chrome.runtime.getURL("audio.mp3"));
        myAudio.play();
      }
    }
  };
  


  //

  // https://www.tutorialspoint.com/how-to-hide-a-div-in-javascript-on-button-click#:~:text=To%20hide%20a%20div%20in%20JavaScript%20on%20button%20click%2C%20we,display%20the%20hidden%20div%20again.
  // https://stackoverflow.com/questions/36324333/refused-to-execute-inline-event-handler-because-it-violates-csp-sandbox/36349056#36349056
  // shows & hides div
  document.getElementById("SettingIcon").addEventListener("click", hideSetting);

  function hideSetting() {
    var divs = document.getElementById("settingDiv");
    divs.classList.toggle("hidden"); // Toggle the hidden class
  }

  document.getElementById("manualIcon").addEventListener("click", hideManual);

  function hideManual() {
    var divs = document.getElementById("manualDiv");
    divs.classList.toggle("hidden"); // Toggle the hidden class
  }

