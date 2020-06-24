from django.http import HttpResponse
from django.shortcuts import redirect,render
from lists.models import Item,List
# 主页：home.html 将文本框中的内容存入数据库 并跳转到list.html
def home_page(request):
    return render(request,'home.html')
# list.html 显示所有items
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request,'list.html',{'list':list_})
def new_list(request):
    list_ = List.objects.create()
    new_item_text = request.POST['item_text']
    Item.objects.create(text=new_item_text, list=list_)
    return redirect(f'/lists/{list_.id}/')
def add_item(request,list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')
