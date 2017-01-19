/*
Author: Diana Cooke
Date: 7/21/2016
Purpose: HOusing Affordability

Percent of "burdened" (paying more than 30% of income on housing-- owner-occupied and rental units) households
*/

clear
set more off

global desktop "C:/Users/h1dac02.RB/Desktop" 	//set working directory 



///////////////////////////////////////////////////
//// import census datafiles of income ////
//////////////////////////////////////////////////

local dates1 10 11 12   //create local to loop through year 2010-2012

//breaking up years into two separate loops because IDs change in 2013


//loop 
foreach x of local dates1 {

import delimited "$desktop/raw/housing_affordability/housing_affordability_`x'.csv", clear varnames(1) //import each dataset by year, have the first row be the column labels

drop in 1 //drop first row 

keep geoid2 geodisplaylabel hc01_vc155 hc01_vc164 hc01_vc191 hc01_vc159 hc01_vc160 hc01_vc170 hc01_vc171 hc01_vc196 hc01_vc197 

/* 
2010-2012:
Total:
HC01_VC155: Housing units with a mortgage (excluding units where SMOCAPI cannot be computed)
HC01_VC164: Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed)
HC01_VC191: Occupied units paying rent (excluding units where GRAPI cannot be computed)

Burdened:
HC01_VC159	Estimate; SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI) - 30.0 to 34.9 percent
HC01_VC160	Estimate; SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI) - 35.0 percent or more
HC01_VC170	Estimate; SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI) - 30.0 to 34.9 percent
HC01_VC171	Estimate; SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI) - 35.0 percent or more
HC01_VC196	Estimate; GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI) - 30.0 to 34.9 percent
HC01_VC197	Estimate; GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI) - 35.0 percent or more */


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
rename hc01_vc155 mortgage_total
rename hc01_vc164 no_mortgage_total
rename hc01_vc191 rent_total


rename hc01_vc159 mortgage_3035
rename hc01_vc160 mortgage_35
rename hc01_vc170 no_mortgage_3035
rename hc01_vc171 no_mortgage_35
rename hc01_vc196 rent_3035
rename hc01_vc197 rent_35


//destring variables so that they are in numeric form 
destring geoid, replace
destring mortgage_total, replace
destring mortgage_3035, replace
destring mortgage_35, replace
destring no_mortgage_total, replace 
destring no_mortgage_3035, replace
destring no_mortgage_35, replace
destring rent_total, replace 
destring rent_3035, replace
destring rent_35, replace

//order variable 
order state county geoid mortgage_total mortgage_3035 mortgage_35 no_mortgage_total no_mortgage_3035 no_mortgage_35 rent_total rent_3035 rent_35

//calculate percentage of burdened, for each year
//ex: "burdended_10" for year 2010
gen burdened_`x' = (mortgage_3035 + mortgage_35 + no_mortgage_3035 + no_mortgage_35 + rent_3035 + rent_35) / (mortgage_total + no_mortgage_total + rent_total) 

// percent of population where we can calculate SMOCAPI that pays  more than 30% on housing 

save "$desktop/intermediate/burdened_`x'", replace 		//create a separate file for each year from 2010-2012 of burdened pop + respective county 

} 
//

local dates2 13 14   //create local to loop through year 2013-2014

//breaking up years into two separate loops because IDs change in 2013


//loop 
foreach x of local dates2 {

import delimited "$desktop/raw/housing_affordability/housing_affordability_`x'.csv", clear varnames(1) //import each dataset by year, have the first row be the column labels

drop in 1 //drop first row 

keep geoid2 geodisplaylabel hc01_vc157 hc01_vc167 hc01_vc196 hc01_vc161 hc01_vc162 hc01_vc173 hc01_vc174 hc01_vc201 hc01_vc202 

/* 
2013-2014
"Total" housing units IDs: 

HC01_VC157: Housing units with a mortgage
HC01_VC167: Housing unit without a mortgage
HC01_VC196: Occupied units paying rent


Burdened households: 

HC01_VC161: Housing units with a mortgage (excluding units where SMOCAPI cannot be computed) - 30.0 to 34.9 percent
HC01_VC162: Housing units with a mortgage (excluding units where SMOCAPI cannot be computed) - 35.0 percent or more
HC01_VC173: Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed) - 30.0 to 34.9 percent
HC01_VC174: Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed) - 35.0 percent or more
HC01_VC201: Occupied units paying rent (excluding units where GRAPI cannot be computed) - 30.0 to 34.9 percent
HC01_VC202: Occupied units paying rent (excluding units where GRAPI cannot be computed) - 35.0 percent or more */


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
rename hc01_vc157 mortgage_total
rename hc01_vc167 no_mortgage_total
rename hc01_vc196 rent_total


rename hc01_vc161 mortgage_3035
rename hc01_vc162 mortgage_35
rename hc01_vc173 no_mortgage_3035
rename hc01_vc174 no_mortgage_35
rename hc01_vc201 rent_3035
rename hc01_vc202 rent_35


//destring variables so that they are in numeric form 
destring geoid, replace
destring mortgage_total, replace
destring mortgage_3035, replace
destring mortgage_35, replace
destring no_mortgage_total, replace 
destring no_mortgage_3035, replace
destring no_mortgage_35, replace
destring rent_total, replace 
destring rent_3035, replace
destring rent_35, replace

//order variable 
order state county geoid mortgage_total mortgage_3035 mortgage_35 no_mortgage_total no_mortgage_3035 no_mortgage_35 rent_total rent_3035 rent_35

//calculate percentage of burdened, for each year
//ex: "burdended_10" for year 2010
gen burdened_`x' = (mortgage_3035 + mortgage_35 + no_mortgage_3035 + no_mortgage_35 + rent_3035 + rent_35) / (mortgage_total + no_mortgage_total + rent_total) 

// percent of population where we can calculate SMOCAPI that pays  more than 30% on housing 

save "$desktop/intermediate/burdened_`x'", replace 		//create a separate file for each year from 2013,2014 of burdened pop + respective county 

} 



///////////////////////////////////////////////////
///////////combine into one master file ///////////
//////////////////////////////////////////////////

clear

//import the merging base file, which has the 3143 census counties from 2010 and the geoids. 
import excel "$desktop/raw/fip_id.xlsx", sheet("Base") first //import each dataset by year, have the first row be the column labels
destring geoid, replace

local dates 10 11 12 13 14		

foreach x of local dates {
merge 1:1 geoid using "$desktop/intermediate/burdened_`x'", keepus(burdened_`x') nogen 		//merge using geoid (numeric variable), only keep diss indx for each race for each year  
}
//
//output to an excel file

export excel using $desktop/output/burdened.xlsx, first(var) replace


