# Malatìa
![Interfaccia](https://i.imgur.com/9knQYPY.png)
![Mappa](https://i.imgur.com/YR3jYne.png)

Strumento per dileguarsi a basso costo e in circostanze misteriose.

Questo programma si occupa di ricercare viaggi a basso costo su diversi vettori da una località di partenza prestabilita verso località designate o comunque offerte dal vettore.

I risultati sono visualizzabili attraverso un'interfaccia realizzata con HTML, CSS e JavaScript base. 

Questa non fa altro che visualizzare i contenuti del file `data.json` in un formato tabellare leggibile.

## Vettori supportati
| Ryanair            | FlixBus            | Italo | Volotea | Wizz Air | Trenitalia | Itabus | easyJet |
|--------------------|--------------------|-------|---------|----------|------------|--------|------|
| ✓ | ✓ | ✓ |         |          |            | ✓ | | |

Il supporto per gli altri vettori sarà introdotto nelle versioni successive.

## Installazione
Le uniche librerie richieste sono `dateutil` e `requests`, entrambe installabili con il seguente comando:
```bash
pip install python-dateutil requests
```

## Utilizzo
Per avviare lo script:
```bash
python main.py
````

Per visualizzare l'interfaccia grafica basta avviare lo script con l'opzione `-i` o `--interface`:
```bash
python main.py -i
````

Le altre opzioni sono visualizzabili con il parametro `-h` o `--help`.

## Configurazione
All'interno del file `config.json` è possibile modificare:
- La città di partenza da cui cercare i viaggi
- Le città supportate
- Il tetto massimo per il prezzo dei viaggi
- Il tempo tra una ricerca e l'altra (in secondi)

È importante assicurarsi che la città selezionata come partenza supporti tutti i vettori utilizzati. 

In breve - bisogna verificare che per la data città, tutti i campi all'interno di `identifiers` siano riempiti adeguatamente.