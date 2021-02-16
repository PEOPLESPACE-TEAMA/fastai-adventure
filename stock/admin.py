from django.contrib import admin
from .models import User, Stock, Bookmark, Question, Answer,News, StockIndex
# Register your models here.

admin.site.register(User)

class StockAdmin(admin.ModelAdmin) :
    list_per_page = 20
    list_display = (
        'company_name','stock_type','open','close','before_close','increase','fluctuation_width',
    )
    search_fields = ( 'stock_code' , 'company_name', )

admin.site.register(Stock,StockAdmin)
admin.site.register(Bookmark)
admin.site.register(News)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(StockIndex)

