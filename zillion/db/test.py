# 配置多个数据源及其连接池参数
from sqlalchemy import text

from zillion.db.DataSourceFactory import session_future

# 执行数据库操作
result = session_future.execute(text("SELECT * FROM basic")).fetchall()
print(result)
