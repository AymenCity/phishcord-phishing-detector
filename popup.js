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