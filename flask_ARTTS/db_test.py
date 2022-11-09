import sqlite3

con = sqlite3.connect('local_trains_subways.db')


c = con.cursor()


#Comment the below Crete Table lines(10-23) when you just wanna insert rows because we can't create same table twice'
c.execute("""CREATE TABLE Subways (
	train_id INTEGER PRIMARY KEY,
	train_name TEXT NOT NULL,
	source_location TEXT NOT NULL,
	destination_location TEXT NOT NULL,
	price INTEGER NOT NULL,
	travel_date datetime default current_timestamp NOT NULL

)""")

c.execute("""CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT,username varchar(50) NOT NULL,
    password varchar(255) NOT NULL,
    email varchar(100) NOT NULL
)""")


# insert as same rows as needed but make sure to have unique id
c.execute("""INSERT INTO Subways(train_id, train_name,source_location, destination_location, price,travel_date)
VALUES(10051, 'Bridgeport Express','Connecticut','Bridgeport',12, "2022-10-18"),
(10052, 'North east Express','Connecticut','Bridgeport',24, "2022-10-18"),
(10053, 'HartFord Express','Connecticut','Bridgeport',20, "2022-10-18"),
(10054, 'NewYork Line','NewYork','Bridgeport',12, "2022-10-18"),
(10055, 'North east Express','Connecticut','NewYork',24, "2022-10-18"),
(10056, 'Manhattan Express','Connecticut','Manhattan',20, "2022-10-18"),
(10057, 'NewYork Express','NewYork','Manhattan',12, "2022-10-18"),
(10058, 'North east Express','NewYork','Manhattan',24, "2022-10-18"),
(10059, 'NewHaven Express','Connecticut','NewHaven',20, "2022-10-18"),
(10060, 'NewHaven Express','Connecticut','NewHaven',20, "2022-10-18")
""")

c.execute("SELECT * FROM Subways")

print(c.fetchall())

con.commit()

con.close()