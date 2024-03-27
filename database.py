from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from databases import Database
from sqlalchemy.pool import NullPool
from models import Base

DATABASE_URL = "sqlite:///.data.db"

# A classe 'Database' serve para gerenciar a conexão com o banco de dados
db = Database(DATABASE_URL)

# o objeto 'Engine' é responsável por estabelecer e gerenciar uma conexão com o banco de dadose e fornece uma interface para executar consultas SQL e gerenciar transações no banco de dados

# "check_same_thread": False
    # threads = contextos
    # No SQLite, por padrão, o acesso ao banco de dados é permitido apenas no mesmo thread em que a conexão foi criada. No entanto, ao definir check_same_thread como False, você está permitindo que a conexão seja usada em threads diferentes do que foi criada.

# 'poolclass=NullPool'
    # Desativa completamente o pooling de conexões (poolclass=NullPool). Pooling de conexões é um cache de conexões de banco de dados que são compartilhadas e reutilizadas. Essa configuração é específica para o SQLite

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=NullPool)

# Objeto 'MetaData()' é usado para armazenar info's sobre as tabelas e outros elementos do banco de dados. ex: Nome de tabelas, indices, info sobre foreign key's etc

metadata = MetaData()

# Agora utilizados o 'create_all' do objeto 'metadata' para criar todas as tabelas definidas no nosso codigo. O 'bind=engine' especifica que as tabelas devem ser criadas usando a conexão do 'Engine' que criamos
Base.metadata.create_all(bind = engine)

# cria sessões que são responsáveis pela interação com o banco de dados
# SessionLocal está configurando uma fábrica de sessões que:
    #  - Desativa o modo de autocommit automático.
    # - Desativa o modo de autoflush automático.
    # - Vincula a sessão a um mecanismo de banco de dados específico (engine).

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def get_db():
    db = SessionLocal()
    
    try:
        yield db # yield retorna um objeto que não ocupa um espaço grande na memória, sendo utilizado quando temos bases de dados muito grandes
    finally:
        db.close