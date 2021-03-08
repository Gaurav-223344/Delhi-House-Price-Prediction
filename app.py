from flask import Flask, render_template, request
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

model = pickle.load(open('model_XGB.pkl', 'rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        Area=int(request.form['area'])
        BHK=int(request.form['bhk'])
        Bathroom_median=int(request.form['bathroom'])
        Parking_median=int(request.form['parking'])
        Per_Sqft_median=int(request.form['Per_Sqft'])
        status = request.form['property']
        if (status == 'Ready_to_move'):
            Status_Ready_to_move = 1
        else:
            Status_Ready_to_move = 0
            
        Transaction = request.form['transaction']
        if (Transaction == 'Resale'):
            Transaction_Resale = 1
        else:
            Transaction_Resale = 0
            
        Type = request.form['type']
        if (Type == 'Builder_Floor'):
            Type_freq_Builder_Floor = 1
        else:
            Type_freq_Builder_Floor = 0
            
        Furnishing = request.form['furnishing']
        if (Furnishing == 'Unfurnished'):
            Furnishing_freq_Semi_Furnished = 0
            Furnishing_freq_Unfurnished = 1
        elif (Furnishing == 'Semi-Furnished'):
            
            Furnishing_freq_Semi_Furnished = 1
            Furnishing_freq_Unfurnished = 0
        else:
            Furnishing_freq_Semi_Furnished = 0
            Furnishing_freq_Unfurnished = 0
        
        Locality_encoder = request.form['locality']
        dictionary =    {'Alaknanda': 18007143.0,
                         'Budh Vihar': 3825000.0,
                         'Chhattarpur': 8783000.0,
                         'Chittaranjan Park': 26335714.0,
                         'Commonwealth Games Village': 45646667.0,
                         'Dilshad Garden': 7226000.0,
                         'Greater Kailash': 50513636.0,
                         'Hauz Khas': 73134615.0,
                         'Kalkaji': 13361290.0,
                         'Karol Bagh': 21173125.0,
                         'Kirti Nagar': 24520000.0,
                         'Lajpat Nagar': 27556778.0,
                         'Laxmi Nagar': 5966176.0,
                         'Mahavir': 4108000.0,  
                         'Malviya Nagar': 33150000.0,
                         'Mehrauli': 4736667.0,
                         'Narela': 2429667.0,
                         'New Friends Colony': 72709677.0,
                         'Okhla': 20601471.0,
                         'Paschim Vihar': 15759000.0,
                         'Patel Nagar': 35876389.0,
                         'Punjabi Bagh': 33103333.0,
                         'Rohini Sector': 8895972.0,
                         'Safdarjung': 42411765.0,
                         'Saket': 34876667.0,
                         'Sarita Vihar': 14507143.0,
                         'Shahdara': 11036267.0,
                         'Sheikh Sarai': 13056667.0,
                         'Sultanpur': 5711111.0,
                         'Uttam Nagar': 3472692.0,
                         'Vasant Kunj': 20433333.0,
                         'Vasundhara': 11105000.0,
                         'other': 12942544.0}
        
 #       Locality_encoder = Locality.map(dictionary)
        
        data = pd.DataFrame([[Area, BHK, Bathroom_median, Parking_median, Per_Sqft_median, Status_Ready_to_move, Transaction_Resale, Type_freq_Builder_Floor, Furnishing_freq_Semi_Furnished, Furnishing_freq_Unfurnished, Locality_encoder]],
                            columns=['Area', 'BHK', 'Bathroom_median', 'Parking_median', 'Per_Sqft_median', 'Status_Ready_to_move', 'Transaction_Resale', 'Type_freq_Builder_Floor', 'Furnishing_freq_Semi-Furnished', 'Furnishing_freq_Unfurnished', 'Locality_encoder'])
        
        data['Locality_encoder'] = data['Locality_encoder'].map(dictionary)
        scaler = StandardScaler()
        
        # This dataset used previously for scaling to train model
        df = pd.read_csv("dataset.csv",usecols=['Area', 'BHK', 'Bathroom_median', 'Parking_median',
       'Per_Sqft_median', 'Status_Ready_to_move', 'Transaction_Resale',
       'Type_freq_Builder_Floor', 'Furnishing_freq_Semi-Furnished',
       'Furnishing_freq_Unfurnished', 'Locality_encoder'])
        
        
        
        scaler.fit(df)
        data_new = scaler.transform(data)
        data_new = pd.DataFrame(data_new,columns=data.columns)
        
        prediction=model.predict(data_new)
        output=prediction[0]
        if output<=0:
            return render_template('index.html',prediction_texts="Please enter correct information")
        else:
            return render_template('index.html',prediction_texts=f"Price = {output}")
    
        
        
    else:
        return render_template('index.html')

    
    
if __name__=="__main__":
    app.run(debug=True)  
#if __name__=="__main__":
#    app.run(host='0.0.0.0',port=8080)
        
