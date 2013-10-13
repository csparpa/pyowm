Per disaccoppiare la fase di parsing JSON dagli specifici formati delle risposte
devo creare un'astrazione e fare dipendere il parser da essa, creerò poi una 
specializzazione per ciascun formato concreto.
La mappa tra ogni tipologia di risposta JSON e la relativa specializzazione
che ne individua le caratteristiche utili per il parsing può così essere
iniettata da configurazione e quindi facilmente cambiata nel caso in cui
il formato JSON delle risposte cambi oppure si debba implementare il
parsing per nuove risposte che prima non c'erano

Cosa cambia?

OWM.py
------
	dentro OWM.py avro ad es:
	
	orp = OWMResponseParser()  <-- staticamente costruito da OWM.py
	def weather_at(...):
		[...]
		observation = orp.parse_weather_at(json_data, DataDescriptor d)
	
OWMResponseParser.py (new class)
--------------------------------

	class OWMResponseParser() <-- contiene dict che mappa i sottotipi di DataDescriptor sui metodi,
	  il dict è iniettabile (es: letto da constants.py)
	  
	orp.parse_weather_at:
	    1. estrae la descrizione dell'oggetto invocando d.description()
	    2. costruisce l'oggetto Observation, ad esempio la costruzione
	       può essere delegata ad uno specifico metodo Factory aggiunto
	       a Observation.py (che dipenderà da ObservationDataDescriptor.py)

DataDescriptor.py
-----------------
	class DataDescriptor():
	    classe atratta, ha il solo metodo description(): è l'astrazione
	    che disaccoppia il parsing dalle specificità dei formati JSON!
	    E' il pattern "framework"
	
ObservationDataDescriptor.py (new class)
----------------------------------------
	class ObservationDataDescriptor(DataDescriptor):
	    1. ritorna un dict con i campi dell'oggetto e dove trovarli nel json
	    es: description() --> dict
	    
Oltre a ObservationDataDescriptor ci sono altre classi figlie di DataDescriptor,
una per ogni risposta dell'API OWM