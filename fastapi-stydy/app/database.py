from click import echo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


MYSQL_URL: str = 'mysql://root:12345678@127.0.0.1:3306/python-study'

engine = create_engine(MYSQL_URL, echo=True)

# 在SQLAlchemy中，CRUD都是通过会话（session）来执行的，所以我们要先创建会话，每一个SessionLocal实例都是一个数据库session
# flush 指发送数据库语句到数据库，但数据库不一定执行写入磁盘，commit指提交事物，将变更保存到数据库文件
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    db_session = SessionLocal()

    try:
        yield db_session
    except:
        db_session.rollback()
        raise

    finally:
        db_session.close()