main :-
    write('--- Prolog Calculator ---'), nl,
    write('1. Addition'), nl,
    write('2. Subtraction'), nl,
    write('3. Multiplication'), nl,
    write('4. Division'), nl,
    write('5. Exit'), nl,
    write('Choose an option (1-5): '),
    read(Choice),
    process(Choice).

% Exit condition
process(5) :-
    write('Goodbye!'), nl, !.

% Process valid arithmetic choices
process(Choice) :-
    Choice >= 1, Choice =< 4,
    write('Enter first number: '), read(A),
    write('Enter second number: '), read(B),
    calculate(Choice, A, B, Result),
    format('Result: ~w~n', [Result]),
    nl, main. % Loop back to menu

% Handle invalid input
process(_) :-
    write('Invalid choice, try again.'), nl,
    main.

% Arithmetic Logic
calculate(1, A, B, R) :- R is A + B.
calculate(2, A, B, R) :- R is A - B.
calculate(3, A, B, R) :- R is A * B.
calculate(4, A, B, R) :- B \= 0, R is A / B.
calculate(4, _, 0, 'Error: Division by zero').