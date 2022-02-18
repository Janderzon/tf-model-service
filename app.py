import flask
from model import Model

_model = Model()
app = flask.Flask(__name__)


@app.route("/model", methods=['GET'])
def predict():
    try:
        prediciton = _model.make_prediction()
    except ValueError as error:
        error = flask.jsonify(error=str(error))
        flask.abort(error, 400)
    return {
        'prediction': prediciton
    }


@app.route("/model/<filename>", methods=['POST'])
def upload_model(filename):
    with open(filename, 'wb') as fp:
        fp.write(flask.request.data)
    _model.set_model(filename)
    return '', 204


@app.route("/data", methods=['POST'])
def upload_data():
    _model.set_input_data(flask.request.data)
    return '', 204
