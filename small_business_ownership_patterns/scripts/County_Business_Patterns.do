/*
Author: Diana Cooke
Date: 7/19/2016
Purpose: County Business Patterns

Number of small businesses divided by labor force participation, i.e. how 
many people in the work force own a small business

*/

clear
set more off

global desktop "C:/Users/h1dac02.RB/Desktop/" 	//set working directory 

/*******************************************************/
/////////////county business pattern data ///////////////
/*******************************************************/

//import individual county business pattern data and merge with FIPS data 
// so that we have geoid attached to CBP data to then merge with labor force.
// we want county, state, geoid and # of small businesses in final dta file from this section. 


local dates 09 10 11 12 13 14
foreach x of local dates {

import delimited "$desktop\raw\small_business_ownership_rate\CBP\cbp`x'co.txt"		//import file 
drop if naics != "------"															//naics is industry type, only need aggregate values which is identified by "------"

//want to create a fips code in the format of the census fips code by combining fips cty + fips state code 
gen fipscty2=string(fipscty, "%03.0f") 	//fips county code should be of the format "001" (3 digits, 2 leading zeros if the number is 1) and destring so we can combine into one overall fips code
gen fipstate2=string(fipstate)	//destring fips state code			
gen geoid=fipstate2+fipscty2		// concatenate into one fips code, call geoid to be consistent with the census
drop fipstate fipscty fipstate2 fipscty2 //drop all other fips IDs besides the combined one we just created 

//create var for # businesses w/ less than 500 people 
gen n1_500_`x' = n1_4 + n5_9 + n10_19 + n20_49 + n50_99 + n100_249 + n250_499 

// organize data 
keep geoid n1_500_`x'		//geoid and small businesses var
destring geoid, replace 			//make geoid a numerical variable

save "$desktop/intermediate/CBP`x'", replace

clear 
} 

//

/*******************************************************/
/////Combine with labor force participation data ///////
/*******************************************************/

clear all

foreach x of local dates { 

import delimited "$desktop/raw/small_business_ownership_rate/laborforce/laborforce_`x'.csv", clear varnames(1) //import each dataset by year, have the first row be the column labels

drop in 1								// drop first row 

keep geodisplaylabel geoid2 hc01_est_vc01 hc02_est_vc01 // county/state, geoid, population, labor force percentage 

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
rename hc02_est_vc01 laborforcepart_rate
rename hc01_est_vc01 population 
rename geoid2 geoid

//found some "N" (n/a) in the data-- replace with empty cell so can deal with them numerically 
replace population = "" if population == "N"
replace laborforcepart_rate = "" if laborforcepart_rate == "N"

//destring variables so in numeric form
destring population, replace
destring geoid, replace
destring laborforcepart_rate, replace 

//labor force is calculated as a percent, and we want an actual number 
gen laborforce = ( population * laborforcepart_rate) / 100		// calculate # of ppl in labor force


drop laborforcepart_rate population								//no longer need these variables now that we have "laborforce" 

merge 1:1 geoid using $desktop/intermediate/cbp`x' // merge with county business pattern dataset 
drop if _merge !=3									//only keep observations that had a match in both using and master datasets (successful merge) 


gen sbor`x'=(n1_500_`x'/laborforce)*100 //calculate small business ownership rate = # of small businesses/ # of people in labor force 

keep county state geoid sbor`x'
order county state geoid sbor`x'

save "$desktop/intermediate/sbor_`x'", replace

}

// combine into one file with time series of small business ownership rate 

clear

//import the merging base file, which has the 3143 census counties from 2010 and the geoids. 
import excel "$desktop/raw/fip_id.xlsx", sheet("Base") first //import each dataset by year, have the first row be the column labels
destring geoid, replace

//using the "base" file, merge each file that contains the small business ownership rate for each year together into one final file
local dates 09 10 11 12 13 14

foreach x of local dates {
merge 1:1 geoid using "$desktop/intermediate/sbor_`x'", keepus(sbor`x')
drop _merge
}


save $desktop/output/small_business.dta, replace
