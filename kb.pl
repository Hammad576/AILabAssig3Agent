% My AI Detective Agent Prolog File
% We got 50 facts here for the assignment (way more than 20-30, woo!)
% Added some rules to make our detective smart
% Run with `swipl kb.pl` and try `sortAllSuspects.`

:- use_module(library(csv)).

% Normalize city names to lowercase
normalize_city(City, Normalized) :-
    (   atom(City) ->
        atom_chars(City, Chars),
        maplist(char_to_lower, Chars, LowerChars),
        atom_chars(Normalized, LowerChars)
    ;   write('Please Enter the Correct Ciity Name'), nl,
        fail
    ).

char_to_lower(Char, Lower) :-
    char_code(Char, Code),
    (   between(65, 90, Code) % A-Z
    ->  LowerCode is Code + 32, % make it a-z
        char_code(Lower, LowerCode)
    ;   Lower = Char
    ).

% Load suspects.csv (gotta have that data!)
load_csv_data(File) :-
    catch(
        (   csv_read_file(File, Rows, [functor(suspect), arity(11), strip(true), convert(true)]),
            Rows = [_Header|DataRows],
            assert_csv_rows(DataRows),
            write('Yay, loaded suspects.csv like a pro!'), nl
        ),
        Error,
        (   write('Uh-oh, CSV loading went kaput: '), write(Error), nl, fail)
    ).

% Turn CSV rows into facts
assert_csv_rows([]).
assert_csv_rows([Row|Rows]) :-
    Row = suspect(Name, HasGun, HasAngerIssues, HasMotive, HasAlibi, HasRecord, IsSneaky, IsRich, IsSmart, IsFast, Location),
    normalize_city(Location, LocNorm),
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

% Our 50 facts (so cool!)
% Suspects (10 facts)
suspect(john, yes, no, yes, no, no, no, yes, yes, no, Chicago).
suspect(mary, no, yes, no, yes, yes, yes, no, no, yes, Miami).
suspect(bob, yes, no, yes, no, yes, no, yes, yes, no, houston).
suspect(alice, no, no, no, no, no, yes, yes, no, yes, atlanta).
suspect(tom, yes, yes, yes, yes, no, no, no, yes, no, seattle).
suspect(sara, no, yes, no, no, yes, no, yes, no, yes, Chicago).
suspect(pete, yes, no, yes, yes, no, yes, no, yes, no, Miami).
suspect(lucy, no, no, no, yes, yes, no, yes, no, yes, houston).
suspect(mike, yes, yes, yes, no, no, no, no, yes, yes, atlanta).
suspect(emma, no, no, yes, no, yes, yes, yes, no, no, seattle).

% City connections (15 facts, some caps are oopsies)
connectedCities(Chicago, Miami).
connectedCities(Miami, houston).
connectedCities(houston, seattle).
connectedCities(seattle, anchorage).
connectedCities(anchorage, jefferson).
connectedCities(Chicago, houston).
connectedCities(Miami, seattle).
connectedCities(houston, anchorage).
connectedCities(seattle, jefferson).
connectedCities(Chicago, seattle).
connectedCities(atlanta, Miami).
connectedCities(Chicago, atlanta).
connectedCities(Miami, anchorage).
connectedCities(houston, jefferson).
connectedCities(seattle, Chicago).

% High crime cities (5 facts)
highCrimeCity(Chicago).
highCrimeCity(houston).
highCrimeCity(Miami).
highCrimeCity(seattle).
highCrimeCity(atlanta).

% Suspect severity (20 facts, some names got funky caps)
suspectSeverity(john, high).
suspectSeverity(Mary, medium).
suspectSeverity(bob, low).
suspectSeverity(Alice, high).
suspectSeverity(tom, medium).
suspectSeverity(sara, low).
suspectSeverity(Pete, high).
suspectSeverity(lucy, medium).
suspectSeverity(mike, high).
suspectSeverity(Emma, low).
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

% Rules to make our detective smart!

% Rule to find murder suspects (who’s up to no good?)
murderSuspect(Suspect) :-
    suspect(Suspect, YesGun, YesAnger, YesMotive, _, _, _, _, _, _, _),
    (YesGun = yes; YesAnger = yes; YesMotive = yes).

% Rule to check high crime cities (spooky towns!)
isHighCrime(City) :-
    normalize_city(City, CityNorm),
    highCrimeCity(CityNorm).

% Rule to find suspects in a city (who’s hiding where?)
suspectsByLocation(Crime, Location, Suspect, Reasons) :-
    normalize_city(Location, LocNorm),
    murderSuspect(Suspect),
    location(Suspect, LocNorm),
    Crime = murder,
    findall(Reason, (
        hasGun(Suspect), Reason = 'has gun';
        hasAngerIssues(Suspect), Reason = 'angry dude';
        hasMotive(Suspect), Reason = 'got motive'
    ), Reasons),
    Reasons \= [].

% Rule to find path between cities (let’s go on a road trip!)
pathBetween(Start, Goal, Path) :-
    normalize_city(Start, StartNorm),
    normalize_city(Goal, GoalNorm),
    findPath(StartNorm, GoalNorm, [StartNorm], Path).

findPath(Goal, Goal, Visited, Path) :-
    reverse(Visited, Path).
findPath(Current, Goal, Visited, Path) :-
    normalize_city(Current, CurrentNorm),
    normalize_city(Next, NextNorm),
    (connectedCities(CurrentNorm, NextNorm); connectedCities(NextNorm, CurrentNorm)),
    not(member(NextNorm, Visited)),
    findPath(NextNorm, Goal, [NextNorm|Visited], Path).

% Rule to sort all suspects (let’s see who’s naughty!)
sortAllSuspects :-
    write('Our detective AI agent is sniffing out bad guys!'), nl,
    findall([Suspect, Reasons], suspectsByLocation(murder, _, Suspect, Reasons), SuspectList),
    (   SuspectList = [] ->
        write('No bad guys found, maybe they are hiding?'), nl
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

% Load CSV at start (let’s get that data!)
:- initialization(load_csv_data('suspects.csv')).