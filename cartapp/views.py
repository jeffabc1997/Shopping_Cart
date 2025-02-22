from django.shortcuts import render, redirect
from cartapp import models
from smtplib import SMTP, SMTPAuthenticationError, SMTPException
from email.mime.text import MIMEText

from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse

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
	productall = models.ProductModel.objects.filter(id__in=[3,4,6,10])
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
			unit[3] = str(int(unit[1]) * int(unit[2]))  #取得總價
			n += 1
		request.session['cartlist'] = cartlist
		return redirect('/cart/')
	elif ctype == 'empty':  #清空購物車
		cartlist = []  #設購物車為空串列
		request.session['cartlist'] = cartlist
		return redirect('/index/')
	elif ctype == 'remove':  #刪除購物車中商品
		del cartlist[int(productid)]  #從購物車串列中移除商品
		request.session['cartlist'] = cartlist
		return redirect('/cart/')
from .forms import CustomerInfoForm
def cartorder(request):  #按我要結帳鈕
	global cartlist, message, customname, customphone, customaddress, customemail
	cartlist1 = cartlist
	total = 0
	for unit in cartlist:  #計算商品總金額
		total += int(unit[3])
	grandtotal = total + 100
	# get user info
	if request.user.is_authenticated:
		customname = request.user.username
		customemail = request.user.email
		customname1 = customname
	else:
		customname1 = ''
	# customname1 = customname  ##以區域變數傳給模版
	customphone1 = customphone
	customaddress1 = customaddress
	customemail1 = customemail
	message1 = message

	host = request.get_host()
	total_price = 0
	# print(f"http://{host}{reverse('payment-success')}")
	for unit in cartlist:  # 記錄總價格
		total_price += int(unit[1]) * int(unit[2])
	paypal_checkout = {
		'business': settings.PAYPAL_RECEIVER_EMAIL,
		'amount': 19876,
		'item_name': "Good_item",
		'invoice': "100", # TODO need to change
		'currency_code': 'TWD',
		'notify_url': f"http://{host}{reverse('paypal-ipn')}",
		'return_url': f"http://{host}{reverse('payment-success', kwargs = {'product_id': 1})}",
		'cancel_url': f"http://{host}{reverse('payment-failed', kwargs = {'product_id': 1})}",
	}

	paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

	# context = {
		# 'product': product,
	# 	'paypal': paypal_payment
	# }
	paypal = paypal_payment

	form = CustomerInfoForm(initial={'name': customname1, 'phone': customphone1, 'address': customaddress1, 'email': customemail1, 'paytype': '測試'}) # 表單會有預設值
	return render(request, "cartorder.html", locals())

def cartok(request):  #按確認購買鈕
	if request.method == 'POST':  #取得購買者資料
		global cartlist, message, customname, customphone, customaddress, customemail
		
		# customphone = request.POST.get('CustomerPhone', '')
		# customaddress = request.POST.get('CustomerAddress', '')
		# customemail = request.POST.get('CustomerEmail', '')
		# paytype = request.POST.get('paytype', '')
		form = CustomerInfoForm(request.POST)
		if form.is_valid():
			total = 0
			for unit in cartlist:
				total += int(unit[3])
			grandtotal = total + 100

			customname = form.cleaned_data['name']
			customphone = form.cleaned_data['phone']
			customaddress = form.cleaned_data['address']
			customemail = form.cleaned_data['email']
			paytype = form.cleaned_data['paytype']
			unitorder = models.OrdersModel.objects.create(subtotal=total, shipping=100, grandtotal=grandtotal, customname=customname, 
							customphone=customphone, customaddress=customaddress, customemail=customemail, paytype=paytype) #建立訂單
			for unit in cartlist:  #將購買商品寫入資料庫
				total = int(unit[1]) * int(unit[2])
				unitdetail = models.DetailModel.objects.create(dorder=unitorder, pname=unit[0], unitprice=unit[1], quantity=unit[2], dtotal=total)
			orderid = unitorder.id  #取得訂單id

			## 寄送訂單通知郵件
			mailto=customemail  #收件者
			mailsubject="棒球購物網-訂單通知";  #郵件標題
			mailcontent = "感謝您的光臨，您已經成功的完成訂購程序。\n我們將儘快把您選購的商品郵寄給您！ 再次感謝您支持\n您的訂單編號為：" + str(orderid) + "，您可以使用這個編號回到網站中查詢訂單的詳細內容。\n棒球購物網" #郵件內容
			send_simple_message(mailto, mailsubject, mailcontent)  #寄信
			##
			cartlist = []
			request.session['cartlist'] = cartlist
			return render(request, "cartok.html", locals())
		else:
			return redirect('/cartorder/')
	return redirect('/cartorder/')

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
	return render(request, "cartordercheck.html", locals())

import os
from django.conf import settings
def send_simple_message(mailto, mailsubject, mailcontent): #寄信
	global message
	strSmtp = "smtp.gmail.com:587"  #主機
	# read the email and password from send_pass.txt
	file1 = open(os.path.join(settings.BASE_DIR, "static", "send_pass.txt"), 'r')
	list1 = file1.read().splitlines() # list1 裡面的每一個element就是file內的每一行內容，

	strAccount = list1[0]  #帳號
	strPassword = list1[1]  #密碼

	# strAccount = mailfrom  #帳號
	# strPassword = mailpw  #密碼
	msg = MIMEText(mailcontent)
	msg["Subject"] = mailsubject  #郵件標題
	mailto1 = mailto  #收件者
	server = SMTP(strSmtp)  #建立SMTP連線
	server.ehlo()  #跟主機溝通
	server.starttls()  #TTLS安全認證
	try:
		server.login(strAccount, strPassword)  #登入
		server.sendmail(strAccount, mailto1, msg.as_string())  #寄信
	except SMTPAuthenticationError:
		message = "無法登入！"
		print("無法登入！")
	except:
		message = "郵件發送產生錯誤！"
		print("郵件發送產生錯誤！")
	server.quit() #關閉連線

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

def PaymentSuccessful(request, product_id):
	# productall = models.ProductModel.objects.filter(id__in=[3,4,6,10])
    # product =  models.ProductModel.objects.get(id=3)

    return render(request, 'payment-success.html', {'product': 3})

def paymentFailed(request, product_id):

    # product =  models.ProductModel.objects.get(id=4)

    return render(request, 'payment-failed.html', {'product': 4})

