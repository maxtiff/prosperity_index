/*
Author: Diana Cooke
Date: 7/21/2016
Purpose: Single parent head of household

Percent of household runs by a single parent. single male + single female / total. 

*/

clear
set more off

global desktop "C:/Users/h1dac02.RB/Desktop" 	//set working directory 



///////////////////////////////////////////////////
//// import census datafiles of head of household ////
//////////////////////////////////////////////////

local dates 09 10 11 12 13 14   //create local to loop through all years available in census data 


//loop 
foreach x of local dates {

import delimited "$desktop/raw/head_of_household/head_of_household_`x'.csv", clear varnames(1) //import each dataset by year, have the first row be the column labels

drop in 1 //drop first row 

keep geoid2 geodisplaylabel hc01_est_vc02 hc03_est_vc02 hc04_est_vc02 //geoid, countystate, total households, male household (no wife present), female household (no husband present)

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
rename hc01_est_vc02 total
rename hc03_est_vc02 single_male
rename hc04_est_vc02 single_female 

//destring variables so that they are in numeric form 
destring total, replace 
destring single_male, replace
destring single_female, replace
destring geoid, replace

//order variable 
order state county geoid total single_male single_female

//calculate percentage of households single, make variable name single_HH + year, 
//ex: "single_HH_10" for year 2010
gen single_HH_`x' = (single_male + single_female)/total

save "$desktop/intermediate/single_HH_`x'", replace 		//create a separate file for each year from 2009-2014 of single parent head of household + respective county 

} 
//



///////////////////////////////////////////////////
///////////combine into one master file ///////////
//////////////////////////////////////////////////

clear

//import the merging base file, which has the 3143 census counties from 2010 and the geoids. 
import excel "$desktop/raw/fip_id.xlsx", sheet("Base") first //import each dataset by year, have the first row be the column labels
destring geoid, replace

local dates 09 10 11 12 13 14			//merge base file with all years available (2009-2014) 

foreach x of local dates {
merge 1:1 geoid using "$desktop/intermediate/single_HH_`x'", keepus(single_HH_`x') nogen 		//merge using geoid (numberic variable), only keep single_HH var from each file 
save $desktop/intermediate/single_HH, replace
}

save $desktop/output/single_HH.dta, replace			//save final file. this will just have "state" "county" "geoid" and a column with percent of households single for each year 2009-2014
