import time

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from order_module.models import Order, OrderDetail
from product_module.models import Product
from django.shortcuts import redirect
import requests
import json

MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "لطفا سفارش خود را نهایی کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/verify_payment/'


def add_product_to_order(request: HttpRequest):
    product_id = int(request.GET.get('product_id'))
    count = int(request.GET.get('count'))

    if count < 1 or count > 10:
        return JsonResponse({
            'status': 'invalid_count',
            'text': 'مقدار وارد شده معتبر نمی باشد',
            'confirm_button_text': 'باشه ممنون',
            'icon': 'warning'
        })

    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()
        if product is not None:
            current_order, created = Order.objects.get_or_create(user_id=request.user.id, is_paid=False)
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.count += count
                current_order_detail.save()

                return JsonResponse({
                    'status': 'success',
                    'text': 'محصول مورد نطر با موفقیت به سبد خرید اضافه شد',
                    'confirm_button_text': 'باشه ممنون',
                    'icon': 'success'
                })

            else:
                new_order_detail = OrderDetail(order_id=current_order.id, product_id=product_id, count=count)
                new_order_detail.save()

                return JsonResponse({
                    'status': 'success',
                    'text': 'محصول مورد نطر با موفقیت به سبد خرید اضافه شد',
                    'confirm_button_text': 'باشه ممنون',
                    'icon': 'success'
                })

        else:
            return JsonResponse({
                'status': 'not_found',
                'text': 'محصول مورد نطر یافت نشد',
                'confirm_button_text': 'باشه ممنون',
                'icon': 'error'
            })

    else:
        return JsonResponse({
            'status': 'not_auth',
            'text': 'برای سفارش یک محصول ابتدا باید لاگین کنید',
            'confirm_button_text': 'ورود به سایت',
            'icon': 'error'
        })


@login_required
def request_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()

    if total_price == 0:
        return redirect(reverse('user_basket_page'))

    tax = int(total_price * (9 / 100))
    total_price += tax

    req_data = {
        "merchant_id": MERCHANT,
        "amount": total_price * 10,
        "callback_url": CallbackURL,
        "description": description,
        # "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


@login_required
def verify_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    tax = int(total_price * (9 / 100))
    total_price += tax

    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": total_price * 10,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                current_order.is_paid = True
                current_order.payment_date = time.time()
                current_order.save()
                ref_str = str(req.json()['data']['ref_id'])
                return render(request, 'order_module/payment_result.html', {
                    'success': f"تراکنش شما با کد پیگیری {ref_str} با موفقیت انجام شد"
                })
            elif t_status == 101:
                ref_str = str(req.json()['data']['message'])
                return render(request, 'order_module/payment_result.html', {
                    'info': f"تراکنش با کد پیگیری {ref_str}  قبلا ثبت شده است"
                })
            else:
                return render(request, 'order_module/payment_result.html', {
                    'error': req.json()['data']['message']
                })
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            # return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
            return render(request, 'order_module/payment_result.html', {
                'error': e_message
            })
    else:
        return render(request, 'order_module/payment_result.html', {
            'error': 'پرداخت با خطا مواجه شد یا کاربر از پرداخت منصرف شد'
        })
