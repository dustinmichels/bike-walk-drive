'''
modes.py
Constrcutors and methods for a Driver, Biker, and Walker class.
Each class initiates to 'average' values but can be customized
using setter methods.

-Each has a getCost method that returns the cost
of using that mode of transit in $/mile.

-Each has a getMPH method that returns the average speed
of that mode of transit (in MPH)

-Driver object has a getCO2 method that returns amnt
of CO2 used in lbs/mile

NOTE: Many of the setter methods that exist here are never used when
the GUI is run thru the graphMain module. Even though they are not used,
I left them in because I believe they are all functional and could easily be
used if a slightly more comprehensive GUI were implemented.
'''

class Driver:
    ''' The driver object knows and can set and return values related to
    calculations for the driver, including speed, cost, and CO2 emissions'''
    def __init__(self):
        '''Constructor set's default values for instance variables.'''
        # Default Values
        self.cat = "average"    # Category of car (others listed in dict below)
        self.miles = 13476.00   # Miles driven in a year (initialized US avg)
        self.MPH = 29.4         # Avg speed MN (infinitemonkeycorps.net)
        self.person = Person("driver")  # Used for determining calorie burn

        # Custom values
        # If any of these are set, costs will be recalcuated accordingly
        self.MPG = None         # Avg fuel economy, from EPA report
        self.gasPrice = None     # Price of gas ($/gal)
        self.gasSpend = None     # What you spend on gas ($/year)
        self.maintSpend = None   # What you spend on maintenance ($/year)
        self.tireSpend = None   # What you spend on tire ($/year)

        # Dictionary of info for different cateogies of car
        # {'Type':[gas($/mile), maintenance($/mile), tires ($/mile)], MPG}
        # Data from AAA's "Your driving costs" (2015)
        self.catDict = {'smallSedan':[.0918,.0468,.0068, 35.36], 'mediumSedan':
            [.1087,.0520,.0111, 30.10], 'largeSedan':[.1358,.0546,.0115, 23.72],
            'average':[.1121,.0511,.0098, 26.20], '4wdSport':
            [.1460,.0565,.0138, 21.00],'minivan':[.1365,.0519,.0084, 20,86]}

        # Dictionary that will hold cost in $/mile for
        # gas, maintenance, and tires for a given driver object
        self.costDict = {'gas':0,'maint':0,'tire':0}

        self.update()

    def reset(self):
        ''' Resets driver object to default values'''
        self.cat = "average"    # Category of car
        self.update()
        self.miles = 13476.00   # Miles driven in a year (initialized US avg)

        self.gasPrice = None     # Cost of gas ($/mile)
        self.MPG = None         # Fuel eff. of your car (miles/gal)
        self.gasSpend = None     # What you spend on gas ($/year)
        self.maintSpend = None   # What you spend on maintenance ($/year)
        self.tireSpend = None   # What you spend on tire ($/year)

        self.update()
        self.person.reset()

    def setCat(self, catInput):
        ''' Accepts a string represening one of the predefined categories of
        car as a parameter (smallSedan, mediumSedan, largeSedan, average,
        4wdSport, and minivan.) Sets the drivers 'cat' instance variable
        accordingly and then updates.'''
        self.cat = catInput
        self.update()

    def setGasPrice(self, gasPriceInput):
        ''' Accepts a gas price as input and adjusts driver object's instance
        variable accordingly, then updates. In the update function, the gas
        price is used to calculate the cost first. If the variable is set to
        None, gasSpend is used ($/year). If that is set to None, the defaults
        for the category of car are used.'''
        self.gasPrice = float(gasPriceInput)
        self.update()

    def setMPG(self, mpgInput):
        ''' Accepts a number representing the MPG the user gets and sets
        the self.MPG varibale accordingly.'''
        self.MPG = float(mpgInput)
        self.update()

    def setMiles(self, milesPerYearInput):
        ''' Accepts a number representing the number of miles the user
        drives in a year and sets the self.miles variable accordingly.'''
        self.miles = float(milesPerYearInput)
        self.update()

    def setGasSpend(self, gasSpendPerYearInput):
        ''' Accepts a number represetning the number of dollars
        a user spends on gas each year, and adjusts the driver object's
        gasSpend instance variable accordingly. The gasPrice variable
        is set to None, because the update function tries to determine
        what the driver spends on gas using the gasPrice variable first, and
        only if that is set to None does it try using the gasSpend variable.'''
        self.gasSpend = gasSpendPerYearInput
        self.gasPrice = None
        self.update()

    def setMaintSpend(self, maintSpendInput):
        ''' Accepts a number representing the dollar amount a user spends
        on maintenance each year, and adjust the driver object's
        maintSpend instance variable accordingly.'''
        self.maintSpend = float(maintSpendInput)
        self.update()

    def setTireSpend(self, tireSpendInput):
        ''' Acccepts a number representing the dollar amount a user spends
        on maintenance each year, and adjusts the driver object's
        tireSpend instance variable accordingly.'''
        self.tireSpend = float(tireSpendInput)
        self.setMiles()
        self.update()

    def update(self):
        ''' Updates the values stored in the costDict dictionary,
        which contains what the user spends on gas, maintenance,
        and tires. The values in this dictionary are summed
        together when the getCost fcn is called, to provide
        an overall cost in $ per mile.  Determines if custom values
        have been set, and if not, uses default values based on
        car category. '''
        # Set gas cost based on custom or default values
        if self.gasPrice:
            if self.MPG:
                self.costDict['gas'] = self.gasPrice/self.MPG
            else:
                self.costDict['gas'] = self.gasPrice/self.catDict[self.cat][3]
        elif self.gasSpend:
            self.costDict['gas'] = self.gasSpend/self.miles
        else:
            self.costDict['gas'] = self.catDict[self.cat][0]

        # Set maint cost based on custom or default values
        if self.maintSpend:
            self.costDict['maint'] = self.maintSpend/self.miles
        else:
            self.costDict['maint'] = self.catDict[self.cat][1]

        # Set tire cost based on custom or default values
        if self.tireSpend:
            self.costDict['tire'] = self.tireSpend/self.miles
        else:
            self.costDict['tire'] = self.catDict[self.cat][2]

    def getCost(self):
        ''' Returns the cost of driving the car object
            in $ per mile. '''
        return sum(self.costDict.values())

    def getCO2(self):
        ''' Returns the CO2 emissions that result
        from driving the car, in pounds per mile'''
        # (19.6 lbs CO2 /gal) / (miles/gal)
        if self.MPG:
            return 19.6 / self.MPG
        else:
            return 19.6 / self.catDict[self.cat][3]

    def getMPH(self):
        '''Returns the avg MPH for this mode of transit'''
        return self.MPH

class Biker:
    ''' The driver object knows and can set and return values related to
    calculations for the biker, including speed and cost.'''
    def __init__(self):
        ''' Constructor that builds biker object which keeps track of the amnt
        spent on bike in parts and maintenance (in $ / year) and number of miles
        biked per year, to determine cost of biking in $ per mile.
        Initial values based on report: http://www.vtpi.org/tca/tca0501.pdf'''
        self.spend = 100.00    # Maintenace and parts ($/year)
        self.miles = 1500.00   # miles biked / year
        self.MPH = 11.5        # Avg speed in city (Livestrong)
        self.person = Person("biker")

    def reset(self):
        ''' Set default values for biker object.'''
        self.spend = 100.00    # Maintenace and parts ($/year)
        self.miles = 1500.00   # miles biked / year
        self.MPH = 11.5        # Avg speed in city (Livestrong)
        self.person.reset()

    def setMiles(self, milesInput):
        ''' Takes in number and sets self.miles accordingly. This number
        represents the number of miles a user bikes in a year, and is used
        together with what they spend in a year to determine the cost
        per mile of biking.'''
        self.miles = float(milesInput)

    def setSpend(self, spendInput):
        ''' Takes a number and sets self.spend accordingly. This number
        represents the amt of $ a user spends in a year on parts and maintenance
        and is used together with how many miles they bike in a year to determine
        the cost per mile of biking.'''
        self.spend = float(spendInput)

    def getCost(self):
        ''' Returns cost per mile in $ for biking
        Based on cost of bike per year divided by miles biked in a year.'''
        return (self.spend/self.miles)

    def getMPH(self):
        '''Returns the avg MPH for this mode of transit'''
        return self.MPH

class Walker:
    ''' The driver object knows and can set and return values related to
    calculations for the walker, including speed and cost.'''
    def __init__(self):
        ''' Constructor that builds walker object which keeps track of the amt
        spent on new shoes and number of miles walked before replacing shoes.
        Initial values based on: http://www.vtpi.org/tca/tca0501.pdf'''
        self.spend = 37.5   # Cost of new pair of shoes ($/shoe)
        self.miles = 1000.0 # Number of miles walked before shoes are replaced
        self.MPH = 3.25     # Avg speed (the-fitness-walking-guide.com/)
        self.person = Person("walker") # Used to determine calorie burn

    def reset(self):
        ''' Reset default values.'''
        self.spend = 37.5   # Cost of new pair of shoes ($/shoe)
        self.miles = 1000.0 # Number of miles walked before shoes are replaced
        self.MPH = 3.25     # Avg speed (the-fitness-walking-guide.com/)
        self.person.reset()

    def setMiles(self, milesInput):
        ''' Takes in a number of miles and sets self.miles accordingly.
        These value is the number of miles the user walks before buying a
        new pair of shoes.'''
        self.miles = float(milesInput)

    def setSpend(self, spendInput):
        ''' Takes in a value representing how much the user spends on a new
        pair of walking shoes and sets self.spend accordingly.'''
        self.spend = float(spendInput)

    def getCost(self):
        ''' Returns cost per mile in $ for walking
        Based on cost of new shoes divided by miles walked until buying shoes'''
        return self.spend/self.miles

    def getMPH(self):
        '''Returns the avg MPH for this mode of transit'''
        return self.MPH

class Person:
    ''' The person object is used to calculate calories. The driver, biker,
    and walker objects each create an instance of the person object, and pass
    'driver', 'biker', or 'walker', into the constructor as the mode of
    transit. The mode is used to determine the person object's activity level
    (no, light, or moderate), which gets used in conjunction with sex, weight,
    height, and age, to determine a amount of calories burned per hour (using
    the Harris–Benedict equation).
    '''
    def __init__(self, mode):
        ''' Constructor for person object. The mode parameter refers
        to the mode of transit and expects either 'driver', 'biker' or
        walker.'    '''
        # Initiates to an avg adult US male, based on figures at
        # http://pediatrics.about.com/
        self.sex = "M"
        self.weight = 195.5 # Avg adult US male weight (lbs)
        self.height = 69.3  # Avg adult US male height (in)
        self.age = 21
        # Mode (should be driver, biker, walker)
        self.mode = mode
        # Activity level (initail value set based on mode)
        self.actLevel = self.getDefaultActLevel()

    def reset(self):
        ''' Resets person object to default values by calling
        the setSex fcn with the parameters 'M' and True.'''
        self.setSex('M',True)

    def setSex(self, sexInput, andDefaults):
        ''' Accepts a sex (M or F) and a boolean value for andDefaults.
        If andDefaults is false, then only sex is changed. If andDefaults is
        True, then sex is changed and the default weight, height, and
        age for that sex are also set. Defauts are based average found here:
        http://pediatrics.about.com/cs/growthcharts2/f/avg_ht_female.htm
        http://pediatrics.about.com/cs/growthcharts2/f/avg_ht_male.htm
        http://pediatrics.about.com/cs/growthcharts2/f/avg_wt_female.htm
        http://pediatrics.about.com/cs/growthcharts2/f/avg_wt_male.htm
        '''
        if sexInput == 'M' or sexInput == 'F':
            self.sex = sexInput
        else:
            print('Error!')

        if andDefaults == True:
            if self.sex == 'M':
                self.weight = 195.5 # Avg weight US adult M (lbs)
                self.height = 69.3  # Avg height US adult M (in)
                self.age = 21
            elif self.sex == 'F':
                self.weight = 162.9 # Avg weight US adult F (lbs)
                self.height = 63.8  # Avg height US adult F (in)
                self.age = 21
            else:
                print("Error!")

    def setWeight(self, weightInput):
        ''' Accepts user's weight and sets instance variable accordingly.'''
        self.weight = float(weightInput)

    def setHeight(self, heightInput):
        ''' Accepts user's height and sets instance variable accordingly.'''
        self.height = float(heightInput)

    def setAge(self, ageInput):
        ''' Accepts user's age and sets instance variable accordingly.'''
        self.age = float(ageInput)

    def setActLevel(self, level):
        ''' Customize activity level to be no, light, moderate, or heavy.'''
        if (level == "no" or level == "light" or level=="moderate"
                        or level=="heavy"):
            self.actLevel = level
        else:
            print ("Error!")

    def getDefaultActLevel(self):
            ''' Uses the mode of the person object (drivr, biker, walker)
            to determine the object's activity level (no, moderate, or light,
            respectively.) Acitivity level can be customized using the setActLevel
            method, for example, if the user bikes at a leisurely pace they could
            change actLevel to light for the biker's instance of the person
            class. This fcn is used to set default values. '''
            if self.mode == "driver":
                return "no"
            elif self.mode == "biker":
                return "moderate"
            elif self.mode == "walker":
                return "light"
            else:
                print ("Error!")

    def getBMR(self):
        ''' Determines basal metabolic rate (BMR) using
        Harris–Benedict equation. This is the amount of resting calories
        a person burns in a day.'''
        if self.sex == 'M':
            BMR = 66+(6.23*self.weight)+(12.7*self.height)-(6.76*self.age)
        elif self.sex == 'F':
            BMR = 655.1+(4.35*self.weight)+ (4.7*self.height)-(4.7*self.age)
        else:
            print("Error!")
        return BMR

    def getCal(self):
        ''' Determines total calorie burn (cal/hour) using basal
        metabolic rate (BMR) and a multiplier determined by activity level.
        The product is divided by 24 to go from cal/day to cal/hour units.'''
        if self.actLevel == "no":
            # Acitivity multiplier for little or no exercise
            calorieBurn = (1.2*self.getBMR()) / 24
        elif self.actLevel == "light":
            # Acitivity multiplier for light exercise
            calorieBurn  = (1.375*self.getBMR()) / 24
        elif self.actLevel == "moderate":
            # Acitivity multiplier for moderate exercise
            calorieBurn = (1.55*self.getBMR()) / 24
        elif self.actLevel == "heavy":
            # Acitivity multiplier for heavy exercise
            calorieBurn = (1.725*self.getBMR()) / 24
        else:
            print("Error!")
        return calorieBurn
