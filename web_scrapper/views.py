from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest
import bs4
import requests
from .models import data

# Create your views here.
def home(request):
    return render(request,'index.html')


def base(request):
    string = request.GET['input']
    print(string)
    string=string.replace(" ","+")
    base_url = 'https://chennai.craigslist.org/search/jjj?query='
    complete_url = base_url+string
    print(complete_url)
    http_text=requests.get(complete_url)

    soup = bs4.BeautifulSoup(http_text.text,'lxml')
    print(type(soup))

    flag = 0
    list_dict=[]

    for i in soup.select(".result-row"):
        flag=1
        data_obj = data()

        try:
            data_obj.title = i.select(".result-title")[0].text
        except:
            data_obj.title = None

        try:
            data_obj.link = i.select(".result-title")[0]["href"]
        except:
            data_obj.link = None

        try:
            image_data_id = i.select(".result-image")[0]["data-ids"]
            if ':' in image_data_id:
                if "," in image_data_id:
                    image_id = image_data_id[image_data_id.index(":")+1:image_data_id.index(",")]
                else:
                    image_id = image_data_id[image_data_id.index(":")+1:]
            else:
                image_id = image_data_id

            image_base_url = 'https://images.craigslist.org/'
            pixel_dimen_exten = '_600x450.jpg'

            complete_image_url = image_base_url+image_id+pixel_dimen_exten
            data_obj.pic_link = complete_image_url

        except:
            data_obj.pic_link = "https://i.pinimg.com/564x/7e/cd/56/7ecd567d6743794e72675f55ac800608.jpg"

        list_dict.append(data_obj)


    if flag == 1:
        return render(request,'index.html',{"list_dict":list_dict})
    else:
        return render(request,'base.html')
