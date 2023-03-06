# 🚎 Bus Seat Allocator and Queue Management (CSP & A*)

This project aims to tackle two important challenges related to the seating and boarding of students on a bus.
  -> The first part of the project involves **finding a valid seating arrangement for different types of students on the bus**.
  -> The second part of the project focuses on **sorting the students in a queue to board the bus** while considering the specific needs of each student type.

The students on the bus belong to various courses and have designated seats. In addition, there are **different types of students**:
  - Some students are siblings who want to sit together.
  - Others are conflictive students who need to sit alone.
  - There are students with reduced mobility who require specific seating arrangements.
  - There can be students combining multiple of these types.
 
The project aims to create a seating plan that considers all these factors and satisfies the requirements of each student type.

<img src="https://venturebustours.com/images/vanture-CAX-double-no-dimension-1.jpg" align="left" width="300px"/>
In the <a href="https://github.com/aaronespasa/bus-seat-allocator/tree/main/parte-1">first part of the project</a>, the problem is modeled as a <b>Constraint Satisfaction Problem (CSP)</b>. This approach allows the project to <b>identify a valid seating arrangement for different types of students on the bus</b>. The seating arrangement must consider the specific needs of each student type while ensuring that there are no conflicts or overlaps in the seating plan. By utilizing the Constraint Satisfaction Problem approach, the project can find the optimal seating arrangement for all students on the bus.

<br clear="left"/>

<br />

<img src="https://us.123rf.com/450wm/gmast3r/gmast3r1906/gmast3r190601040/128444504-group-of-people-tourists-standing-line-queue-to-boarding-tour-bus-men-women-passengers-waiting-at.jpg?ver=6" align="right" width="300px"/>
The <a href="https://github.com/aaronespasa/bus-seat-allocator/tree/main/parte-2">second part of the project</a> involves <b>sorting the students in a queue to board the bus</b>. This part of the project takes into account the different needs of each student type while ensuring that the boarding process is as efficient as possible. For instance, students with reduced mobility may require additional time to board the bus, which can slow down the person behind them in the queue. Similarly, conflictive students may cause delays for other students behind them. The project utilizes the <b>A* algorithm</b> to sort the students in the queue efficiently while <b>minimizing the impact of each student type on the boarding process</b>.

<br clear="right"/>

<br />

Overall, this project aims to create a comprehensive solution for the seating and boarding of students on a bus. By considering the needs of different student types and utilizing advanced algorithms, the project aims to optimize the seating and boarding process, ensuring a safe and comfortable journey for all students.

## Getting Started 🛠
🗂 Clone the repository (the command below uses HTTPS):
```sh
$ git clone https://github.com/aaronespasa/practica2-100451339-100451273.git
```

🌲 Create a virtual environment and activate it (make sure you're using Python 3.8):
```sh
$ python3 -m venv ./venv
```
- To activate it in a machine using unix (MacOS or Linux):
```sh
$ source ./venv/bin/activate
```

- To activate it in a machine using Windows:
```sh
$ .\venv\Scripts\activate
```

📄 Install the required libraries (python-constraint):
```sh
$ pip install -r requirements.txt
```

🎉 Now, you are ready to go!

## Project Structure
![image](https://user-images.githubusercontent.com/39239895/201787659-6477026b-7516-4d87-b262-5110462d67fc.png)

## Made by Alejandra Galán & Aarón Espasandín
