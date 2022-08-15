from src import app
from src.db import cur, connection

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
    cur.close()
    connection.close()
