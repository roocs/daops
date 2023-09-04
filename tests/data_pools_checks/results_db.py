import os
from itertools import chain
import csv
import gzip
import sqlite3


class ResultsDB:    
    
    def __init__(self,
                 columns,
                 csvgz_file='tests.csv.gz', sqlite_file='tests_tmp.db',
                 sql_table_name = 'test_results',
                 sql_primary_key='id',
                 merge_every=100):
        self.columns = columns[:]
        self._csvgz_file = csvgz_file
        self._sqlite_file = sqlite_file
        self._conn = None
        self._cur = None
        self._sql_table_name = sql_table_name
        self._sql_primary_key = sql_primary_key
        self._merge_every = merge_every
        self._num_tmp_rows = 0
        
    def read_csvgz(self, src=None):
        "read .csv.gz, yield a sequence of rows (each is a list)"
        if src is None:
            src = self._csvgz_file
        if not os.path.exists(src):
            return []
        with gzip.open(src, 'rt') as f:
            reader = csv.reader(f)
            headers = next(reader)
            if headers != self.columns:
                raise Exception('CSV file does not have the expected columns')
            for row in reader:
                yield row


    def _read_as_dicts(self, reader, remove_blank=True, **kwargs):
        if remove_blank:
            cond = lambda t: t[1]
        else:
            cond = lambda t: True
            
        return (dict(t for t in zip(self.columns, row) if cond(t))
                for row in reader(**kwargs))
                        
    def read_csvgz_as_dicts(self, **kwargs):
        return self._read_as_dicts(self.read_csvgz, **kwargs)
        
    def read_sqlite_as_dicts(self, **kwargs):
        return self._read_as_dicts(self.get_sqlite_rows, **kwargs)
                
    def write_csvgz(self, rows, dest=None):
        "write .csv.gz, input is a sequence of rows"
        if dest is None:
            dest = self._csvgz_file
        tmpname = dest.replace('.gz', '.tmp.gz')
        try:
            with gzip.open(tmpname, 'wt') as fout:
                writer = csv.writer(fout)
                writer.writerow(self.columns)
                for row in rows:
                    writer.writerow(row)
            os.rename(tmpname, dest)
        finally:
            if os.path.exists(tmpname):
                os.remove(tmpname)

    def add_row(self, **row_dict):
        "add a single row - goes into the sqlite file"
        cur, conn = self._get_cur_conn()
        sql_keys = ','.join(row_dict.keys())
        sql_vals = ','.join((f"'{str(val)}'" for val in row_dict.values()))
        sql = f'insert into {self._sql_table_name} ({sql_keys}) values ({sql_vals})'
        cur.execute(sql)
        conn.commit()
        self._num_tmp_rows += 1
        if self._num_tmp_rows == self._merge_every:
            self.merge_and_tidy()            

    def _init_sqlite(self):
        sql_columns = ','.join([f'{self._sql_primary_key} integer PRIMARY KEY'] +
                               [f'{col} text' for col in self.columns])
        sql = f'CREATE TABLE IF NOT EXISTS {self._sql_table_name}({sql_columns})'
        conn = sqlite3.connect(self._sqlite_file)
        cur = conn.cursor()
        cur.execute(sql)
        self._conn = conn
        self._cur = cur

    def _get_cur_conn(self):
        if self._cur is None or self._conn is None:
            self._init_sqlite()
        return self._cur, self._conn

    def get_sqlite_rows(self, include_primary_key=False):
        cur, conn = self._get_cur_conn()
        cur.execute(f'SELECT * from {self._sql_table_name}')
        for row in cur:
            if include_primary_key:
                yield row
            else:
                yield row[1:]

    def _destroy_sqlite(self):
        if os.path.exists(self._sqlite_file):
            os.remove(self._sqlite_file)
        self._conn = self._cur = None
        self._num_tmp_rows = 0
                
    def merge_and_tidy(self):
        csv_rows = self.read_csvgz()
        new_rows = self.get_sqlite_rows()
        self.write_csvgz(chain(csv_rows, new_rows))
        self._destroy_sqlite()

    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.merge_and_tidy()

        
if __name__ == "__main__":
    import random

    def dump_db():
        print("=====================")
        os.system('zcat tests.csv.gz')
        print()
        os.system('echo .dump | sqlite3 -header -readonly tests_tmp.db')
        print("=====================")
    
    columns = ['test_location', 'test_time', 'collection', 'area',
               'level', 'time', 'success', 'message']

    with ResultsDB(columns, merge_every=7) as rdb:
        for _ in range(13):
            rdb.add_row(collection='foo', success='False')
            rdb.add_row(collection=str(random.random()), time='blah', success='True')
