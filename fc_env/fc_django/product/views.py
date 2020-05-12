from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from fcuser.decorators import admin_required
from .models import Product
from .forms import Registerform
from order.forms import Registerform as OrderForm

# Create your views here.

class ProductList(ListView):
  model = Product
  template_name = 'product.html'
  context_object_name = 'product_list' # attribute name 설정 > 안할시 object_list

@method_decorator(admin_required, name='dispatch')
class ProductCreate(FormView):
  template_name = 'register_product.html'
  form_class = Registerform
  success_url = '/product/'

  def form_valid(self, form):
    product = Product(
      name=form.data.get('name'),
      price=form.data.get('price'),
      description=form.data.get('description'),
      stock=form.data.get('stock')
    )
    product.save()
    return super().form_valid(form)

class ProductDetail(DetailView):
  template_name = 'product_detail.html'
  queryset = Product.objects.all() # 추후 filter통해 보여줄것들만 걸러낼수도있음
  context_object_name = 'product' #실제 탬플릿에서 사용할 변수명

  def get_context_data(self, **kwargs):
    for key in kwargs:
      print(key,'->', kwargs[key])

    context = super().get_context_data(**kwargs)
    print(context)

    context['form'] = OrderForm(self.request)
    print(context)

    return context