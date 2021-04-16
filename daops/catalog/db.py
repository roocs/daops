import pandas as pd
import sqlalchemy
from pywps.dblog import get_session
from sqlalchemy.types import DateTime
from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Text

from .base import Catalog
from .intake import IntakeCatalog
from .util import MAX_DATETIME
from .util import MIN_DATETIME
from .util import parse_time


class DBCatalog(Catalog):
    def __init__(self, project, url=None):
        super(DBCatalog, self).__init__(project)
        self.table_name = f"rook_catalog_{self.project}".replace("-", "_")
        self.intake_catalog = IntakeCatalog(project, url)

    def exists(self):
        session = get_session()
        engine = get_session().get_bind()
        try:
            ins = sqlalchemy.inspect(engine)
            exists_ = ins.dialect.has_table(engine.connect(), self.table_name)
        except Exception:
            exists_ = False
        finally:
            session.close()
        return exists_

    def update(self):
        if not self.exists():
            self.to_db()

    def to_db(self):
        df = self.intake_catalog.load()
        # workaround for NaN values when no time axis (fx datasets)
        sdf = df.fillna({"start_time": MIN_DATETIME, "end_time": MAX_DATETIME})
        sdf = sdf.set_index("ds_id")
        # db connection
        session = get_session()
        try:
            sdf.to_sql(
                self.table_name,
                session.connection(),
                if_exists="replace",
                index=True,
                chunksize=500,
            )
            session.commit()
        finally:
            session.close()

    def _query(self, collection, time=None):
        """
        https://stackoverflow.com/questions/8603088/sqlalchemy-in-clause
        """
        self.update()
        start, end = parse_time(time)

        session = get_session()
        try:
            if len(collection) > 1:
                query_ = (
                    f"SELECT * FROM {self.table_name} WHERE ds_id IN {tuple(collection)} "
                    f"and end_time>='{start}' and start_time<='{end}'"
                )

            else:
                query_ = (
                    f"SELECT * FROM {self.table_name} WHERE ds_id='{collection[0]}' "
                    f"and end_time>='{start}' and start_time<='{end}'"
                )
            result = session.execute(query_).fetchall()

        except Exception:
            result = []
        finally:
            session.close()
        records = {}
        for row in result:
            if row.ds_id not in records:
                records[row.ds_id] = []
            records[row.ds_id].append(row.path)
        return records
