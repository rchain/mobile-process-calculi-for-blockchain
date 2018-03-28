.. _enter-the-blockchain:

*******************************************************************************
Dentro la blockchain
*******************************************************************************

Un modo semplice per interpretare la tecnologia blockchain è il fatto che fornisca una tecnologia di replica decentralizzata. Lo stato può essere replicato attraverso una rete di nodi senza un'autorità centralizzata che gestisca la replica. La sottile interazione tra questo meccanismo di replica e la sicurezza basata sull'economia, a volte oscura il valore di base della replica stessa. La replica di questa natura è già una proposta di grande valore con un alto impatto. Ne è testimone la proposta di Ethereum. L'essenza di questa è di replicare lo stato di una macchina virtuale (VM), anziché lo stato del registro, sulla blockchain. Ciò fornisce non solo un sistema di contratto intelligente, ma una risorsa di calcolo pubblica globale che non può essere ignorata.

Altri oltre Wall Street o la City dovrebbero sedersi e prendere nota. AWS di Amazon, il Cloud Service di Google, Azure di Microsoft, tutte queste attività sono profondamente influenzate dalla proposta di Ethereum. Il fatto che il registro o l'aspetto economico dello stato replicato possa ora essere utilizzato come misura di sicurezza economica contro gli attacchi DoS alla risorsa di calcolo globale serve a rafforzare la proposta. Cambia anche la natura dell'ecosistema che utilizza questi servizi.

L'intero valore della proposta dei provider di infrastrutture di servizi cloud dipende in modo vitale dalle microtransazioni legate all'uso delle risorse di calcolo. La proposta Ethereum integra questo al livello più basso di esecuzione e archiviazione, in un modo cruciale per la sicurezza del sistema. È semplicemente un design migliore, più elegante, rispetto alle soluzioni cloud esistenti. Cosa ancora più importante, è realizzato come risorsa pubblica. Una delle recenti rivoluzioni che condivide alcune caratteristiche di questa situazione emergente è il cambiamento delle telecomunicazioni avvenuto grazie a Internet. I provider di telefonia sapevano che Internet avrebbe cambiato il modo di fare telecomunicazione e dovette impegnarsi per adattarsi a un paesaggio in cui più della metà delle telecomunicazioni a lunga distanza sarebbero state condotte utilizzando servizi gratuiti come Skype, zoom e Google Hangouts. Anche i fornitori di servizi di infrastruttura cloud e l'intera rete di servizi interconnessi che ne fanno parte, dovranno passare a un panorama in cui esiste un sofisticato mercato di criptovalute integrato con risorse di calcolo pubbliche disponibili a livello globale al livello più basso.

Casper
===============================================================================

A livello di 20K piedi questa è un'idea profonda, ma a livello di esecuzione per i sistemi di produzione, mette in evidenza diversi desiderata. Prima di tutto, richiede una tecnologia di replica diversa! La stessa tecnologia che ha dato vita alla proposta di Ethereum è la prima cosa che deve essere reimmaginata per rendere possibile l'idea di Ethereum su scala di Internet per i sistemi di produzione. La prova del lavoro è semplicemente troppo costosa in termini di energia. Gli argomenti su questo sono numerosi e tutti i principali stakeholder nella comunità di sviluppo di Ethereum li hanno abbracciati. Invece, un nuovo algoritmo pay-to-play, chiamato Casper, è in fase di sviluppo da parte di una libera federazione di stakeholder, tra cui Buterin, Zamfir e Meredith.

Scommessa per blocco contro scommessa per proposta
-------------------------------------------------------------------------------

Al centro dell'algoritmo di consenso di Casper vi è un ciclo di scambio di messaggi tra i validatori che partecipano al protocollo di replica. Questo ciclo di scambio di messaggi alla fine converge per produrre lo stato di consenso. Il protocollo è costruito in modo tale che il ciclo di consenso, a volte chiamato ciclo di scommesse, funzioni indipendentemente dal tipo di stato su cui i validatori stanno sviluppando un consenso. Potrebbe essere utilizzato per sviluppare il consenso su un singolo valore booleano (ad esempio il risultato di un coin flip), o qualcosa di molto più sofisticato, come lo stato di una macchina virtuale (VM). Questo si articola ulteriormente nel modo in cui lo stato è confezionato. Nello specifico, il nome stesso, blockchain, si riferisce al fatto che lo stato è impacchettato in blocchi concatenati. Quindi, un oggetto molto naturale del ciclo di consenso è un blocco. In parole povere, i validatori scambiano messaggi per convergere sul prossimo blocco della catena.

Ciò rappresenta un'evoluzione naturale, passo dopo passo, degli algoritmi PoW. Si noti, tuttavia, che questo tasso limita la produzione dei blocchi al ritmo del ciclo di consenso. Poiché i blocchi costituiscono un pacchetto di transazioni (in breve txn), ciò fornisce una stima approssimativa della capacità di elaborazione delle transazioni dell'algoritmo. Il PoC di Vitalik suggerisce che questo è molto, molto più veloce delle prestazioni della blockchain BTC basata su PoW. Tuttavia, l'obiettivo è quello di entrare nel range di 40K txns/sec, approssimativamente alla pari con i tassi di transazione delle reti finanziarie come Visa.
Per ottenere questo facciamo due osservazioni fondamentali. La prima di queste è il senso comune: la maggior parte delle transazioni è isolata. La transazione associata alla persona che acquista ricambi di automobili a Shanghai è separata e isolata dalla transazione associata alla persona che acquista il caffè a Seattle. L'isolamento di più transazioni concorrenti simultanee segue lo stesso principio dell'autostrada multi-corsia. Finché c'è poco o nessun cambiamento di corsia, c'è un rendimento molto maggiore su una superstrada a più corsie che su un'autostrada a corsia unica. Nessun cambiamento di corsia è ciò che intendiamo per isolamento. Seguendo questa analogia, vogliamo che un blocco rappresenti una sezione di autostrada con più corsie per le quali non vi è praticamente alcun cambio di corsia.

L'altra osservazione è più sottile. Ha a che fare con la compressione programmatica. Un'analogia che potrebbe aiutare viene dalla grafica del computer. Per molte immagini, come quella di una felce, ci sono due modi fondamentalmente diversi per disegnare l'immagine. In uno di essi, al programma di rendering viene fornito un ampio set di punti di dati corrispondenti ai pixel. Presumibilmente, questo set di dati è fornito dal campionamento, come potrebbe essere fornito dalla scansione di una felce reale. L'altro modo è riconoscere che esiste un modello algoritmico associato alle felci che viene essenzialmente catturato da un frattale. Quindi il set di dati dei pixel può essere rappresentato in un piccolo programma che genera l'immagine frattale corrispondente alla felce. In questo senso il programma rappresenta una forma di compressione. Anziché spedire il set di dati di grandi dimensioni di pixel al programma di rendering, viene inviato un programma relativamente piccolo e il programma di rendering esegue il programma per ottenere un flusso di pixel che può disegnare il più velocemente possibile.

Le raccolte di transazioni possono essere fornite con compressione simile usando le proposizioni. L'algoritmo LADL di Stay e Meredith descrive precisamente come una proposizione corrisponde a una raccolta di transazioni. Ciò che rimane è come mettere in relazione diverse proposizioni proposte da diversi validatori. In particolare, supponiamo che il validatore Abed stia guardando transazioni derivanti da una parte della rete mentre il validatore Troy sta esaminando le transazioni derivanti da un'altra porzione della rete. Supponendo che Abed e Troy stiano comunicando su quei gruppi di transazioni che usano le proposizioni, come possiamo assicurarci che i gruppi di transazioni siano coerenti? Questo è il caso in cui le proposizioni interpretate dall'algoritmo LADL hanno un potere di compressione significativo.

Attraverso il ragionamento mediante il livello logico è possibile determinare se una raccolta di proposizioni è coerente. Nel caso di proposizioni interpretate dall'algoritmo LADL esse saranno coerenti se e solo se il significato della loro combinazione (diciamo congiunzione) (cioè la raccolta che denotano) non è vuoto. Quando la combinazione è vuota, una o più proposizioni sono incoerenti. A questo punto i validatori invocano il ciclo di scommesse di Casper per scegliere un vincitore tra i sottoinsiemi di proposizioni massimamente coerenti. Una volta che il ciclo di scommesse converge, il blocco che viene determinato è dato in termini di una raccolta di proposizioni coerenti che poi si espande in un insieme molto più grande di transazioni, nello stesso modo in cui la felce viene resa dall'algoritmo di decompressione frattale che produce il set di pixel per l'immagine.

Dall’archiviazione di dati all’archiviazione dei blocchi nel modello RChain
-------------------------------------------------------------------------------

Basandoci sulle osservazioni nella sezione sull'archiviazione del contenuto e sulla query, ora possiamo fare nel dettaglio una rappresentazione diretta di JSON in un frammento della sintassi rholang di cui al diagramma qui sotto come RHOCore.

.. figure:: img/rhocore-1.png
   :align: center

   RSON : Rappresentazione dei dati di RChain

Questo illustra un punto di meta-livello sull'interpretazione dell'archiviazione dei dati. La semantica di archiviazione e accesso è coerente con un formato di serializzazione self-hosted, per il rendering dello stato su disco o filo. In termini pratici, ciò che un programmatore ha reso a JSON per la serializzazione sul filo o l'archiviazione in un database come mongodb, può essere reso a un'espressione isomorfa in un frammento della sintassi di rholang; e quell'espressione, se fosse eseguita, avrebbe effetti sull'archiviazione. Inoltre, la complessità del formato rispecchia esattamente JSON. Tuttavia, i tipi spaziali di rholang servono a fornire un meccanismo di convalida dei dati di tipo diretto per serializzare e deserializzare i dati.

Tuttavia, questo utilizza solo l'output o il lato del produttore della rappresentazione. Includendo il lato di input o del consumatore della rappresentazione, possiamo anche fornire una rappresentazione fedele ed efficiente della struttura dei blocchi. Per prima cosa, si noti il ​​significato della forma protetta di input. La prosecuzione è garantita per l'esecuzione in un contesto in cui i valori sono stati osservati nei canali.


.. figure:: img/rhocore-2.png
   :align: center

   RSON : Rappresentazione dei dati di RChain

Questa è esattamente una garanzia transazionale. Da ciò possiamo creare un'interpretazione fedele della struttura dei blocchi che corrisponde precisamente alla sintassi del programma.

.. figure:: img/rhocore-3.png
   :align: center

   RSON : Rappresentazione dei dati di RChain

    Anche la rappresentazione a blocchi si integra direttamente in RHOCore

Sharding
===============================================================================

Un altro obiettivo nel rendere pratica la proposta di Ethereum è quella di abbandonare il computer globale! Invece di una singola VM in esecuzione sulla blockchain, ciò che è richiesto è una composizione di VM che servono ciascuna un frammento di elaborazione del client. In un certo senso questo segna un ritorno alla visione originale di Internet come concepita quando è stato proposto il progetto Rosette/ESS. Ci sono alcune differenze chiave, tuttavia. Innanzitutto, lo stato di ogni VM è memorizzato sulla blockchain. In secondo luogo, anche se ogni VM è tagliata dallo stesso tessuto, c'è una disciplina che governa il modo in cui interagiscono. Nello specifico, sebbene siano tutte copie effettive della stessa VM, ciascuna opera su specifici spazi di indirizzi virtuali, o namespace come li chiamiamo noi. Quando operano sullo stesso namespace abbiamo la garanzia che lo stato su ogni copia è esattamente lo stesso. Questo è ciò a cui serve l'algoritmo di consenso.

L'uso di un account compositivo di namespace da coordinare tra le VM è uno degli ingredienti chiave mancanti nel design VM di Ethereum, e la ragione principale sta nel fatto che non è compositiva. L'altro cambiamento fondamentale è che il design della macchina RChain, come il design di Rosette/ESS, è fondamentalmente concorrente. I contratti intelligenti in RChain, come gli attori di Rosette/ESS, godono di una concorrenza fine-grained durante la loro esecuzione. Due fattori chiave contribuiscono a rendere questo sicuro per le transazioni finanziarie.

Concorrenza, non determinismo e sicurezza
-------------------------------------------------------------------------------

I due meccanismi che consentono l'esecuzione concorrente fine-grained per ottenere sicurezza nell'ambiente distribuito, operano a livelli fondamentalmente diversi. Uno è un meccanismo di runtime e l'altro è un meccanismo a tempo di compilazione. Il runtime è più facile da capire. Il non-determinismo derivante dall'esecuzione concorrente associata a un contratto nasce sempre come una gara della forma:

* due uscite che gareggiano per servire una richiesta di input

.. code-block:: scala

   x!( v1 ) | for( y <- x )P | x!( v2 )

* due richieste di input in competizione per un singolo output

.. code-block:: scala

  for( y <- x )P1 | x!( v ) | for( y <- x )P2

Sia che quella gara nasca dal calcolo interno al contratto sia che nasca tra il contratto e il suo ambiente. In uno qualunque dei due casi di gara possibili, per il progresso del contratto si sceglierà una delle riduzioni e quella scelta è la transazione. Questo è il significato del confine transazionale descritto sopra. Quindi, queste sono le transazioni che vengono replicate dall'algoritmo di consenso di Casper. Quindi, mentre esiste un non-determinismo interno, lo stato replicato è deterministico. Tutti i nodi nello stesso frammento vedono lo stesso stato.

Ciò rende ancora possibile scrivere codici non sicuri. Nonostante il determinismo dell'EVM, il bug DAO si presenta come una sorta di ingiustizia nella pianificazione degli aggiornamenti di stato relativi all'assistenza delle nuove richieste dei client; e, quando è espresso come contratto di rholang, si presenta una condizione di gara indesiderata. Cioè, c'è un livello di non-determinismo che è stato permesso dal contratto che non era sicuro rispetto alla semantica prevista del contratto. Nella maggior parte delle situazioni pratiche queste possono essere rilevate e prevenute in fase di compilazione utilizzando i tipi di comportamento spaziale di rholang. È certamente il caso nell'istanza specifica del bug sfruttato nell'attacco contro il DAO.


Cos'è una VM?
-------------------------------------------------------------------------------

Prendiamo un momento per esaminare cosa c'è in una VM. Ogni VM corrisponde a una tabella.
La tabella elenca un insieme di transizioni. Le transizioni sono della forma::

  <byte code, machine state> -> <byte code’, machine state’>

Le transizioni specificano cosa succede quando una macchina in un dato stato incontra
una particolare istruzione di byte code::

  rosette> (code-dump (compile '(+ 1 2)))
  litvec:
     0: {RequestExpr}
  codevec:
     0: alloc 2
     1: lit 1, arg[0]
     2: lit 2, arg[1]
     3: xfer global[+],trgt
     5: xmit/nxt 2
  rosette>

Gli esempi includono il caricamento di un letterale in un registro o nei valori del registro che appaiono e l'aggiunta di essi. Registri, heap, stack, questi sono esempi di componenti dello stato della macchina. Nel caso di RhoVM la transizione più importante è quella associata con I/O::

  for( y <- x )P | x!( Q ) -> P{ @Q / y }

Questa transizione dice che quando un thread protetto da input nella VM è in attesa di input su x, è in esecuzione concorrente con un thread impegnato e con output su x, quindi i dati passano lungo x, legati alla variabile y nella continuazione P. È importante capire che questa è davvero una transizione di livello più alto che può coinvolgere molti cambiamenti di stato di livello inferiore. Questo perché x può essere associato a un'ampia varietà di canali, dalle tabelle nella memoria locale, alle code AMQP, alle prese tcp/ip. Ognuno di questi ha una semantica naturale che interagisce senza intoppi con questa regola di transizione di livello superiore. L'interoperabilità tra questa regola di transizione di alto livello e la semantica dei diversi canali è esattamente ciò che fornisce la semantica Tuplespace.

Ciò che è importante per questa discussione, tuttavia, è il riconoscimento che una determinata istanza VM, ad esempio una copia della tabella VM più una configurazione specifica dello stato della macchina, può essere limitata per operare su una specifica raccolta di nomi. Questa raccolta di nomi, quello che abbiamo chiamato un namespace, può essere specificata a livello di programmazione e quindi non necessariamente finita.

In questa architettura un frammento corrisponde approssimativamente a un namespace e un'istanza della macchina ai nodi RChain nella rete su cui è memorizzato lo stato di questa VM. Diciamo "approssimativamente" perché i frammenti possono essere composti da frammenti, il che significa che esistono sottogruppi di nodi in un dato frammento che replicano lo stato della macchina limitato a un sottospazio del namespace. Allo stesso modo, poiché le macchine virtuali possono interagire solo se dispongono di namespace sovrapposti, è possibile sovrapporre più frammenti sugli stessi nodi. Ciò fornisce sia la funzionalità di disponibilità che di sicurezza, poiché l'utilizzo di questi fatti sulle relazioni tra VM, nodi e namespace, trovando una correlazione tra posizioni fisiche di nodi e namespace, può essere reso computazionalmente difficile quanto desiderato.

