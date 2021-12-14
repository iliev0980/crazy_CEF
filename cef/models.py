from django.db import models


class Ticker(models.Model):
    ticker = models.CharField(max_length=7, blank=False)
    category = models.CharField(max_length=100, blank=True)
    price = models.FloatField(null=True, blank=True)
    nav = models.FloatField(null=True, blank=True)
    price_change = models.FloatField(null=True, blank=True)
    nav_change = models.FloatField(null=True, blank=True)
    price_minus_nav = models.FloatField(null=True, blank=True)
    current_discount = models.FloatField(null=True, blank=True)
    avg_52w = models.FloatField(null=True, blank=True)
    low_52w = models.FloatField(null=True, blank=True)
    high_52w = models.FloatField(null=True, blank=True)
    avg_minus_current = models.FloatField(null=True, blank=True)
    cents_to_avg = models.FloatField(null=True, blank=True)
    div = models.FloatField(null=True, blank=True)
    distribution_frequency = models.CharField(max_length=100, blank=True)
    current_yield = models.FloatField(null=True, blank=True)
    fiscal_year_end = models.CharField(max_length=50, blank=True)
    z_month_3 = models.FloatField(null=True, blank=True)
    z_month_6 = models.FloatField(null=True, blank=True)
    z_year = models.FloatField(null=True, blank=True)
    fund_sponsor = models.CharField(max_length=100, blank=True)
    last_updated = models.DateField()


    def __str__(self):
        return self.ticker