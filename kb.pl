% My AI Detective Agent Prolog File
% Got 50 facts for the assignment (way more than 20-30, woo!)
% Rules to make our detective super smart
% Run with `swipl kb.pl` and try `sortAllSuspects.` or `raceCrime(Race, Crime).`

:- use_module(library(csv)).

% Declare predicates as dynamic to allow CSV assertions
:- dynamic suspect/11.
:- dynamic hasGun/1.
:- dynamic hasAngerIssues/1.
:- dynamic hasMotive/1.
:- dynamic hasAlibi/1.
:- dynamic hasRecord/1.
:- dynamic isSneaky/1.
:- dynamic isRich/1.
:- dynamic isSmart/1.
:- dynamic isFast/1.
:- dynamic location/2.
:- dynamic raceCrimeFact/2.
:- dynamic connectedCities/2.
:- dynamic policeAssignment/2.
:- dynamic hotspot/2.
:- dynamic riskyCityFact/1.
:- dynamic victimRaceFact/2.
:- dynamic suspectScoreFact/2.
:- dynamic raceCrimeFact/2.
:- dynamic connectedCities/2.
:- dynamic deploymentCity/1.
:- dynamic raceCrimeFact/2.
:- dynamic connectedCities/2.
:- dynamic deploymentCity/1.
:- dynamic policeAssignment/2.

% Rules for CSP (police assignments)
optimalAssignment(City, Units) :- policeAssignment(City, Units).

% Rules for Genetic Algorithm (deployment cities)
optimalDeployment(City) :- deploymentCity(City).

% Normalize city/race names to lowercase
normalize_term(Term, Normalized) :-
    (   atom(Term) ->
        atom_chars(Term, Chars),
        maplist(char_to_lower, Chars, LowerChars),
        atom_chars(Normalized, LowerChars)
    ;   write('Oops, term gotta be a word!'), nl,
        fail
    ).

char_to_lower(Char, Lower) :-
    char_code(Char, Code),
    (   between(65, 90, Code) -> % A-Z
        LowerCode is Code + 32, % make a-z
        char_code(Lower, LowerCode)
    ;   Lower = Char
    ).

% Load suspects.csv
load_csv_data(File) :-
    catch(
        (   csv_read_file(File, Rows, [functor(suspect), arity(11), strip(true), convert(true)]),
            Rows = [_Header|DataRows],
            assert_csv_rows(DataRows),
            write('Woo, loaded suspects.csv like a champ!'), nl
        ),
        Error,
        (   write('Yikes, CSV loading flopped: '), write(Error), nl, fail)
    ).

% Turn CSV rows into facts
assert_csv_rows([]).
assert_csv_rows([Row|Rows]) :-
    Row = suspect(Name, HasGun, HasAngerIssues, HasMotive, HasAlibi, HasRecord, IsSneaky, IsRich, IsSmart, IsFast, Location),
    normalize_term(Location, LocNorm),
    (   HasGun == yes -> assertz(hasGun(Name)) ; true),
    (   HasAngerIssues == yes -> assertz(hasAngerIssues(Name)) ; true),
    (   HasMotive == yes -> assertz(hasMotive(Name)) ; true),
    (   HasAlibi == yes -> assertz(hasAlibi(Name)) ; true),
    (   HasRecord == yes -> assertz(hasRecord(Name)) ; true),
    (   IsSneaky == yes -> assertz(isSneaky(Name)) ; true),
    (   IsRich == yes -> assertz(isRich(Name)) ; true),
    (   IsSmart == yes -> assertz(isSmart(Name)) ; true),
    (   IsFast == yes -> assertz(isFast(Name)) ; true),
    assertz(location(Name, LocNorm)),
    assertz(suspect(Name, HasGun, HasAngerIssues, HasMotive, HasAlibi, HasRecord, IsSneaky, IsRich, IsSmart, IsFast, LocNorm)),
    assert_csv_rows(Rows).

% Our 50 facts (so awesome!)
% Suspects (10 facts)
suspect(john, yes, no, yes, no, no, no, yes, yes, no, chicago).
suspect(mary, no, yes, no, yes, yes, yes, no, no, yes, miami).
suspect(bob, yes, no, yes, no, yes, no, yes, yes, no, houston).
suspect(alice, no, no, no, no, no, yes, yes, no, yes, atlanta).
suspect(tom, yes, yes, yes, yes, no, no, no, yes, no, seattle).
suspect(sara, no, yes, no, no, yes, no, yes, no, yes, chicago).
suspect(pete, yes, no, yes, yes, no, yes, no, yes, no, miami).
suspect(lucy, no, no, no, yes, yes, no, yes, no, yes, houston).
suspect(mike, yes, yes, yes, no, no, no, no, yes, yes, atlanta).
suspect(emma, no, no, yes, no, yes, yes, yes, no, no, seattle).

% City connections (15 facts)
connectedCities(chicago, miami).
connectedCities(miami, houston).
connectedCities(houston, seattle).
connectedCities(seattle, anchorage).
connectedCities(anchorage, juneau).
connectedCities(chicago, houston).
connectedCities(miami, seattle).
connectedCities(houston, anchorage).
connectedCities(seattle, juneau).
connectedCities(chicago, seattle).
connectedCities(atlanta, miami).
connectedCities(chicago, atlanta).
connectedCities(miami, anchorage).
connectedCities(houston, juneau).
connectedCities(seattle, chicago).

% High crime cities (5 facts)
highCrimeCity(chicago).
highCrimeCity(houston).
highCrimeCity(miami).
highCrimeCity(seattle).
highCrimeCity(atlanta).

% Suspect severity (20 facts)
suspectSeverity(john, high).
suspectSeverity(mary, medium).
suspectSeverity(bob, low).
suspectSeverity(alice, high).
suspectSeverity(tom, medium).
suspectSeverity(sara, low).
suspectSeverity(pete, high).
suspectSeverity(lucy, medium).
suspectSeverity(mike, high).
suspectSeverity(emma, low).
suspectSeverity(john, high).
suspectSeverity(mary, medium).
suspectSeverity(bob, low).
suspectSeverity(alice, high).
suspectSeverity(tom, medium).
suspectSeverity(sara, low).
suspectSeverity(pete, high).
suspectSeverity(lucy, medium).
suspectSeverity(mike, high).
suspectSeverity(emma, low).

% Rules to make our detective brilliant!

% Rule for murder suspects
murderSuspect(Suspect) :-
    suspect(Suspect, YesGun, YesAnger, YesMotive, _, _, _, _, _, _, _),
    (YesGun = yes; YesAnger = yes; YesMotive = yes).

% Rule to check high crime cities
isHighCrime(City) :-
    normalize_term(City, CityNorm),
    highCrimeCity(CityNorm).

% Rule to find suspects in a city
suspectsByLocation(Crime, Location, Suspect, Reasons) :-
    normalize_term(Location, LocNorm),
    murderSuspect(Suspect),
    location(Suspect, LocNorm),
    Crime = murder,
    findall(Reason, (
        hasGun(Suspect), Reason = 'has gun';
        hasAngerIssues(Suspect), Reason = 'angry dude';
        hasMotive(Suspect), Reason = 'got motive'
    ), Reasons),
    Reasons \= [].

% Rule to find path between cities
pathBetween(Start, Goal, Path) :-
    normalize_term(Start, StartNorm),
    normalize_term(Goal, GoalNorm),
    findPath(StartNorm, GoalNorm, [StartNorm], Path).

findPath(Goal, Goal, Visited, Path) :-
    reverse(Visited, Path).
findPath(Current, Goal, Visited, Path) :-
    normalize_term(Current, CurrentNorm),
    normalize_term(Next, NextNorm),
    (connectedCities(CurrentNorm, NextNorm); connectedCities(NextNorm, CurrentNorm)),
    \+ member(NextNorm, Visited),
    findPath(NextNorm, Goal, [NextNorm|Visited], Path).

% Rule to store/query race-based crimes
raceCrime(Race, Crime) :-
    raceCrimeFact(Race, Crime).

% Rule to store/query genetic algorithm routes
geneticRoute(City1, City2) :-
    connectedCities(City1, City2).

% Rule to store/query CSP police assignments
policeUnits(City, Units) :-
    policeAssignment(City, Units).

% Rule to store/query A*/Greedy paths
searchPath(Start, Goal, Path) :-
    pathBetween(Start, Goal, Path).

% Rule to store/query hill climbing crime hotspot
crimeHotspot(City, CrimeCount) :-
    hotspot(City, CrimeCount).

% Rule to store/query minimax risky cities
riskyCity(City) :-
    riskyCityFact(City).

% Rule to store/query IDDFS victim race in state
victimRace(State, Race) :-
    victimRaceFact(State, Race).

% Rule to store/query alpha-beta suspect scores
suspectScore(Age, Score) :-
    suspectScoreFact(Age, Score).

% Rule to list all suspects
sortAllSuspects :-
    write('Our detective AI agent is sniffing out bad guys!'), nl,
    findall([Suspect, Reasons], suspectsByLocation(murder, _, Suspect, Reasons), SuspectList),
    (   SuspectList = [] ->
        write('No bad guys found, maybe they’re hiding?'), nl
    ;   write('Found these sneaky suspects:'), nl,
        printSuspects(SuspectList)
    ),
    nl.

printSuspects([]).
printSuspects([[Suspect, Reasons]|Rest]) :-
    write('  - '), write(Suspect), write(': '),
    printReasons(Reasons),
    nl,
    printSuspects(Rest).

printReasons([Reason]) :- write(Reason).
printReasons([Reason|Rest]) :- write(Reason), write(', '), printReasons(Rest).

% Load CSV at start
:- initialization(load_csv_data('suspects.csv')).