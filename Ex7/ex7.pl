% ==================================================
% FACTS: Genders
% ==================================================
male(john). male(bob). male(tom). male(steve).
male(fred). male(scott). male(jack). male(rich).
male(mike). male(harry). male(carol). male(jim).

female(patty). female(mary). female(alice). female(linda).
female(valerie). female(barbara). female(donna). female(rachel).
female(jane). female(cindy).

% ==================================================
% FACTS: Parentage (Based strictly on the image)
% ==================================================
% Carol: Parents are Patty & John
father(john, carol).
mother(patty, carol).

% Tom & Linda: Parents are John & Mary
father(john, tom).     mother(mary, tom).
father(john, linda).   mother(mary, linda).

% Jim: Parents are Mary & Bob
father(bob, jim).
mother(mary, jim).

% Children of Tom & Alice
father(tom, valerie).   mother(alice, valerie).
father(tom, barbara).   mother(alice, barbara).

% Children of Linda & Steve
father(steve, jack).    mother(linda, jack).
father(steve, rich).    mother(linda, rich).

% Great-grandchildren generation
father(fred, jane).     mother(valerie, jane).
father(scott, cindy).   mother(barbara, cindy).
father(jack, mike).     mother(donna, mike).
father(rich, harry).    mother(rachel, harry).

% ==================================================
% RULES: Strict Logic
% ==================================================
parent(X, Y) :- father(X, Y) ; mother(X, Y).

% STRICT SIBLING: Must share BOTH Father and Mother
sibling(X, Y) :-
    father(F, X), father(F, Y),
    mother(M, X), mother(M, Y),
    X \= Y.

brother(X, Y) :- sibling(X, Y), male(X).
sister(X, Y) :- sibling(X, Y), female(X).

% Ancestry
grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
grandfather(X, Y) :- grandparent(X, Y), male(X).
grandmother(X, Y) :- grandparent(X, Y), female(X).

% Extended Family
aunt(X, Y) :- sister(X, P), parent(P, Y).
uncle(X, Y) :- brother(X, P), parent(P, Y).
cousin(X, Y) :- parent(P1, X), parent(P2, Y), sibling(P1, P2).

% ==================================================
% RELATION WRAPPER
% ==================================================
relation(X, Y, brother) :- brother(X, Y).
relation(X, Y, sister) :- sister(X, Y).
relation(X, Y, father) :- father(X, Y).
relation(X, Y, mother) :- mother(X, Y).
relation(X, Y, grandfather) :- grandfather(X, Y).
relation(X, Y, grandmother) :- grandmother(X, Y).
relation(X, Y, uncle) :- uncle(X, Y).
relation(X, Y, aunt) :- aunt(X, Y).
relation(X, Y, cousin) :- cousin(X, Y).
