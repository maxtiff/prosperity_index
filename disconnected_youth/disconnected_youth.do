/*
Author: Diana Cooke
Date: 7/21/2016
Purpose: Disonnected Youth

Youth, ages 16-19 (really should be to age 24 but can't find that data) that are neither in school 
in training, or employed. 


*/

clear
set more off

global desktop "C:/Users/h1dac02.RB/Desktop" 	//set working directory 



///////////////////////////////////////////////////
///import census datafiles of disconnected youth///
//////////////////////////////////////////////////

local dates 09 10 11 12 13 14   //create local to loop through all years available in census data 


//loop 
foreach x of local dates {

import delimited "$desktop/raw/disconnected_youth/disconnected_youth_`x'.csv", clear varnames(1) //import each dataset by year, have the first row be the column labels

drop in 1 //drop first row 

keep geoid2 geodisplaylabel hd01_vd01 hd01_vd10 hd01_vd11 hd01_vd14 hd01_vd15 hd01_vd24 hd01_vd25 hd01_vd28 hd01_vd29 

/*
geoid, countystate
HD01_VD01	Estimate; Total:
HD01_VD10	Estimate; Male: - Not enrolled in school: - High school graduate: - Unemployed
HD01_VD11	Estimate; Male: - Not enrolled in school: - High school graduate: - Not in labor force
HD01_VD14	Estimate; Male: - Not enrolled in school: - Not high school graduate: - Unemployed
HD01_VD15	Estimate; Male: - Not enrolled in school: - Not high school graduate: - Not in labor force
HD01_VD24	Estimate; Female: - Not enrolled in school: - High school graduate: - Unemployed
HD01_VD25	Estimate; Female: - Not enrolled in school: - High school graduate: - Not in labor force
HD01_VD28	Estimate; Female: - Not enrolled in school: - Not high school graduate: - Unemployed
HD01_VD29	Estimate; Female: - Not enrolled in school: - Not high school graduate: - Not in labor force

*/

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
rename hd01_vd10 male_HS_unemp
rename hd01_vd11 male_HS_NLF
rename hd01_vd14 male_NHS_unemp
rename hd01_vd15 male_NHS_NLF
rename hd01_vd24 female_HS_unemp
rename hd01_vd25 female_HS_NLF
rename hd01_vd28 female_NHS_unemp
rename hd01_vd29 female_NHS_NLF


//destring variables so that they are in numeric form 
destring geoid, replace
destring total, replace
destring male_HS_unemp, replace
destring male_HS_NLF, replace
destring male_NHS_unemp, replace
destring male_NHS_NLF, replace
destring female_HS_unemp, replace
destring female_HS_NLF, replace
destring female_NHS_unemp, replace
destring female_NHS_NLF, replace 


//order variable 
order state county geoid total male_HS_unemp male_HS_NLF male_NHS_unemp male_NHS_NLF female_HS_unemp female_HS_NLF female_NHS_unemp female_NHS_NLF

//calculate proportion of disconnected youth
gen disconnected_youth_`x' = 100*(male_HS_unemp + male_HS_NLF + male_NHS_unemp + male_NHS_NLF + female_HS_unemp + female_HS_NLF + female_NHS_unemp + female_NHS_NLF) / total

save "$desktop/intermediate/disconnected_youth_`x'", replace 		//create a separate file for each year from 2009-2014 

} 
//



///////////////////////////////////////////////////
///////////combine into one master file ///////////
//////////////////////////////////////////////////

clear

//import the merging base file, which has the 3143 census counties from 2010 and the geoids. 
import excel "$desktop/raw/fip_id.xlsx", sheet("Base") first //import each dataset by year, have the first row be the column labels
destring geoid, replace

local dates 09 10 11 12 13 14			//use 2012 file as base file and merge with 2013, 2014 

foreach x of local dates {
merge 1:1 geoid using "$desktop/intermediate/disconnected_youth_`x'", keepus(disconnected_youth_`x') nogen 		//merge using geoid (numeric variable), only keep % of disconnected youth for each year  
}

export excel using $desktop/output/disconnected_youth.xlsx, first(var) replace
