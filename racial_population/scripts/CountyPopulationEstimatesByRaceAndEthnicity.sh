#!/bin/bash
cd /samba/share/common/DATADESK/sources/UsBureauOfTheCensus/CountyPopulationEstimatesByRaceAndEthnicity
sourcesRootDirectory="$PWD/"
workflowRootDirectory="/samba/share/common/DATADESK/fred_datadesk_workflow/"
scriptsDirectory="${sourcesRootDirectory}scripts/"
downloadsDirectory="${sourcesRootDirectory}downloads/"
downloadsArchiveDirectory="${sourcesRootDirectory}downloads_archive/"
activeChangedPassDirectory="${sourcesRootDirectory}active_changed_passed/"
outputDirectory="${sourcesRootDirectory}output/"
missingMissingsDirectory="${sourcesRootDirectory}missing_missings/"
configDirectory="${sourcesRootDirectory}config/"
logsDirectory="${sourcesRootDirectory}logs/"
apDirectory="/www/fred/data/UsBureauOfTheCensus/CountyPopulationEstimatesByRaceAndEthnicity/"
releaseID=429

echo "Cleaning up old files and creating required directories"
php ${workflowRootDirectory}utilities/delete_release_files.php ${sourcesRootDirectory}

echo "Processing Data"
python ${scriptsDirectory}CountyPopulationEstimatesByRaceAndEthnicity.py

echo "Preparing files for upload"
concurrent_runs.sh ${sourcesRootDirectory} 1