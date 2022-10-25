from InterestRateMethods import AccumulationRateMethods, DiscountRateMethods


class Rate:
    """ A class that contains properties and functions for working with rates.  """

    is_simple_rate: bool = False
    is_foi: bool = False
    is_discount_rate: bool = False

    interest_rate: float = 0
    discount_rate: float = 0
    foi: float = 0

    def __init__(self, raw_rate:float, norminal_period: float= 1, is_foi: bool= False, is_simple: bool= False, is_discount: bool= False):
        self.is_simple_rate = bool(is_simple)
        self.is_discount_rate = bool(is_discount)
        self.is_foi = bool(is_foi)
        self.norminal_period = float(norminal_period)
        
        # Validate Entries
        self.__validate_entries(raw_rate)
        raw_rate = float(raw_rate)

        # provide a value for the core rate(simple or effective).
        if(self.is_simple_rate):
            self.__to_simple_rates(raw_rate )
        else:
            self.__to_effective_rates(raw_rate)

        
    def __validate_entries(self, raw_rate: float):
        """ 
            Validates varables values and raises errors where relevant. 
        """

        # Rate should be a float value.        
        try:
            raw_rate = float(raw_rate)
        except ValueError:
            raise ValueError("The rate provided is invalid. Use a positive float value.")
        
        # rates should be non-negative 
        if raw_rate < 0:
            raise ValueError("The provided rate is invalid. It should be a positive float value.")

        # norminal time should be positive
        if self.norminal_period < 0:
            raise ValueError("The norminal time period is invalid. It should be a positive float value.")


    def __to_effective_rates(self, raw_rate):
        """
            Returns effective interest and discount rates from the provided rate as the core rates.
        """

        disc_rate = None
        int_rate = None
        foi = None
        if self.is_discount_rate:
            # generate effective rates from discount rate
            disc_rate = DiscountRateMethods.effective_from_norminal(raw_rate, norminal_period= self.norminal_period)
            int_rate = DiscountRateMethods.discount_to_accumulation(disc_rate)
            foi = DiscountRateMethods.effective_to_foi(disc_rate)

        elif self.is_foi:
            # generate effective rates from force of interest.
            int_rate = AccumulationRateMethods.effective_from_foi(raw_rate)
            disc_rate = AccumulationRateMethods.accumulation_to_discount(int_rate)
            foi = AccumulationRateMethods.effective_to_foi(int_rate)
        else:   
            # generate effective rates from intrest rate
            int_rate = AccumulationRateMethods.effective_from_norminal(raw_rate, norminal_period= self.norminal_period)
            disc_rate = AccumulationRateMethods.accumulation_to_discount(int_rate)
            foi = AccumulationRateMethods.effective_to_foi(int_rate)

        self.interest_rate = int_rate
        self.foi = foi
        self.discount_rate = disc_rate

        return (int_rate, foi, disc_rate)


    def __to_simple_rates(self, raw_rate):
        """ 
            Returns simple interest and discount rates from the provided rate as the core rates.
        """
        
        disc_rate = None
        int_rate = None
        if self.is_discount_rate:
            # generate simple rates from discount rate
            disc_rate = raw_rate
            int_rate = DiscountRateMethods.simple_discount_to_interest(raw_rate)
        
        else:
            # generate effective rates from intrest rate
            int_rate = raw_rate
            disc_rate = AccumulationRateMethods.simple_interest_to_discounting(raw_rate)
        
        self.interest_rate = int_rate
        self.discount_rate = disc_rate
        return (int_rate, disc_rate)

    def __convert_simple(self, to: str, simple_period: float= 1):
        """
            Handles conversions in simple interest rates.
        """

        rate = None
        if "compound interest" in to:
            rate = AccumulationRateMethods.effective_from_simple(self.interest_rate, simple_period= simple_period)
        elif "simple discount" in to:
            rate = AccumulationRateMethods.simple_interest_to_discounting(self.interest_rate, simple_period)
        else:
            raise AssertionError(f"Cannot convert to type '{to}'. \n\t\tValid convertion types for simple interest are: 'compound interest', 'simple discount'")
        return rate


    def __convert_compound(self, to: str, compound_period: float= 1):
        """
            Handles conversions in compound interest rates.
        """

        rate = None
        if "compound interest" in to:
            # conver to norminal intrest
            rate = AccumulationRateMethods.effective_to_norminal(self.interest_rate, compound_period)
        
        elif "simple interest" in to:
            # conver to simple intrest
            rate = AccumulationRateMethods.effective_to_simple(self.interest_rate, compound_period= compound_period)

        elif to == "foi":
            # convert to force of interest
            rate = AccumulationRateMethods.effective_to_foi(self.interest_rate)

        elif "compound discount" in to:
            # convert to (norminal or effective) discoount rate
            rate = DiscountRateMethods.effective_to_norminal(self.discount_rate, compound_period)

        elif "simple discount" in to:
            # conver to simple discount
            rate = DiscountRateMethods.effective_to_simple(self.discount_rate, compound_period= compound_period)
        else: 
            raise AssertionError(f"Cannot convert to type '{to}'. \n\t\tValid convertion types for compound interest are: 'compound interest', 'simple interest', 'foi', 'compound discount', 'simple discount' ")

        return rate


    def time_value_factor(self, period:float, discount: bool= False):
        """ 
            Returns the time value factor (accumulating and discounting factors) of the effective and simple interest rates
        """

        factor = None
        if self.is_simple_rate:
            # time value of simple interest and discount rates
            if discount or (period < 0):
                factor = DiscountRateMethods.simple_factor(self.discount_rate, abs(period))
            else:
                factor = AccumulationRateMethods.simple_factor(self.interest_rate, period)

        else:
            # time value of compound interest and discount rates
            if discount or (period < 0):
                factor = DiscountRateMethods.compound_factor(self.discount_rate, abs(period))
            else:
                factor = AccumulationRateMethods.compound_factor(self.interest_rate, period)

        return factor


    def convert_to(self, to: str, norminal_period: float= 1):
        """
            Returns an equivalent rate based on the effective interest and the parameters provided of interest.  
        """       

        to = to.lower().strip()

        rate = None
        if self.is_simple_rate:
            rate = self.__convert_simple(to, simple_period= norminal_period)
        else:
            rate = self.__convert_compound(to, compound_period= norminal_period)

        return rate


if __name__ == "__main__":
    rate = Rate("0.05", is_simple= True)
    n = 5
    acc = rate.time_value_factor(n)
    disc = (1 - n * rate.convert_to("simple discount", norminal_period= n))
    print(acc, disc, acc * disc)