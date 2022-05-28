from flask import Flask
from werkzeug.datastructures import FileStorage
import tempfile
from flask_restful import Resource, Api, reqparse
from tensorflow import keras
from keras.preprocessing import image
import tensorflow as tf
import keras

import numpy as np

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('file',
                    type=FileStorage,
                    location='files',
                    required=True,
                    help='provide a file')
def predict(fname):
    model = keras.models.load_model('model/model.h5')

    input_shape = (64, 64, 3)
    img = keras.utils.load_img(fname,  grayscale=False, target_size=(64, 64))
    x = keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x /= 255

    custom = model.predict(x)
    print(custom[0])

    covidPercentage = custom[0][0] * 100

    def getResult(covPerc):
        if (covPerc >= 90):
            return 'High Covid'
        elif (covPerc >= 50):
            return 'Low Covid'
        else:
            return 'No Covid'
    return getResult(covidPercentage)


class Image(Resource):

    def post(self):
        args = parser.parse_args()
        the_file = args['file']
        ofile, ofname = tempfile.mkstemp()
        the_file.save(ofname)
        print(the_file, ofname)
        output = predict(ofname)
        # results = predict(ofname)[0]
        # output = {'top_categories': []}
        # for _, categ, score in results:
        #     output['top_categories'].append((categ, float(score)))

        return output


api.add_resource(Image, '/image')

if __name__ == '__main__':
    app.run(debug=True)