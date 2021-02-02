from django.contrib import admin
from .models import User, Stock
# Register your models here.

admin.site.register(User)

class StockAdmin(admin.ModelAdmin) :
    list_per_page = 10
    list_display = (
        'company_name','stock_type','open','close'
    )
    search_fields = ( 'stock_code' , )

admin.site.register(Stock,StockAdmin)

