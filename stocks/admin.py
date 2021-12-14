from django.contrib import admin
from .models import Stock
# Register your models here.
@admin.register(Stock)
class CEFAdmin(admin.ModelAdmin):
    list_display = (
        'ticker', 'is_updated', 'category', 'nav_', 'price_', 'price_chg', 'nav_chg', 'price_minus_nav', 'curr_disc',
        'avg_minus_curr', 'c_to_avg', 'dist_frq', 'curr_yield', 'year_end',
        'sponsor')
    fieldsets = (
        (None, {
         'fields': ('price', 'nav', 'price_change', 'nav_change', 'price_minus_nav', )
        }),
        ('Distribution', {
            'fields': ('current_yield', 'distribution_frequency')
        }),
        ('Basic Information', {
            'fields': ('category', 'ticker', 'fiscal_year_end')
        }),
        ('52 Weeks Premium/Discount', {
            'fields': ('average_52w', 'low_52w', 'high_52w')
        }),
        ('Pricing Information', {
            'fields': ('z_score_3', 'z_score_6', 'z_score_12')
        })
    )
    list_display_links = ('ticker',)
    empty_value_display = '-Not Updated-'
    list_filter = ('distribution_frequency', 'is_updated', 'category')
    search_fields = ['ticker']


