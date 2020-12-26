from django.shortcuts import render,redirect
from .models import Product,Contact,Order,OrderUpdate,SignUp
from math import ceil
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
import django
from django.core.mail import send_mail,BadHeaderError
from django.contrib import messages
from django.db import connection
import xlsxwriter

# cursor=connection.cursor()
# a=cursor.execute("select * from mymac_product")
# print(type(a.fetchall()))


MERCHANT_KEY='QzDmQ%lAU4WR#QOj'

def index(request):
	all_prods=[]
	catprods=Product.objects.values('category')# fetch only category column and retruns a list of dictionaries in the form of queryset
	#print(catprods.query) #to see query manually that how looks my query 
	cats={item['category'] for item in catprods}
	for cat in cats:
		prod=Product.objects.filter(category=cat)# fetch all data matching category column and retruns only queryset
		n=len(prod)
		nslides=ceil(n/6)
		all_prods.append([prod,range(1,nslides),nslides])
	if request.session.has_key('username'):
		name=SignUp.objects.get(username=request.session['username'])
		return render(request,'mymac/index.html',{'all_prods':all_prods,'Login_Success':'Yes','name':name})
	else:
		return render(request,'mymac/index.html',{'all_prods':all_prods})




def about(request):
	return render(request,'mymac/about.html')

def login(request):
	if request.method=="POST":
		username=request.POST.get('username')
		password=request.POST.get('password')
		if SignUp.objects.filter(username=username,password=password):
			request.session['username']=username
			request.session['password']=password
			name=SignUp.objects.get(username=request.session['username'])
			print('j')
			return redirect('/mymac/')
		else:
			return redirect('/mymac/')
			#{'Login_Failed':'Invalid Username/Password/Login Failed'}
	
	if request.session.has_key('username'):
		return redirect('/mymac/')
	else:
		return redirect('/mymac/')

def logout(request):
	del request.session['username']
	del request.session['password']
	return redirect('/mymac/')

def signup(request):
	if request.method=="POST":
		name=request.POST.get('name')
		username=request.POST.get('username')
		password=request.POST.get('password')
		phone=request.POST.get('phone')
		if name.strip()=="" or username.strip=="" or password.strip()=='' or phone.strip()=='':
			return render(request,'mymac/index.html',{'ErrorMsg':'Kindly Fill The Form Correctly'})
		else:
			signup=SignUp.objects.create(name=name,username=username,password=password,phone=phone)
			signup.save()
			return render(request,'mymac/index.html',{'SucMsg':'Successfully Joined Us'})
	return render(request,'mymac/index.html')



def contact(request):
	if request.method=="POST":
		name=request.POST.get('name','')
		email=request.POST.get('email','')
		phone=request.POST.get('phone','')
		msg=request.POST.get('msg','')

		if len(name)<4 or len(email)<10 or len(phone)<10 or len(msg)<5:
			messages.error(request,"Please fill the form correctly")
		else:
			contactt=Contact(name=name, email=email, phone=phone, msg=msg)
			contactt.save()
			messages.success(request,"Your message has been successfully sent")
	return render(request,'mymac/contact.html')




def tracker(request):
	if request.method=="POST":
		order_id=request.POST.get('order_id','')
		email=request.POST.get('email','')
		try:
			order=Order.objects.filter(order_id=order_id,email=email)
			if len(order)>0:
				update=OrderUpdate.objects.filter(order_id=order_id)
				updates=[]
				for item in update:
					updates.append({'text':item.update_desc,'time':item.timestamp})
					
					response=json.dumps(updates,default=str)
					print(response)
				return HttpResponse(response)
			else:
				return HttpResponse('{}')
		except Exception as e:
			return HttpResponse('{}')



	return render(request,'mymac/track.html')


def searchMatch(query, item):
	'''return true only if query matches the item'''
	if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
		return True
	else:
		return False

def search(request):
	query = request.GET.get('search')
	allProds = []
	a=[]
	catprods = Product.objects.values('category', 'id')
	cats = {item['category'] for item in catprods}
	for cat in cats:
		prodtemp = Product.objects.filter(category=cat)
		prod = [item for item in prodtemp if searchMatch(query, item)]
		for i in prod:
			a.append(i.id)
		n = len(prod)
		nSlides =ceil(n/6)
		if len(prod) != 0:
			allProds.append([prod, range(1, nSlides), nSlides])
	
	params = {'allProds': allProds, "msg": "",'a':a}
	if len(allProds) == 0 or len(query)<4:
		params = {'msg': "Please make sure to enter relevant search query"}

	return render(request, 'mymac/search.html', params)
	


def productView(request,myid):
	product=Product.objects.filter(id=myid)
	return render(request,'mymac/productView.html',{'product':product[0]})




def checkout(request,myid,qty):
	if request.session.has_key('username'):
		product=Product.objects.filter(id=myid)
		qtyAmount=Product.objects.get(id=myid)
		qty=qtyAmount.price*qty
		print(qty)
		if request.method=="POST":
			itemsJson=request.POST.get('itemsJson','')
			name=request.POST.get('name','')
			amount=request.POST.get('amount','')
			email=request.POST.get('email','')
			phone=request.POST.get('phone','')
			address=request.POST.get('address_line_1','')+' ' + request.POST.get('address_line_2','')
			city=request.POST.get('city','')
			state=request.POST.get('state','')
			zip_code=request.POST.get('zip_code','')


			if len(name)<3 or len(email)<10 or len(phone)<10 or len(phone)>10 or len(address)<3 or len(city)<3 or len(state)<3 or len(zip_code)<6:
				messages.error(request,"Please fill the form correctly")
			else:
				order=Order(
					item_json=itemsJson,name=name,amount=amount,
					email=email,phone=phone,address=address,city=city,state=state,zip_code=zip_code)
				order.save()
				thank=True
				id=order.order_id
				update=OrderUpdate(order_id=order.order_id,update_desc='The order has been placed')
				update.save()
	        #return render(request,'mymac/checkout.html',{'thank':thank,'id':id,'myid':myid})
			#send request to paytm to transfer the amount to your account after payment by user
				param_dict={'MID':'aMCQhd99173249987800',
							'ORDER_ID':str(order.order_id),
							'TXN_AMOUNT':str(amount),
							'CUST_ID':email,
							'INDUSTRY_TYPE_ID':'Retail',
							'WEBSITE':'WEBSTAGING',
							'CHANNEL_ID':'WEB',
							'CALLBACK_URL':'http://127.0.0.1:8000/mymac/handle_request/',
				}
				param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
				return render(request,'mymac/paytm.html',{'param_dict': param_dict,'thank':thank,'myid':myid})
		
		return render(request,'mymac/checkout.html',{'product':product,'qty':qty})
	else:
		return render(request,'mymac/index.html',{'Login_First':'kindly Login First Then Continue'})



def cart(request):
	return render(request,'mymac/cart.html')



def checkout2(request,myid,price):
	product=Product.objects.filter(id=myid)
	return render(request,'mymac/checkout.html',{'product':product,'price':price})



def checkout_all(request):
	if request.session.has_key('username'):
		if request.method=="POST":
			itemsJson=request.POST.get('itemsJson','')
			name=request.POST.get('name','')
			amount=request.POST.get('amount','')
			email=request.POST.get('email','')
			phone=request.POST.get('phone','')
			address=request.POST.get('address_line_1','')+' ' + request.POST.get('address_line_2','')
			city=request.POST.get('city','')
			state=request.POST.get('state','')
			zip_code=request.POST.get('zip_code','')
			if len(name)<3 or len(email)<10 or len(phone)<10 or len(phone)>10 or len(address)<3 or len(city)<3 or len(state)<3 or len(zip_code)<6:
				messages.error(request,"Please fill the form correctly")
			else:
				order=Order(
					item_json=itemsJson,name=name,amount=amount,
					email=email,phone=phone,address=address,city=city,state=state,zip_code=zip_code)
				order.save()
				thank=True
				id=order.order_id
				update=OrderUpdate(order_id=order.order_id,update_desc='The order has been placed')
				update.save()
	        #return render(request,'mymac/checkout.html',{'thank':thank,'id':id,'myid':myid})
			#send request to paytm to transfer the amount to your account after payment by user
				param_dict={'MID':'aMCQhd99173249987800',
							'ORDER_ID':str(order.order_id),
							'TXN_AMOUNT':str(amount),
							'CUST_ID':email,
							'INDUSTRY_TYPE_ID':'Retail',
							'WEBSITE':'WEBSTAGING',
							'CHANNEL_ID':'WEB',
							'CALLBACK_URL':'http://127.0.0.1:8000/mymac/handle_request/',
				}
				param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
				return render(request,'mymac/paytm.html',{'param_dict': param_dict,'thank':thank})
				
		return render(request,'mymac/checkout_all.html')
	else:
		return render(request,'mymac/index.html',{'Login_First':'kindly Login First Then Continue'})




@csrf_exempt
def handle_request(request):
	
	if(request.POST):
	    #paytm will send to response or request after user payment 
		form = request.POST
		response_dict = {}
		for i in form.keys():
			response_dict[i] = form[i]
			if i == 'CHECKSUMHASH':
				checksum = form[i]
		verify=Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
		if verify:
			if response_dict['RESPCODE'] == '01':
				print('order successful')
			else:
				print('order was not successful because' + response_dict['RESPMSG'])
	else:
		return render(request, 'mymac/paymentStatus.html')

	return render(request, 'mymac/paymentStatus.html', {'response': response_dict})
#print(django.VERSION)














# got=Table.objects.values('category')
# items={item['category'] for item in got}
# for i in items:
# 	got=Table.objects.filter(category=i)