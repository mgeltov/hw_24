import os
from flask import Flask, request, jsonify, abort, Response
from marshmallow import ValidationError
from typing import Iterable, Union, List, Optional

from models import ReqSchema
from functions import read_file, filter_query, map_query, unique_query, sort_query, limit_query, create_query, regex_query

app: Flask = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query", methods=['POST'])
def perform_query() -> Union[Response, tuple[Response, int]]:
    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    data = request.json
    try:
        valid_data = ReqSchema().load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # проверить, что файл file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    if os.path.exists(os.path.join(DATA_DIR, valid_data["file_name"])) is False:
        abort(400, f'File {valid_data["file_name"]} not found in the directory {DATA_DIR}')

    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    res_1 = create_query(filename=os.path.join(DATA_DIR, valid_data["file_name"]),
                         cmd=valid_data["cmd1"], value=valid_data["value1"], data=None)
    res_2 = create_query(filename=os.path.join(DATA_DIR, valid_data["file_name"]),
                         cmd=valid_data["cmd2"], value=valid_data["value2"], data=res_1)

    # вернуть пользователю сформированный результат
    return jsonify(list(res_2))

app.run()
