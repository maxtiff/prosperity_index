/*
Author: Diana Cooke
Date: 7/21/2016
Purpose: Educational Attainment

Percent of population (25 + )with associates degree or some college / higher. 

*/

clear
set more off

global desktop "C:/Users/h1dac02.RB/Desktop" 	//set working directory 



///////////////////////////////////////////////////
//// import census datafiles of housing tenure ////
//////////////////////////////////////////////////

local dates 09 10 11 12 13 14   //create local to loop through all years available in census data 


//loop 
foreach x of local dates {

import delimited "$desktop/raw/educational_attainment/educational_attainment_`x'.csv", clear varnames(1) //import each dataset by year, have the first row be the column labels

drop in 1 //drop first row 

keep geoid2 geodisplaylabel hc01_est_vc11 hc01_est_vc12 hc01_est_vc13 //geoid, countystate, 

//percent pop 25+ with associates degree, percent pop 25 + with bachelors degree, percent pop 25+ with grad degree

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
rename hc01_est_vc11 pop25_assoc
rename hc01_est_vc12 pop25_bach
rename hc01_est_vc13 pop25_grad


//destring variables so that they are in numeric form 
destring pop25_assoc, replace
destring pop25_bach, replace
destring pop25_grad, replace
destring geoid, replace

//order variable 
order state county geoid pop25_assoc pop25_bach pop25_grad

//calculate percentage of households single, make variable name percent_higher_educ + year, 
//ex: "percent_higher_educ_10" for year 2010
gen percent_higher_educ`x' = pop25_assoc + pop25_bach + pop25_grad // percent with associates degree or higher 

save "$desktop/intermediate/percent_higher_educ`x'", replace 		//create a separate file for each year from 2009-2014 of percent of pop with higher educ + respective county 

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
merge 1:1 geoid using "$desktop/intermediate/percent_higher_educ`x'", keepus(percent_higher_educ`x') nogen 		//merge using geoid (numberic variable), only keep single higher educ var from each file 
save $desktop/intermediate/percent_higher_educ, replace
}

save $desktop/output/percent_higher_educ.dta, replace			//save final file. this will just have "state" "county" "geoid" and a column with higher educ var for each year 2009-2014
