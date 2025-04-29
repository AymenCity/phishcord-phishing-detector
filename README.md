# Project Title: Phishcord - AI-Powered Phishing Email Detector

## **Installation**
To install Phishcord, follow these steps:

1. Clone the repository: **`git clone https://github.com/AymenCity/phishcord-phishing-detector`**
2. Ensure you have Python 3.9 or higher
2. Ensure you have Chrome version 135 or higher installed & Open Google Chrome
3. Load the extension in Google
    * Open Google Chrome
    * Go to chrome://extensions 
    * Enable Developer Mode
    * Click "Load unpacked" 
    * Select the folder where you cloned the repository
4. Install backend dependencies: **`pip install -r requirements.txt`**
5. Start the backend server: **`python app.py`**

## **Usage**
To use Phishcord, follow these steps:

1. Open Google Chrome
2. Activate Phishcord by clicking the Extension icon
3. To change the model:
    * Click on the settings icon:
    
    ![Settings Icon](screenshots/settings.png)
    * It will display a dropdown list where you can choose a model (SVC is on by default)
    * Click on the setting icon again to hide the dropdown list
4. To manually test the detection:
    * Click on the keyboard icon (screenshot below)
    
    ![manual](screenshots/manual.png)
    * A text area will appear for you to type your message
    * Click the predict button
    * It will display the prediction and explanation result
5. To auto detect with your email:
    * Go to Gmail and login with your account
    * Ensure that your Gmail account has 2-factor-authentication enabled
    * Create an App password (https://support.google.com/mail/answer/185833?hl=en-GB)
    * Rename `.env.example` to `.env`.
    * Inside `.env`, update the following:
        * USER_EMAIL: your email address
        * USER_PASSWORD: your app password (not your actual password!)
    * Click the Start Button
    * Send an email to yourself (or receive one from another email address)!


## **License**

* This project is licensed under the MIT License.

## **Dataset Acknowledgment**

* This project used the **Phishing Email Dataset** dataset, available on https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset/data.  
* The dataset is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
* All rights to the dataset belong to the original creators.

## **FAQ**

**Q:** What is Phishcord?

**A:** Phishcord deliver a Google Chrome extension of an AI-powered phishing detector that aims to enhance the email security for Chrome users by implementing real-time detection and improving existing solutions.

**Q:** How do I install Phishcord?

**A:** Follow the installation steps in the README file.

**Q:** How do I use Phishcord?

**A:** Follow the usage steps in the README file.

**Q:** My Start/Stop button is frozen and unresponsive, how do I fix?

**A:** Ensure that app.py is running. If it is running, then you may have terminated app.py (Ctrl+C terminal) whilst the Start/Stop was toggled as another state. If this occurs, close and open the extension from clicking the Extension icon on Chrome. The software will fix itself by checking the status of the imap process.

**Q:** How do I disable the alert sound when it detects? 

**A:** Click on the sound icon (screenshot below)

![sound](screenshots/sound.png)


## **Thank you**

The format of my README guide was inspired from https://medium.com/@sumudithalanz/the-art-of-crafting-an-effective-readme-for-your-github-project-cf425a8b1580 