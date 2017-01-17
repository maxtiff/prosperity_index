/*
Author: Diana Cooke
Date: 7/21/2016
Purpose: Homeownership Rate

Number of homeowners as a percentage of occupied housing units. 

*/

clear
set more off

global desktop "C:/Users/h1dac02.RB/Desktop/" 	//set working directory 



///////////////////////////////////////////////////
//// import census datafiles of housing tenure ////
//////////////////////////////////////////////////

local dates 09 10 11 12 13 14   //create local to loop through all years available in census data 


//loop 
foreach x of local dates {

import delimited "$desktop/raw/homeownership_rate/housingtenure_`x'.csv", clear varnames(1) //import each dataset by year, have the first row be the column labels

drop in 1 //drop first row 

keep geoid2 geodisplaylabel hd01_vd01 hd01_vd02 //geoid, countystate, total, owner-occupied

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
rename hd01_vd01 total
rename hd01_vd02 owner_occupied

//destring variables so that they are in numeric form 
destring total, replace 
destring owner_occupied, replace
destring geoid, replace

//order variable 
order state county geoid total owner_occupied

//calculate homeownership rate, make variable name homeownership rate + year, 
//ex: "homeownership_rate10" for year 2010
gen homeownership_rate`x' = owner_occupied/total

save "$desktop/intermediate/homeownership_rate_`x'", replace 		//create a separate file for each year from 2009-2014 of homeownership rate + respective county 

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
merge 1:1 geoid using "$desktop/intermediate/homeownership_rate_`x'", keepus(homeownership_rate`x') nogen 		//merge using geoid (numberic variable), only keep homeownership_rate var from each file 
save $desktop/intermediate/homeownership_rate, replace
}

save $desktop/output/homeownership_rate.dta, replace			//save final file. this will just have "state" "county" "geoid" and a column with homeownership rate for each year 2009-2014
