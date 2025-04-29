# Project Title: Phishcord - AI-Powered Phishing Email Detector
Phishcord delivers a Google Chrome extension that aims to enhance the email security for Chrome users by implementing real-time detection and improving existing solutions.

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
2. Activate Phishcord by clicking the Extension icon (screenshot below)

![guide](screenshots/guide.png)


3. To change the model:
    * Click on the settings icon (screenshot below)
    
    ![settings](screenshots/settings.png)
    * It will display a dropdown list where you can choose a model (SVC is on by default)
    * (Click on the setting icon again to undisplay it)
4. To manually test the detection:
    * Click on the keyboard icon (screenshot below)
    
    ![manual](screenshots/manual.png)
    * A text area will appear for you to type your message
    * Click the predict button
    * It will display the prediction and explanation result
    * (Click on the keyboard icon again to undisplay it)
5. To **AUTO DETECT** with your email:
    * Go to Gmail and login with your account
    * Ensure that your Gmail account has 2-factor-authentication enabled
    * Create an App password (https://support.google.com/mail/answer/185833?hl=en-GB)
    * Rename `.env.example` to `.env`.
    * Inside `.env`, update the following:
        * USER_EMAIL: your email address
        * USER_PASSWORD: your app password (not your actual password!)
    * Click the Start Button
    * Send an email to the email you have specified on .env
    * Once email has been picked up, you shall receive an alert sound with its prediction & explanation result

## **License**
* This project is licensed under the MIT License.

## **Dataset Acknowledgment**
* This project used the **Phishing Email Dataset** dataset, available on https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset/data.  
* The dataset is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
* All rights to the dataset belong to the original creators.

## **FAQ**
**Q:** How do I install Phishcord?

**A:** Follow the installation steps in the README file.

**Q:** How do I use Phishcord?

**A:** Follow the usage steps in the README file.

**Q:** My Start/Stop button is frozen and unresponsive, how do I fix?

**A:** Ensure that app.py is running. If it is running, then you may have terminated app.py (Ctrl+C terminal) whilst the Start/Stop was toggled as another state. If this occurs, close and open the extension from clicking the Extension icon on Chrome. The software will fix itself by checking the status of the imap process.

**Q:** The results isn't showing up when auto-detecting, how do I fix?

**A:** Ensure that app.py is running. If it is running, then terminate and run app.py again, click the Start button and send an email to the email you have specified on .env - the likelihood of this occurring is lower ever since I've implemented sessions.

**Q:** Do I need to have the Gmail website to be displayed when auto-detecting?

**A:** No.

**Q:** How do I disable the alert sound when it detects? 

**A:** Click on the sound icon to toggle the alert sound on/off. (screenshot below)

![sound](screenshots/sound.png)

**Q:** Why is SVC toggled on by default? What's the best model?

**A:** Every model is different. This is why I have included the manual detection (via the keyboard icon from Step 4 of Usage) to allow you to choose your preference when testing each model. SVC has the highest accuracies but it's also the slowest out of the other models. The models (SVC, Random Forest, Naive Bayes and XGBoost) were all chosen due to its best performance in detecting phishing emails.

## **Thank you**
The format of my README guide was inspired from https://medium.com/@sumudithalanz/the-art-of-crafting-an-effective-readme-for-your-github-project-cf425a8b1580 