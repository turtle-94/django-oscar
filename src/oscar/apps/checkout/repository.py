from oscar.core import prices
from oscar.core.loading import get_class

from decimal import Decimal as D

PaymentCharge = get_class("checkout.surcharges", "PaymentCharge")
BlaatCharge = get_class("checkout.surcharges", "BlaatCharge")

class SurchargeRepository(object):

    methods = (PaymentCharge(charge_excl_tax=D("10.0"), charge_incl_tax=D("10.0")), BlaatCharge(charge_excl_tax=D("20.0"), charge_incl_tax=D("20.0")), )
    # methods = ()

    def get_surcharges(self, basket, shipping_addr=None, **kwargs):
        return self.methods

    def get_applicable_surcharges(self, basket, shipping_addr=None, **kwargs):
        return [{
            "method": method,
            "price": method.calculate(basket)
        } for method in self.get_surcharges(basket, shipping_addr) if self.is_applicable(basket, shipping_addr)]

    def get_surcharges_with_prices(self, basket, shipping_addr=None, **kwargs):
        methods = self.get_surcharges(basket, shipping_addr)
        return [{
            "method": method,
            "price": method.calculate(basket)
        } for method in methods]

    def is_applicable(self, surcharge, basket, shipping_addr=None, **kwargs):
        """
        Checks if surcharge is applicable based on basket and/or shipping address
        """
        return True

    def get_surcharges_total(self, basket, shipping_addr=None, **kwargs):
        total_surcharge = prices.Price(
            currency=basket.currency,
            excl_tax=D('0.00'), tax=D('0.00'))

        for charge in self.get_surcharges(basket):
            chargeprice = charge.calculate(basket)
            total_surcharge.excl_tax += chargeprice.excl_tax
            total_surcharge.incl_tax += chargeprice.incl_tax

        return total_surcharge
