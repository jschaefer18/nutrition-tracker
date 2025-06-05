## Overview

**Project Title**: Nutrition Tracker

**Project Description**:
This is a command line application that allows the user to track their nutrition intake, set goals, and analyze their eating habits over time. This application uses Firebase as a backend to store user data securely and efficiently.

**Project Goals**:
- Enable users to create and manage accounts securely
- Allow users to log their daily nutrition intake
- Provide analytics on nutrition data to help users meet their health goals
- Allow users to set and track nutrition goals
- Store all user data persistently using a cloud-based database
- Provide automated feedback based on performance


## Instructions for Build and Use

Steps to build and/or run the software:

1. Clone the repository from GitHub.
2. Set up a Firebase project and download the service account key.
3. Place the service account key JSON file in the project directory and update the `firebase_config.py` file with the correct path.
4. Download libraries: pip install firebase-admin google-cloud-firestore bcrypt


Instructions for using the software:

1. Run main.py to start the application.
2. Sign up for a new account
3. Log in with your credentials.
4. Navigate through the menu to log nutrition data, set goals, and view analytics.

## Development Environment 

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* Python 3.8 or higher
* pip install firebase-admin
* pip install google-cloud-firestore
* pip install bcrypt

## Useful Websites to Learn More

I found these websites useful in developing this software:

* [Firebase Documentation](https://firebase.google.com/docs)
* [Good Cloud Firestore Client Libraries](https://firebase.google.com/docs/firestore/client-libraries)
* [Python Bcrypt Documentation](https://pypi.org/project/bcrypt/)
* [Firebase offical GPT model] (https://cloud.google.com/python/docs/reference/firestore/latest)

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] It would be cool to add some sort of graphing library to visualize nutrition data over time.
* [ ] Add a feature to export nutrition logs to CSV or Excel format.
* [ ] Add more detailed goal tracking, such as monthly progress reports.
