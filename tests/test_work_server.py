import pytest
import requests_mock
import fakeredis
from work_server import *
import work_server
import mock
from redis_manager import RedisManager

base_url = 'https://10.76.100.164:420/'
#JUST BASIC BAD KEY, MUST CHANGE THIS
test_key = os.environ['WORK_SERVER_KEY']

@pytest.fixture
def mock_req():
    with requests_mock.Mocker() as m:
        yield m

@pytest.fixture
def client():
    work_server.app.config['TESTING'] = True
    client = work_server.app.test_client()
    yield client


def make_empty_database():
    r = fakeredis.FakeRedis()
    r.flushall()
    return r

def make_databse():
    r = fakeredis.FakeRedis()
    r.flushall()
    r.set('1234567891011121', ['www.url.com', "www.wwww"])
    return r


def test_16_character_id():
    assert len(generate_random_id()) == 16

#IGNORED - MOCK THE REDIS
def ignore_test_post_request_successful_connection(client):
    result = client.post('/add_work', data=dict(job_id='1234567891011121', job_units=['www.url.com', "www.wwww"], key=test_key), follow_redirects=True)
    assert result.status_code == 200

#DOESNT PASS BECAUSE NOT MOCKED REDIS
def test_get_request_successful_connection(client):
    result = client.get('/get_data', query_string={'job_id': '1234567891011121'})
    assert result.status_code == 200

def test_invalid_key(client):
    with pytest.raises(PostException):
        client.post('/add_work', data=dict(job_id='1234567891011121', job_units=['www.url.com'], key="FEDCBA"), follow_redirects=True)

def test_incorrect_id(client):
    with pytest.raises(PostException):
        client.post('/add_work', data=dict(job_id='123', job_units=['www.url.com'], key=test_key),
                    follow_redirects=True)

def test_job_units_not_list(client):
    with pytest.raises(PostException):
        client.post('/add_work', data=dict(job_id='1234567891011121', job_units='Not a list', key="FEDCBA"),
                follow_redirects=True)

def test_missing_paramst(client):
    with pytest.raises(PostException):
        client.post('/add_work', data=dict(job_units='Not a list', key="FEDCBA"),
                follow_redirects=True)

def test_new_empty_database():
    r = make_empty_database()
    assert 0 == len(r.keys())

def test_database_has_object():
    r = make_databse()
    assert 1 == len(r.keys())

def test_add_item_to_database():
    r = make_empty_database()
    assert 0 == len(r.keys())
    r.set('1234567891011121', ['www.url.com', "www.wwww"])
    assert 1 == len(r.keys())
    r.set('1234567891011421', ['www.url.com', "www.vvv"])
    assert 2 == len(r.keys())


def test_get_bad_id(client):
    with pytest.raises(GetException):
        client.get('/get_data', data=dict(job_id='123'), follow_redirects=True)







