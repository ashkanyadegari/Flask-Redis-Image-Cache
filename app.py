from io import BytesIO
from flask import Flask, send_file, request
import requests
import redis

app = Flask(__name__)
redis_server = redis.StrictRedis(host='localhost', port=6379)

@app.route('/')
def image():
    url = request.args.get('link')
    cached = redis_server.get(url)
    if cached:
        buffer_image = BytesIO(cached)
        buffer_image.seek(0)
    else:
        r = requests.get(url)
        buffer_image = BytesIO(r.content)
        buffer_image.seek(0)
        redis_server.setex(url, (60*60*24*7),
                           buffer_image.getvalue())
    return send_file(buffer_image, mimetype='image/jpeg')


