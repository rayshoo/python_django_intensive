from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView
from .forms import Registerform
from .models import Order
# Create your views here.

class OrderCreate(FormView):
  form_class = Registerform
  success_url = '/product/'

  def form_invalid(self, form): # 수량이라던가 제품값이 없어서 실패하는 경우 돌아갈 페이지 지정하기 위해 사용
    return redirect('/product/' + str(form.product))


  # class 기반의 view 안에 기본적으로 내장되있는 함수 > form을 생성할때 인자 전달할것들 정하기 위해 사용 > request 전달하기 위해 사용
  # def get_form_kwargs()
  def get_form_kwargs(self, **kwargs): # 기존에 자동으로 생성되던 인자값과 request 도 같이 보내겠다!
    kw = super().get_form_kwargs(**kwargs)
    kw.update({
      'request' : self.request
    })
    return kw

class OrderList(ListView):
  # model = Order # 자신이 주문한것만 보이게 하기위해 filter 적용(하단의 get_queryset > session 접근하기위해 사용하는 함수)
  template_name = 'order.html'
  context_object_name = 'order_list' # attribute name 설정 > 안할시 object_list

  def get_queryset(self, **kwargs):
    queryset = Order.objects.filter(fcuser__email=self.request.session.get('user'))
    return queryset