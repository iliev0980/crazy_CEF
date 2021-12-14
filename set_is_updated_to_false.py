from stocks.models import Stock

def clean_update_field():
    for stock in Stock.objects.all():
        stock.is_updated = False
        stock.save()

clean_update_field()