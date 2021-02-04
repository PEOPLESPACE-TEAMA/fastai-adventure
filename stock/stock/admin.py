from django.contrib import admin
from .models import User, Stock
# Register your models here.

admin.site.register(User)

class StockAdmin(admin.ModelAdmin) :
    list_per_page = 20
    list_display = (
        'company_name','stock_type','open','close','before_close','increase','fluctuation_width',
    )
    search_fields = ( 'stock_code' , )

admin.site.register(Stock,StockAdmin)

