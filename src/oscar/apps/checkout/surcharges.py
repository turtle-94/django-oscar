from oscar.core import prices


class Base(object):
    """
    Surcharge interface class

    This is the superclass to the classes in surcharges.py. This allows using all
    surcharges interchangeably (aka polymorphism).

    The interface is all properties.
    """

    # The name of the surcharge, shown to the customer during checkout
    name = "Default surcharge"

    description = ""

    charge_is_percentage = False

    charge_excl_tax = None
    charge_incl_tax = None

    charge_is_percentage = True

    def __init__(self, charge_excl_tax=None, charge_incl_tax=None):
        if charge_excl_tax is not None:
            self.charge_excl_tax = charge_excl_tax
        if charge_incl_tax is not None:
            self.charge_incl_tax = charge_incl_tax

    def calculate(self, basket):
        """
        Return the surcharge for the given basket
        """
        if self.charge_is_percentage:
            return prices.Price(
                currency=basket.currency,
                excl_tax=basket.total_excl_tax * (self.charge_excl_tax / 100),
                incl_tax=basket.total_incl_tax * (self.charge_incl_tax / 100)
            )
        else:
            return prices.Price(
                currency=basket.currency,
                excl_tax=self.charge_excl_tax,
                incl_tax=self.charge_incl_tax)

class PaymentCharge(Base):
    name = "Payment surcharge"
    charge_is_percentage = True

class BlaatCharge(Base):
    name="Henk is een koe charge"
