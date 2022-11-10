# DPS AI Challenge: Accident Value Prediction
## Translations
### Sample Data
![Screenshot 2022-11-10 at 5 50 48 PM](https://user-images.githubusercontent.com/35871415/201090267-cca649ef-20c8-4e94-ac3d-39dad044da01.png)

### Columns
MONATSZAHL - MONTH NUMBER: Category <br />
AUSPRAEGUNG - SPECIFICATION: Accident Type <br />
JAHR - YEAR <br />
MONAT - MONTH <br />
WERT - VALUE: Number of Accidents

NOTE: Some rows in `MONAT` contain the value `Summe` which denotes the sum of number of accidents for all the months in a particular year.

### Categorical Variables
#### MONATSZAHL
Alkoholunfälle - Alcohol Accident <br />
Verkehrsunfälle - Traffic Accident <br />
Fluchtunfälle - Escape Accident 

#### AUSPRAEGUNG
insgesamt - total <br />
Verletzte und Getötete - Injured and Killed <br />
mit Personenschäden - with Personal injury

NOTE: The number of accidents for `insgesamt` is not equal to the sum of number of accidents of the other 2 categories.

## Exploratory Data Analysis
### Category-wise Count Distribution
![Screenshot 2022-11-10 at 5 54 11 PM](https://user-images.githubusercontent.com/35871415/201090983-031c5d6c-0388-4d11-a3ec-8fdcfc144ed4.png)

### Correlation Heatmap
![Screenshot 2022-11-10 at 5 56 17 PM](https://user-images.githubusercontent.com/35871415/201091307-2793a5e4-bc02-4b4b-bd57-15b1d390d395.png)

### Category-wise WERT Distribution
#### MONATSZAHL
![Screenshot 2022-11-10 at 6 04 38 PM](https://user-images.githubusercontent.com/35871415/201092981-05912ec1-f2cd-4ac6-b353-feaee071c6fb.png)

Inferences from Box Plot:-  
1. Distribution variation different for every Category (Order: Alcohol<Escape<Traffic)  
2. Increasing Order of Means same as above  

![Screenshot 2022-11-10 at 6 05 12 PM](https://user-images.githubusercontent.com/35871415/201093103-be7e925e-8225-4df7-b2d2-efd4cde70c05.png)

Inferences from Strip Plot:-  
1. Escape and Traffic Accidents making 2 clusters.  
Need to go into detail what factor/variable in causing this clustering  

#### AUSPRAEGUNG
![Screenshot 2022-11-10 at 6 06 28 PM](https://user-images.githubusercontent.com/35871415/201093341-f13868ce-16b8-4d54-af20-002a06c70c8a.png)

Inferences:-  
1. Distribution variation similar for Injured & Killed, Personal Injury. Total Distribution more variation.  
2. Increasing Order of Means: Injured & Killed < Personal Injury < Total  

![Screenshot 2022-11-10 at 6 07 36 PM](https://user-images.githubusercontent.com/35871415/201093561-fa7643e7-6cad-479f-b09d-699d56d3853f.png)

Inferences:-  
1. `Total` accident-type has visibly separate clusters denoting each Category.  
2. For `Injured & Killed`, Alcohol and Escape Accident clusters overlapping.  
3. `Personal Injury` has only one cluster: Traffic Accident Category.  

### Time-Series Analysis
#### Month-wise Distribution
![Screenshot 2022-11-10 at 6 12 15 PM](https://user-images.githubusercontent.com/35871415/201094414-21e937c9-f0b1-4e1b-90c7-843c3d8f89d8.png)

Inference:-  
1. Stable Increasing trend for more than half a year (first half)  
2. Irregular decreasing trend after July(7)  
Might help making a regression plot here that prevents overfitting  

![Screenshot 2022-11-10 at 6 13 20 PM](https://user-images.githubusercontent.com/35871415/201094614-60082274-e7db-49fd-beb9-38e5b5e7b567.png)

Inferences:-  
1. Regression Plot of order 2 shows a parabolic shape peaking around July as we expected.  

#### Time-Series Line plot for every Category & Accident-Type pair
NOTE: Only putting one plot here for reference

![Screenshot 2022-11-10 at 6 17 44 PM](https://user-images.githubusercontent.com/35871415/201095511-2a6b1e88-8f56-4722-88ca-28dce01986fd.png)

#### Check if the Time-Series are stationary (Using Augmented Dickey-Fuller Test)
NOTE: Putting output for only one Time-Series for reference (All of them had the same inference)

![Screenshot 2022-11-10 at 6 28 40 PM](https://user-images.githubusercontent.com/35871415/201097722-b4069662-8d48-40d0-b016-6678ac1ec30a.png)

Inferences:-  
1. None of the Time-Series are stationary since the p-value is coming >0.05  
2. They all have stationary differences  
Now we can check for cointegrating relationships (Note: Non-Stationary series is said to be cointegrated if there exists atleast one linear combination of these variables that is stationary)  

#### Check for Cointegration (Using Johansen Test)
![Screenshot 2022-11-10 at 6 30 31 PM](https://user-images.githubusercontent.com/35871415/201098154-a5a2b223-fc89-4e3b-8fd2-45346ed14883.png)

Inferences:-  
1. Since trace statistic > critical value for all rows in the summary, we can reject the null hypothesis.  
Thus, cointegration relationships exist.  

#### Auto-Correlation and Partial Auto-Correlation Function Plots
NOTE: Putting output for only one Time-Series for reference (All of them had the same inference)

![Screenshot 2022-11-10 at 6 34 03 PM](https://user-images.githubusercontent.com/35871415/201098892-f7544fe1-cd18-49c0-870a-901f8e0feb49.png)
![Screenshot 2022-11-10 at 6 34 41 PM](https://user-images.githubusercontent.com/35871415/201099031-643e665f-49f1-4f83-956e-54b6cb35d3fa.png)

Inferences:-  
1. ACF tails off, PACF cuts off.  
2. At an average, our Auto-Regression model should be of window somewhere between 10-15 lags.  
That is when the correlation effect starts to get lesser and lesser as the lags increase.  

#### Trend & Seasonality Check
NOTE: Putting output for only one Time-Series for reference

![Screenshot 2022-11-10 at 6 40 39 PM](https://user-images.githubusercontent.com/35871415/201100316-4199be41-b70f-43e7-a453-1968bbe982db.png)

Inferences:-  
1. Trend with Alcohol Accidents is generally increasing.  
2. Trend for all other types of accidents is first increasing, then decreasing and finally increasing again.  
