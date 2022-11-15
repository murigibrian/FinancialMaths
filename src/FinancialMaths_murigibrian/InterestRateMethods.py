from math import log, exp

class AccumulationRateMethods:
    """Contains methods for converting to and from effecive interest rates and accumualtion factors"""

    def simple_factor(simple_ir: float, period: float):
        """
            Returns the simple accumulation factor
        """
        
        factor = (1 + (simple_ir * period))
        return factor


    
    def compound_factor(compound_ir: float, period: float):
        """
            Returns the effective accumulation factor
        """
        
        factor = (1 + compound_ir) ** period
        return factor
        
    def effective_from_simple(simple_rate:float, simple_period: float= 1):
        """
            Returns an effective interest rate that will yeild a similar amount to the simple rate.
            The amount should be same after compunding for 'sample_period' units of time
        """

        rate = ((1 + (simple_rate * simple_period)) ** (1/simple_period)) -1

        return rate

    def effective_to_simple(eff_rate:float, compound_period: float= 1):
        """
            Returns a simple interest rate that will yeild a similar amount to the simple rate.  
            The amount should be same after compunding for 'compound_period' units of time.
        """

        rate = (((1 + eff_rate)**compound_period)-1) / compound_period

        return rate


    def effective_from_norminal(norminal_rate:float, norminal_period: float= 1, compound_period: float= 1):
        """
            Retruns an effective rate from the porvided norminal rate.
        """

        rate = ((1 + (norminal_rate / norminal_period)) ** (compound_period * norminal_period) ) - 1
        return rate


    def effective_to_norminal(eff_rate:float, norminal_period: float):
        """
            Returns a normial interest rate from the norminal rate.
        """
        
        rate = ((1 + eff_rate) ** (1/norminal_period) - 1) * norminal_period
        return rate


    def effective_from_foi(foi_rate:float):
        """
            Retruns the effective interest rate from the force of interest(foi).
        """

        rate = exp(foi_rate) - 1
        return rate

        
    def effective_to_foi(eff_rate: float):
        """
            Returns force of interest(foi) from the effective interest rate.
        """

        foi_rate = log(1 + eff_rate)
        return foi_rate


    def accumulation_from_discount(eff_disc_rate: float):
        """
            Returns the effective interest rate from the effective discount rate
        """

        eff_int_rate =  eff_disc_rate / (1 - eff_disc_rate)
        return eff_int_rate


    def accumulation_to_discount(eff_int_rate: float):
        """
            Returns the effective discount rate from the effective interest rate
        """

        eff_disc_rate =  eff_int_rate / (1 + eff_int_rate)
        return eff_disc_rate


    def simple_interest_from_discounting(simple_dr: float, discount_period: float= 1):
        """
            Returns a simple interest rate (simple_ir) based on the equivalent simple discounting rate (simple_dr).
        """        
        simple_ir = simple_dr/(1- (simple_dr * discount_period))
        return simple_ir


    def simple_interest_to_discounting(simple_ir: float, interest_period: float= 1):
        """
            Returns a simple discounting rate (simple_dr) based on the equivalent simple interest rate (simple_ir).
            By discounting with (simple_dr) over the span (interest_period) to time 0, the accummulated value should be discounted to the original value.
        """
        simple_dr =  simple_ir / (1 + (simple_ir * interest_period ))
        return simple_dr




class DiscountRateMethods:
    """ Contains methods for converting to and from effecive discounting interest rates """

    def simple_factor(simple_dr: float, period: float):
        """
            Returns the simple discounting factor
        """
        
        factor = (1 - (simple_dr * period))
        return factor


    def compound_factor(compound_dr: float, period: float):
        """
            Returns the effective discounting factor
        """
        factor = (1 - compound_dr) ** period
        return factor


    def effective_from_simple(simple_rate: float, simple_period: float= 1):
        """
            Returns the effective discount rate from the simple discount rate.
            The rate will yield a similar amount     
        """

        rate = 1 - ((1 - simple_rate * simple_period)**(1 / simple_period))
        return rate


    def effective_to_simple(eff_rate: float, compound_period: float= 1):
        """
            Returns a simple discount rate from the effective discount rate.
        """
        rate = (1 - (1 - eff_rate)** compound_period) / compound_period
        return rate


    def effective_from_norminal(norminal_rate: float, norminal_period: float = 1):
        """
            Returns the effective discount rate from the norminal discount rate
        """
        
        rate = 1 - (( 1 - norminal_rate / norminal_period) ** norminal_period)
        return rate


    def effective_to_norminal( eff_rate: float, norminal_period: float ):
        """
            Returns the normnal discount rate from the provided effective discount rate
        """
        rate = (1 - (1 - eff_rate) ** (1 / norminal_period)) * norminal_period
        return rate


    def effective_from_foi(foi_rate:float):
        """
            Retruns the effective interest rate from the force of interest(foi).
        """

        rate = 1 - exp(- foi_rate) 
        return rate

        
    def effective_to_foi(eff_rate: float):
        """
            Returns force of interest(foi) from the effective interest rate.
        """

        foi_rate = -log(1 - eff_rate)
        return foi_rate


    def discount_from_accumulation(eff_int_rate: float):
        """
            Returns the effective discount rate from the effective interest rate
        """

        eff_disc_rate =  eff_int_rate / (1 + eff_int_rate)
        return eff_disc_rate


    def discount_to_accumulation(eff_disc_rate: float):
        """
            Returns the effective interest rate from the effective discount rate
        """

        eff_int_rate =  eff_disc_rate / (1 - eff_disc_rate)
        return eff_int_rate


    def simple_discount_to_interest(simple_dr: float, discount_period: float= 1):
        """
            Returns a simple interest rate (simple_ir) from the simple discount rate (simple_dr)
        """
        
        simple_ir = simple_dr/(1- (simple_dr * discount_period))
        return simple_ir


    def simple_discount_from_interest(simple_ir: float, interest_period: float= 1):
        """
            Returns a simple discounting rate (simple_dr) based on the equivalent simple interest rate (simple_ir).
        """
        simple_dr =  simple_ir / (1 + (simple_ir * interest_period ))
        return simple_dr

     