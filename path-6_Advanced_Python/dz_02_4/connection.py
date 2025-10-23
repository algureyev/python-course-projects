from sqlalchemy import create_engine

class Connection:
    def __init__(self, sql_type, user, password, server, port=None, **args) -> None:
        self.user = user
        self.password = password
        self.server = server
        self.port = port
        self.sql_type = sql_type
        self.args = args
        self._engine = None

    @property
    def connection_string(self):
        if self.sql_type == "MSSQL":
            return f"mssql+pymssql://{self.user}:{self.password}@{self.server}/{self.args.get('db_name', '')}"
        elif self.sql_type == "PostgressQL":
            port_str = f":{self.port}" if self.port else ""
            return f"postgresql://{self.user}:{self.password}@{self.server}{port_str}/{self.args.get('db_name', '')}"
        else:
            raise Exception("Соединение не поддерживается")

    @property
    def engine(self):
        if self._engine is None:
            self._engine = create_engine(self.connection_string)
        return self._engine