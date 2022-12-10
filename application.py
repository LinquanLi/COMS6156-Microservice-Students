import json
import logging.handlers

from flask import Flask, request, Response, make_response
from flask_cors import CORS

from columbia_student_resource import ColumbiaStudentResource


application = Flask(__name__)
CORS(application)

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handler 
LOG_FILE = '/tmp/sample-app.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1048576, backupCount=5)
handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add Formatter to Handler
handler.setFormatter(formatter)

# add Handler to Logger
logger.addHandler(handler)


@application.get("/")
def hello():
    return "<h1>Hello</h1>"


@application.get("/students")
def get_students_by_template():
    params = request.args
    students_per_page = int(params["limit"]) if "limit" in params else 10
    offset = students_per_page * (int(params["page"]) - 1) if "page" in params else 0

    result = ColumbiaStudentResource().get_by_template(students_per_page, offset)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


@application.get("/students/<uni>")
def get_student_by_uni(uni):
    result = ColumbiaStudentResource().get_by_key(uni)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


@application.delete("/students/<uni>")
def delete_student(uni):
    try:
        ColumbiaStudentResource().delete_by_key(uni)
        response = make_response("Delete Success!", 200)
    except:
        response = make_response("Delete Fail!", 400)
    return response


@application.put("/students/<uni>")
def put_student(uni):
    body = request.json
    ColumbiaStudentResource().update_by_key(uni, body)
    return get_student_by_uni(uni)


@application.post("/students")
def post_student():
    body = request.json
    try:
        ColumbiaStudentResource().insert_by_key(body)
    except:
        return Response("Insert Failure", status=404, content_type="text/plain")
    return get_student_by_uni(body["uni"])


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5011)
