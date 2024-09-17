from flask import Flask,render_template,request
import pickle
import sklearn
import os

app = Flask(__name__)

# def prediction(lst):
#     filename = 'model/LungCancerPredictorM.pickle'
#     with open(filename, 'rb') as file:
#         model = pickle.load(file)
#     pred_value = model.predict([lst])
#     return pred_value

def prediction(lst):
    filename = os.path.join(os.path.dirname(__file__), 'model', 'LungCancerPredictorMF.pickle')
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst])
    return pred_value

@app.route('/', methods=['POST', 'GET'])
def index():
    
    pred_value = 2
    if request.method == 'POST':
        age = request.form['age']
        smoking = request.form['smoking']
        fatigue = request.form['fatigue']
        alcohol = request.form['alcohol']
        cough = request.form['cough']
        male = request.form.getlist('Male')
        female = request.form.getlist('Female')

         # Validate the age field
        if not age.isdigit():
            error_message = "Please enter a valid numeric age."
            return render_template("index.html", pred_value=pred_value, error_message=error_message)
            
        
        feature_list = []

        feature_list.append(int(age))
        feature_list.append(len(male))
        feature_list.append(len(female))

        smoking_list = ['YES', 'NO']
        fatigue_list = ['YES', 'NO']
        alcohol_list = ['YES', 'NO']
        cough_list = ['YES', 'NO']

        def map_to_int(lst, value):
            # Map 'YES' to 1 and 'NO' to 0
            return 1 if value == 'YES' else 0

        # Map 'YES' and 'NO' values to 1 and 0 in the feature_list
        feature_list.append(map_to_int(smoking_list, smoking))
        feature_list.append(map_to_int(fatigue_list, fatigue))
        feature_list.append(map_to_int(alcohol_list, alcohol))
        feature_list.append(map_to_int(cough_list, cough))
        
        pred_value = prediction(feature_list)
        
    return render_template("index.html", pred_value=pred_value)

@app.route('/home')  # Add a new route for the home page
def home():
    return render_template('index.html')


if __name__ == '__main__':
    print("scikit-learn version:", sklearn.__version__)
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
