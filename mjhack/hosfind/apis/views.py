from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
import json
import requests
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def category_search_using_symptoms(request,symptoms_query,age,gender):

    symptoms_query=''
    age=''
    gender=''
    if request.method =='POST':
        symptoms_query=request.POST.symptoms_query
        age=request.POST.age
        gender=request.POST.gender


    my_token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFiaW9uZTEyMDZAZ21haWwuY29tIiwicm9sZSI6IlVzZXIiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9zaWQiOiIxODUxIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy92ZXJzaW9uIjoiMTA4IiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9saW1pdCI6IjEwMCIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbWVtYmVyc2hpcCI6IkJhc2ljIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9sYW5ndWFnZSI6ImVuLWdiIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9leHBpcmF0aW9uIjoiMjA5OS0xMi0zMSIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbWVtYmVyc2hpcHN0YXJ0IjoiMjAxOS0wMS0yNyIsImlzcyI6Imh0dHBzOi8vYXV0aHNlcnZpY2UucHJpYWlkLmNoIiwiYXVkIjoiaHR0cHM6Ly9oZWFsdGhzZXJ2aWNlLnByaWFpZC5jaCIsImV4cCI6MTU0ODU3NTkyNCwibmJmIjoxNTQ4NTY4NzI0fQ.a__vds2c_8rKA_J0aIy4V7q6dJ1hb0KvIc5WT2P1w6o'

    url='https://healthservice.priaid.ch/symptoms?token='+my_token+'&language=en-gb'

    symptoms_response=requests.get(url)
    symptoms_response=symptoms_response.json()

    symptoms_list=[]
    for r in symptoms_response:
        symptoms_list.append(r['Name'])

    close_results=process.extract(symptoms_query,symptoms_list)

    symptom_ids=[]
    for i in range(3):
        symptom_ids.append(symptoms_list.index(close_results[i]))

    ret_dict=find_category(symptom_ids,age,gender)

    return HttpResponse(json.dumps(ret_dict), content_type="application/json")
    pass

def find_category(symptom_ids,p_age,p_gender):

    my_token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFiaW9uZTEyMDZAZ21haWwuY29tIiwicm9sZSI6IlVzZXIiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9zaWQiOiIxODUxIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy92ZXJzaW9uIjoiMTA4IiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9saW1pdCI6IjEwMCIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbWVtYmVyc2hpcCI6IkJhc2ljIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9sYW5ndWFnZSI6ImVuLWdiIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9leHBpcmF0aW9uIjoiMjA5OS0xMi0zMSIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbWVtYmVyc2hpcHN0YXJ0IjoiMjAxOS0wMS0yNyIsImlzcyI6Imh0dHBzOi8vYXV0aHNlcnZpY2UucHJpYWlkLmNoIiwiYXVkIjoiaHR0cHM6Ly9oZWFsdGhzZXJ2aWNlLnByaWFpZC5jaCIsImV4cCI6MTU0ODU4NTc5NSwibmJmIjoxNTQ4NTc4NTk1fQ.BIlGOnjF9Em5OlVlcAGk21leoZ8Y6OLJATdEnkWMDe0'

    url='https://healthservice.priaid.ch/diagnosis?token='+my_token+'&language=en-gb&symptoms='+symptom_ids+'&gender='+p_gender+'&year_of_birth'+(2019-p_age)

    diagnosis_response=requests.get(url)
    diagnosis_response=diagnosis_response.json()

    diagnosis_response_len=len(diagnosis_response)

    diagnosis_dict={'problem':[],'accuracy':[],'specialisation':[]}

    diagnosis_list=[]

    for i in range(diagnosis_response_len):

        specialisation_len=len(diagnosis_response[i]['Specialisation'])

        diagnosis_dict['problem'].append(diagnosis_response[i]['Issue']['Name'])

        diagnosis_dict['accuracy'].append(diagnosis_response[i]['Issue']['Accuracy'])

        diagnosis_dict['specialisation'].append(diagnosis_response[i]['Specialisation'][specialisation_len-1]['Name'])

    return diagnosis_dict
    pass



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
