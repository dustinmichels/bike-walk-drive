'''
graphMain.py
Driver, Biker, and Walker objects from the modes module
are used here to calculate appropriate time, cost, calorie burn, and CO2
information for various simulated trips. Matplotlib is used to display
information graphically and gather user input.

Some of the code here is based on tutorials and demos found online here:
http://people.duke.edu/~ccc14/pcfb/numpympl/MatplotlibBarPlots.html
http://matplotlib.org/examples/index.html
https://pythonprogramming.net/matplotlib-intro-tutorial/

Most of the code here has been highly modified and customized from those
examples, but where my code closely resembles another's it is clearly noted.
'''
from modes import *
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons, Button
from matplotlib.figure import Figure

plt.xkcd()  # Styles the graphing window in the xkcd style!!
mpl.rcParams['toolbar'] = 'None'    # Disables matplotlib toolbar

class RunSim:
    ''' This class is the core of the program. It uses matplotlib to gather
    user input and dispaly results, and also preforms requisite calculations.'''

    def __init__(self):
        ''' The constructor creates instances of the walker, biker, and driver
        objects from the 'modes' module, sets a default distance and trip
        number, and then calculates the time, cost, calories,
        and CO2 emissions for all modes of tranit. Then it sets up graphs
        for displaying the information, as well as sliders, buttons, and
        RadioButtons for gathering user input. The functions that those
        buttons execute are defined internally.
        '''
        # Create instances of the driver, biker, and walker objects
        # Whose instance variables will be used heavily in calculations.
        self.d = Driver()
        self.b = Biker()
        self.w = Walker()

        # Default vaulues
        self.dist = 1
        self.trips = 1

        # Do initial calculations (calcualte returns calcDict)
        self.calcDict = self.calculate()

        # Create figure object which we will place everything on
        # of dimensions 14" by 10"
        self.fig = plt.figure(figsize=(14,10))

        # Create 4 axes objects evenly spaced in a column. These will
        # hold the four graphs/figures (time, cost, calories, and CO2.)
        self.ax1 = self.fig.add_subplot(411)
        self.ax2 = self.fig.add_subplot(412)
        self.ax3 = self.fig.add_subplot(413)
        self.ax4 = self.fig.add_subplot(414)

        # Adjust the location of subplots (the axes holding graphs)
        self.fig.subplots_adjust(left = .74, right = .94, bottom = .18,
                    top=.98,hspace=.25)

        ### Set up Buttons, RadioButtons, Sliders and their fcns! ###

        # The structure of setting up the temporary rax axes, then making
        # the RadioButton, then defining it's function, then adding the
        # on_clicked statement is taken from this example:
        # http://matplotlib.org/examples/widgets/radio_buttons.html

        axcolor = 'lightgoldenrodyellow'

        def getRadioPosList(ax):
            ''' This function is simply for positioning the 4 radio buttons
            used to change units approporatiely, vertically centered in
            relation to the adjacent graph. '''
            # Width and height are the same for each radio button
            widthRax = 0.12
            heightRax = 0.10

            # Find the lower (left) x value of adjacent graph
            # And construct appropriate x value for radio axes
            x0Ax = ax.get_position().get_points()[0,0]
            xRax = x0Ax - (widthRax*1.8)

            # Find lower and upper y values of the adjacent graph,
            # average them, and add half the height of the radiobutton axes
            # to determine a y value that will vertically center the radiobutton
            y0Ax = ax.get_position().get_points()[0,1]
            y1Ax = ax.get_position().get_points()[1,1]
            yRax = ((y0Ax+y1Ax)/2) - (heightRax/2)

            return [xRax, yRax, widthRax, heightRax]

        # Unit Change RadioButton 1: Change Time Units
        rax = plt.axes(getRadioPosList(self.ax1), axisbg=axcolor)
        self.radioTime = RadioButtons(rax, ('Hours', 'Minutes', 'Audiobooks'))
        def timeChange(label):
            self.updateGraph()
            plt.draw()
        self.radioTime.on_clicked(timeChange)

        # Unit Change RadioButton 2: Change Money Units
        rax = plt.axes(getRadioPosList(self.ax2), axisbg=axcolor)
        self.radioCost = RadioButtons(rax, ('Dollars', 'Coffees'))
        def costChange(label):
            self.updateGraph()
            plt.draw()
        self.radioCost.on_clicked(costChange)

        # Unit Change RadioButton 3: Change calorie burn units
        rax = plt.axes(getRadioPosList(self.ax3), axisbg=axcolor)
        self.radioCal = RadioButtons(rax, ('Cal (total)', 'Cal (/hour)'))
        def calChange(label):
            self.updateGraph()
            plt.draw()
        self.radioCal.on_clicked(calChange)

        # Unit Change RadioButton 4: Change CO2 Emissions Units
        rax = plt.axes(getRadioPosList(self.ax4), axisbg=axcolor)
        self.radioCO2 = RadioButtons(rax, ('CO2 (lbs)', 'CO2 (trees)'))
        def CO2Change(label):
            self.updateGraph()
            plt.draw()
        self.radioCO2.on_clicked(CO2Change)

        # Sliders 1 and 2: Distnace and Number of Trips
        # Axes and instance of slider for distance control
        axslideDist = plt.axes([0.17, 0.10, 0.77, 0.03], axisbg=axcolor)
        self.slideDist = Slider(axslideDist, 'Distance (miles)', 0.0, 100.0,
                    valinit=self.dist, valfmt='%4.2f')
        # Axes and instance of slider for number of trips control
        axslideTrip = plt.axes([0.17, 0.05, 0.77, 0.03], axisbg=axcolor)
        self.slideTrip = Slider(axslideTrip, 'Trips', 0.0, 100.0,
                    valinit=self.trips, valfmt='%4.2f')
        # Function for updating values after either slider is moved.
        def sliderUpdate(val):
            self.trips = self.slideTrip.val
            self.dist = self.slideDist.val
            self.calcDict = self.calculate()
            self.updateGraph()
        self.slideTrip.on_changed(sliderUpdate)
        self.slideDist.on_changed(sliderUpdate)

        axcolor = 'gold'

        # Customization RadioButton 1: Car - Car Type
        rax = plt.axes([.06, .72, .15, 0.2], axisbg=axcolor)
        rax.text(0, 1.15, "Customize Driving Info", fontsize=11)
        rax.text(0,1.05, "Car Type", fontsize=11)
        self.radioCarType = RadioButtons(rax, ('Average','Small Sedan',
            'Medium Sedan', 'Large Sedan', '4WD/Sport',
            'Minivan'))
        def carTypeChange(label):
            ''' Adjusts instance of driver object based on the category selected
            using the driver object's setCat function.'''
            if label == 'Average':
                self.d.setCat('average')
            elif label == 'Small Sedan':
                self.d.setCat('smallSedan')
            elif label == ('Medium Sedan'):
                self.d.setCat('mediumSedan')
            elif label == 'Large Sedan':
                self.d.setCat('largeSedan')
            elif label == '4WD/Sport':
                self.d.setCat('4wdSport')
            elif label == 'Minivan':
                self.d.setCat('minivan')
            else:
                print('Error!')
            self.updateGraph()
            plt.draw()
        self.radioCarType.on_clicked(carTypeChange)

        # Customization RadioButton 2: Bike - Spend on Bike
        rax = plt.axes([.26, .72, .15, 0.2], axisbg=axcolor)
        rax.text(0, 1.15, "Customize Biking Info:", fontsize=11)
        rax.text(0,1.05, "Spend on parts/maintenance ($/year)", fontsize=11)
        self.radioBikeSpend = RadioButtons(rax, ('$0-25','$25-50',
            '$50-100', '$100-150', '$150-200', '>$200'), active=2)
        def bikeSpendChange(label):
            ''' Adjusts instance of biker object based on selected spending,
            using the biker object's setSpend fcn. Then updates graph.'''
            if label == '$0-25':
                self.b.setSpend(12.5)
            elif label == '$25-50':
                self.b.setSpend(37.5)
            elif label == '$50-100':
                self.b.setSpend(75)
            elif label == ('$100-150'):
                self.b.setSpend(125)
            elif label == '$150-200':
                self.b.setSpend(175)
            elif label == '>$200':
                self.b.setSpend(250)
            else:
                print('Error!')
            self.updateGraph()
            plt.draw()
        self.radioBikeSpend.on_clicked(bikeSpendChange)

        # Customization RadioButton 3: Walk - Spend on Shoes
        rax = plt.axes([.06, .424, .15, 0.2], axisbg=axcolor)
        rax.text(0, 1.15, "Customize Walking Info:", fontsize=11)
        rax.text(0,1.05, "Spend on a new pair of shoes", fontsize=11)
        self.radioWalkSpend = RadioButtons(rax, ('$0-25','$25-50',
            '$50-100', '$100-150', '$150-200', '>$200'), active=1)
        def walkSpendChange(label):
            ''' Changes instance of walker object based on spending.'''
            if label == '$0-25':
                self.w.setSpend(12.5)
            elif label == '$25-50':
                self.w.setSpend(37.5)
            elif label == '$50-100':
                self.w.setSpend(75)
            elif label == ('$100-150'):
                self.w.setSpend(125)
            elif label == '$150-200':
                self.w.setSpend(175)
            elif label == '>$200':
                self.w.setSpend(250)
            else:
                print('Error!')
            self.updateGraph()
            plt.draw()
        self.radioWalkSpend.on_clicked(walkSpendChange)

        # Customization RadioButton 4: Person - Sex
        rax = plt.axes([.26, .424, .15, 0.2], axisbg=axcolor)
        rax.text(0, 1.15, "Customize Calorie Burn Info:", fontsize=11)
        rax.text(0,1.05, "Sex", fontsize=11)
        self.radioPersonSex = RadioButtons(rax, ('Male','Female'), active=0)
        def personSexChange(label):
            ''' Changes the sex of the person instance of the current instnace
            of the driver, biker, and walker objects. So much OOP!!!!'''
            if label == 'Male':
                self.d.person.setSex('M', True)
                self.b.person.setSex('M', True)
                self.w.person.setSex('M', True)
            elif label == 'Female':
                self.d.person.setSex('F', True)
                self.b.person.setSex('F', True)
                self.w.person.setSex('F', True)
            else:
                print('Error!')
            self.updateGraph()
            plt.draw()
        self.radioPersonSex.on_clicked(personSexChange)

        # Reset Button
        axReset = plt.axes([0.17, 0.25, 0.15, 0.10])
        bReset = Button(axReset, 'Reset Defaults')
        def resetDefaults(event):
            ''' Resets all buttons/sliders to their default position,
            which triggers recalculations and redrawing of the
            graphs. This function is a little slow.'''
            self.slideDist.set_val(1)
            self.slideTrip.set_val(1)
            self.radioTime.set_active(0)
            self.radioCost.set_active(0)
            self.radioCal.set_active(0)
            self.radioCO2.set_active(0)
            self.radioCarType.set_active(0)
            self.radioBikeSpend.set_active(2)
            self.radioWalkSpend.set_active(1)
            self.radioPersonSex.set_active(0)
            plt.draw()
        bReset.on_clicked(resetDefaults)

        # These keep the current drawing current.
        self.updateGraph()
        plt.show()

    def calculate(self):
        ''' This function does all the calculating behind the program. It uses
        attributes of the driver, walker, and biker object's to calculate
        values for time, cost, calorie burn, and CO2 emitted in various units.
        This information is stored in the handy-dandy dictionary: calcDict.'''

        # Dictionary that holds calculations for different categories in the form
        # of lists, where [0]=driver, [1]=biker, [2]=walker
        calcDict = {'time':[],'cost':[], 'cal':[],'time-mins':[], 'time-audio':[],
        'cost-coffee':[], 'cal-hour':[], 'cal-sansBMR':[],
        'CO2':0.0, 'CO2-tree':0.0}

        # Time in hours
        calcDict['time'].append(self.dist*self.trips / self.d.getMPH())
        calcDict['time'].append(self.dist*self.trips / self.b.getMPH())
        calcDict['time'].append(self.dist*self.trips / self.w.getMPH())

        # Cost in US dollars
        calcDict['cost'].append(self.d.getCost()*self.dist*self.trips)
        calcDict['cost'].append(self.b.getCost()*self.dist*self.trips)
        calcDict['cost'].append(self.w.getCost()*self.dist*self.trips)

        # Total calories burned
        calcDict['cal'].append(self.d.person.getCal()*calcDict['time'][0])
        calcDict['cal'].append(self.b.person.getCal()*calcDict['time'][1])
        calcDict['cal'].append(self.w.person.getCal()*calcDict['time'][2])

        ## Alternative units for above categories

        # Time in audiobooks (based on avg len of 12.59 hours)
        # Note: avg length determined from sample of 25 bestsellers on Audible.com
        calcDict['time-mins'].append(calcDict['time'][0]*60)
        calcDict['time-mins'].append(calcDict['time'][1]*60)
        calcDict['time-mins'].append(calcDict['time'][2]*60)

        # Time in audiobooks (based on avg len of 12.59 hours)
        # Note: avg length determined from sample of 25 bestsellers on Audible.com
        calcDict['time-audio'].append(calcDict['time'][0]/12.59)
        calcDict['time-audio'].append(calcDict['time'][1]/12.59)
        calcDict['time-audio'].append(calcDict['time'][2]/12.59)

        #Cost in terms of coffee at blue Mondays burned per hour
        calcDict['cost-coffee'].append(calcDict['cost'][0]/2.60)
        calcDict['cost-coffee'].append(calcDict['cost'][1]/2.60)
        calcDict['cost-coffee'].append(calcDict['cost'][2]/2.60)

        #Cal burned per hour
        calcDict['cal-hour'].append(self.d.person.getCal())
        calcDict['cal-hour'].append(self.b.person.getCal())
        calcDict['cal-hour'].append(self.w.person.getCal())

        # CO2 emissions in lbs
        calcDict['CO2'] = self.d.getCO2()*(self.dist*self.trips)

        # CO2 emissions in terms of trees planted
        # A single tree planted thru americanforests.org sequesters 911 pounds of CO2
        # This value reflects the number of trees one should plant to sequester the carbon
        # emitted by driving
        calcDict['CO2-tree'] = (calcDict['CO2'] / 911)

        return calcDict

    def makeGraph(self, ax, data, ylab):
        ''' makeGraph is called by updateGraph and redraws the 3 graphs
        every time it is called. The x labels are always the same but the
        y values are passed in as 'data'. '''

        ax.clear()

        N = 3                   # 3 divisions of x axis
        maxNum = max(data)      # determine max y value

        ind = np.arange(N)      # the x locations for the groups
        width = 0.5             # the width of the bars

        ## the bars
        rects1 = ax.bar(ind, data, width, color=['cyan','yellow','magenta'])

        # axes and labels
        ax.set_xlim(-.1,len(ind)-.4)
        ax.set_ylim(0,maxNum+(maxNum/10)*2)

        xTickMarks = ['Drive','Bike','Walk']
        ax.set_xticks(ind+(width/2))
        xtickNames = ax.set_xticklabels(xTickMarks)
        ax.set_ylabel(ylab)

        def autolabel(rects):
            ''' Adds labels above bars. Code adapted from matplotlib demo code:
            http://matplotlib.org/examples/api/barchart_demo.html'''
            # attach some text labels
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                        '%4.2f' % (height), fontsize=11,
                        ha='center', va='bottom')

        autolabel(rects1)

    def showInfo(self, ax, data, msg):
        ''' The forth subplot (axes) holds text instead of a bar plot
        and it gets updated using this function.'''

        # Erase any existing information to avoid redrawing
        ax.clear()

        # Remove labels
        ax.set_xticklabels('')
        ax.set_yticklabels('')

        ax.text(.08, .70, "By not driving...", fontsize=11)

        ax.text(.4, .45, '%4.2f' % (data), style='italic',
            bbox={'facecolor':'lightgreen', 'alpha':0.65, 'pad':10})
        ax.text(.08, .20, msg, fontsize=11)

    def updateGraph(self):
        ''' This is called whenever the graph needs to be updated. It calls
        self.calculate to make sure self.calcDate is up to date and it uses
        the values of the radio buttons and sliders as well as the values stored
        in calcDict to determine which y values to pass into makeGraph to
        make the 3 graphs and which values to pass to showInfo.'''

        self.calcDict = self.calculate()

        if self.radioTime.value_selected == 'Hours':
            self.makeGraph(self.ax1, self.calcDict['time'], 'Time (Hours)')
        elif self.radioTime.value_selected == 'Minutes':
            self.makeGraph(self.ax1, self.calcDict['time-mins'], 'Time (Minutes)')
        elif self.radioTime.value_selected == 'Audiobooks':
            self.makeGraph(self.ax1, self.calcDict['time-audio'], 'Time (Audiobooks)')

        if self.radioCost.value_selected == 'Dollars':
            self.makeGraph(self.ax2, self.calcDict['cost'], 'Cost ($)')
        elif self.radioCost.value_selected == 'Coffees':
            self.makeGraph(self.ax2, self.calcDict['cost-coffee'], 'Cost (Coffees)')
        else:
            print('Error!')

        if self.radioCal.value_selected == 'Cal (total)':
            self.makeGraph(self.ax3, self.calcDict['cal'], 'Calories (total)')
        elif self.radioCal.value_selected == 'Cal (/hour)':
            self.makeGraph(self.ax3, self.calcDict['cal-hour'], 'Calories (/hour)')
        else:
            print('Error!')

        if self.radioCO2.value_selected == 'CO2 (lbs)':
            self.showInfo(self.ax4, self.calcDict['CO2'], 'Pounds of CO2 not emitted')
        elif self.radioCO2.value_selected == 'CO2 (trees)':
            self.showInfo(self.ax4, self.calcDict['CO2-tree'], 'Trees planted!')
        else:
            print('Error!')

def main():
    ''' The main function (and the bit of code beneath)
    makes the program runable from the command line
    by simply typing the name of this module. All the function does is create
    a new instance of the RunSim class, which will build and keep live
    the matplotlib window, graphs, and user interface.'''

    newSim = RunSim()

if __name__ == "__main__":
    main()
