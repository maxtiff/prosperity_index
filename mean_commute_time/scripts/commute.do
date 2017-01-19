/*
Author: Diana Cooke
Date: 7/26/2016
Purpose: Average Commuting Time

In this do file, we have to import and clean two separate datafiles in order to construct the average commuting time. 
First, we have to import total number of workers not working from home, then we have to import aggregate commuting times
both of them are by county. Then finally we can construct the average commute time by county. 

*/

clear
set more off

global desktop "C:/Users/h1dac02.RB/Desktop" 	//set working directory 


///////////////////////////////////////////////////
//////////workers not working from home////////////
//////////////////////////////////////////////////

local dates 09 10 11 12 13 14   //create local to loop through all years available in census data 


//loop 
foreach x of local dates {

import delimited "$desktop/raw/commute/workforce_`x'.csv", clear varnames(1) //import each dataset by year, have the first row be the column labels

drop in 1 //drop first row 

keep geoid2 geodisplaylabel hd01_vd01  //geoid, countystate, total number of workers not working from home

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
rename hd01_vd01 workforce_`x'

//destring variables so that they are in numeric form 
destring workforce_`x', replace 
destring geoid, replace

//order variable 
order state county geoid workforce_`x'

save "$desktop/intermediate/workforce_`x'", replace 		//create a separate file for each year from 2009-2014 of percent of pop with higher educ + respective county 

} 
//

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////
///////////aggregate commute time ///////////
//////////////////////////////////////////////////

local dates 09 10 11 12 13 14   //create local to loop through all years available in census data 


//loop 
foreach x of local dates {

import delimited "$desktop/raw/commute/aggregate_commute_`x'.csv", clear varnames(1) //import each dataset by year, have the first row be the column labels

drop in 1 //drop first row 

keep geoid2 geodisplaylabel hd01_vd01  //geoid, countystate, aggregate travel time to work 

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
rename hd01_vd01 aggregate_commute_`x'

//destring variables so that they are in numeric form 
destring aggregate_commute_`x', replace 
destring geoid, replace

//order variable 
order state county geoid aggregate_commute_`x'

save "$desktop/intermediate/aggregate_commute_`x'", replace 		//create a separate file for each year from 2009-2014 of percent of pop with higher educ + respective county 

} 
//

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//merge TOTAL WORKERS NOT WORKING FROM HOME with AGGREGATE COMMUTE TIME

clear

//import the merging base file, which has the 3143 census counties from 2010 and the geoids. 
import excel "$desktop/raw/fip_id.xlsx", sheet("Base") first //import each dataset by year, have the first row be the column labels
destring geoid, replace

local dates 09 10 11 12 13 14

foreach x of local dates {
merge 1:1 geoid using "$desktop/intermediate/aggregate_commute_`x'", keepus(aggregate_commute_`x') nogen 		//merge using geoid (numberic variable)
merge 1:1 geoid using "$desktop/intermediate/workforce_`x'", keepus(workforce_`x') nogen 		//merge using geoid (numberic variable)


gen average_commute_time`x' = aggregate_commute_`x' / workforce_`x'				//calculate average commuting time 

drop aggregate_commute_`x' workforce_`x'
}
//


save $desktop/output/commute.dta, replace			//save final file. this will just have "state" "county" "geoid" and a column with average commute time 
