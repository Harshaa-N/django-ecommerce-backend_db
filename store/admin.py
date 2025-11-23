from django.contrib import admin
from .models import Category,Product,ProductImage,Address, Cart, CartItem, Wishlist, Order, OrderItem, PaymentRecord

#admin.site.register(Category)
#admin.site.register(Product)
admin.site.register(ProductImage)
#admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist)
#admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PaymentRecord)

#Customize Product Admin
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'stock', 'created_date']
    search_fields = ['title', 'description']
    list_filter = ['category', 'created_date']
    inlines = [ProductImageInline]  # Inline images


#Category Admin (Add List View & Search)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']


#Order & Order Item Display
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'created']
    search_fields = ['user__username']
    list_filter = ['status', 'created']
    inlines = [OrderItemInline]  # Show items inside order form

# Register/Customize Other Models
from .models import Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'city', 'default']
    search_fields = ['full_name', 'city']
    list_filter = ['city', 'default']
