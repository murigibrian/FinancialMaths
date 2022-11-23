# FinancialMaths objects 
Objects and methods in the module comprise of the following.

## FinancialMaths.Rate 

`FinancialMaths.Rate(raw_rate, nominal_period=  1, is_foi=  False,  is_discount=  False,  is_simple=  False )` [[source]](https://github.com/murigibrian/FinancialMaths/blob/main/src/FinancialMaths_murigibrian/InterestRates.py)

Above is a constructor for the Rate object with which one can obtain the discounting or accumulating factor. 

The attributes of the rate (discounting or accumulating) are fed in then an effective interest rate is generated. When the time value factor is required, the generated effective interest rate is reconverted to the required rate.  A similar idea is implemented for simple and nominal rates. This is done to ensure a single function can be called to provide the time value factor irrespective of the interest rate's profile. 

**Parameters**
- **raw_rate: float** 
The direct rate as a decimal value.  
- **norminal_period: float**
The amount of periods until the interest is gained. 
- **is_foi: bool**
Is the raw rate a force of interest or otherwise (accumulating or discounting)?
- **is_simple: bool**
Is the raw rate a simple interest rate or otherwise (compounding)?
- **is_discount: bool**
Is the raw rate a discounting rate or otherwise (accumulating or force of interest)?

**Returns**
Rate object. 

**Methods**
* `time_value_factor( self, period, discount=  False )`

Returns the time value factor (a float) for the Rate object. The `period` parameter sets the number of effective periods for which the rate is enforced. Should a discounting factor be required change `discount` to `True`.
* `convert_to(self, to, nominal_period=  1)`

One may need to find a nominal rate that would provide the same accumulated (or discounted) value as some effective rate. `convert_to` method accepts the `nominal_period` parameter (a float) that assists in the same.

**Properties**
* is_simple_rate 
* is_foi
* is_discount_rate 
* interest_rate 
* discount_rate
* foi 
