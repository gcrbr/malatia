# Malatìa
![Interfaccia](https://i.imgur.com/FYRMGvl.png)
Misterioso strumento per dileguarsi da Napoli (o altre città, con codice opportunamente modificato) a basso costo e in occulte circostanze.

Questo piccolo script scritto in Python effettua le seguenti operazioni:
- Ricerca viaggi con partenza da Napoli verso destinazioni stabilite (solo per alcuni vettori) o comunque tra quelle offerte dal vettore
- Confronta i prezzi con una soglia stabilita 
- Aggiunge i risultati in una lista 
- Riordina i risultati in base al prezzo (ascendente)
- Li salva in un file (`data.json`)

Questa sequenza di operazioni viene ad intervalli regolari.

I risultati sono visualizzabili attraverso un'interfaccia realizzata con HTML, CSS e JavaScript base. 

Questa non fa altro che visualizzare i contenuti del file `data.json` in un formato tabellare leggibile.

## Vettori supportati
| Ryanair            | FlixBus            | Italo | Volotea | Wizz Air | Trenitalia | Itabus |
|--------------------|--------------------|-------|---------|----------|------------|--------|
| ✓ | ✓ |  |         |          |            | ✓ |

Il supporto per gli altri vettori sarà introdotto nelle versioni successive.

# Installazione
Le uniche librerie richieste sono `dateutil` e `requests`, entrambe installabili con il seguente comando:
```bash
pip install python-dateutil requests
```

Per avviare lo script:
```bash
python main.py
````

Per visualizzare l'interfaccia grafica basta avviare lo script con l'opzione `-i` o `--interface`:
```bash
python main.py -i
````

Le altre opzioni sono visualizzabili con il parametro `-h` o `--help`.