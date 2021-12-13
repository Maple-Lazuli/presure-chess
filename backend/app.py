from flask import Flask, request, Response
from flask_cors import CORS
import chess_funcs as chess
import tensorflow as tf
import numpy as np
import json

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True
model_name = './backend/chess_10000_10_redux'
model = tf.keras.models.load_model(model_name + '.h5')


@app.route("/", methods=["GET"])
def root():
    # get positions from the web app
    message = request.args.get('positions')
    message = message.split(',')
    for i in range(0, len(message)):
        message[i] = int(message[i])
    positions = np.array(message).reshape((8, 8))
    base, val = chess.board_eval(positions)
    white_move, white_distro, white_move_ml, white_distro_ml = chess.recommend_white(
        chess.create_board_from_positions(positions), model)
    black_move, black_distro, black_move_ml, black_distro_ml = chess.recommend_black(
        chess.create_board_from_positions(positions), model)

    return_json = {
        "base_relative": chess.calculate_relative_color_percentiles(base).reshape((1, 64)).tolist(),
        "base_individual": chess.calculate_individual_color_percentiles(base).reshape((1, 64)).tolist(),
        # val_relative is normalized to color the cells
        "val_relative": chess.calculate_relative_color_percentiles(val).reshape((1, 64)).tolist(),
        "val_individual": chess.calculate_individual_color_percentiles(val).reshape((1, 64)).tolist(),
        "base": base.reshape((1, 64)).tolist(),
        "val": val.reshape((1, 64)).tolist(),
        'white_move': white_move,
        'white_distro': white_distro,
        'white_move_ml': white_move_ml,
        'white_distro_ml': white_distro_ml,
        'black_move': black_move,
        'black_distro': black_distro,
        'black_move_ml': black_move_ml,
        'black_distro_ml': black_distro_ml,
    }
    return Response(json.dumps(return_json), status=200, mimetype='application/json')


def main():
    app.run(host='0.0.0.0', port=3001)


if __name__ == "__main__":
    main()
