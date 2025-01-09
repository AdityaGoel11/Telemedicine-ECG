#Code to generate graphs for each user from the database

import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute("SELECT * FROM users")
users = c.fetchall()
print(users)

for user in users:
    c.execute('SELECT message, timestamp FROM data WHERE user_id=?', (user[0],))
    data = c.fetchall()
    data.sort(key=lambda x: x[1])
    print(data)
    plt.plot([i for i in range(len(data))], [x[0] for x in data], label=user[1])
    plt.show()

