from flask import Flask, Response, request, make_response
import json
from columbia_student_resource import ColumbiaStudentResource
from flask_cors import CORS

# Create the Flask application object.
application = Flask(__name__)

CORS(application)

student = ColumbiaStudentResource()


@application.route("/test", methods=["GET", "POST"])
def test_flask():
    # params = request.args
    # body = request.json
    print("test")
    if request.method == "POST":
        msg = {1: "test POST"}
        print(request.data)
        print(request.get_json(force=True))
        print(request.form)
        rsp = Response(json.dumps(msg), status=200, content_type="application/json")
    else:
        msg = {2: "test GET"}
        rsp = make_response(msg)
        rsp.status = 404
        rsp.headers['customHeader'] = 'This is a custom header'

    return rsp


@application.put("/students/<uni>")
def put_student(uni):
    body = request.json
    student.update_by_key(uni, body)
    return get_student_by_uni(uni)


@application.post("/students")
def post_student():
    body = request.json
    try:
        student.insert_by_key(body)
    except:
        return Response("Insert Failure", status=404, content_type="text/plain")
    return get_student_by_uni(body["uni"])


@application.delete("/students/<uni>")
def delete_student(uni):
    try:
        student.delete_by_key(uni)
        response = make_response("Delete Success!", 200)
    except:
        response = make_response("Delete Fail!", 400)
    return response


@application.get("/students")
def get_students_by_template():
    params = request.args
    students_per_page = int(params["limit"]) if "limit" in params else 10
    offset = students_per_page * (int(params["page"]) - 1) if "page" in params else 0

    result = student.get_by_template(10, offset)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


@application.route("/students/<uni>", methods=["GET"])
def get_student_by_uni(uni):
    result = student.get_by_key(uni)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5011)
