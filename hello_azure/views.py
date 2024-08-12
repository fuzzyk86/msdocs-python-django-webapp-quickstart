from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pysentimiento import create_analyzer
analyzer = create_analyzer(task="sentiment", lang="es")

def index(request):
    print('Request for index page received')
    return render(request, 'hello_azure/index.html')

@csrf_exempt
def hello(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        
        if name is None or name == '':
            print("Request for hello page received with no name or blank name -- redirecting")
            return redirect('index')
        else:
            result = analyzer.predict(name)            
            if result :
                probas = result['probas']
                
            print(f"Result after sentiment analysis: NEGATIVE {probas.NEG} POSITVE {probas.POS} NEUTRAL {probas.NEU}")
            context = {'name': name }
            return render(request, 'hello_azure/hello.html', context)
    else:
        return redirect('index')