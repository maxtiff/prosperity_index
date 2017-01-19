/*
Author: Diana Cooke
Date: 7/21/2016
Purpose: Poverty Rate

Percent of population below poverty threshold (For whom poverty status is determined) 

*/

clear
set more off

global desktop "C:/Users/h1dac02.RB/Desktop" 	//set working directory 



///////////////////////////////////////////////////
//// import census datafiles of poverty rate////
//////////////////////////////////////////////////

local dates 12 13 14   //create local to loop through all years available in census data 


//loop 
foreach x of local dates {

import delimited "$desktop/raw/poverty_rate/povertyrate_`x'.csv", clear varnames(1) //import each dataset by year, have the first row be the column labels

drop in 1 //drop first row 

keep geoid2 geodisplaylabel hc03_est_vc01 //geoid, countystate, Percent below poverty level; Estimate; Population for whom poverty status is determined

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
rename hc03_est_vc01 poverty_rate_`x'


//destring variables so that they are in numeric form 
destring poverty_rate_`x', replace 
destring geoid, replace

//order variable 
order state county geoid poverty_rate_`x'

save "$desktop/intermediate/povertyrate_`x'", replace 		//create a separate file for each year from 2012-2014 of poverty rate 

} 
//



///////////////////////////////////////////////////
///////////combine into one master file ///////////
//////////////////////////////////////////////////

clear

//import the merging base file, which has the 3143 census counties from 2010 and the geoids. 
import excel "$desktop/raw/fip_id.xlsx", sheet("Base") first //import each dataset by year, have the first row be the column labels
destring geoid, replace

local dates 12 13 14			//use 2012 file as base file and merge with 2013, 2014 

foreach x of local dates {
merge 1:1 geoid using "$desktop/intermediate/povertyrate_`x'", keepus(poverty_rate_`x') nogen 		//merge using geoid (numeric variable), only keep poverty rate for each year  
save $desktop/intermediate/povertyrate, replace
}

save $desktop/output/povertyrate.dta, replace			//save final file. this will just have "state" "county" "geoid" and a column with the poverty rate for 2012-2014
