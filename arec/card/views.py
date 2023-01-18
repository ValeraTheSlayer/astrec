from django.shortcuts import render


# rendering main page
def main_page(request):
    return render(request, 'html/index.html')
