from flask import Flask, request, Response
import redis
import json
import random
import string
import os
from redis_manager import RedisManager


app = Flask(__name__)

#JUST BASIC BAD KEY, MUST CHANGE THIS
key = os.environ['WORK_SERVER_KEY']

r = RedisManager(redis.Redis())



@app.route('/')
def default():
    return json.dumps({})


@app.route('/add_work', methods=['POST'])
def add_work():
    try:
        job_id = request.form['job_id']
        job_units = request.form['job_units']
        received_key = request.form['key']
    except:
        raise PostException

    if(received_key != key):
        raise PostException
    if(len(job_id) != 16):
        raise PostException
    if(isinstance(job_units, list)):
        raise PostException

    # EITHER MOCK CLASS OR MOCK REDIS
    r.add_data(job_id, job_units)

    return json.dumps({'Ok'})


@app.route('/get_data')
def get_data():

    if len(request.args) != 1:
        raise GetException

    job_id = request.args.get('job_id')

    if len(job_id) != 16:
        raise GetException

    urls = []
    for id in r.get_job_id_list():
        if job_id == id:
            urls = r.get_job_units(id).decode("utf-8")
            id = id.decode("utf-8")

    return 'Good'



if __name__ == '__main__':
    app.run('0.0.0.0',port=5000)


class PostException(Exception):
    print("Bad Request")

class GetException(Exception):
    print("Bad Request")

def generate_random_id():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
