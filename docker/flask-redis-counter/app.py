from flask import Flask
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379)

@app.route('/')
def hello_world():
    return 'Welcome to my Flask Redis app!😊'

@app.route('/count')
def count():
    visits = r.incr('visits')
    return f'This page has been visited {visits} times'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)