from flask import Flask, render_template, request
from flask_cors import cross_origin
import pickle

application = Flask(__name__)
app = application
@app.route('/',methods=['GET'])
@cross_origin()
def home_page():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            wheelbase = float(request.form['wheelbase'])
            carwidth = float(request.form['carwidth'])
            enginesize = int(request.form['enginesize'])
            boreratio = float(request.form['boreratio'])
            horsepower = int(request.form['horsepower'])
            carname = request.form['carname']
            count = {'toyota': 31,'nissan': 17,'mazda': 15,'honda': 13,'subaru': 12,'volvo': 11,
                     'dodge': 9,'bmw': 8,'audi': 7,'saab': 6,'isuzu': 4,'jaguar': 3,'maxda': 2,'toyouta': 1}
            key_list = list(count.keys())
            val_list = list(count.values())
            val = key_list.index(carname)
            Carname = val_list[val]
            fueltype = request.form['fueltype']
            if (fueltype == 'diesel'):
                fueltype_diesel = 1
            else :
                fueltype_diesel = 0

            aspiration = request.form['aspiration']
            if (aspiration == 'turbo') :
                aspiration_turbo = 1
            else :
                aspiration_turbo = 0

            doornumber = request.form['doornumber']
            if (doornumber == 'two') :
                doornumber_two = 1
            else :
                doornumber_two = 0

            drivewheel = request.form['drivewheel']
            if (drivewheel == 'fwd'):
                drivewheel_fwd = 1
                drivewheel_rwd = 0
            elif (drivewheel == 'rwd'):
                drivewheel_fwd = 0
                drivewheel_rwd = 1
            else :
                drivewheel_fwd = 0
                drivewheel_rwd = 0

            enginelocation = request.form['enginelocation']
            if(enginelocation == 'rear'):
                enginelocation_rear = 1
            else :
                enginelocation_rear = 0


            filename = 'modelForPrediction.sav'
            model = pickle.load(open(filename, 'rb'))
            scalefile = 'sandardScalar.sav'
            scalar = pickle.load(open(scalefile, 'rb'))
            scaled_data = scalar.transform([[wheelbase,carwidth,enginesize,boreratio,horsepower,Carname,fueltype_diesel,aspiration_turbo,doornumber_two,drivewheel_fwd,drivewheel_rwd,enginelocation_rear]])
            prediction = model.predict(scaled_data)
            print('prediction value is ', prediction)
            # showing the prediction results in a UI
            return render_template('results.html', prediction=round(prediction[0],3))

        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)



