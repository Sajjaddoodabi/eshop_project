from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from account_module.models import User
from django.utils.text import slugify


# Create your models here.
class ProductCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name="عنوان")
    url_title = models.CharField(max_length=300, db_index=True, verbose_name="عنوان در url")
    is_active = models.BooleanField(verbose_name="فعال / غیر فعال")
    is_delete = models.BooleanField(verbose_name="حذف شده / نشده")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return f'{self.title} - {self.url_title}'


class ProductBrand(models.Model):
    title = models.CharField(max_length=300, verbose_name="نام برند", db_index=True)
    url_title = models.CharField(max_length=300, verbose_name="نام در url", db_index=True)
    is_active = models.BooleanField(verbose_name="فعال / غیر فعال")

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برند ها"

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان محصول")
    category = models.ManyToManyField(
        ProductCategory,
        related_name="product_categories",
        verbose_name='دسته بندی ها')
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر محصول')
    brand = models.ForeignKey(
        ProductBrand,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="product_brand",
        verbose_name="برند")

    price = models.IntegerField(verbose_name="قیمت")
    short_description = models.CharField(max_length=500, db_index=True, null=True, verbose_name="توضیحات کوتاه")
    description = models.TextField(db_index=True, verbose_name="توضیحات تکمیلی")
    slug = models.SlugField(default="", null=False, blank=True, db_index=True, max_length=200, unique=True,
                            verbose_name="عنوان در url")
    is_active = models.BooleanField(default=False, verbose_name="فعال / غیر فعال")
    is_delete = models.BooleanField(verbose_name="حذف شده / نشده")

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return f'{self.title} ({self.price})'


class ProductTag(models.Model):
    caption = models.CharField(max_length=300, db_index=True, verbose_name="عنوان")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="productTags")

    class Meta:
        verbose_name = "تگ محصول"
        verbose_name_plural = "تگ های محصولات"

    def __str__(self):
        return self.caption


class ProductVisit(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=30, verbose_name='آی پی کاربر')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='کاربر')

    def __str__(self):
        return f'{self.product.title} / {self.ip}'

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدید های محصول'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    image = models.ImageField(upload_to='images/product_gallery', verbose_name='تصویر')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = "تصویر گالری"
        verbose_name_plural = "تصاویر گالری"


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    text = models.TextField(verbose_name="متن نظر")
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده')

    class Meta:
        verbose_name = "نظر محصول"
        verbose_name_plural = "نظرات محصول"

    def __str__(self):
        return str(self.user)
