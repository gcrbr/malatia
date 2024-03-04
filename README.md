# Malatìa
![Interfaccia](https://i.imgur.com/CVmR3XJ.png)
Misterioso strumento per dileguarsi da Napoli (o altre città, con codice opportunamente modificato) a basso costo e in occulte circostanze.

Questo piccolo script scritto in Python effettua le seguenti operazioni:
- Ricerca viaggi con partenza da Napoli verso destinazioni stabilite (solo per alcuni vettori) o comunque tra quelle offerte dal vettore
- Confronta i prezzi con una soglia stabilita all'interno del codice
- Aggiunge i risultati in una lista 
- Riordina i risultati in base al prezzo (ascendente)
- Li salva in un file (`data.json`)

Questa sequenza di operazioni viene eseguita ogni cinque ore.

I risultati sono visualizzabili attraverso un'interfaccia realizzata con HTML, CSS e JavaScript base. 

Questa non fa altro che visualizzare i contenuti del file `data.json` in un formato tabellare leggibile.

## Vettori supportati
| Ryanair            | FlixBus            | Italo | Volotea | Wizz Air | Trenitalia | Itabus |
|--------------------|--------------------|-------|---------|----------|------------|--------|
| ✓ | ✓ |       |         |          |            |        |

Il supporto per gli altri vettori sarà introdotto nelle versioni successive.

# Installazione
Le uniche librerie richieste sono `dateutil` e `requests`, entrambe installabili con il seguente comando:
```bash
pip install python-dateutil requests
```

Per avviare lo script:
```bash
python backend/core.py
````

Per visualizzare l'interfaccia invece, bisogna avviare un server HTTP che possa servire i file opportuni.

Banalmente, è possibile utilizzare `SimpleHTTPServer` di python eseguendo il seguente comando all'interno della cartella root della repository:
```bash
python3 -m http.server
``` 