# Climate Analysis using SQLAlchemy

## Climate Data Analysis

In this section, a combination of ***Python and SQLAlchemy*** were used to perform basic climate analysis and data exploration of the Hawaii climate sqlite database.

![img](https://github.com/pkrachakonda/SQLAlchemy_Challenge/assets/20739237/13287fc1-1452-441f-9236-95d8afe0f229)

In cell 1 of *jupyter notebook*, all the required modulus of ***Matplotlib, pandas,datetime and SQLAlchemy*** for the analysis were imported.

![img_1](https://github.com/pkrachakonda/SQLAlchemy_Challenge/assets/20739237/c5920f13-7928-4e3e-aa45-f0ddcb3dcfe0)

In cells 2 - 6, using *SQLAlchemy ORM functions*, tables of various classes of climate database are read.

![img_2](https://github.com/pkrachakonda/SQLAlchemy_Challenge/assets/20739237/942ce637-4eaa-4042-afa1-35c75a886c7e)

In cell 7, using *select and execute* functions of SQLAlchemy, the weather station with the highest number of readings and the recent date of climate recording are obtained ***Measurement*** class. The table was sorted in descending order using *descending* function.

![img_3](https://github.com/pkrachakonda/SQLAlchemy_Challenge/assets/20739237/26cc9624-3de1-403a-b206-933adfc8f8c3)

Using the *datetime* function from **Datetime** module of Python, last 12 months (365 days) from the recent data of record, ***precipitation*** data from **Measurement** class were read into a dataframe using Pandas. 

Using *Precipitation data* and *Date*, a plot was created.

![img_4](https://github.com/pkrachakonda/SQLAlchemy_Challenge/assets/20739237/4a23a88c-3b80-4129-83cc-1b86caf5be03)

Cell 9, presents the *statistical* summary of precipitation data using Pandas.

![img_5](https://github.com/pkrachakonda/SQLAlchemy_Challenge/assets/20739237/7ab67903-6c90-4c1f-9219-c97a005e400c)

In Cell 10, total number of *Weather* station in the **Weather** class are estimated using scalar function of SQLAlchemy. By grouping the *measurement* class based on *station* column, the number of *temperature* observation records for each weather station in *descending* order were estimated.

![img_6](https://github.com/pkrachakonda/SQLAlchemy_Challenge/assets/20739237/50e68e1c-4f3e-4bfa-9c62-57818b27c5ae)

Cell 12 estimates temperature ranges (minimum, maximum and average) for the station with the highest number of temperature records. Temperature records for the last 12 months from the recent temperature record date were estimated by filtering Climate data
of *Measurement* class. A histogram was generated using this data.

![img_7](https://github.com/pkrachakonda/SQLAlchemy_Challenge/assets/20739237/98551126-269a-4d2a-b0e0-d918f4250c6c)

After completing the analysis, the SQLAlchemy session is closed, i.e. the connection to climate database is terminated. 

## Climate App
In this section, a Flask API based on the queries created in the previous section is developed.

![img_8](https://github.com/pkrachakonda/SQLAlchemy_Challenge/assets/20739237/a4e57566-3c77-4275-b5d9-1563116321f0)

All the modulus required for the ***Climate App*** creation were imported in lines 1 - 5. 

![img_9](https://github.com/pkrachakonda/SQLAlchemy_Challenge/assets/20739237/e4b326d0-2945-4e5e-898c-7aaab43926f9)

In lines 10 - 14, Database has been setup (connection) using SQLAlchemy ORM functions. Both Measurement and Station Classes were also imported. 

In line 20, *Climate App* has been setup using *Flask*.

![img_11](https://github.com/pkrachakonda/SQLAlchemy_Challenge/assets/20739237/40ce9b18-d951-4570-a978-417c2c016479)

In Lines 27 - 42, all available *routes/api* are listed along with a main message.
  + *Route/api* for Precipitation Analysis 
  + *Route/api* for Station Analysis
  + *Route/api* for Temperature Analysis at Station with the highest observation data
  + *Route/api* for Specified Start Date for estimating Minimum, maximum and average temperatures
  + *Route/api* for Specified Start and End Dates for estimating Minimum, maximum and average temperatures

### Precipitation Analysis

![img_12](https://github.com/pkrachakonda/SQLAlchemy_Challenge/assets/20739237/15e57068-f687-4daa-89a5-828910de5442)

Similar to *Precipitation analysis* performed in the previous section, initially the most recent precipitation record date is estimated for the weathered station (line 48-49) and using this information *precipitation data* for last *12 months* from that date is estimated (lines 51 - 55). 
The estimated precipitation data is converted into dictionary format (Lines 58 - 63) and finally the data is jsoinfied in order for the display in the App (line 65).

### Station Analysis

![img_13](https://github.com/pkrachakonda/SQLAlchemy_Challenge/assets/20739237/30e028fa-d58e-4f17-96b6-d0b51d4307a6)

Using pandas's SQL functions, both *station name* and *station id* from **Station** class were extracted and were saved in *dictionary* format (Line 70 - 75). The *dictionary* formatted data is jsonified for the App (line 77).

The data in sqlite database is only used in the analysis. However, in the *csv* files provided in the Resource folder som e additional data (obtained by using *inspect.get_columns* function of SQLAlchemy) is also available.

### Temperature Analysis

![img_14](https://github.com/pkrachakonda/SQLAlchemy_Challenge/assets/20739237/2aa269ee-1502-44bc-953a-b587b594fb0c)

Similar to *Temperature analysis* performed in the previous section, initially the station with the *highest* number temperature records is estimated and then most recent temperature record date is estimated for that *weathered station* (line 48-49) and using this information *temperature data* for last *12 months* from that date is estimated (lines 84 - 98).
The estimated Temperature data is converted into dictionary format (Lines 102 - 108) and finally the data is jsoinfied in order for the display in the App (line 110).

### Specified Start Date

![img_15](https://github.com/pkrachakonda/SQLAlchemy_Challenge/assets/20739237/6c05d9c6-1ae3-4335-ae7c-36e6514f307f)

Initially the *start date* in string format is converted into date format (Line 117) and checked to see if the start date is within a specified starting date range (line 118 - 119). If the start date is between 2017- 2018, 365 days were subtracted. 
If the *start date* is before 2017, same start date is used (Line 121 - 125). 
For the specified start date, the *minimum, maximum and average temperatures* were estimated from that *day till end of the recording period of the database* (126 - 130) and data is jsonified (Line 134).

### Specified Start and End Date

![img_16](https://github.com/pkrachakonda/SQLAlchemy_Challenge/assets/20739237/8fe5dfdf-ce8a-4d0e-b573-d163300bea3f)

Similar to above route, initially *start and end dates* are converted from *string* format to *date* format. If the start date is before *23-8-2017*, same start date was used (Line147 - 149) otherwise 365 days were subtracted from both start and end dates (lines 151 - 153).
For estimated *start and end dates*, the *minimum, maximum and average temperatures* were estimated based on the existing temperature data in the database* (154 - 158) and data is jsonified (Line 162).

Lines 164 - 165, allow the app to run in *debugging mode*, if necessary.
