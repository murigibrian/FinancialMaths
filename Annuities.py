from InterestRates import Rate

class Annuity:
    """
        Handles non-varying annuity calculations.
    """
    is_arrear: bool
    is_advance: bool
    is_continuous: bool

    annuity_rate: Rate 
    annuity_term: float
    annuity_amount: float
    norminal_period: float


    arrear_pv: float

    def __init__(self, annuity_rate: Rate, payment_mode: str= "arrear",  annuity_term: float= 1, annuity_amount: float= 1, norminal_period: float= 1, ):
        
        self.__set_payment_mode(payment_mode)

        self.annuity_rate = annuity_rate
        self.annuity_term = annuity_term
        self.annuity_amount = annuity_amount
        self.norminal_period = norminal_period
      

        self.arrear_pv = self.__to_arrear()


    def __set_payment_mode(self, payment_mode: str):
        """
            Sets the mode of payment. 
            Either arrear, continuous or advance.
        """
        payment_mode = payment_mode.lower().strip()
        if "arrear" in payment_mode:
            # set is_arrear flag to true
            self.is_arrear = True
            self.is_continuous = False
            self.is_advance = False

        elif "continuous" in payment_mode:
            # set is_continuous flag to true
            self.is_arrear = False
            self.is_continuous = True 
            self.is_advance = False

        elif ("due" in payment_mode) or ("advance" in payment_mode):
            # set is_advance flag to true
            self.is_arrear = False
            self.is_continuous = False
            self.is_advance = True
            
        else:
            # Error otherwise
            raise AssertionError(f"The payment mode {payment_mode} is invalid.\n\t\tThe valid payment modes are: 'arrear', 'continuous', 'advance'")


    def __validate_entries(self):
        """
            Validates varables values and raises errors where relevant. 
        """
        # rates should be compounding.


    def __to_arrear(self):
        """
            Returns the present value of an annuity arrear based on the provided properties.
            The value is set at the core arrear present value(arrea_pv).
        """

        arrear_pv = (1 - self.annuity_rate.time_value_factor(self.annuity_term, discount= True)) / self.annuity_rate.convert_to("compound interest", norminal_period= self.norminal_period)
        return arrear_pv


    def __get_pv_factor(self):
        """
            Returns the present value factor of an annuity.
            The annuity's factor will be multiplied by the present value (PV) of an arrear annuity to find the annuity's PV 
        """

        factor = None
        if self.is_arrear:
            # no factor is required for the annuity arrear.
            factor = 1

        elif self.is_continuous:
            # interest / foi
            factor = self.annuity_rate.convert_to("compound interest", norminal_period= self.norminal_period) / self.annuity_rate.foi
        
        elif self.is_advance:
            # interest / discount
            factor = self.annuity_rate.convert_to("compound interest", norminal_period= self.norminal_period) / self.annuity_rate.convert_to("compound discount", norminal_period= self.norminal_period)

        return factor
   

    def time_value(self, differ_rate: Rate= None, differ_period: float= 0, is_fv: bool= False):
        """
            Returns the time value based on the period and type of annuity
        """

        # find present value factors
        annuity_pv = self.arrear_pv * self.__get_pv_factor()

        # Differ the annuity. 
        if differ_rate == None:
            # initializing the defualt differ rate 
            differ_rate = self.annuity_rate
 

        elif not isinstance(differ_rate, Rate):
            # using assinged differ rate
            raise TypeError(f"The differ rate is invalid. It should be of type 'Rate' not {type(differ_rate)}.")

        annuity_pv *= differ_rate.time_value_factor(differ_period, discount= True)

        if is_fv:
            # get future value of the pv amount.
            annuity_pv *= self.annuity_rate.time_value_factor(self.annuity_term + differ_period)
        
        # Present value of the annuity
        annuity_pv *= self.annuity_amount

        return annuity_pv       
        
    













