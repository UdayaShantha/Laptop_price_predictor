#This is like a backend file for the web application


from flask import Flask,render_template,request
import pickle
import numpy as np

#setup application
app = Flask(__name__)


#create web pages
@app.route('/',methods=['POST','GET'])  #create url address


def home():
    pred=0.0  #If not submit the button or click the button

    #Get form's input values into variables
    if request.method == 'POST':
        ram = request.form['ram']
        inches= request.form['inches']
        weight = request.form['weight']
        brand = request.form['brand']
        lapType=request.form['usage']
        resolution=request.form['resolution']
        os=request.form['os']
        cpuType=request.form['cpu'] 
        cpuSeries=request.form['cpu_series']
        gpu=request.form['gpu']
        touchscreen=request.form.getlist('touchscreen')
        ips=request.form.getlist('ips')

        #craete the list to add the form's POST values 
        feature_list=[]
        
        feature_list.append(float(inches))
        feature_list.append(int(ram))
        feature_list.append(float(weight))
       

        #Create the feature lists which relevant to model's x's attributes 
        company_list=['Acer', 'Apple', 'Asus', 'Chuwi', 'Dell','Fujitsu', 'Google', 'HP', 'Huawei', 'LG', 'Lenovo', 'MSI', 'Mediacom','Microsoft', 'Razer', 'Samsung', 'Toshiba', 'Vero', 'Xiaomi']
        typename_list=['2 in 1 Convertible', 'Gaming', 'Netbook', 'Notebook', 'Ultrabook','Workstation']               
        opsys_list=['Linux', 'MacOS', 'Other/No OS', 'Windows'] 
        cpu_list=['CPU_AMD', 'CPU_Intel', 'CPU_Samsung']
        cpu_series_list=['AMD_series_processor', 'Intel Core i3', 'Intel Core i5','Intel Core i7', 'Other_series_processor'] 
        gpu_list=['GPU_AMD', 'GPU_ARM','GPU_Intel', 'GPU_Nvidia']
        resolution_list=['1366*768', '1440*900', '1600*900','1920*1080', '1920*1200', '2160*1440', '2256*1504', '2304*1440','2400*1600', '2560*1440', '2560*1600', '2736*1824', '2880*1800','3200*1800', '3840*2160'] 

        #create function for traversing the list and add values as 0 or 1
        def traverse_list(list_name,feature):
            for i in list_name:
                if i==feature:
                    feature_list.append(1)
                else:
                    feature_list.append(0)

        #Traverse list with respect to the model's x's attributes orderly
        traverse_list(company_list,brand)
        traverse_list(typename_list,lapType)


        feature_list.append(len(touchscreen))
        feature_list.append(len(ips))

        traverse_list(resolution_list,resolution)
        traverse_list(cpu_list,cpuType)
        traverse_list(cpu_series_list,cpuSeries)
        traverse_list(gpu_list,gpu)
        traverse_list(opsys_list,os)


        
        
        #create function for input a 2D array as the input for the saved model and get the prediction value for model and return it
        def prediction(feature_list):
            file='model/predictor_model.pickle'
            with open(file,'rb') as f:
                model=pickle.load(f)
            pred_value=model.predict([feature_list])
            return pred_value   

        pred=prediction(feature_list)*280.36  #get the prediction value from the model and multiply by 306.36 to get the price in dollars
        pred=np.round(pred[0])  #round the value to the nearest integer


    #return the webpage for display and submit pred value as the pred variable then pred can access inside the index.html page also
    return render_template('index.html',pred=pred)  #return the index.html file

if __name__ == '__main__':
    app.run(debug=True)
