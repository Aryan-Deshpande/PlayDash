from backend import app
from backend import cur, connection

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
    cur.close()
    connection.close()
