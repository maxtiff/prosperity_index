/*
Author: Diana Cooke
Date: 7/21/2016
Purpose: Income Inequality

Ratio of mean income of highest quintile (top 20%) divided by mean income of lowest quintile of income (bottom 20%) 

*/

clear
set more off

global desktop "C:/Users/h1dac02.RB/Desktop" 	//set working directory 



///////////////////////////////////////////////////
//// import census datafiles of income ////
//////////////////////////////////////////////////

local dates 10 11 12 13 14   //create local to loop through all years available in census data 


//loop 
foreach x of local dates {

import delimited "$desktop/raw/income_inequality/income_inequality_`x'.csv", clear varnames(1) //import each dataset by year, have the first row be the column labels

drop in 1 //drop first row 

keep geoid2 geodisplaylabel hd01_vd02 hd01_vd06 //geoid, countystate, average income in lowest quintile, average income in highest quintile 


//create separate county and state vars from geodisplay var 
// ex: geodislaylabel will currently have "Walker County, Alabama" and I want to create two separate variables
// one called "State" that will just have "Alabama" and another "County" that will just have "Walker"

split geodisplaylabel, parse(,)
drop geodisplaylabel
rename geodisplaylabel2 state
split geodisplaylabel1, parse()
drop geodisplaylabel1 geodisplaylabel12 geodisplaylabel13 geodisplaylabel14 geodisplaylabel15
rename geodisplaylabel11 county

//rename variables 
rename geoid2 geoid	
rename hd01_vd02 lowest20
rename hd01_vd06 highest20


//destring variables so that they are in numeric form 
destring lowest20, replace
destring highest20, replace 
destring geoid, replace

//order variable 
order state county geoid lowest20 highest20

//calculate 20/20 ratio = average income in highest quintile divided by average income in lowest quintile
//calculated for each county (will loop through to calculate for each county for each year available) 
gen ratio_2020_`x' = highest20/lowest20 

save "$desktop/intermediate/ratio_2020_`x'", replace 		//create a separate file for each year from 2010-2014 of 20 20 ratio 

} 
//



///////////////////////////////////////////////////
///////////combine into one master file ///////////
//////////////////////////////////////////////////

clear

//import the merging base file, which has the 3143 census counties from 2010 and the geoids. 
import excel "$desktop/raw/fip_id.xlsx", sheet("Base") first //import each dataset by year, have the first row be the column labels
destring geoid, replace


local dates 10 11 12 13 14		

foreach x of local dates {
merge 1:1 geoid using "$desktop/intermediate/ratio_2020_`x'", keepus(ratio_2020_`x') nogen 		//merge using geoid (numberic variable), only keep single 2020 ratio from each year for each county
save $desktop/intermediate/ratio_2020, replace
}

save $desktop/output/ratio_2020.dta, replace			//save final file. this will just have "state" "county" "geoid" and a column with 2020 ratio for each year 2010-2014
