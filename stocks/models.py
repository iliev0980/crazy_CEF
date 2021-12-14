from django.db import models


# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=4)
    category = models.CharField(max_length=100, blank=True, null=True)
    nav = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    price_change = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    nav_change = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    price_minus_nav = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    current_discount = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    average_52w = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    low_52w = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    high_52w = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    average_minus_current = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    cents_to_average = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    distribution_frequency = models.CharField(max_length=30, blank=True, null=True)
    current_yield = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fiscal_year_end = models.CharField(max_length=30, blank=True, null=True)
    z_score_3 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    z_score_6 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    z_score_12 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    fund_sponsor = models.CharField(max_length=40, blank=True, null=True)
    last_update = models.CharField(max_length=100, blank=True, null=True)
    is_updated = models.BooleanField(default=False)

    def __str__(self):
        return self.ticker

    def price_chg(self):
        return f'${self.price_change}'

    def nav_chg(self):
        return f'${self.nav}'

    def nav_(self):
        return f'${self.nav}'

    def price_(self):
        return f'${self.price}'

    def curr_disc(self):
        return f'{self.current_discount}%'

    def avg_52(self):
        return f'{self.average_52w}%'

    def low_52(self):
        return f'{self.low_52w}%'

    def high_52(self):
        return f'{self.high_52w}%'

    def avg_minus_curr(self):
        return f'{self.average_minus_current}%'

    def c_to_avg(self):
        return f'{self.cents_to_average}%'

    def dist_frq(self):
        return self.distribution_frequency

    def curr_yield(self):
        return f'{self.current_yield}'

    def year_end(self):
        return self.fiscal_year_end

    def sponsor(self):
        return self.fund_sponsor
