from .Annuities import Annuity
from .InterestRates import Rate

class VaryAnnuityMethods:
    def increasing_arrear_pv(annuity_arrear: Annuity):
        """
            Returns the present value of a increasing annuity arrear.
        """

        # annuity Props
        rate = annuity_arrear.annuity_rate
        to_adv_factor = rate.convert_to("compound interest", norminal_period= annuity_arrear.norminal_period) / rate.convert_to("compound discount", norminal_period= annuity_arrear.norminal_period)
        disc_factor = rate.time_value_factor(annuity_arrear.annuity_term, discount= True)
        advance_pv = annuity_arrear.arrear_pv * to_adv_factor       

        # varying annuity arrears present value
        inc_arrear_pv = (advance_pv - (annuity_arrear.annuity_term * disc_factor))/rate.interest_rate

        return inc_arrear_pv


    def increasing_advance_pv(annuity_advance):
        """
            Returns the present value of a varying annuity arrear.
        """ 
        # annuity props
        rate = annuity_advance.annuity_rate
        vary_arrear = VaryAnnuityMethods.increasing_arrear_pv(annuity_advance)
        to_adv_factor = rate.convert_to("compound interest", norminal_period= annuity_advance.norminal_period) / rate.convert_to("compound discount", norminal_period= annuity_advance.norminal_period)

        # varying annuity due present value
        inc_adv_pv = vary_arrear * to_adv_factor

        return inc_adv_pv 
    
    def increasing_continuous_pv(annuity_continuous):
        """
            Returns the present value of a varying continous annuity.
        """
        # annuity props
        rate = annuity_continuous.annuity_rate
        vary_arrear = VaryAnnuityMethods.increasing_arrear_pv(annuity_continuous)
        to_cont_factor = rate.convert_to("compound interest", norminal_period= annuity_continuous.norminal_period) / rate.foi

        # varying annuity due present value
        inc_adv_pv = vary_arrear * to_cont_factor

        return inc_adv_pv 


    def increasing_time_continuous_pv(annuity_continuous):
        """
            Returns the present value of an annuity where the amount increases continuously with time
        """

        # annuity Props
        rate = annuity_continuous.annuity_rate
        to_cont_factor = rate.convert_to("compound interest", norminal_period= annuity_continuous.norminal_period) / rate.foi
        disc_factor = rate.time_value_factor(annuity_continuous.annuity_term, discount= True)
        continuous_pv = annuity_continuous.arrear_pv * to_cont_factor

        # varying annuity arrears present value
        inc_time_cont_pv = (continuous_pv - (annuity_continuous.annuity_term * disc_factor))/rate.foi

        return inc_time_cont_pv 




class VaryAnnuity:
    """ Handles Varying annuities"""
    annuity: Annuity
    annuity_rate: Rate
    annuity_term: float
    base_amount: float
    vary_amount: float
    is_time_continuous: bool

    def __init__(self, annuity_rate: Rate, base_amount: float= 1, vary_amount: float= 0, is_time_continuous: bool= False, is_decreasing: bool= False,  **kwargs):
        self.annuity_rate = annuity_rate
        self.annuity = Annuity(annuity_rate, **kwargs)
        self.annuity_term = self.annuity.annuity_term

        self.vary_amount = vary_amount if(not is_decreasing)else( -1 * abs(vary_amount) )
        self.base_amount = base_amount
        self.is_time_continuous = is_time_continuous

    
    def time_value(self, differ_period: float= 0, differ_rate: Rate= None,  is_fv: bool= False):
        """
            Returns the time value of the annuity (present value and future value).
            It also differs the annuity. 
        """ 


        annuity_pv = None
        if self.annuity.is_arrear:
            # increasing annuity paid in arrears
            inc_arrear = VaryAnnuityMethods.increasing_arrear_pv(self.annuity)
            annuity_pv = (self.base_amount - self.vary_amount) * self.annuity.time_value() + self.vary_amount * inc_arrear
            print(inc_arrear, )

        elif self.is_time_continuous:
            # increasing annuity paid continously with the varrying amount varrying with per unit time   
            inc_tym_continuous = VaryAnnuityMethods.increasing_time_continuous_pv(self.annuity)
            annuity_pv = self.base_amount * inc_tym_continuous
            
        elif self.annuity.is_continuous:
            # increasing annuity paid continously with the varrying amount constant with per unit time   
            inc_continuous = VaryAnnuityMethods.increasing_continuous_pv(self.annuity)
            annuity_pv = (self.base_amount - self.vary_amount) * self.annuity.time_value() + self.vary_amount * inc_continuous

        elif self.annuity.is_advance:
            # increasing annuity paid in advance
            inc_advance = VaryAnnuityMethods.increasing_advance_pv(self.annuity)
            annuity_pv = (self.base_amount - self.vary_amount) * self.annuity.time_value() + self.vary_amount * inc_advance 
            
        # Differ the annuity. 
        if differ_rate == None:
            # initializing the defualt differ rate 
            differ_rate = self.annuity_rate

        
        elif not isinstance(differ_rate, Rate):
            # using assinged differ rate
            raise TypeError(f"The differ rate is invalid. It should be of type 'Rate' not {type(differ_rate)}.")

        annuity_pv *= differ_rate.time_value_factor(differ_period, discount= True)
        
        # Future Value
        if is_fv:
            # get future value of the pv amount.
            annuity_pv *= self.annuity_rate.time_value_factor(self.annuity_term + differ_period)
                
        return annuity_pv 



if __name__ == "__main__":
    rate = Rate(0.034)
    rate2 = Rate(0.042)
    annuity = Annuity(rate, annuity_term= 4, annuity_amount= 1000, norminal_period= 4)
    annuity2 = Annuity(rate2, annuity_term= 2, annuity_amount= 1000, norminal_period= 4)

    print(rate.interest_rate)
    print(rate2.interest_rate)
    print(annuity.time_value() )
    print(annuity2.time_value(differ_period= 4, differ_rate= rate))
    print(annuity.time_value() + annuity2.time_value(differ_period= 4, differ_rate= rate))
