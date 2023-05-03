![Logo](static/media/logo.ba7f1eb0bde41999c918.png)

# Preview
AlignMe is a posture tracking system that utilizes computer vision technology to monitor the movement of joints during exercise routines. The system is designed to ensure correct posture and reduce the risk of injury. 

Incorrect posture is a common cause of injuries during exercise. Poor alignment places undue stress on joints, ligaments, and muscles, leading to discomfort, pain, and even long-term damage. AlignMe aims to address this problem by providing real-time feedback to users, helping them correct their form and maintain proper alignment. 

The system uses a camera to capture the user's movements during exercise, which are then analysed by the computer vision algorithm. The algorithm identifies the position of the user's joints and tracks their movement throughout the exercise routine. The system then provides feedback to the user, indicating whether their form is correct or incorrect. 

## Environment Variables

To run this project, 

- rename the .env.example file to .env

- Create and deploy Oracle Database. Get the connection account, password, url from oracle developer.

## Local Development

Install Python,pip and pipenv (`pip install pipenv`).  
Clone this repository.

```bash
  git clone https://github.com/PyroSama07/alignMe.git
```

Install the required packages for the project.

```bash
  cd alignMe
  pipenv shell
  pipenv install
  cd code
  python app.py
```
Navigate to http://localhost:1300.
