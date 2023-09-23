import mysql.connector


class DbManager:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            print(f"Connected to MySQL database: {self.database}")
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL database: {e}")

    def execute(self, sql):
        if not self.conn:
            self.connect()
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
            print("sql executed successfully")
        except mysql.connector.Error as e:
            print(f"Error execute: {e}")

    def executemany(self, sql, data):
        if not self.conn:
            self.connect()
        try:
            cursor = self.conn.cursor()
            cursor.executemany(sql, data)
            self.conn.commit()
            cursor.close()
            print("Batch executed successfully")
        except mysql.connector.Error as e:
            print(f"Error executing batch: {e}")

    def fetch_data(self, query):
        if not self.conn:
            self.connect()
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            return data
        except mysql.connector.Error as e:
            print(f"Error fetching data: {e}")

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print(f"Connection to MySQL database {self.database} closed")


# 示例用法
if __name__ == "__main__":
    db_manager = DbManager(
        host="localhost",
        username="linjingu",
        password="linjingu",
        database="stock"
    )

    # 创建表
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255)
    );
    """
    db_manager.execute(create_table_query)

    # 插入数据
    insert_data_query = "INSERT INTO users (name, email) VALUES ('John', 'john@example.com');"
    db_manager.execute(insert_data_query)

    # 查询数据
    select_data_query = "SELECT * FROM users;"
    data = db_manager.fetch_data(select_data_query)
    print(data)

    # 关闭连接
    db_manager.close_connection()
