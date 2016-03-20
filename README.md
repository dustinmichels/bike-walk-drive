# bike-walk-drive
A rudimentary python program that allows a user to gain insights into time, cost, calorie burn, and CO2 emissions related to walking, biking, or driving a given distance. Accepts some user input and utilizes matplotlib.


1. Background

Climate change is already posing a major threat to homes, communities, and food system across the world. As the threat worsens, it is important that we continue searching for ways to reduce our personal and societal CO2 emissions. The cars we drive are a major source of our personal CO2 emissions. By choosing to walk or bike instead of drive we can reduce our CO2 emissions, but doing so does not always feel like a viable option because it would take longer.

The cost of walking or biking is obvious, but the benefits are sometimes less evident. Biking or walking provides exercise which the traveler does not get by driving, and thus confers a health benefit. Additionally, walking or biking tends to be cheaper since the traveler does not have to pay for gas or the wear and tear on the car. And while walking or biking will likely take longer (though this is not always the case!) there are circumstances where that extra time might feel like a gift rather than a sacrifice. For example, if one listened to audiobooks while walking, the time might feel productive and enjoyable rather than “wasted.”


2. Using the Program

This project allows users to gain a fuller picture about the implications of walking, biking, or driving a given distance and given number of times. They are graphically presented with numbers relaying the time, cost, calorie burn, and CO2 emissions related to each mode of transportation. And they are able to put the figures into alternative units that might make the numbers more compelling and meaningful. Additionally they are enabled some ability to customize the data analysis by entering the type of car they drive, how much they spend on shoes when the old ones wear down, how much they spend on bike parts and maintenance each year, and their sex. Ideally much more customization would be possible.

If python3 and matplotlib are present on the computer, the program should be executable simply by entering into the console:
>> python3 graphMain.py


3. Program Organization

The program is organized into two modules: graphMain.py and modes.py. The modes.py module contains a biker, walker, driver, and person class. These classes are used to keep track of, change, and retrieve data needed to make the program’s core calculations (cost, time, calories, and CO2 emissions for a given distance.) The biker, walker, and driver object each create their own instance of a person object. The graphMain.py contains a main() function and a RunSim class. The RunSim class constructs instances of the walker, biker, and driver objects. It uses matplot to create graphs as well as sliders, buttons, and radio-buttons used to gather user input, and has functions to modify its walker, biker, and driver objects, calculate relevant values, and visually represent those values.


4. Data Analysis

—COST—
The driver, biker, and walker object each have a getCost() method which returns a $/mile value based on current instance variables.

Driver
The cost of driving is determined by summing a $/mile cost for gas, tires, and maintenance. The AAA releases an annual report titled “Your Driving Costs” which lists these costs for different vehicle types. By default we use an “average” car, whose costs are 11.21 cents per mile for fuel, 5.11 cents per mile for maintenance, and 0.98 cents per mile for tires. We can change to a different type of car using the radio buttons. In the Driver class there are also methods for setting custom values for how much gas costs in your area, how much you spend on gas in a year, how much you spend on tires in a year, how much you spend on maintenance in a year, and how many miles you drive in a year, and how many MPG your vehicle gets. If any of these values are set, a better $/mile estimate can be calculated. For example, the gas cost ($/mile) could be calculated by dividing gas price by MPG. (See the driver’s update() function for all equations.) There is currently no way to customize these values from the user interface.

Biker
The cost of driving is determined by dividing what the user spends on parts and maintenance each year by the number of miles they bike each year. By default we use $100 a year and 14000 miles a year, but these values can be changed with setter methods.

Walker
The cost of walking is based on the cost of a new pair of shoes when the old ones get worn out. By default, we spend $37.5 on a new pair of shoes every 1000 miles, but these values can be changed. To get the cost, we divide the price of the shoes by the number of miles.

Alternative Units (coffee)
The cost is also calculated in units of fancy coffee drinks, by dividing by $2.60.

—TIME—
The time each mode of transit takes is found simply by multiplying MPH by the number of miles. By default, the driver goes 29.4 MPH (the average in Minneapolis according to infinitemonkeycorps.net). The biker goes 11.5 MPH (based on an article on livestrong.com) and the walker goes 3.25 MPH (based on an article on the-fitness-walking-guide.com)

Alternate Units (Audiobooks)
We also convert time from hours to audiobooks. To do this, I measured the mean duration of audiobooks from a sample of 25 bestselling books on audible.com. The average is 12.58 hours. So we divide time by 12.58 to get the time in audiobooks.

—CALORIES—
To determine calories burned, we use the Harris–Benedict equation, which uses a person’s sex, height, age, and weight, to determine their basal metabolic rate (BMR). This is the amount of calories they burn in a day just by existing (aka resting calorie burn). Then the BMR is multiplied by an activity multiplier to find the number of calories burned in a day taking into account exercise. We achieve this by using a Person object, which has attributes like sex, height, weight, and activity level. The biker, walker, and driver all create their own instance of the person object, set to the appropriate activity level. (none for driver, light for walker, and moderate for biker.) The resulting value is divided by 24 to give the calorie burn per hour rather than per day. The information can be displayed graphically either as calorie burn per hour or total calorie burn, where we multiply calories burned per hour by hours.

—CO2—
The CO2 is presented differently than the other measurements, since it really only pertains to driving. The default unit is lbs of CO2 not emitted by refraining from driving. This is calculated by calling the getCO2() method of the Driver object, which returns 19.6 divided by the MPG of the car. The 19.6 comes from an EPA spreadsheet relaying the formulas behind their “Green House Gas Calculator”. (Spreadsheet included in the data folder.) It is an estimate of the lbs of CO2 emitted per gallon of fuel burned. The result of this function call is multiplied by the distance traveled (dist*trips) in the calculate function of the RunSim object.
  
Alternative Units (Trees Planted)
A more compelling way to think about CO2 emissions prevented is the equivalent number of trees planted. That is to say, planting a given number of trees will sequester the CO2 equal to not driving that distance. Using data from the American Forests website, under the “Carbon Calculator Assumptions and Sources” we attain the number 911, the lbs of CO2 sequestered by a single tree. So lbs of CO2 is converted to trees planted by dividing by 911.


5. Sources

—COST—
Driving
“Your Driving Costs”, AAA (in folder)
http://publicaffairsresources.aaa.biz/resources/yourdrivingcosts/index.html

Biking and Walking (in folder)
“Transportation Cost and Benefit AnalysisII–Vehicle Costs”, Victoria Transport Policy Institute http://www.vtpi.org/tca/tca0501.pdf

—TIME—
Driving
29.4 mph (in Minneapolis)
http://infinitemonkeycorps.net/projects/cityspeed/city.html?city=minneapolismn 

Biking
11.5 mph (in city)
http://www.livestrong.com/article/413599-the-average-bike-riding-speed/ 

Walking
3.25 mph
http://www.the-fitness-walking-guide.com/average-walking-speed.html

Audiobooks
12.58 hours
Based on sample of 25 bestselling audiobooks on Audible.com, see spreadsheet in Data folder.

—CALORIES—

AVG HEIGHT/WEIGHT
Person - Male Sex
http://pediatrics.about.com/cs/growthcharts2/f/avg_ht_male.htm
http://pediatrics.about.com/cs/growthcharts2/f/avg_wt_male.htm

Person- Female Sex
http://pediatrics.about.com/cs/growthcharts2/f/avg_ht_female.htm
http://pediatrics.about.com/cs/growthcharts2/f/avg_wt_female.htm

CALORIE BURN CALCULATION
https://en.wikipedia.org/wiki/Harris%E2%80%93Benedict_equation

—CO2—
MPG
Spreadsheet (in folder)
Calculated using the same sampling methodology as AAA

Lbs
“Green House Gas Calculator”, EPA (in folder) http://www3.epa.gov/carbon-footprint-calculator/

Trees
“Carbon Calculator Assumptions and Sources”, American Forests http://www.americanforests.org/assumptions-and-sources/#carbon
