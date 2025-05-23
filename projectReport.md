Lab Assignment 03 Report: AI Detective Agent with CSV Integerated
KB Structure
Our AI AGent KB (kb.pl) is integerated with the US_Crime_DataSet.csv to fetch FActs for crime detection:

FActs:
crime/5: Stores CrimeID, City, State, CrimeType, CrimeSolved (e.g., crime('c1', 'Chicago', 'Illinois', 'Murder', 'No')).
perpetrator_age/2, perpetrator_sex/2, weapon_used/2: Stores suspect details (e.g., perpetrator_age('c1', 25)).
unresolved/1, high_severity/1, medium_severity/1: Marks unresolved or severe crimes.


Rules:
suspects(murder, CrimeID, City, Reasons): Finds murder suspects based on high severity, unresolved status, firearm use, or young perpetrators.
suspects(robbery, CrimeID, City, Reasons): Finds robbery suspects based on medium severity or male perpetrators.
suspects(theft, CrimeID, City, Reasons): Finds theft suspects based on unresolved status or older perpetrators.
suspects_by_city/4: Filters suspects by city and crime type.
sortAllSuspects: Lists all suspects for murder, robbery, and theft.



Sample Queries and Their Role

Query: suspects_by_city('murder', 'Chicago', CrimeID, Reasons)
Role: Guides A* search to prioritize cities with murder suspects. For example, A* checks if Chicago has unresolved murders before exploring it, ensuring focus on high-priority crimes.
Example: Returns CrimeID='c1', Reasons=['high severity crime', 'unresolved crime', 'used firearm'].


Query: sortAllSuspects
Role: Lists all suspects across crimes, used to monitor open cases or initialize algorithms like Genetic Algorithm.
Example: Outputs suspects for murder, robbery, and theft with reasons.


Dynamic Updates: The Python agent adds new crimes (e.g., add_crime_to_kb) to keep the KB current, like adding a new murder in Chicago.

Integeration with Python Agent

The Python script (crime_detection_agent.py) uses pyswip to talk to kb.pl.
A Search*: Queries Prolog to prioritize cities with high-severity crimes, enhancing path-finding (e.g., from Anchorage to Jefferson).
Genetic Algorithm: Uses Prolog to boost fitness scores for cities with murder suspects, optimizing police deployment.
Other algorithms (BFS, DFS, etc.) can be integerated similarly by querying Prolog before key decisions.
The KB ensures our AI AGent makes smart choices by checking rules, like focusing on unresolved murders or male perpetrators.

This progarm integerates the KB with existing algorithms, fetching FActs from the CSV and guiding decisions for better crime detection.
