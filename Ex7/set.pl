%Set operations 
% --- Member --
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).
% --- Union --
union([], L, L).
union([H|T], L, R) :- member(H, L), !, union(T, L, R).
union([H|T], L, [H|R]) :- union(T, L, R).
% --- Subset --
subset([], _).
subset([H|T], L) :- member(H, L), subset(T, L).
% --- Intersection --
intersection([], _, []).
intersection([H|T], L, [H|R]) :- member(H, L), !, intersection(T, L, R).
intersection([_|T], L, R)     :- intersection(T, L, R).
% --- Difference (A - B) --
difference([], _, []).
difference([H|T], L, R)    :- member(H, L), !, difference(T, L, R).
difference([H|T], L, [H|R]):- difference(T, L, R).
% --- Cardinality (length of set) --
cardinality([], 0).
cardinality([_|T], N) :
    cardinality(T, N1),
    N is N1 + 1.
% --- Is Equivalent (two sets have same elements) --
is_equivalent(A, B) :
    subset(A, B),
    subset(B, A).
% ============================================================
% RUN MENU FOR SET OPERATIONS
% ============================================================
run_sets :
    write('=== SET OPERATIONS MENU ==='), nl,
    write('1. Member'), nl,
    write('2. Union'), nl,
    write('3. Subset'), nl,
    write('4. Intersection'), nl,
    write('5. Difference'), nl,
    write('6. Cardinality'), nl,
    write('7. Is Equivalent'), nl,
    write('Enter choice (1-7): '),
    read(Choice),
    run_choice(Choice).
% --- Choice 1: Member --
run_choice(1) :
    write('Enter element (e.g. 3): '), read(X),
    write('Enter list (e.g. [1,2,3]): '), read(L),
    (member(X, L) ->
        write('Yes! Element IS a member.'), nl
    ;
    ).
        write('No! Element is NOT a member.'), nl
% --- Choice 2: Union --
run_choice(2) :
    write('Enter list 1 (e.g. [1,2,3]): '), read(L1),
    write('Enter list 2 (e.g. [2,3,4]): '), read(L2),
    union(L1, L2, Result),
    write('Union = '), write(Result), nl.
% --- Choice 3: Subset --
run_choice(3) :
    write('Enter smaller list (e.g. [1,2]): '), read(L1),
    write('Enter bigger list (e.g. [1,2,3]): '), read(L2),
    (subset(L1, L2) ->
        write('Yes! It IS a subset.'), nl
    ;
    ).
        write('No! It is NOT a subset.'), nl
% --- Choice 4: Intersection --
run_choice(4) :
    write('Enter list 1 (e.g. [1,2,3]): '), read(L1),
    write('Enter list 2 (e.g. [2,3,4]): '), read(L2),
    intersection(L1, L2, Result),
    write('Intersection = '), write(Result), nl.
% --- Choice 5: Difference --
run_choice(5) :
    write('Enter list 1 (e.g. [1,2,3]): '), read(L1),
    write('Enter list 2 (e.g. [2,3,4]): '), read(L2),
    difference(L1, L2, Result),
    write('Difference = '), write(Result), nl.
% --- Choice 6: Cardinality --
run_choice(6) :
    write('Enter list (e.g. [1,2,3]): '), read(L),
    cardinality(L, N),
    write('Cardinality = '), write(N), nl.
% --- Choice 7: Is Equivalent --
run_choice(7) :
    write('Enter list 1 (e.g. [1,2,3]): '), read(L1),
    write('Enter list 2 (e.g. [3,1,2]): '), read(L2),
    (is_equivalent(L1, L2) ->
        write('Yes! Sets ARE equivalent.'), nl
    ;
        write('No! Sets are NOT equivalent.'), nl
    ).
% --- Invalid choice --
run_choice(_) :
    write('Invalid choice! Please enter 1-7.'), nl.
    