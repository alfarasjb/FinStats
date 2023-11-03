# Stocks-In-A-Nutshell

#### Video Demo: https://youtu.be/hs_t3B6dDh8

#### A query engine for generating a statistical summary for a selected stock listed on Yahoo Finance, such as Standard Deviation, Variance, Skewness for a user-specified period. The program also displays a histogram, with a distribution curve, and a simple line graph of closing prices for that said period. An option to save as pdf is also provided. Examples of which can be found [here]().

![hist](https://github.com/alfarasjb/Stocks-In-A-Nutshell/assets/72119101/27109270-46e3-4d6f-88b7-dcd8f3ed505a)

_summary with histogram plot_


![prc](https://github.com/alfarasjb/Stocks-In-A-Nutshell/assets/72119101/d5d18669-c7f1-4e05-b701-9202690cfd77)

_summary with price plot_

#### **OBJECTIVE**
Generate a user-friendly query engine for providing statistical information and figures for financial instruments to provide a quantitative overview to aid in arriving at profitable investment and trading decisions.

#### Project Contents 
- [project.py]() - Main project file 
- [test_project.py]() - Testing 
- [exports]() - Output directory for saved PDFs and Figures


A common, quantitative approach to investing, and trading, is through the assessment of a financial instrument's statistical summary. This program provides a simple, straight-forward, easily-interpretable user-interface for gathering statistical data. 

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


#### **FUNCTIONS AND CLASSES**

**App Class**
```
UI methods - runs on start. builds main UI 
1. build_parent_frames
2. build_main_header
3. build_input_fields
4. build_stats
5. build_tabview

Functionality
1. fetch_data - triggers an external function call to yfinance, and updates ui with received data.
2. plot_gif - plotting figures on tabview 
3. export_data - triggers an external function call to export current data to a PDF

Utilities:
1. err_msg - triggered by catching an exception, and displays an error message on the ui
```
**GENERIC FUNCTIONS**


*validate_entry()*
```
parameters: symbol:str, samples:str
raises: ValueError - Empty fields, AssertionError - Non-numeric input
returns: symbol -> str, samples -> int

- validates user input (Ticker ID and Sample Size) 
- checks for empty inputs and non-numeric inputs for Sample Size
```

*start_download_thread*
```
parameters: app: App instance, symbol: str, samples: int

- triggers the download thread
```

*download()*
```
parameters: symbol:str, samples:int
raises: ValueError - No data for specified symbol
returns: df -> Pandas DataFrame

- downloads stock data from yahoo finance, trims the data using the tail() function
```
*build_data()*
```
parameters: symbol:str, samples: int
raises: AssertionError - Too few samples
returns: data -> dict, close -> Pandas Series

- calculates statistical data for specified symbol
```
*plot_data()*
```
parameters: data: Pandas Series, main_data: dict, symbol: str
returns: figures

- generates figures using matplotlib and seaborn to be displayed on the UI
```
*export()*
```
parameters: sym:str, main_data:dict, figs:tuple

- exports figures and summary as pdf
- directory: root/exports/[symbol]_[samples]_[date]
```
#### **TESTING APPROACH**
Tests were implemented on the core dependencies of the program: mainly for entry validation, downloading, and building main data. 

Tests Done were the ff: 
1. Testing for return data types
2. Shape of output data: confirming if received the samples requested
3. Raising errors for invalid inputs: non-existent symbols, non-numeric sample sizes, empty fields. 

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
