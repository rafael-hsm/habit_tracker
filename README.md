# Habit Tracker

Access the system: https://rafael-habit-tracker.onrender.com

Solution developed during the course: [Web Developer Bootcamp with Flask and Python in 2023](https://www.udemy.com/course/web-developer-bootcamp-flask-python/) and implemented some tweaks and features like deleting a task.

![Habit_tracker](https://github.com/rafael-hsm/habit_tracker/blob/main/static/habit_tracker_main.png)
## Tools
1. Python
2. VScode
3. MongoDB

## Create a path and clonning the repository
```
mkdir habit_tracker && cd habit_tracker
git clone https://github.com/rafael-hsm/habit_tracker.git
```

## Navigate to path and active a virtual enviroment
```
cd habit_tracker
python -m venv venv
venv\Scripts\activate
```

## Install requirements and settings MongoDB
```
pip install -r requirements.txt
```

## Create a file with name .env and set data for access your MongoDB, you can see a example in file .env.example
```
MONGODB_URI=mongodb+srv://<your_username>:<your_password>@<name_your_db>.dbjo0y7.mongodb.net/
```

## Running application
```
flask run
```

## If you can activate debug mode type this command:
```
set FLASK_DEBUG=True
```