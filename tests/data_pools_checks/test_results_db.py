import os
import random
import subprocess as sp

from results_db import ResultsDB


columns = ['test_location', 'test_time', 'collection', 'area',
           'level', 'time', 'success', 'message']

tst_data = [{'collection': str(random.random()),
             'time': 'blah',
             'success': 'True'}
            for _ in range(30)]


tst_data2 = [{'collection': 'foo',
              'time': 'bar'},
             {'collection': 'baz',
              'message': 'qux'},
             {'collection': 'quux',
              'message': 'corge'}]

tst_csv_data = (','.join(columns) + '\n' +
                ',,foo,,,bar,,\n,,baz,,,,,qux')

tst_sql_data = f'''PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE test_results(id integer PRIMARY KEY,{','.join(f'{col} text' for col in columns)});
INSERT INTO "test_results" VALUES(1,NULL,NULL,'quux',NULL,NULL,NULL,NULL,'corge');
COMMIT;'''

tmp_csvgz = '/tmp/test.csv.gz'
tmp_sqlite = '/tmp/test_tmp.sql'

def _purge():
    for path in (tmp_csvgz, tmp_sqlite):
        if os.path.exists(path):
            os.remove(path)

def _open_test_db(merge_every=10):
    return ResultsDB(columns,
                     csvgz_file=tmp_csvgz,
                     sqlite_file=tmp_sqlite,
                     merge_every=merge_every)


def test_write_and_read():
    _purge()
    with _open_test_db() as rdb:
        for row in tst_data:
            rdb.add_row(**row)
            
    with _open_test_db() as rdb:
        data_read = list(rdb.read_csvgz_as_dicts())

    assert tst_data == data_read


def test_write_and_read_while_open():
    
    _purge()
    merge_every = 7
    
    with _open_test_db(merge_every=merge_every) as rdb:
        for i, row in enumerate(tst_data, start=1):
            rdb.add_row(**row)

            rows_in_csv = list(rdb.read_csvgz_as_dicts())
            rows_in_sqlite = list(rdb.read_sqlite_as_dicts())

            print(f'CSV: {len(rows_in_csv)} rows, '
                  f'sqlite: {len(rows_in_sqlite)} rows, ')
            
            assert rows_in_csv + rows_in_sqlite == tst_data[:i]
            assert len(rows_in_csv) % merge_every == 0
            assert len(rows_in_sqlite) < merge_every

            
def test_manual_merge():

    _purge()
    merge_every = 7
    
    with _open_test_db(merge_every=merge_every) as rdb:
        for i, row in enumerate(tst_data, start=1):
            rdb.add_row(**row)
            rdb.merge_and_tidy()

            rows_in_csv = list(rdb.read_csvgz_as_dicts())
            rows_in_sqlite = list(rdb.read_sqlite_as_dicts())
            assert rows_in_csv == tst_data[:i]
            assert rows_in_sqlite == []


def test_dump_data():

    _purge()
    with _open_test_db(merge_every=2) as rdb:
        for row in tst_data2:
            rdb.add_row(**row)
        csvdata = sp.getoutput(f'zcat {tmp_csvgz}')
        sqldata = sp.getoutput('echo .dump '
                               f'| sqlite3 -header {tmp_sqlite}')
    assert csvdata == tst_csv_data
    assert sqldata == tst_sql_data
