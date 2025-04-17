from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd

def load_data_scchen():
    # Read data from csv file
    df_data = pd.read_csv('app_key_person/dataset/lie_cheater_data.csv',sep=',')
    global response
    response = dict(list(df_data.values))
    del df_data

# load data
load_data_scchen()

#print(response)

def home(request):
    return render(request,'app_key_person/home.html', response)


