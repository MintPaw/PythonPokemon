This is the client application

This was meant to be quite a complex game. Let me quickly explain how it was suppose to work.
Each Pokemon is this game, using the random seed of their name minus their base stats, they are given new stats.
A stun, a debuff, and a counter.
The stun stuns for X turns with an Y% chance.
The debuff reduces attack for X and defense for Y for Z turns.
The counter has a X% chance to return Y% of the next damage taken.

All of this was generated off their name so they're consistant without me having to write all the values.
Each Pokemon's base stats are considered as well, so a Pokemon like Mewtwo won't get an insane stun because he already has so much base damage and defense.

I hopped this would create some kind of fair meta, like Mewtwo has high base stats.
But Charmander has a ridiculous 50% 7 turn stun, so he'd be a logic counter to Mewtwo.
And since you're both pulling from pools unknown to your opponent this could actually be a quite engaging game.

Although little of this actually works.
The Pokemon are generated properly, you can connect properly, you can Swap, Attack, and Stun properly.
Debuff works inconstantly, and Prepare(counter) doesn't work at all.
Death doesn't work.
And theirs a random glitch I don't understand that causes both clients to no longer respond. Although it's somewhat rare.

Server related stuff is explained in the server README.txt but it's a basic turn-based setup.

I took on way too much and don't have enough of an understanding of Python to get it done.
I did although learn quite a bit about sockets and had fun, see ya next semester.