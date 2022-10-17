from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView, DetailView
from django.db.models import Max
from utils.convertors import group_list
from site_module.models import SiteBanner
from utils.http_service import get_client_ip
from .models import Product, ProductCategory, ProductBrand, ProductVisit, ProductGallery, ProductComment
from django.http import Http404, HttpRequest, HttpResponse


class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['price']
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        query = Product.objects.all()
        product: Product = query.order_by('-price').first()
        db_max_price = product.price if product is not None else 0
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPositions.product_list)
        return context

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        category_name = self.kwargs.get('category')
        brand_name = self.kwargs.get('brand')
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        if start_price is not None:
            query = query.filter(price__gte=start_price)

        if end_price is not None:
            query = query.filter(price__lte=end_price)

        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)

        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)

        return query


class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        request = self.request
        favorite_product_id = request.session.get("product_favorites")
        galleries = list(ProductGallery.objects.filter(product_id=loaded_product.id).all())
        galleries.insert(0, loaded_product)
        context['is_favorite'] = favorite_product_id == str(loaded_product.id)
        context['banners'] = SiteBanner.objects.filter(
            is_active=True,
            position__iexact=SiteBanner.SiteBannerPositions.product_detail
        )
        context['product_galleries_group'] = group_list(galleries, 3)
        context['related_products'] = group_list(
            list(Product.objects.filter(brand_id=loaded_product.brand_id).exclude(id=loaded_product.id).all()[:12]), 3)

        context['comments'] = ProductComment.objects.filter(product_id=loaded_product.id, is_delete=False).order_by(
            '-date')
        context['count'] = ProductComment.objects.filter(product_id=loaded_product.id, is_delete=False).count()

        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id

        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()

        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=loaded_product.id)
            new_visit.save()

        return context


class AddFavoriteProduct(View):
    def post(self, request):
        product_id = request.POST["product_id"]
        product = Product.objects.get(pk=product_id)
        request.session["product_favorites"] = product_id
        return redirect(product.get_absolute_url())


def product_categories_component(request: HttpRequest):
    product_categories = ProductCategory.objects.filter(is_active=True, is_delete=False)
    context = {
        'product_categories': product_categories
    }
    return render(request, 'product_module/components/product_categories_component.html', context)


def product_brands_component(request: HttpRequest):
    product_brands = ProductBrand.objects.annotate(products_count=Count('product_brand')).filter(is_active=True)
    context = {
        'product_brands': product_brands
    }
    return render(request, 'product_module/components/product_brand_component.html', context)


def add_product_comments(request: HttpRequest):
    if request.user.is_authenticated:
        product_id = request.GET.get('product_id')
        product_comment = request.GET.get('product_comment')
        new_comment = ProductComment(user_id=request.user.id, product_id=product_id, text=product_comment)
        new_comment.save()
        context = {
            'comments': ProductComment.objects.filter(product_id=product_id, is_delete=False).order_by(
                '-date'),
            'comments_count': ProductComment.objects.filter(product_id=product_id).count()
        }
        return render(request, 'product_module/includes/product_comment_partial.html', context)

    return HttpResponse('response')

# ------------------------different types of this shit --------------------------------------
# class ProductListView(TemplateView):
#     template_name = 'product_module/product_list.html'
#
#     def get_context_data(self, **kwargs):
#         products = Product.objects.all().order_by("price")[:5]
#         context = super(ProductListView, self).get_context_data()
#         context['products'] = products
#         return context
#
# def product_list(request):
#     products = Product.objects.all().order_by("price")[:5]
#     return render(request, 'product_module/product_list.html', {
#         'products': products,
#
#     })


# class ProductDetailView(TemplateView):
#     template_name = 'product_module/product_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ProductDetailView, self).get_context_data()
#         slug = kwargs['slug']
#         product = get_object_or_404(Product, slug=slug)
#         context['product'] = product
#         return context

# def product_detail(request, slug):
#     product = get_object_or_404(Product, slug=slug)
#     return render(request, 'product_module/product_detail.html', {
#         'product': product
#     })
