/*
Author: Diana Cooke
Date: 8/23/2016
Purpose: Credit Qualtiy

Percent of population with a credit score below 660

*/

clear
set more off

global desktop "C:/Users/h1dac02.RB/Desktop" 	//set working directory 


///////////////////////////////////////////////////////////////////
/*importing fips excel sheet to attach fips code to equifax data */
///////////////////////////////////////////////////////////////////

import excel "$desktop/raw/fip_id.xlsx", sheet("State") first 
save fipstate, replace


///////////////////////////////////////////////////////////////////
//////////////*import equifax data, clean, etc. *//////////////////
//////////////////////////////////////////////////////////////////

import delimited "$desktop/raw/credit/equifax.csv", clear varnames(1) //import data that I queried from radar 

merge m:m state using fipstate 				//merge with fips data to add a column of the fipstate variable so we can have a complete geoid 
keep if _merge==3							//only keep matched variables
drop _merge									//drop merge variable 


//put fipstate variable into string format 
gen fipstate2=string(fipstate) 	

//fips county code should be of the format "001" (3 digits, 2 leading zeros if the number is 1) and destring so we can combine into one overall fips code
destring county_code, replace	
gen county_code2=string(county_code, "%03.0f")

//combine fipstate and fips county to get geoid
gen geoid=fipstate2+county_code2
destring geoid, replace 

//organization
keep qtr state num_total num_below660 geoid
order qtr state geoid num_total num_below660

///////////////////////////////////////////////////////////////////
///////////*Create credit quality & date variables *//////////////
//////////////////////////////////////////////////////////////////

//gen percent of households with bad credit --- this is our variable of interest 
gen pct_below660 = num_below660/num_total

//we can only use counties with more than 20 observations, privacy restriction with equifax. drop the other counties, these will just be "missing"
drop if num_total <=20

//organization
sort state geoid qtr
keep qtr state geoid pct_below660

//change date format from "MM/1/YYYY" to "YYYqX"
split qtr, parse(/)
drop qtr qtr2
rename qtr3 year
destring qtr1, replace 
gen qtr =qtr1 / 3
destring year, replace
gen date = yq(year, qtr)

//organize
drop qtr1 qtr year
order state geoid date pct_below660

save $desktop/intermediate/equifax, replace


///////////////////////////////////////////////////////////////////
////////*Split files up by time and merge with fips data */////////
//////////////////////////////////////////////////////////////////

foreach x of num 156/225 {   //dates are in this form to easily loop through will pu tthem in "YYYqX" form after
use $desktop/intermediate/equifax, replace
keep if date == `x'			//keep specific year-quarter
format date %tq
rename pct_below660 pct_below660_`x'
save "$desktop/intermediate/credit_quality`x'", replace 	//save a file for each date	
}
//


///////////////////////////////////////////////////
///////////combine into one master file ///////////
//////////////////////////////////////////////////

clear

//import the merging base file, which has the 3143 census counties from 2010 and the geoids. 
import excel "$desktop/raw/fip_id.xlsx", sheet("Base") first //import each dataset by year, have the first row be the column labels
destring geoid, replace

foreach x of num 156/225 {
merge 1:1 geoid using "$desktop/intermediate/credit_quality`x'", keepus(pct_below660_`x') 		//merge using geoid (numeric variable)                                                                                                                              
drop if _merge==2
drop _merge
save $desktop/intermediate/credit_quality, replace
}

export excel using $desktop/output/credit_quality.xlsx, first(var) replace
