.. _actors-tuples-and-pi:

*******************************************************************************
Attori, Tuple e π
*******************************************************************************

Rosette
===============================================================================

Al MCC, il gruppo di ricerca Carnot ha predetto la commercializzazione di Internet un intero decennio prima che Netscape diventasse famoso. Il gruppo Carnot, tuttavia, era concentrato su applicazioni decentralizzate e distribuite e sullo sviluppo di un nodo di applicazione di rete, denominato Extensible Services Switch, o ESS, e al linguaggio di programmazione Rosette per la programmazione di questi nodi. In Rosette/ESS il modello in esame era il modello dell’attore. Qui stiamo parlando in modo abbastanza specifico di un'elaborazione del modello sviluppato da Carl Hewitt e raffinato da Gul Agha, che successivamente si sono consultati sulla progettazione di Rosette.

L'elaborazione di Rosette è stata sorprendente per portata ed eleganza. In particolare, Rosette decompone un attore in

* una casella di posta (una coda in cui arrivano i messaggi dei client dell'attore)
* uno stato (una tupla di valori)
* una meta (una descrizione di come accedere ai valori nello stato in termini di chiavi più astratte)
* e un oggetto di comportamento condiviso (una mappa dai tipi di messaggi al codice da eseguire in risposta, approssimativamente equivalente a un vtable in linguaggi come C ++)

L'elaborazione di un attore consiste nella lettura del messaggio successivo nella casella postale, utilizzando l'oggetto del comportamento condiviso (o sbo) per determinare quale codice eseguire in risposta al messaggio e quindi eseguire quel codice in un ambiente in cui i riferimenti alle chiavi descritti nella meta sono legati a posizioni nella tupla di stato. Tale codice invierà principalmente messaggi ad altri attori e probabilmente attenderà delle risposte.

Un attore fornisce una visione coerente dello stato in esecuzione concorrente tramite un aggiornamento; ovvero, un attore non elabora il messaggio successivo nella casella postale finché non viene richiamato l'aggiornamento e mentre l'attore sta elaborando il messaggio corrente, la casella postale viene considerata bloccata e mette in coda le richieste dei client. Quando un attore richiama un aggiornamento, viene creato un nuovo thread logico di attività per elaborare il messaggio successivo in coda nella casella postale. La vista di quel thread sullo stato dell'attore è qualsiasi cosa venga fornita all'aggiornamento. Il thread precedente può ancora apportare modifiche allo stato, ma non saranno osservabili da tutti i thread successivi che elaborano i messaggi successivi nella casella postale e quindi da tutte le richieste successive dei client. Questo approccio fornisce una nozione scalabile di concorrenza che collassa al non determinismo dell'ordine di arrivo dei messaggi in contenitori a thread singolo, e si espande quando esiste un supporto a livello di sistema per mappare i thread logici in alcuni contenitori esterni (come una VM, un sistema operativo o l'hardware, di per sé).

Già, questo è un modello di attori molto più articolato di quanto esista oggi nella maggior parte dei sistemi industriali (cfr. Struttura AKKA di Scala). Ciò che rende il modello Rosette molto più elegante, tuttavia, è il suo totale impegno nella programmazione di meta-livello. Nel modello Rosette, tutto è un attore. In particolare, la casella postale di un attore è un attore, e questo ha, a sua volta, una casella di posta, stato, meta e sbo. È interessante notare che Rosette rende questo modello completamente riflettente con la possibilità di eseguire regressioni infinite alla pari o migliori rispetto a linguaggi come Java o C #.

In un certo senso, la riflessione strutturale degli attori nel modello Rosette viene ripresa in linguaggi come Java, dove le classi sono a loro volta oggetti che possono essere analizzati a livello di codice e inseriti nella computazione. Tuttavia, Rosette fa fare al principio di riflessione un ulteriore passo avanti. Il modello offre non solo una riflessione strutturale, ma una riflessione procedurale, fornendo una nozione di continuità riconciliata con la concorrenza insita nel modello. Specificamente, proprio come uno shift-block in una presentazione in stile shift-reset di continuazioni delimitate rende la continuazione in attesa disponibile al codice nel blocco, il metodo di riflessione di Rosette rende disponibile la continuazione in attesa come parametro del metodo nel corpo del metodo. Maggiori informazioni su questo più avanti.

Per chiudere questa breve nota di sintesi, si noti che Rosette non è solo strutturalmente e proceduralmente riflessiva, ma anche lessicalmente riflessiva. Cioè, tutta la struttura sintattica dei programmi in Rosette sono anche attori! L'infrastruttura riflettente per questo fornisce la base per un sistema macro igienico, un supporto per linguaggi incorporati specifici del dominio e ospita una miriade di altre caratteristiche di elaborazione sintattica e simbolica che molti linguaggi industriali ancora faticano a fornire circa 20 anni dopo l'inizio di Rosette.

Tuplespaces
===============================================================================

Più o meno nello stesso periodo in cui il modello Rosette veniva studiato per lo sviluppo di applicazioni in questo ambiente decentralizzato e distribuito, Gelernter ha proposto Tuplespaces. Qui l'idea è di creare un deposito logico al di sopra di quello fisico e livelli di comunicazione di Internet. Il deposito è essenzialmente organizzato come un database di valori-chiave distribuiti in cui le coppie di valori-chiave vengono usate come meccanismi di comunicazione e di coordinamento tra i calcoli. Gelernter descrive tre operazioni di base per l'interazione con il tuplespace, :code:`out` per creare un nuovo oggetto dati in tuplespace, :code:`in` per consumare (rimuovere) un oggetto da tuplespace e :code:`rd` per leggere un oggetto senza rimuoverlo.

A differenza dei sistemi di trasmissione dei messaggi, questo approccio consente a mittenti e destinatari di operare senza alcuna conoscenza l'uno dell'altro. Quando un processo genera un nuovo risultato di cui altri processi avranno bisogno, semplicemente scarica i nuovi dati in tuplespace. I processi che hanno bisogno di dati possono cercarlo nel tuplespace utilizzando la corrispondenza dei modelli.


.. code-block:: lisp

   out("job", 999, "abc")

   in("job", 1000, ?x) ; si blocca perché non c'è alcuna tupla corrispondente
   in("job", 999, x:string) ; prende quella tupla dal tuplespace, assegnando 'abc' a x


Ciò solleva domande su come la pubblicazione dei dati viene mantenuta e cosa succede ai calcoli che sono stati sospesi in attesa di coppie valore-chiave che non sono presenti nel tuplespace. Inoltre, il meccanismo del tuplespace non si impegna in nessun modello di programmazione. Gli agenti che utilizzano il tuplespace possono essere scritti in un'ampia varietà di modelli di programmazione con un'ampia varietà di implementazioni e interpretazioni della semantica concorrente concordata. Questo rende il ragionamento sulla semantica end-to-end di un’applicazione fatta da molti agenti che interagiscono attraverso il tuplespace, molto, molto più difficile. Tuttavia, la semplicità del modello di comunicazione e coordinamento è stata molto apprezzata e ci sono state molte implementazioni dell'idea del tuplespace nei decenni successivi.

Una notevole differenza tra la nozione tuplespace di coordinamento e il modello dell'attore si trova nel principale limite del port degli attori. Un attore ha un posto, la sua casella di posta, dove sta ascoltando il resto del mondo. I sistemi reali e lo sviluppo dei sistemi reali spesso richiedono che le applicazioni ascoltino due o più origini di dati e che si coordinino tra di loro. Procedure decisionali di fork-join, ad esempio, in cui le richieste di informazioni vengono generate da più origini di dati e quindi il calcolo successivo rappresenta un'unione dei flussi di informazioni risultanti dalle origini di dati autonome, sono piuttosto standard nei processi decisionali umani, dall'elaborazione del prestito, alla revisione di articoli accademici. Ovviamente è possibile disporre di un attore che coordini più attori che sono poi incaricati di gestire le fonti di dati indipendenti. Questo produce un sovraccarico dell'applicazione e interrompe l'incapsulamento in quanto gli attori devono essere consapevoli del loro coordinamento.

Al contrario, il modello tuplespace è adatto ai calcoli che si coordinano su più fonti di dati autonomi.

Implementazioni distribuite di calcoli di processi mobili
===============================================================================

Tomlinson, Lavender e Meredith, tra gli altri, hanno fornito una realizzazione del modello di tuplespace all'interno di Rosette/ESS come mezzo per studiare i due modelli fianco a fianco e confrontare le applicazioni scritte in entrambi gli stili. Fu durante questo lavoro che Meredith iniziò un'indagine intensiva sui calcoli del processo mobile come terza alternativa al modello attore e al modello tuplespace. Uno dei principali obiettivi era quello di collegare un modello di programmazione uniforme, come il modello attore di Rosette, rendendo molto più facile ragionare sulla semantica delle applicazioni, con la nozione semplice e flessibile di comunicazione e coordinamento offerta nel modello di tuplespace.

Nel codice mostrato qui sotto, i metodi che i nomi consumano e producono, sono usati invece dei verbi tradizionali di Linda :code:`in` e :code:`out`. La ragione è che una volta scoperta la strategia del metodo riflessivo, e poi perfezionata con continuazioni delimitate, si è arrivati a nuove osservazioni vitali relative al ciclo di vita dei dati e alla loro continuazione.

.. code-block:: none
   :caption: Un'implementazione di Rosette nel tuplespace ottiene la semantica

   (defRMethod NameSpace (consume ctxt & location)
    ;;; facendo di questo un metodo riflessivo - RMethod - otteniamo l'accesso alla prosecuzione in attesa
    ;;; legato al parametro formale ctxt
    (letrec [[[channel ptrn] location]
                   ;;; il canale e il modello dei messaggi in arrivo da cercare sono destrutturati e legati
           [subspace (tbl-get chart channel)]
                   ;;; i messaggi in arrivo associati al canale sono raccolti in una sottotabella
                   ;;; in questo senso possiamo vedere che la struttura semantica supporta una composizione
                   ;;; argomento/sottoargomento/sottoargomento/… tecnica di strutturazione che unifica il passaggio dei messaggi
                   ;;; con primitivi di consegna del contenuto
                   ;;; il nome del canale diventa l'argomento e la struttura del modello diventa
                   ;;; l'albero sottoargomento
                   ;;; anche questo si unifica con la vista URL dell'accesso alle risorse
          [candidates (names subspace)]
          [[extractions remainder]
             (fold candidates
               (proc [e acc k]
                   (let [[[hits misses] acc]
                   [binding (match? ptrn e)]]
               (if (miss? binding)
                   (k [hits [e & misses]])
                   (k [[[e binding] & hits] misses])))))]
                     ;;; nota che questo è generico nei predicati corrispondenza? e manca?
                     ;;; la corrispondenza potrebbe essere unificata (come in SpecialK) o potrebbe essere
                     ;;; un certo numero di altri protocolli a scopi speciali
                     ;;; il prezzo per questa genericità è la prestazione
                     ;;; c'è una ricerca accettabile che mostra che esistono discipline di hashing
                     ;;; ciò potrebbe fornire un'approssimazione più che ragionevole dell'unificazione
          [[productions consummation]
               (fold extractions
                 (proc [[e binding] acc k]
                   (let [[[productions consumers] acc]
                  [hit (tbl-get subspace e)]]
                     (if (production? hit)
                  (k [[[[e binding] hit] & productions] consumers])
                  (k [productions [[e hit] & consumers]])))))]]
                     ;;; questo divide i colpi in quelle corrispondenze che sono dati e
                     ;;; quelle partite che sono continuazioni
                     ;;; e il resto del codice invia i dati alla prosecuzione in attesa
                     ;;; e aggiunge la continuazione a quelle partite che sono attualmente
                     ;;; a corto di dati
                     ;;; questa è una visione molto più fine-grained del centro escluso

      (seq
        (map productions
          (proc [[[ptrn binding] product]]
               (delete subspace ptrn)))
        (map consummation
             (proc [[ptrn consumers]]
               (tbl-add subspace
               ptrn (reverse [ctxt & (reverse consumers)]))))
        (update!)
        (ctxt-rtn ctxt productions))))

.. code-block:: none
   :caption: Un'implementazione di Rosette nel tuplespace mette la semantica

   ;;; Questo codice è perfettamente duale al codice del consumatore e quindi tutti i commenti
   ;;; si applicano nei codici dei siti corrispondenti
   (defRMethod NameSpace (produce ctxt & production)
    (letrec [[[channel ptrn product] production]
           [subspace (tbl-get chart channel)]
          [candidates (names subspace)]
          [[extractions remainder]
             (fold candidates
               (proc [e acc k]
                   (let [[[hits misses] acc]
                   [binding (match? ptrn e)]]
               (if (miss? binding)
                   (k [[e & hits] misses])
                   (k [hits [e & misses]])))))]
          [[productions consummation]
               (fold extractions
                 (proc [[e binding] acc k]
                   (let [[[productions consumers] acc]
                  [hit (tbl-get subspace e)]]
                     (if (production? hit)
                  (k [[[e hit] & productions] consumers])
                  (k [productions [[[e binding] hit] & consumers]])))))]]
      (seq
        (map productions
          (proc [[ptrn prod]] (tbl-add subspace ptrn product)))
        (map consummation
          (proc [[[ptrn binding] consumers]]
          (seq
               (delete subspace ptrn)
               (map consumers
                 (proc [consumer]
                   (send ctxt-rtn consumer [product binding])
                   binding)))))
        (update!)
        (ctxt-rtn ctxt product))))

In sostanza, la domanda è cosa succede a uno o entrambi i dati e alla continuazione dopo che una richiesta di input soddisfa una richiesta di output. Nella semantica tradizionale tuplespace e del π-calculus sia i dati che la continuazione vengono rimossi dal negozio. Tuttavia, è perfettamente possibile lasciare uno o entrambi nel negozio dopo l'evento. Ogni scelta indipendente porta a un diverso paradigma di programmazione principale.

.. topic:: Operazioni DB tradizionali

   Rimuovendo la continuazione ma lasciando i dati si costituisce un database standard:

   +----------+------------------+-------------------+------------------+----------------------+
   |          | ephemeral - data | persistent - data | ephemeral - data | persistent - data    |
   |          |                  |                   |                  |                      |
   |          | ephemeral - k    | ephemeral - k     | persistent - k   | ephemeral - k        |
   +----------+------------------+-------------------+------------------+----------------------+
   | producer | put              | **store**         | publish          | publish with history |
   +----------+------------------+-------------------+------------------+----------------------+
   | consumer | get              | **read**          | subscribe        | subscribe            |
   +----------+------------------+-------------------+------------------+----------------------+


.. topic:: Operazioni di messaggistica tradizionali

   Rimuovendo dei dati, ma lasciando la continuazione si costituisce un’iscrizione in un modello di pub/sub:

   +----------+------------------+-------------------+------------------+--------------------------+
   |          | ephemeral - data | persistent - data | ephemeral - data | persistent - data        |
   |          |                  |                   |                  |                          |
   |          | ephemeral - k    | ephemeral - k     | persistent - k   | ephemeral - k            |
   +----------+------------------+-------------------+------------------+--------------------------+
   | producer | put              | store             | **publish**      | **publish with history** |
   +----------+------------------+-------------------+------------------+--------------------------+
   | consumer | get              | read              | **subscribe**    | **subscribe**            |
   +----------+------------------+-------------------+------------------+--------------------------+

.. topic:: Blocco a livello di articolo in un'impostazione distribuita

   La rimozione di entrambi i dati e la continuazione sono la semantica standard dei calcoli e dei tuplespace del processo mobile:

   +----------+------------------+-------------------+------------------+----------------------+
   |          | ephemeral - data | persistent - data | ephemeral - data | persistent - data    |
   |          |                  |                   |                  |                      |
   |          | ephemeral - k    | ephemeral - k     | persistent - k   | ephemeral - k        |
   +----------+------------------+-------------------+------------------+----------------------+
   | producer | **put**          | store             | publish          | publish with history |
   +----------+------------------+-------------------+------------------+----------------------+
   | consumer | **get**          | read              | subscribe        | subscribe            |
   +----------+------------------+-------------------+------------------+----------------------+

Basandosi sulle intuizioni di Tomlinson sull'uso dei metodi riflessivi di Rosette per modellare la semantica dei tuplespace (vedi il codice sopra), Meredith ha fornito una codifica diretta del π-calculus nella semantica del tuplespace tramite continuazioni lineari. Questa semantica era al centro del BizTalk Process Orchestration Engine di Microsoft e Microsoft XLang, probabilmente il primo linguaggio di contrattazione intelligente su scala Internet, è stato il modello di programmazione risultante. Questo modello ha avuto un'influenza diretta sugli standard del W3C, come BEPL e WS-Choreography, e ha generato un'intera serie di applicazioni e framework per l'automazione dei processi aziendali.

Come per i raffinamenti apportati da Rosette al modello dell'attore, il π-calculus porta un'ontologia specifica per le applicazioni basate sulla nozione di processi che comunicano tramite il messaggio che passa sui canali. È importante notare che la nozione di processo è parametrica in una nozione di canale e Meredith ha utilizzato questo livello di astrazione per fornire un'ampia varietà di tipi di canali in XLang, inclusi i collegamenti alle code di messaggi MSMQ di Microsoft, agli oggetti COM e molti altri punti di accesso nelle tecnologie popolari del tempo. Forse la cosa più importante per le odierne astrazioni di Internet è che gli URI forniscano una nozione naturale di canale che consenta la realizzazione del modello di programmazione tramite protocolli di comunicazione consapevoli dell'URI, come l’http. Allo stesso modo, in termini del clima di archiviazione odierno, le chiavi in ​​un archivio di valori-chiave, come un database nosql, si mappano direttamente alla nozione di canale nel π-calculus, e Meredith ha usato proprio questa idea per fornire la codifica del π-calculus nella semantica del tuplespace.

Da Tuplespace a π-calculus
-------------------------------------------------------------------------------

Il π-calculus cattura un modello strutturale di calcolo concorrente costruito dall'interazione basata sul passaggio di messaggi. Svolge lo stesso ruolo nel calcolo concorrente e distribuito come il lambda calcolo lo fa per i linguaggi funzionali e la programmazione funzionale, stabilendo l'ontologia di base del calcolo e trasformandolo in una sintassi e in una semantica in cui i calcoli possano essere eseguiti. Data una certa nozione di canale, costruisce una manciata di forme base di processo, le prime tre delle quali riguardano l'I/O, descrivendo le azioni di passaggio dei messaggi.

* :code:`0` è la forma del processo inerte o arrestato che costituisce il fondamento del modello
* :code:`x?( ptrn )P` è la forma di un processo protetto da input in attesa di un messaggio su
  canale :code:`x` che corrisponde a un modello, ptrn, e alla ricezione di tale messaggio
  continua eseguendo :code:`P` in un ambiente in cui qualsiasi variabile nel modello
  è legata ai valori nel messaggio
* :code:`x!( m )` è la forma di invio di un messaggio, :code:`m`, su un canale :code:`x`

I secondi tre riguardano la natura concorrente dei processi, la creazione di canali e la ricorsione.

* :code:`P|Q` è la forma di un processo che è la composizione parallela di due processi P e Q in cui entrambi i processi sono in esecuzione concorrente
* :code:`(new x)P` è la forma di un processo che esegue un sottoprocesso, P, in un contesto in cui x è associato a un nuovo canale, distinto da tutti gli altri canali in uso
* :code:`(def X( ptrn ) = P)[ m ]` e :code:`X( m )`, queste sono le forme di processo per la definizione ricorsiva e l'invocazione

Queste forme di base possono essere interpretate in termini di operazioni su Tuplespaces::

 P,Q ::=                     [[-]](-) : π -> Scala =
     0                       { }
     | x?(prtn)P             { val ptrn = T.get([[x]](T)); [[T]](P) }
     | x!(m)                 T.put([[x]], m)
     | P|Q                   spawn{ [[P]](T)  }; spawn{ [[P]](T) }
     | (new x)P              { val x = T.fresh("x"); [[P]](T) }
     | (def X(ptrn) = P)(m)  object X { def apply(ptrn) = { [[P]](T) } }; X(m)
     | X(ptrn)               X(ptrn)

Astrazione a struttura monadica del canale 
-------------------------------------------------------------------------------

Meredith ha quindi perseguito due distinte linee di miglioramento per queste caratteristiche. Entrambi sono collegati all'astrazione del canale. Il primo di questi mette in relazione l'astrazione del canale con l'astrazione del flusso che è diventata così popolare nel paradigma di programmazione reattiva. Nello specifico, è facile dimostrare che un canale nel π-calculus asincrono corrisponde a una coda non vincolata e persistente. Questa coda può essere vista come un flusso e l'accesso al flusso viene trattato in modo monodico, come avviene nel paradigma di programmazione reattiva. Questo ha l'ulteriore vantaggio di fornire una sintassi e una semantica naturali per il pattern fork-join così prevalente nelle applicazioni concorrenti che supportano le applicazioni decisionali umane menzionate in precedenza.

.. code-block:: none

  ( let [[data (consume ns channel pattern)]] P)

.. code-block:: scala

  for( data <- ns.consume(channel, pattern) ){ P }

Questo punto merita di essere discusso in modo più dettagliato. Mentre il π-calculus risolve la limitazione della porta principale del modello attore, non fornisce un supporto sintattico o semantico naturale per il modello fork-join. Alcune varianti del π-calculus, come il calcolo del join, sono state proposte per risolvere questa tensione, ma probabilmente quelle proposte subiscono un intreccio di caratteristiche che le rende inadatte a molti schemi di programmazione distribuita e decentralizzata. Invece, l'interpretazione monadica del canale fornisce un refactoring molto più mirato e elementare della semantica del π-calculus, coerente con tutte le semantiche denotazionali esistenti del modello, che fornisce una nozione naturale di fork-join mentre mappa anche in modo pulito nel paradigma della programmazione reattiva, e quindi rendendo l'integrazione dello sviluppo di grandi dimensioni, come Apache Spark, relativamente semplice.

Se guardiamo a questo dal punto di vista dell'evoluzione del linguaggio di programmazione, per prima cosa vediamo un refactoring della semantica come:

.. code-block:: none
   :emphasize-lines: 3

   P,Q ::=                     [[-]](-) : π -> Scala =
       0                       { }
       | x?(prtn)P             for( ptrn <- [[x]](T) ){ [[P]](T) }
       | x!(m)                 T.put([[x]], m)
       | P|Q                   spawn{ [[P]](T)  }; spawn{ [[P]](T) }
       | (new x)P              { val x = T.fresh("x"); [[P]](T) }
       | (def X(ptrn) = P)(m)  object X { def apply(ptrn) = { [[P]](T) } }; X(m)
       | X(ptrn)               X(ptrn)

dove la comprensione è lo zucchero sintattico per un uso della continuazione monadica. Il successo di questa interpretazione suggerisce un refactoring della **fonte** dell'interpretazione.

.. code-block:: none
   :emphasize-lines: 2

   P,Q :: = 0
            | for (ptrn <- x)P
            | x!(m)
            | P|Q
            | (new x)P
            | (def X(ptrn) = P)[m]
            | X(ptrn)

Questo refactoring si presenta nel lavoro di Meredith e Stay sulla semantica categoriale più alta per il π-calculus :cita:`DBLP:journals/corr/StayM15`, e successivamente viene incorporato nel design di rholang. Il punto importante da notare è che l'input basato sulla comprensione può ora essere facilmente esteso all'input da più fonti, ognuna delle quali deve passare un filtro, prima che la continuazione venga invocata.

.. math::

  for( ptrn_{1} \leftarrow x_{1}; \dotso; ptrn_{n} \leftarrow x_{n} if cond )P

L'utilizzo di una comprensione preliminare consente alla semantica di input guard di essere parametrica nella monade utilizzata per i canali, e quindi la particolare semantica del join può essere fornita in modo polimorfico. Il significato di questo non può essere sottovalutato. In particolare:

* Contrasta con il join-calculus in cui il join è inseparabilmente legato insieme alla ricorsione. La input guard monadica consente join anonimi, e unici, che sono abbastanza standard nei modelli di fork-join nei processi decisionali umani.
* Fornisce l'impostazione corretta in cui interpretare il trasformatore monade LogicT di Kiselyov. Ricercare ogni fonte di input fino a che non viene trovata una tupla di input che soddisfi le condizioni, è sensibile alla divergenza in ogni fonte di input. La fair interleaving e, soprattutto, un mezzo per descrivere in modo programmatico la politica di interleaving, è fondamentale per l’affidabilità e la disponibilità di servizi performanti. Questa è l'effettiva importazione di LogicT e il giusto contesto in cui schierare quel macchinario.
* Ora abbiamo una forma sintattica per le transazioni nidificate. In particolare,
  :code:`P` può essere eseguito solo in un contesto in cui sono associate tutte le modifiche di stato
  con le fonti di input e le condizioni sono soddisfatte. Inoltre, :code:`P` può essere
  ancora un altro processo protetto da input. Quindi un programmatore, o un analizzatore di programmi,
  è in grado di rilevare i confini delle transazioni *sintatticamente*. Questo è vitale per i contratti
  che coinvolgono transazioni finanziarie e altre transazioni mission-critical.

Un modello pre-RChain per i contratti intelligenti
-------------------------------------------------------------------------------

Questo è un precursore del modello RChain per i contratti intelligenti, come codificato nel design di rholang. Fornisce il più ricco set di primitive di comunicazione per i contratti di costruzione proposti fino ad oggi, guidati sia dalla teoria che dalla realizzazione e l’implementazione su scala industriale. Tuttavia, l'intera serie di primitive di contratto si adatta su un'unica riga. Non c'è una sola proposta di design in questo spazio, dalla blockchain basata su PoW all'EVM, che soddisfi le pressioni sull'assicurazione della qualità che questa proposta abbia sostenuto. Nello specifico, la proposta ripiega tutte le esperienze usando Rosette, Tuplespace e BizTalk e le riduce ad un unico progetto che soddisfa i desiderata scoperti in tutti questi sforzi. Lo fa con solo sette primitivi e primitivi che si allineano con i paradigmi di programmazione dominanti del mercato attuale. Tuttavia, come mostrano gli esempi delle specifiche di rholang e il documento sulla prevenzione del bug DAO con i tipi comportamentali, l'intera gamma di contratti che è possibile esprimere nella tecnologia blockchain esistente è espressa in modo compatto in questo modello.

Come visto nel design rholang, tuttavia, questo è solo l'inizio della storia. Un piccolo background è necessario per capire l'importazione e questo sviluppo. Negli ultimi 20 anni si è svolta una rivoluzione silenziosa in informatica e logica. Per molti anni era noto che i piccoli frammenti, anche se in crescita, dei tipi di modelli di programmazione funzionale, corrispondevano alle proposizioni e le prove corrispondevano ai programmi. Se la corrispondenza, conosciuta in vari modi come il paradigma proposizioni-come-tipi o l'isomorfismo di Curry-Howard, potesse essere usata per coprire una porzione significativa e pratica del modello, avrebbe profonde implicazioni per lo sviluppo del software. Ciò significa come minimo che la pratica standard dei programmi di controllo dei tipi coincide con la dimostrazione che i programmi godono di determinate proprietà come parte della loro esecuzione. Le proprietà associate al frammento iniziale coperto dall'isomorfismo di Curry-Howard hanno ampiamente a che fare con il rispetto della forma dei dati che fluiscono dentro e fuori le funzioni, eliminando efficacemente alcune classi di violazioni di accesso alla memoria mediante verifiche del tempo di compilazione.

Con l'avvento della logica lineare di J-Y Girard, abbiamo assistito a una drammatica espansione del paradigma proposizioni-come-tipi. Con la logica lineare vediamo l'espansione della copertura ben oltre il modello funzionale, che è strettamente sequenziale. Invece, la copertura offerta dal controllo dei tipi per la dimostrazione delle proprietà, si estende ai controlli di conformità del protocollo in esecuzione concorrente. Quindi Caires e Cardelli scoprirono le logiche spaziali che ampliarono ulteriormente la copertura per includere le proprietà strutturali della forma interna dei programmi. Basandosi su queste scoperte, Stay e Meredith hanno identificato un algoritmo, l'algoritmo LADL, per la generazione di sistemi di tipi, tali che i programmi ben tipizzati godessero di un'ampia varietà di proprietà strutturali e comportamentali che vanno dalla certezza e vivacità alle proprietà di sicurezza. Mediante l'applicazione dell'algoritmo LADL sviluppato da Stay e Meredith, questo modello non tipizzato delle primitive del contratto qui identificate può essere dotato di un sistema di tipo completo e sufficientemente ricco da fornire salvaguardie in termini di tempo di compilazione che assicurino le principali caratteristiche di sicurezza e vivacità attese dalle applicazioni mission-critical per la gestione di attività finanziarie e altri contenuti sensibili. Un singolo esempio di tale protezione del tempo di compilazione è sufficiente per aver catturato e impedito il bug che ha portato alla perdita di 50 milioni di dollari dal DAO, in fase di compilazione.

SpecialK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Il trattamento monadico della semantica dei canali è l'intuizione esplorata nello stack SpecialK. In primo luogo, esso mappa l'accesso al canale per la programmazione reattiva strutturata monodicamente per la comprensione. In secondo luogo, esegue il mapping dei canali simultaneamente alla memoria locale associata all'intero nodo, nonché alle code in un'infrastruttura di comunicazione basata sui provider AMQP tra i nodi. Ciò fornisce la base di una rete di distribuzione dei contenuti che può essere realizzata su una rete di nodi comunicanti, che è integrata con un modello di programmazione basato su π-calculus. In particolare, come si può vedere nei commenti del codice precedente, il trattamento monadico di canale + pattern unifica i paradigmi di programmazione di passaggio dei messaggi e di consegna del contenuto. Nello specifico, il canale può essere visto come un argomento, mentre il pattern fornisce una struttura subtopica annidata al flusso di messaggi. Questo integra tutti i meccanismi standard di indirizzamento del contenuto, come URL + http, oltre a fornire un modello di query. Vedi la sezione sottostante per i dettagli.


Da SpecialK a RChain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Come vedremo, il modello RChain per i contratti eredita tutto il trattamento di consegna dei contenuti da parte di SpecialK. Tuttavia, mentre SpecialK ha realizzato il modello di contratto pre-RChain come un linguaggio specifico del dominio incorporato, ospitato come un set di librerie in Scala, il modello RChain realizza il modello come un linguaggio di programmazione completo da eseguire su una VM replicata sulla blockchain, come nello spirito dell'architettura e del design di Ethereum. Questa scelta affronta numerose lacune nell'architettura Synereo V1 come delineato nel primo white paper Synereo. In particolare, evita il problema di dover pagare altre commissioni di blockchain per gestire le capacità finanziarie dell’attenzione all'economia, e quindi subire una serie di attacchi basati sull'economia ai contratti del sistema di attenzione all'economia. Affronta anche il debito tecnico nello stack SpecialK relativo alla libreria di continuazioni delimitate di Scala, centrale rispetto alla semantica SpecialK, aumentando drasticamente la capacità dei contratti intelligenti supportati.

Rho-calculus
-------------------------------------------------------------------------------

Mentre l'astrazione monadica fornisce una struttura sul flusso di contenuti che fluisce sui canali, un'osservazione più fondamentale fornisce la struttura necessaria per supportare la programmazione meta-livello su scala industriale. È importante riconoscere che praticamente tutti i principali linguaggi di programmazione supportano la programmazione meta-livello. Il motivo è semplicemente il fatto che i programmatori non scrivono programmi. I programmi scrivono programmi. I programmatori scrivono i programmi che scrivono programmi. Questo è il modo in cui l'enorme compito di programmare sulla scala di Internet è effettivamente realizzato, utilizzando i computer per automatizzare il più possibile il compito. Dagli editor di testo ai compilatori, ai generatori di codice in AI, tutto questo fa parte dell'ecosistema di base che circonda la produzione di codici per servizi che operano sulla scala di Internet.

Assumendo una prospettiva più ristretta, è utile assistere alle dolorose esperienze di Scala per aggiungere supporto alla programmazione di meta-livello dopo il fatto della progettazione del linguaggio. La riflessione su Scala non era nemmeno sicura per anni. Probabilmente, questa esperienza, oltre ai problemi con il sistema di tipi, sono stati i motivi dello sforzo dei compilatori di tornare a progettare da zero il nuovo design del linguaggio. Questi e altri sforzi ben esplorati chiariscono che fornire primitivi per la programmazione meta-livello fin dall'inizio della progettazione di base del modello di programmazione è essenziale per la longevità e praticità d’uso. In breve, un design che supporti in pratica la programmazione meta-livello è semplicemente più conveniente in un progetto che vuole arrivare a funzionalità pronte per la produzione alla pari di Java, C# o Scala.

Prendendo spunto dall'impegno totale di Rosette per la programmazione meta-livello, il “**r**-flective **h**-igher **o**-rder π-calculus”, o rho-calculus, in breve, introduce la riflessione come parte del modello di base. Fornisce due primitivi di base, riflettere e reificare, che consentono un calcolo continuo per trasformare un processo in un canale e un canale che è un processo reificato, di nuovo nel processo che reifica. Il modello è stato revisionato più volte negli ultimi dieci anni. Sono stati disponibili prototipi che forniscono una chiara dimostrazione della sua solidità per quasi un decennio. Questo porta l'insieme dei primitivi di costruzione del contratto a un totale di nove primitivi, molti meno di quelli trovati in Solidity, il  linguaggio contrattuale intelligente di Ethereum, tuttavia il modello è molto più espressivo di Solidity. In particolare, i contratti intelligenti basati su Solidity non godono della concorrenza interna.

Implicazioni per l'indirizzamento delle risorse, la consegna di contenuti, query e sharding
===============================================================================

Prima di immergerti nel modo in cui il modello si riferisce all'indirizzamento delle risorse, alla consegna dei contenuti, alla query e allo sharding, facciamo alcune osservazioni rapide sull'indirizzamento basato sul percorso. Si noti che i percorsi non sempre si compongono. Ad esempio, prendi `/a/b/c` e `/a/b/d`. Questi non si compongono naturalmente per dare un percorso. Tuttavia, ogni percorso è automaticamente un albero, e come alberi questi si compongono per produrre un nuovo albero `/a/b/c+d`. In altre parole, gli alberi offrono un modello componibile per l'indirizzamento delle risorse. Questo funziona anche come un modello di query. Per vedere quest'ultima metà di questa affermazione, riscriviamo i nostri alberi in questa forma:

.. math::
  /a/b/c \mapsto a(b(c))

.. math::
  /a/b/c+d \mapsto a(b(c, d))

Quindi nota che l'unificazione funziona come un algoritmo naturale per la corrispondenza e la decomposizione di alberi e la corrispondenza e le decomposizioni basate sull'unificazione forniscono la base della query.

Alla luce di questa discussione, diamo un'occhiata alle azioni I/O del π-calculus:

.. code-block:: none

   input: x?(a(b(X,Y)))P ↦ for(a(b(X,Y)) <- x)P
   output: x!(a(b(c,d)))

Quando questi vengono messi in esecuzione simultanea abbiamo:

.. code-block:: none

   for(a(b(X,Y)) <- x)P | x!(a(b(c,d)))

che valuta :codice:`P { X: = c, Y: = d }`, cioè iniziamo a eseguire
:code:`P` in un ambiente in cui :codice:`X` è associato a :codice:`c`, e
:code:`Y` è associato a :codice:`d`. Scriviamo simbolicamente la fase di valutazione:

.. code-block:: none

   for(a(b(X,Y)) <- x)P | x!(a(b(c,d))) → P{ X := c, Y := d }

Ciò dà origine a un'interpretazione molto naturale:

* L'output colloca risorse in sedi:

.. code-block:: none

   x!(a(b(c,d)))

* Inserisci query per risorse in sedi:

.. code-block:: none

   for(a(b(X,Y)) <- x)P

This is only the beginning of the story. With reflection we admit structure on channel names, like x in the example above, themselves. This allows to subdivide the space where resources are stored via namespaces. Namespaces become the basis for a wide range of features from security to sharding.

Il modello RChain di contratti intelligenti
-------------------------------------------------------------------------------

Ora abbiamo una completa caratterizzazione del modello RChain di contratti intelligenti. È codificato nel design di rholang. Il numero di funzioni di cui gode come risultato della sola riflessione, dalle macro agli adattatori di protocollo, è sufficiente per meritare considerazione. Facendo un passo indietro, tuttavia, vediamo che inoltre

* gode di un sistema di tipo sano e corretto
* una specifica formale
* un rendering delle specifiche formali al codice funzionante
* Stabilisce una specifica formale di una VM corretta per costruzione
* questo impone una chiara strategia di compilazione come una serie di trasformazioni corrette per costruzione nel codice byte per una VM che è stata testata sul campo per 20 anni

Ora confronta questo punto di partenza con il punto attuale di Ethereum con Solidity e EVM. Se l'obiettivo è quello di produrre una linea temporale credibile sulla quale raggiungiamo una rete di nodi blockchain che eseguono un codice corretto per costruzione, verificato formalmente, allora anche con l'effetto di rete di Ethereum questo approccio avrà vantaggi distinti. Chiaramente, c'è abbastanza interesse del mercato per supportare lo sviluppo di entrambe le opzioni.

.. bibliography:: references.bib
   :cited:
