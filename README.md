# Hawaii-Climate-Analysis

The purpose of this project is to analyze the climate in Hawaii by using SQLAlchemy, Pandas and Matplotlib. 
First I used SQLAlchemy to connect to my sqlite database and then I designed a query to retrieve the last 12 months 
of precipitation data and created a dataframe showing this information.
Then I designed a Flask API based on the previous queries and created different routes that will return a JSON list
with information regarding min/max temperature, latest observations, stations list, etc.
