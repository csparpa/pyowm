Cosa succede se il JSON ritornato da uno degli endpoint cambia?
===============================================================
Uso una strategia di parsing per ogni endpoint (pattern Strategy).
Lo step di parsing dell'algoritmo comune di richiesta dati all'API si affida
ad un'istanza specifica del parser, la quale implementa il "lavoro sporco"

Cosa succede se viene introdotto un nuovo endpoint?
===================================================
Devo aggiungere un nuovo feature method a owm.py, il quale eredita/ridefinisce gli step
dell'alg comune di richiesta dati all'API e implementa lo step di parsing JSON
usando una nuova strategia di parsing
    
  
Come isolare il baco del n di risultati?
========================================
Uso il pattern template method (hook): ogni feature method di owm.py usa un'istanza
concreta dell'algoritmo comune di richiesta dati all'API, il quale prevede uno
step di sintesi dei query parameters. Se un domani il baco viene corretto, basta
creare una nuova istanza concreta dell'alg/estendere quella del baco e rimpiazzarla:
non si modifica codice.

Cosa succede se viene rilasciata una nuova versione dell'API?
=============================================================
Si riutilizzano le astrazioni - TBD