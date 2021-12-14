from django.contrib import admin
from cef.models import Ticker


@admin.register(Ticker)
class CEFAdmin(admin.ModelAdmin):
    list_display = (
        'ticker', 'category', 'price', 'nav', 'price_change', 'nav_change', 'price_minus_nav', 'current_discount',
        'avg_minus_current', 'cents_to_avg', 'div', 'distribution_frequency', 'current_yield', 'fiscal_year_end',
        'fund_sponsor')
    fieldsets = (
        (None, {
         'fields': ('price', 'nav', 'price_change', 'nav_change', 'price_minus_nav', )
        }),
        ('Distribution', {
            'fields': ('current_yield', 'div', 'distribution_frequency')
        }),
        ('Basic Information', {
            'fields': ('category', 'ticker', 'fiscal_year_end')
        }),
        ('52 Weeks Premium/Discount', {
            'fields': ('avg_52w', 'low_52w', 'high_52w')
        }),
        ('Pricing Information', {
            'fields': ('z_month_3', 'z_month_6', 'z_year')
        })
    )
    list_display_links = ('ticker',)
    empty_value_display = '-Not Updated-'
    list_filter = ('category', 'distribution_frequency', 'fund_sponsor',)
    search_fields = ['ticker']


