// https://www.youtube.com/watch?v=Jxj_jfh4IDk

const form = document.getElementById('email-form');


form.addEventListener('submit', async (event) => {

  event.preventDefault();


  const input = document.getElementById('email-text').value;

  try {
 
    const response = await fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({text: input}),
    });


    if (response.ok) {
 
      const prediction = (await response.json()).prediction;
      const resultDiv = document.getElementById('prediction-result');
      resultDiv.innerText = prediction === 0 ? 'The email is Regular' : 'The email is Phishing';
    } else {
      console.error('Request failed:', response.status);
    }
  } catch (error) {
    console.error('Request failed:', error);
  }
});

let scriptRunning = false;

const toggleButton = document.getElementById('toggle-script');

toggleButton.addEventListener('click', async () => {
  const endpoint = scriptRunning ? 'stop' : 'start';

  try {
    const response = await fetch(`http://127.0.0.1:5000/${endpoint}`, {
      method: 'POST'
    });

    if (response.ok) {
      scriptRunning = !scriptRunning;
      toggleButton.textContent = scriptRunning ? 'Stop Script' : 'Start Script';
    } else {
      console.error(await response.text());
    }
  } catch (error) {
    console.error('Failed to connect to Python server:', error);
  }
});

const stream = new EventSource('http://127.0.0.1:5000/stream');

stream.onmessage = function(event) {
  const data = JSON.parse(event.data);
  const resultDiv = document.getElementById('prediction-result-auto');

  const summary = `
    New Email Detected!
    Subject: ${data.subject}
    From: ${data.from}
    Prediction: ${data.prediction === 1 ? "Phishing" : "Regular"}
  `;

  resultDiv.innerText = summary;
};

