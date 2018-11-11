import decimal

class ConvertDecimalToString:
    def __init__(self):
        self.decimal_obj = None

    def process(self, obj: any)-> str:
        self.decimal_obj = obj
        dec = decimal.Decimal(self.decimal_obj)
        dec = str(dec)
        return dec

