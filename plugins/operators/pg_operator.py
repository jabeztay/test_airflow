from typing import Iterable
from typing import Mapping
from typing import Optional
from typing import Union

from airflow.models import BaseOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


class PostgresToPostgresOperator(BaseOperator):
    """
    Executes sql code in a specific Postgres database

    :param sql: the sql code to be executed. (templated)
    :type sql: Can receive a str representing a sql statement,
        a list of str (sql statements), or reference to a template file.
        Template reference are recognized by str ending in '.sql'
    :param postgres_conn_id: The :ref:`postgres conn id <howto/connection:postgres>`
        reference to a specific postgres database.
    :type postgres_conn_id: str
    :param autocommit: if True, each command is automatically committed.
        (default value: False)
    :type autocommit: bool
    :param parameters: (optional) the parameters to render the SQL query with.
    :type parameters: dict or iterable
    :param database: name of database which overwrite defined one in connection
    :type database: str
    """

    template_fields = ("sql",)
    template_fields_renderers = {"sql": "sql"}
    template_ext = (".sql",)
    ui_color = "#ededed"

    def __init__(
        self,
        *,
        sql: str,
        source_postgres_conn_id: str = "postgres_default",
        target_postgres_conn_id: str = "postgres_default",
        autocommit: bool = False,
        parameters: Optional[Union[Mapping, Iterable]] = None,
        database: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.sql = sql
        self.source_postgres_conn_id = source_postgres_conn_id
        self.target_postgres_conn_id = target_postgres_conn_id
        self.autocommit = autocommit
        self.parameters = parameters
        self.database = database
        self.source_hook = None

    def execute(self, context):
        self.log.info("Extracting Data: %s", self.sql)
        self.source_hook = PostgresHook(
            postgres_conn_id=self.source_postgres_conn_id, schema=self.database
        )
        source_conn = self.source_hook.get_conn()
        source_cursor = source_conn.cursor()
        source_cursor.execute(self.sql, self.parameters)

        self.log.info("Loading data into target db")
        self.target_hook = PostgresHook(
            postgres_conn_id=self.target_postgres_conn_id, schema=self.database
        )
        self.target_hook.insert_rows("sales", source_cursor)
