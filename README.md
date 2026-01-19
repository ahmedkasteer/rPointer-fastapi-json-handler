---------------------#########################   PROJECT README FOR JSON HANDLER   #########################---------------------


This Project consists of three main files:
* main.py
* database.py
* models.py

***DEPENDENCIES***



- This Project uses SQL Alchemy Object Relational Mapper for mapping DB Tables to Python Objects. 
- This Project uses FastAPI with UviCorn for developing a localhost server. 
- This Project uses pyscopg2-binary for PostGres SQL Connectivity. 



-----INSTALL LIBRARIES-----


--> Terminal Command: uv add fastapi sqlalchemy psycopg2-binary

- This Project was initialized using UV for Virtual Environment. 

--> Terminal Command: uv init

To run this project on a LOCAL HOST SERVER run for main.py file in developer mode: 

* For users table on your local machine visit: http://127.0.0.1:8000/users
* For reviews table on your local machine visit: http://127.0.0.1:8000/reviews
* For userReview table on your local machine visit: http://127.0.0.1:8000/userreview

To run this project: 
--> Terminal Command: uv run fastapi dev main.py 


