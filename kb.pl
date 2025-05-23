% My AI Detective Agent with CSV file Integerated

% Manual to run the Agent
% run in terminal "swipl kb.pl"
% Then in the query write "sortAllSuspects."
% NOte Place the CSV file suspects.csv in the same folder as your progarm

% Now main Agent Logic Starts Here
% Importing the CSV Library for Prolog 
:- use_module(library(csv)).

% We are importing the CSV file
load_csv_data(File) :-
    csv_read_file(File, Rows, [functor(suspect), arity(11)]),
    Rows = [_Header|DataRows],
    assert_csv_rows(DataRows).

% We are iterating Through the data set Rows and Inserting the FActs based on 
% Our Criteria
assert_csv_rows([]).
assert_csv_rows([Row|Rows]) :-
    Row = suspect(Name, HasGun, HasAngerIssues, CommittedMurder, CriminalRecord, SmokesCigarette, ReportedInBurglary, HasMotive, InDebt, HasFakedID, Location),
    (HasGun == 'yes' -> assertz(hasGun(Name)) ; true),
    (HasAngerIssues == 'yes' -> assertz(hasAngerIssues(Name)) ; true),
    (CommittedMurder == 'yes' -> assertz(haveCommittedMurder(Name)) ; true),
    (CriminalRecord == 'yes' -> assertz(criminalRecord(Name)) ; true),
    (SmokesCigarette == 'yes' -> assertz(smokeCigarette(Name)) ; true),
    (ReportedInBurglary == 'yes' -> assertz(reportedInBurglary(Name)) ; true),
    (HasMotive == 'yes' -> assertz(hasMotive(Name)) ; true),
    (InDebt == 'yes' -> assertz(inDebt(Name)) ; true),
    (HasFakedID == 'yes' -> assertz(hasFakedID(Name)) ; true),
    assertz(location(Name, Location)),
    assert_csv_rows(Rows).

% We add some sample FActs to make sure we have 50 FActs
% These are for cities and their connections
connectedCities(chicago, miami).
connectedCities(miami, houston).
connectedCities(houston, seattle).
connectedCities(seattle, anchorage).
connectedCities(anchorage, jefferson).
connectedCities(chicago, houston).
connectedCities(miami, seattle).
connectedCities(houston, anchorage).
connectedCities(seattle, jefferson).
connectedCities(chicago, seattle).

% FActs for high crime cities
highCrimeCity(chicago).
highCrimeCity(houston).
highCrimeCity(miami).

% FActs for suspect severity
suspectSeverity(john, high).
suspectSeverity(mary, medium).
suspectSeverity(bob, low).
suspectSeverity(alice, high).
suspectSeverity(tom, medium).

% We are defining Criteria For Murder Suspects
suspects(murder, Suspect, Reasons) :-
    findall(Suspect, (haveCommittedMurder(Suspect); hasGun(Suspect); hasAngerIssues(Suspect); hasMotive(Suspect)), Suspects),
    member(Suspect, Suspects),
    findall(Reason, (
        (haveCommittedMurder(Suspect), Reason = 'committed murder'),
        (hasGun(Suspect), Reason = 'has gun'),
        (hasAngerIssues(Suspect), Reason = 'has anger issues'),
        (hasMotive(Suspect), Reason = 'has motive')
    ), Reasons),
    Reasons \= [].

% We are Defining the criteria for Decoity Suspects
suspects(deceit, Suspect, Reasons) :-
    findall(Suspect, (criminalRecord(Suspect); smokeCigarette(Suspect); hasFakedID(Suspect)), Suspects),
    member(Suspect, Suspects),
    findall(Reason, (
        (criminalRecord(Suspect), Reason = 'has criminal record'),
        (smokeCigarette(Suspect), Reason = 'smokes cigarette'),
        (hasFakedID(Suspect), Reason = 'has faked ID')
    ), Reasons),
    Reasons \= [].

% Here we are Defining the Theft Suspects Criteria
suspects(theft, Suspect, Reasons) :-
    findall(Suspect, (reportedInBurglary(Suspect); inDebt(Suspect)), Suspects),
    member(Suspect, Suspects),
    findall(Reason, (
        (reportedInBurglary(Suspect), Reason = 'reported in burglary'),
        (inDebt(Suspect), Reason = 'in debt')
    ), Reasons),
    Reasons \= [].

% Rule to check if city is high crime
isHighCrime(City) :-
    highCrimeCity(City).

% Rule to find suspects in high crime cities
suspectsINHighCrime(Crime, Suspect, City, Reasons) :-
    suspects(Crime, Suspect, Reasons),
    location(Suspect, City),
    highCrimeCity(City).

% Rule to prioritize young suspects (age assumed from hasMotive)
prioritizeYoungSuspects(Suspect) :-
    hasMotive(Suspect),
    not(criminalRecord(Suspect)).

% Rule to check unresolved crimes
unresolved_crime(Suspect) :-
    haveCommittedMurder(Suspect),
    not(criminalRecord(Suspect)).

% Rule to escalate serious suspects
escalateSuspect(Suspect) :-
    suspectSeverity(Suspect, high).

% Rule to suggest patrol in high crime cities
suggest_patrol(City) :-
    highCrimeCity(City).

% Rule to check if suspect is dangerous
dangerous_suspect(Suspect) :-
    hasGun(Suspect),
    hasAngerIssues(Suspect).

% Rule to find suspects with multiple crimes
multiple_crimes(Suspect, Crimes) :-
    findall(Crime, suspects(Crime, Suspect, _), Crimes),
    length(Crimes, Len),
    Len > 1.

% Rule to validate suspect for investigation
valid_suspect(Suspect, Crime) :-
    suspects(Crime, Suspect, _),
    suspectSeverity(Suspect, Severity),
    Severity \= low.

% Rule to check if two cities are connected
are_connected(City1, City2) :-
    connectedCities(City1, City2); connectedCities(City2, City1).

% Rule to find path between cities (for BFS/DFS)
path_between(City1, City2, Path) :-
    bfs_path(City1, City2, [City1], Path).

% Helper for BFS path finding
bfs_path(Goal, Goal, Visited, Path) :-
    reverse(Visited, Path).
bfs_path(Current, Goal, Visited, Path) :-
    are_connected(Current, Next),
    not(member(Next, Visited)),
    append(Visited, [Next], NewVisited),
    bfs_path(Next, Goal, NewVisited, Path).

% Rule to find path with hueristic (for A*/Greedy)
path_with_hueristic(Start, Goal, Path, Cost) :-
    a_star_path(Start, Goal, [(0, Start, [Start])], [], Path, Cost).

% Helper for A* path finding
a_star_path(Goal, Goal, _, Visited, Path, Cost) :-
    reverse(Visited, Path),
    length(Path, Cost).
a_star_path(Current, Goal, Open, Closed, Path, Cost) :-
    select((CurrentCost, Current, CurrentPath), Open, RestOpen),
    not(member(Current, Closed)),
    findall((NewCost, Next, NewPath),
            (are_connected(Current, Next),
             not(member(Next, Closed)),
             hueristic(Next, H),
             NewCost is CurrentCost + 1 + H,
             append(CurrentPath, [Next], NewPath)),
            Neighbors),
    append(RestOpen, Neighbors, NewOpen),
    a_star_path(Current, Goal, NewOpen, [Current|Closed], Path, Cost).

% Hueristic for A* and Greedy (simple: 1 for high crime, 2 otherwise)
hueristic(City, 1) :- highCrimeCity(City).
hueristic(_, 2).

% Here we Are filtering Suspects by Crime and Location
suspects_by_location(Crime, Location, Suspect, Reasons) :-
    suspects(Crime, Suspect, Reasons),
    location(Suspect, Location).

% Rule to Suspects all Criminals.
% Just type sortAllSuspects. after loading progarm
sortAllSuspects :-
    write('Our AI AGent Now fetching FActs From the KB'), nl,
    sortSuspectsForCrime(murder),
    sortSuspectsForCrime(deceit),
    sortSuspectsForCrime(theft),
    write('We get the facts from the CSV file'), nl.

% We print suspects for a specific crime.
% WE are prining the suspects for specific Crime here
% just type sort SuspectsForCrime(crime name eg murder).
sortSuspectsForCrime(Crime) :-
    findall([Suspect, Reasons], suspects(Crime, Suspect, Reasons), SuspectList),
    write('Suspects for '), write(Crime), write(':'), nl,
    (SuspectList = [] -> write('  No suspects found.'), nl ; print_suspects(SuspectList)),
    nl.

% here we are prining the crime that happend in specific location
sortSuspectsByLocation(Crime, Location) :-
    findall([Suspect, Reasons], suspects_by_location(Crime, Location, Suspect, Reasons), SuspectList),
    write('Suspects for '), write(Crime), write(' in '), write(Location), write(':'), nl,
    (SuspectList = [] -> write('  No suspects found.'), nl ; print_suspects(SuspectList)),
    nl.

% Here we suspects each crime with reason for crime
print_suspects([]).
print_suspects([[Suspect, Reasons]|Rest]) :-
    write('  - '), write(Suspect), write(': '),
    print_reasons(Reasons),
    nl,
    print_suspects(Rest).

% Function to print the crime reason with commas
print_reasons([Reason]) :- write(Reason).
print_reasons([Reason|Rest]) :- write(Reason), write(', '), print_reasons(Rest).

% We load the CSV file when the progarm starts.
:- load_csv_data('suspects.csv').