# CSV REPORT PROCESSING SCRIPT
This python script will process your reports.
Input format: UTF-8 or UTF-16 CSV file (with any kind of line endings), with columns: date(MM/DD/YYYY), state name, number of impressions and CTR percentage.

example input:

01/21/2019,Mandiana,883,0.38%  
01/21/2019,Lola,76,0.78%  
01/21/2019,Fāryāb,919,0.67%  
01/22/2019,Lola,201,0.82%  
01/22/2019,Beroun,139,0.61%  
01/22/2019,Mandiana,1050,0.93%  
01/23/2019, 🐱 ,777,0.22%  
01/23/2019,Gaoual,72,0.7%  
01/23/2019,Lola,521,0.19%  
01/24/2019,Beroun,620,0.1%  
01/24/2019,Unknown,586,0.86%  
01/24/2019, 🐱 ,1082,0.68%  

example output:  

2019-01-21,AFG,919,6  
2019-01-21,GIN,959,4  
2019-01-22,CZE,139,1  
2019-01-22,GIN,1251,12  
2019-01-23,GIN,593,2  
2019-01-23,XXX,777,2  
2019-01-24,CZE,620,1  
2019-01-24,XXX,1668,12  

# GETTING STARTED
