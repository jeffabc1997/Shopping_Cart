from django.shortcuts import render, redirect
from cartapp import models


from django.contrib.auth import authenticate
from django.contrib import auth

from django.contrib.auth.forms import UserCreationForm



message = ''
cartlist = []  #購買商品串列
customname = ''  #購買者姓名
customphone = ''  #購買者電話
customaddress = ''  #購買者地址
customemail = ''  #購買者電子郵件

def index(request):
	global cartlist
	if 'cartlist' in request.session:  #若session中存在cartlist就讀出
		cartlist = request.session['cartlist']
	else:  #重新購物
		cartlist = []
	cartnum = len(cartlist)  #購買商品筆數
	# productall = models.ProductModel.objects.all()  #取得資料庫所有商品
	productall = models.ProductModel.objects.filter(pname__contains="Signed")
	if request.user.is_authenticated:
		name = request.user.username
	else:
		name = '最優質的顧客'
	return render(request, "index.html", locals())

def detail(request, productid=None):  #商品詳細頁面
	product = models.ProductModel.objects.get(id=productid)  #取得商品
	return render(request, "detail.html", locals())

def cart(request):  #顯示購物車
	global cartlist
	cartlist1 = cartlist  #以區域變數傳給模版
	total = 0
	for unit in cartlist:  #計算商品總金額
		total += int(unit[3])
	grandtotal = total + 100  #加入運費總額
	return render(request, "cart.html", locals())

def addtocart(request, ctype=None, productid=None):
	global cartlist
	if ctype == 'add':  #加入購物車
		product = models.ProductModel.objects.get(id=productid)
		flag = True  #設檢查旗標為True
		for unit in cartlist:  #逐筆檢查商品是否已存在
			if product.pname == unit[0]:  #商品已存在
				unit[2] = str(int(unit[2])+ 1)  #數量加1
				unit[3] = str(int(unit[3]) + product.pprice)  #計算價錢
				flag = False  #設檢查旗標為False
				break
		if flag:  #商品不存在
			temlist = []  #暫時串列
			temlist.append(product.pname)  #將商品資料加入暫時串列
			temlist.append(str(product.pprice))  #商品價格
			temlist.append('1')  #先暫訂數量為1
			temlist.append(str(product.pprice))  #總價
			cartlist.append(temlist)  #將暫時串列加入購物車
		request.session['cartlist'] = cartlist  #購物車寫入session
		return redirect('/cart/')
	elif ctype == 'update':  #更新購物車
		n = 0
		for unit in cartlist:
			unit[2] = request.POST.get('qty' + str(n), '1')  #取得數量
			# print('qty' + str(n))
			unit[3] = str(int(unit[1]) * int(unit[2]))  #取得總價
			n += 1
		request.session['cartlist'] = cartlist
		if request.POST.get('Update', '') == '繼續購物':
			return redirect('/index/')
		else:
			return redirect('/cartorder/')
	elif ctype == 'empty':  #清空購物車
		cartlist = []  #設購物車為空串列
		request.session['cartlist'] = cartlist
		return redirect('/index/')
	elif ctype == 'remove':  #刪除購物車中商品
		del cartlist[int(productid)]  #從購物車串列中移除商品
		request.session['cartlist'] = cartlist
		return redirect('/cart/')
from .forms import CustomerInfoForm
def cartorder(request):  #按我要結帳鈕之後的畫面.
	global cartlist, message, customname, customphone, customaddress, customemail
	cartlist1 = cartlist
	total = 0
	for i, unit in enumerate(cartlist):  #計算商品總金額
		# print(unit)
		total += int(unit[3])
	grandtotal = total + 100
	# get user info
	if request.user.is_authenticated:
		customname = request.user.username
		customemail = request.user.email
		customname1 = customname
	else:
		customname1 = '未登入使用者'
	# customname1 = customname  ##以區域變數傳給模版
	customphone1 = customphone
	customaddress1 = customaddress
	customemail1 = customemail
	message1 = message

	form = CustomerInfoForm(initial={'name': customname1, 'phone': customphone1, 'address': customaddress1, 'email': customemail1, 'paytype': '測試'}) # 表單會有預設值
	return render(request, "cartorder.html", locals())



def cartordercheck(request):  #查詢訂單
	orderid = request.GET.get('orderid', '')  #取得輸入id
	customemail = request.GET.get('customemail', '')  #取得輸email
	if orderid == '' and customemail == '':  #按查詢訂單鈕
		firstsearch = 1
	else:
		order = models.OrdersModel.objects.filter(id=orderid).first()
		if order == None or order.customemail != customemail:  #查不到資料
			notfound = 1
		else:  #找到符合的資料
			details = models.DetailModel.objects.filter(dorder=order)
			# print(details)
	return render(request, "cartordercheck.html", locals())

import os

def login(request):
	if request.user.is_authenticated:
		return redirect('/index/')
	if request.method == 'POST':
		name = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=name, password=password)
		# print(cartlist)
		if user is not None:
			if user.is_active:
				auth.login(request,user)
				request.session['cartlist'] = cartlist
				return redirect('/index/')
				message = '登入成功！'
			else:
				message = '帳號尚未啟用！'
		else:
			message = '登入失敗！'
	return render(request, "login.html", locals())
	
def logout(request):
	auth.logout(request)
	return redirect('/index/')	

def register(request):
    if request.user.is_authenticated:
        return redirect('/index/')	
    elif request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)  # 註冊後自動登入
            return redirect('/login/')  # 導回購物頁面
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


