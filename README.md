# FinStats
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
#### Video Demo: https://youtu.be/hs_t3B6dDh8

#### A query engine for generating financial statistics for a selected stock listed on Yahoo Finance, such as Standard Deviation, Variance, Skewness for a user-specified period. The program also displays a histogram, with a distribution curve, and a simple line graph of closing prices for that said period. An option to save as pdf is also provided. Examples of which can be found [here](https://github.com/alfarasjb/Stocks-In-A-Nutshell/tree/main/exports).

![hist](https://github.com/alfarasjb/FinStats/blob/main/screenshots/hist.png)

_summary with histogram plot_


![prc](https://github.com/alfarasjb/FinStats/blob/main/screenshots/prc.png)

_summary with price plot_

#### **OBJECTIVE**
Generate a user-friendly query engine for providing financial statistics and figures for financial instruments to provide a quantitative overview to aid in arriving at profitable investment and trading decisions.


#### **MAIN LIBRARIES AND IMPORTS**
1. _customtkinter_ - UI Library
2. _pandas_ - Data Wrangling
3. _numpy_ - Calculations
4. _scipy_ - Calculations
5. _yfinance_ - Financial Data
6. _matplotlib_ - Data Visualization
7. _seaborn_ - Data Visualization
8. _fpdf_ - Exporting

#### **MAIN OPERATION**
1. Takes 2 inputs from the user: Symbol and Sample Size
2. Requests data from Yahoo Finance.
3. Calculates statistical summary using numpy, and scipy. 
4. Generates a histogram, distribution, and price plot using Matplotlib and Seaborn
5. Displays calculated data, and figures, which can be summarized into a PDF File. 

#### **DESIGN PHILOSOPHY**
The main focus in terms of UI design is simplicity and convenience, hence the main priority was to build a UI where all essential information would be visible immediately. 

Building the input fields as well as the summary was a straight-forward approach, due to it being mostly text-elements.

Initially, a "gallery" style was to be tested for showing multiple figures, allowing the user to scroll through, as if, navigating through a photo-gallery. Ultimately, a tabview was implemented with the CustomTkinter library. 


#### **CHALLENGES, ISSUES, AND RESOLUTIONS** 
**Data Availability vs Time Complexity**

One main decision point which was critical to the overall quality of the program was to decide on the methodology of fetching, and slicing data for calculation. Two options were available:

1. Fetch data by calculating start date and end date using the *timedelta* function
2. Fetch all, and slice using the *tail* function. 

The latter, despite the cost of time complexity, was chosen to ensure the availability of requested data, as opposed to the former, whereby specifying date and time, does not account for the time when markets are closed, therefore creating a mismatch between specified sample size, and actual, received data. 

**Download Time** 

One major hurdle during testing was the download time from fetching data from Yahoo Finance. Initially, the fetch button triggers the external download function directly. Doing so, would freeze the app completely, rendering it unusuable until download is completed. 

The first attempted resolution was by using a Thread. However, creating a thread within the App's Main Class, raises a RuntimeError. The issue was resolved by triggering an external thread, which starts the entire download tree, instead of addressing it directly. Consequently, instead of returning values from the *build_data* function, it instead, sets the values for data and close. 

A boolean event handler was also created which monitors loading state, which controls a progress bar, and updating UI elements, using the *after* function to monitor the loading state.  

#### **Future Improvements**
- Support for multi-asset comparison, and correlation matrix for identifying statistical arbitrage, and pairs-trading opportunities.
