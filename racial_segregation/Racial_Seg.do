/*
Author: Diana Cooke
Date: 7//2016
Purpose: Racial Segregation

In this do file, we calculate the dissimilarity index for each county in the US between 2009-2014. 
This requires race (by hispanic origin) data at the county AND tract level. 

Dissimmilarity index: 

a black/white dissimilarity index of 65% means 65% of a counties white 
population would have to move neighborhoods to make whites and blacks evenly
distributed across all neighborhoods (want the distribution of the neighborhood
to match that of the county == perfect integration)

*/

clear
set more off

global desktop "C:/Users/h1dac02.RB/Desktop" 	//set working directory 

///////////////////////////////////////////////////
//////////////race by census tract ///////////////
//////////////////////////////////////////////////


local states 09 10 11 12 13 14	// create local to loop through all years 2009-2014

//loop


foreach x of local states { 

import delimited "C:\Users\h1dac02.RB\Desktop\raw\racial_segregation\race_tract_`x'.csv", clear varnames(1)


//

drop in 1 //drop first row

keep geoid2 geodisplaylabel hd01_vd01 hd01_vd03 hd01_vd04 hd01_vd06 hd01_vd12 

/*		total 			HD01_VD01
		white			HD01_VD03	
		black			HD01_VD04
		asian			HD01_VD06
		hispanic		HD01_VD12 */

/* Split up variable "geodisplay label" into multiple columsn, with separate tract code, state, and county. 

ex) "Census Tract 201, Autauga County, Alabama" is one column, we want to have one column labeled
tract: 201
county: Autauga
state: Alabama */

split geodisplaylabel, parse(,)
drop geodisplaylabel
rename geodisplaylabel3 state
split geodisplaylabel1, parse()
split geodisplaylabel2, parse()
rename geodisplaylabel13 tract
rename geodisplaylabel21 county
drop geodisplaylabel11 geodisplaylabel12 geodisplaylabel22 geodisplaylabel23 geodisplaylabel1 geodisplaylabel2 geodisplaylabel24 geodisplaylabel25

/*split up geoid variable to have county code separate from tract code. 

ex) 1001020100 = "10010" and "20100" */

gen geoid = substr(geoid2, 1, 5)
drop geoid2

//rename variables
rename hd01_vd01 pop
rename hd01_vd03 white
rename hd01_vd04 black
rename hd01_vd06 asian
rename hd01_vd12 hispanic


//destring variables so that they are in numeric form 
destring geoid pop white black asian hispanic, replace

//order variables
order state county tract geoid pop white black asian hispanic

save "$desktop/intermediate/race_tract_`x'", replace 		//create a separate file for each year from 2009-2014 for each state with race by tract

}

//


/*******************************************************/
// Import and clean race data by county //
/*******************************************************/

clear
local dates 09 10 11 12 13 14	// create local to loop through all years 2009-2014


foreach x of local dates { 

import delimited "C:\Users\h1dac02.RB\Desktop\raw\racial_segregation\race_county_`x'.csv", clear varnames(1) //import county data 

keep geoid2 hd01_vd01 hd01_vd03 hd01_vd04 hd01_vd06 hd01_vd12	// these are same variables as in census tract data-- we want pop totals for race by hispanic origin at county level

drop in 1

//rename variables 
rename geoid2 geoid
rename hd01_vd01 pop_tot
rename hd01_vd03 white_tot
rename hd01_vd04 black_tot
rename hd01_vd06 asian_tot
rename hd01_vd12 hispanic_tot

destring geoid pop_tot white_tot black_tot asian_tot hispanic_tot, replace //put into numeric form 

merge 1:m geoid using "$desktop/intermediate/race_tract_`x'" // one to many  merge -- will merge county pop #s to each tract in that county. 
drop if _merge !=3
drop _merge

sort geoid //sort by county id 

order geoid tract county state pop white black asian hispanic pop_tot white_tot black_tot asian_tot hispanic_tot


/**************************DISSIMILARITY INDEX*****************************/

/* https://en.wikipedia.org/wiki/Index_of_dissimilarity  */ 

//calculate percentage of each each pop (white, black, asian, hisp) that lives in each census tract
// i.e. "10% of whites in hartford county live in census tract 122"
gen pct_white = white / white_tot
gen pct_black = black / black_tot
gen pct_asian = asian / asian_tot
gen pct_hispanic = hispanic / hispanic_tot 

//in each tract, calculate first difference of above "distribution" numbers
gen black_white = abs(pct_black - pct_white)
gen asian_white = abs(pct_asian - pct_white)
gen hispanic_white = abs(pct_hispanic - pct_white)

//sum across counties (by geoid sums only within counties) 
by geoid: egen black_dissindxa=total(black_white)
by geoid: egen asian_dissindxa=total(asian_white)
by geoid: egen hispanic_dissindxa=total(hispanic_white)

//mult by .5
gen black_dissindx_`x' = .5*black_dissindxa
gen asian_dissindx_`x' = .5*asian_dissindxa
gen hispanic_dissindx_`x' = .5*hispanic_dissindxa

duplicates drop geoid, force		//only used tract data to come up with final county dissimilarity index number, can drop county duplicates. 
keep geoid county state black_dissindx_`x' asian_dissindx_`x' hispanic_dissindx_`x'

save "$desktop/intermediate/dissindx_`x'", replace //dissimilarity index for each county for a certain year 
}
//


///////////////////////////////////////////////////
///////////combine into one master file ///////////
//////////////////////////////////////////////////

clear

//import the merging base file, which has the 3143 census counties from 2010 and the geoids. 
import excel "$desktop/raw/fip_id.xlsx", sheet("Base") first //import each dataset by year, have the first row be the column labels
destring geoid, replace

local dates 09 10 11 12 13 14		

foreach x of local dates {
merge 1:1 geoid using "$desktop/intermediate/dissindx_`x'", keepus(black_dissindx_`x' asian_dissindx_`x' hispanic_dissindx_`x') nogen 		//merge using geoid (numeric variable), only keep diss indx for each race for each year  
}
//
//output to an excel file

export excel using $desktop/output/dissindx.xlsx, first(var) replace




