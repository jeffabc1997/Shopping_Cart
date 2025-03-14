from django.shortcuts import render, redirect
from smtplib import SMTP, SMTPAuthenticationError, SMTPException
from email.mime.text import MIMEText

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
from cartapp import models
from cartapp.forms import CustomerInfoForm
import os
from cart.password import eMAIL_HOST_USER, eMAIL_HOST_PASSWORD
message = ''
cartlist = []  #購買商品串列
customname = ''  #購買者姓名
customemail = ''  #購買者電子郵件

# from django.http import HttpResponse 
# def paymentapp(request):
#     return HttpResponse('<h1>Payment App</h1>')


def payment(request): # 按確認購買之後的畫面. 先用post 確認購買者資料，再進行付款
	if request.method == 'POST':  #取得購買者資料
		global cartlist, customname, customemail
		cartlist = request.session.get('cartlist', [])
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
							customphone=customphone, customaddress=customaddress, customemail=customemail, paytype=paytype, payment_completed=False) #建立訂單
			host = request.get_host()
			total_price = 100 # 運費
			# print(f"http://{host}")
			# print(f"http://{host}{reverse('payment-success', kwargs = {'orderid': unitorder.id})}")
			for unit in cartlist:  # 記錄總價格
				total_price += int(unit[1]) * int(unit[2])
			paypal_checkout = {
				'business': settings.PAYPAL_RECEIVER_EMAIL,
				'amount': total_price,
				'item_name': "Good_item",
				'invoice': uuid.uuid4(), # TODO need to change
				'currency_code': 'TWD',
				'notify_url': f"http://{host}{reverse('paypal-ipn')}",
				'return_url': f"http://{host}{reverse('payment-success', kwargs = {'orderid': unitorder.id})}",
				'cancel_url': f"http://{host}{reverse('payment-failed', kwargs = {'orderid': unitorder.id})}",
			}

			paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
			paypal = paypal_payment
			return render(request, 'payment.html', locals())
		else:
			return redirect('/cartorder/')
	return redirect('/cartorder/')

def send_simple_message(mailto, mailsubject, mailcontent): #寄信
	global message
	strSmtp = "smtp.gmail.com:587"  #主機
	# read the email and password from send_pass.txt
	file1 = open(os.path.join(settings.BASE_DIR, "static", "send_pass.txt"), 'r')
	list1 = file1.read().splitlines() # list1 裡面的每一個element就是file內的每一行內容，

	strAccount = eMAIL_HOST_USER #list1[0]  #帳號
	strPassword = eMAIL_HOST_PASSWORD  #密碼

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

def PaymentSuccessful(request, orderid): # TODO 使用cartok的方式在資料庫建立訂單和detail
	global cartlist, customname, customemail
	unitorder = models.OrdersModel.objects.filter(id=orderid).first()
	if unitorder is None: #若訂單不存在
		return redirect('/index/')
	unitorder.payment_completed = True  #設定付款完成
	unitorder.save()  #儲存訂單
	
	for unit in cartlist:  #將購買商品寫入資料庫
		total = int(unit[1]) * int(unit[2])
		unitdetail = models.DetailModel.objects.create(dorder=unitorder, pname=unit[0], unitprice=unit[1], quantity=unit[2], dtotal=total)
	
	cartlist = []
	request.session['cartlist'] = cartlist #清空購物車
	## 寄送訂單通知郵件
	mailto=customemail  #收件者
	mailsubject="棒球購物網-訂單通知";  #郵件標題
	mailcontent = "感謝您的光臨，您已經成功的完成訂購程序。\n我們將儘快把您選購的商品郵寄給您！ 再次感謝您支持\n您的訂單編號為：" + str(orderid) + \
						"，您可以使用這個編號回到網站中查詢訂單的詳細內容。\n棒球購物網" #郵件內容
	send_simple_message(mailto, mailsubject, mailcontent)  #寄信
	##

	# customname1 = customname
	context = {
		'orderid': orderid,
		'customname1': customname,
		'mailto': mailto,
	}
	return render(request, 'payment-success.html', locals())

def paymentFailed(request, orderid): # TODO 引導回cartorder

    return render(request, 'payment-failed.html', {'product': orderid})
