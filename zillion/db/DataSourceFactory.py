from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

db_stock = 'stock'
db_future = 'future'

config = {
    'data_sources': {
        db_future: {
            'url': 'mysql+pymysql://linjingu:linjingu@127.0.0.1:3306/future?charset=UTF8MB4',
            'pool_size': 5,  # 连接池大小5
            'max_overflow': 10,  # 允许的最大溢出连接数10
            'pool_timeout': 10,  # 获取连接超时时间10秒
            'pool_recycle': 3600  # 连接最大生命周期3600秒（1小时）
        },
        db_stock: {
            'url': 'mysql+pymysql://linjingu:linjingu@127.0.0.1:3306/stock?charset=UTF8MB4',
            'pool_size': 5,  # 连接池大小5
            'max_overflow': 10,  # 允许的最大溢出连接数10
            'pool_timeout': 10,  # 获取连接超时时间10秒
            'pool_recycle': 3600  # 连接最大生命周期3600秒（1小时）
        }
    }
}


class DataSourceFactory:
    def __init__(self, config):
        self.config = config
        self.engines = {}
        self.sessions = {}

    def get_engine(self, name):
        if name not in self.engines:
            ds_config = self.config['data_sources'][name]
            self.engines[name] = create_engine(
                ds_config['url'],
                echo=True,
                pool_size=ds_config.get('pool_size', 5),  # 连接池大小，默认5
                max_overflow=ds_config.get('max_overflow', 10),  # 允许的最大溢出连接数，默认10
                pool_timeout=ds_config.get('pool_timeout', 30),  # 获取连接超时时间，默认30秒
                pool_recycle=ds_config.get('pool_recycle', 3600)  # 连接最大生命周期，默认3600秒（1小时）
            )
        return self.engines[name]

    def get_session(self, name):
        if name not in self.sessions:
            engine = self.get_engine(name)
            session_factory = sessionmaker(bind=engine)
            self.sessions[name] = scoped_session(session_factory)
        return self.sessions[name]

    def close_all(self):
        for session in self.sessions.values():
            session.remove()
        for engine in self.engines.values():
            engine.dispose()


# 初始化数据源工厂
factory = DataSourceFactory(config)

# 获取并使用会话
session_future = factory.get_session(db_future)
session_stock = factory.get_session(db_stock)
