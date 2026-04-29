% Criminal problem 
% Facts
american(west).
enemy(nono, america).
owns(nono, m1).
missile(m1).
sold(west, m1, nono).
% Rules
criminal(X) :
    american(X),
    weapon(Y),
    sold(X, Y, Z),
    hostile(Z).  % Added this to connect the "criminal" to the "enemy"
hostile(X) :
    enemy(X, america).
weapon(X) :
    missile(X).