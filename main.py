from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle
import os
import flask_monitoringdashboard as dashboard

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)
@app.route('/' , methods =['GET'])
@cross_origin()
def homepage():
    return render_template('index.html')

@app.route('/predict' , methods =['GET','POST'])
@cross_origin()
def Prediction():
    if request.method == 'POST':
        try:
            age = float(request.form['age'])
            Gender = float(request.form['Gender'])
            on_thyroxine = float(request.form['on_thyroxine'])
            on_antithyroid_medication = float(request.form['on_antithyroid_medication'])
            I131_treatment = float(request.form['I131_treatment'])
            query_hypothyroid = float(request.form['query_hypothyroid'])
            goitre = float(request.form['goitre'])
            psych = float(request.form['psych'])
            TSH_measured = float(request.form['TSH_measured'])
            TSH = float(request.form['TSH'])
            T3_measured = float(request.form['T3_measured'])
            T3 = float(request.form['T3'])
            FTI = float(request.form['FTI'])

            if Gender == 0:
                male = 1.0
                female =0
            elif Gender == 1:
                male = 0
                female =1.0

            filename = 'Internshipmodel.pickle'
            load_model = pickle.load(open(filename, 'rb'))
            standfile = 'sd_sc_Intern'
            Stand = pickle.load(open(standfile,'rb'))
            prediction = load_model.predict(Stand.transform([[age,on_thyroxine,on_antithyroid_medication,I131_treatment,query_hypothyroid,goitre
                                                                 ,psych,TSH_measured,TSH,T3_measured,T3,FTI,male,female]]))
            if int(prediction) == 0:
                Pred = 'You are fine the result is negative'
            elif int(prediction) == 1:
                Pred = 'You have compensated hypothyroid'
            elif int(prediction) ==2:
                Pred = 'You have primary hypothyroid'
            elif int(prediction) == 3:
                Pred = 'Your have secondary hypothyroid'
            return render_template('results.html', prediction=Pred)
        except Exception as e:
            print('the exception msg is : ' , e)
            return 'Something went wrong'
    else:
        return render_template('index.html')


port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    host = '0.0.0.0'
    # port = 5000
    httpd = simple_server.make_server(host, port, app)
    # print("Serving on %s %d" % (host, port))
    httpd.serve_forever()e)