.. _actors-tuples-and-pi:

*******************************************************************************
Actors, Tuples and π
*******************************************************************************

Rosette
===============================================================================

At MCC the Carnot research group predicted the commercialization of the Internet a full decade before Netscape rose to fame. The Carnot group, however was focused on decentralized and distributed applications, and developed a network application node, called the Extensible Services Switch, or ESS, and the programming language Rosette for programming these nodes. In Rosette/ESS the model under investigation was the actor model. Here we are speaking quite specifically of an elaboration of the model developed by Carl Hewitt and refined by Gul Agha, who subsequently consulted on the design of Rosette.

The Rosette elaboration was striking in scope and elegance. Specifically, Rosette decomposes an actor into

* a mailbox (a queue where messages from the actor’s clients arrive)
* a state (a tuple of values)
* a meta (a description of how to access values in the state in terms of more abstract keys)
* and a shared behavior object (a map from message types to code to run in response, roughly equivalent to a vtable in languages like C++)

An actor’s processing consists of reading the next message in the mailbox, using the shared behavior object (or sbo) to determine which code to run in response to the message and then execute that code in an environment in which references to keys described in the meta are bound to locations in the state tuple. That code will principally send messages to other actors and possibly await for responses.

An actor provides a consistent view of state under concurrent execution via an update; that is, an actor does not process the next message in the mailbox until it has called update, and while the actor is processing the current message, the mailbox is considered locked and is queuing client requests. When an actor calls an update a new logical thread of activity is created to process the next message in the mailbox queue. That thread’s view of the state of the actor is whatever is supplied to the update. The previous thread may still make changes to the state, but they are not observable to all subsequent threads processing subsequent messages in the mailbox, and hence to all subsequent client requests. This approach provides a scalable notion of concurrency that collapses to message arrival order non-determinism in single threaded containers, and expands when there is system level support to map the logical threads in some outer container (such as a VM, an operating system, or the hardware, itself).

Already, this is a much more deliberately articulated model of actors than exists in most industrial systems today (cf Scala’s AKKA framework). What makes the Rosette model so much more elegant, however, is its total commitment to meta-level programming. In the Rosette model, everything is an actor. In particular, the mailbox of an actor is an actor, and that has, in turn, a mailbox, state, meta, and sbo. It is noteworthy that Rosette makes this fully reflective model with the possibility of infinite regress perform on par or better than languages like Java or C#.

In some sense, the structural reflection of actors in the Rosette model is echoed in languages like Java where classes are in turn objects that can be programmatically probed and enlisted in computation. However, Rosette takes the reflective principle a step further. The model offers not just structural reflection, but procedural reflection, by providing a notion of continuation reconciled with the concurrency inherent in the model. Specifically, just as a shift-block in a shift-reset style presentation of delimited continuations makes the awaiting continuation available to the code in the block, Rosette’s reflective method makes the awaiting continuation available as a parameter to the method in the body of the method. More on this later.

To close out this brief summary note that Rosette was not merely structurally and procedurally reflective, but also lexically reflective. That is, all syntactic structure of programs in Rosette are also actors! The reflective infrastructure for this provides the basis for a hygienic macro system, support for embedded domain specific languages, and a host of other syntactic and symbolic processing features that many industrial languages still struggle to provide some 20 years after Rosette’s inception.

Tuplespaces
===============================================================================

Around the same time as the Rosette model was being investigated for developing
applications in this decentralized and distributed setting, Gelernter proposed
Tuplespaces. Here the idea is to create a logical repository above the physical
and communications layers of the Internet. The repository is essentially
organized as a distributed key-value database in which the key-value pairs are
used as communication and coordination mechanisms between computations. Gelernter
describes three basic operations for interaction with the tuplespace, :code:`out`
to create a new data object in tuplespace, :code:`in` to consume (remove) an
object from tuple space and :code:`rd` to read an object without removing it

In contrast to message passing systems this approach allows senders and receivers to
operate without any knowledge of each other. When a process generates a new result
that other processes will need, it simply dumps the new data into tuplespace.
Processes that need data can look for it in tuple space using pattern matching.


.. code-block:: lisp

   out("job", 999, "abc")

   in("job", 1000, ?x) ; blocks because there is no matching tuple
   in("job", 999, x:string) ; takes that tuple out of tuple space, assigning 'abc' to x


This raises questions about how  publication of data is persisted and what happens
to computations suspended waiting on key-value pairs that are not present in the
tuplespace. Moreover, the tuplespace mechanism makes no commitment to any programming
model. Agents using the tuplespace may be written in a wide variety of programming
models with a wide variety of implementations and interpretations of the agreed
concurrency semantics. This makes reasoning about the end-to-end semantics of an
application made of many agents interacting through the tuplespace much, much harder.
However, the simplicity of the communication and coordination model has enjoyed wide
appeal and there were many implementations of the tuplespace idea over the ensuing decades.

A notable difference between the tuplespace notion of coordination and the actor model lies in the principal port limitation of actors. An actor has one place, its mailbox, where it is listening to the rest of the world. Real systems and real system development require that applications often listen to two or more data sources and coordinate across them. Fork-join decision procedures, for example, where requests for information are spawned to multiple data sources and then the subsequent computation represents a join of the resulting information streams from the autonomous data sources, are quite standard in human decision making processes, from loan processing, to the review of academic papers. Of course it is possible to arrange to have an actor that coordinates amongst multiple actors who are then charged with handling the independent data sources. This introduces application overhead and breaks encapsulation as the actors need to be aware they are coordinating.

In contrast, the tuplespace model is well suited to computations that coordinate across multiple autonomous data sources.

Distributed implementations of mobile process calculi
===============================================================================

Tomlinson, Lavender, and Meredith, among others, provided a realization of the tuplespace model inside Rosette/ESS as a means to investigate the two models side-by-side and compare applications written in both styles. It was during this work that Meredith began an intensive investigation of the mobile process calculi as yet a third alternative to the actor model and the tuplespace model. One of the primary desiderata was to bridge between having a uniform programming model, such as the actor model of Rosette, making reasoning about application semantics much easier, with the simple, yet flexible notion of communication and coordination afforded in the tuplespace model.

In the code depicted below the method names consume and produce are used instead of the traditional Linda verbs :code:`in` and :code:`out`. The reason is that once reflective method strategy was discovered, and then refined using delimited continuations, this lead to new vital observations relating to the life cycle of the data and continuation.

.. code-block:: none
   :caption: A Rosette implementation of the tuplespace get semantics

   (defRMethod NameSpace (consume ctxt & location)
    ;;; by makng this a reflective method - RMethod - we gain access to the awaiting continuation
    ;;; bound to the formal parameter ctxt
    (letrec [[[channel ptrn] location]
                   ;;; the channel and the pattern of incoming messages to look for are destructured and bound
           [subspace (tbl-get chart channel)]
                   ;;; the incoming messages associated with the channel are collected in a subtable
                   ;;; in this sense we can see that the semantic framework supports a compositional
                   ;;; topic/subtopic/subsubtopic/… structuring technique that unifies message passing
                   ;;; with content delivery primitives
                   ;;; the channel name becomes the topic, and the pattern structure becomes
                   ;;; the subtopic tree
                   ;;; this also unifies with the URL view of resource access
          [candidates (names subspace)]
          [[extractions remainder]
             (fold candidates
               (proc [e acc k]
                   (let [[[hits misses] acc]
                   [binding (match? ptrn e)]]
               (if (miss? binding)
                   (k [hits [e & misses]])
                   (k [[[e binding] & hits] misses])))))]
                     ;;; note that this is generic in the match? and miss? predicates
                     ;;; matching could be unification (as it is in SpecialK) or it could be
                     ;;; a number of other special purpose protocols
                     ;;; the price for this genericity is performance
                     ;;; there is decent research showing that there are hashing disciplines
                     ;;; that could provide a better than reasonable approximation of unification
          [[productions consummation]
               (fold extractions
                 (proc [[e binding] acc k]
                   (let [[[productions consumers] acc]
                  [hit (tbl-get subspace e)]]
                     (if (production? hit)
                  (k [[[[e binding] hit] & productions] consumers])
                  (k [productions [[e hit] & consumers]])))))]]
                     ;;; this divides the hits into those matches that are data and
                     ;;; those matches that are continuations
                     ;;; and the rest of the code sends data to the awaiting continuation
                     ;;; and appends the continuation to those matches that are currently
                     ;;; data starved
                     ;;; this is a much more fine-grained view of excluded middle

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
   :caption: A Rosette implementation of the tuplespace put semantics

   ;;; This code is perfectly dual to the consumer code and so all the comments
   ;;; there apply in the corresponging code sites
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

Essentially, the question is what happens to either or both of data and continuation after an input request meets an output request. In traditional tuplespace and π-calculus semantics both data and continuation are removed from the store. However, it is perfectly possible to leave either or both of them in the store after the event. Each independent choice leads to a different major programming paradigm.

.. topic:: Traditional DB operations

   Removing the continuation but leaving the data constitutes a standard database read:

   +----------+------------------+-------------------+------------------+----------------------+
   |          | ephemeral - data | persistent - data | ephemeral - data | persistent - data    |
   |          |                  |                   |                  |                      |
   |          | ephemeral - k    | ephemeral - k     | persistent - k   | ephemeral - k        |
   +----------+------------------+-------------------+------------------+----------------------+
   | producer | put              | **store**         | publish          | publish with history |
   +----------+------------------+-------------------+------------------+----------------------+
   | consumer | get              | **read**          | subscribe        | subscribe            |
   +----------+------------------+-------------------+------------------+----------------------+


.. topic:: Traditional messaging operations

   Removing the data, but leaving the continuation constitutes a subscription in a pub/sub model:

   +----------+------------------+-------------------+------------------+--------------------------+
   |          | ephemeral - data | persistent - data | ephemeral - data | persistent - data        |
   |          |                  |                   |                  |                          |
   |          | ephemeral - k    | ephemeral - k     | persistent - k   | ephemeral - k            |
   +----------+------------------+-------------------+------------------+--------------------------+
   | producer | put              | store             | **publish**      | **publish with history** |
   +----------+------------------+-------------------+------------------+--------------------------+
   | consumer | get              | read              | **subscribe**    | **subscribe**            |
   +----------+------------------+-------------------+------------------+--------------------------+

.. topic:: Item-level locking in a distributed setting

   Removing both data and continuation is the standard mobile process calculi and tuplespace semantics:

   +----------+------------------+-------------------+------------------+----------------------+
   |          | ephemeral - data | persistent - data | ephemeral - data | persistent - data    |
   |          |                  |                   |                  |                      |
   |          | ephemeral - k    | ephemeral - k     | persistent - k   | ephemeral - k        |
   +----------+------------------+-------------------+------------------+----------------------+
   | producer | **put**          | store             | publish          | publish with history |
   +----------+------------------+-------------------+------------------+----------------------+
   | consumer | **get**          | read              | subscribe        | subscribe            |
   +----------+------------------+-------------------+------------------+----------------------+

Building on Tomlinson’s insights about the use of Rosette’s reflective methods to model the tuplespace semantics (see code above), Meredith provided a direct encoding of the π-calculus into tuplespace semantics via linear continuations. This semantics was at the heart of Microsoft’s BizTalk Process Orchestration Engine, and Microsoft’s XLang, arguably the first Internet scale smart contracting language, was the resulting programming model. This model was a direct influence on W3C standards, such as BEPL and WS-Choreography, and spawned a whole generation of business process automation applications and frameworks.

As with the refinements Rosette brings to the actor model, the π-calculus brings a specific ontology for applications built on the notion of processes that communicate via message passing over channels. It is important to note that the notion of process is parametric in a notion of channel, and Meredith used this level of abstraction to provide a wide variety of channel types in XLang, including bindings to Microsoft’s MSMQ message queues, COM objects, and many other access points in popular technologies of the time. Perhaps most central to today’s Internet abstractions is that URIs provide a natural notion of channel that allows for a realization of the programming model over URI aware communications protocols, such as http. Likewise, in terms of today’s storage climate, keys in a key-value store, such as a nosql database also map directly to the notion of channel in the π-calculus, and Meredith used this very idea to provide the encoding of the π-calculus into tuplespace semantics.

From Tuplespaces to π-calculus
-------------------------------------------------------------------------------

The π-calculus captures a core model of concurrent computation built from message-passing based interaction. It plays the same role in concurrent and distributed computation as the lambda calculus plays for functional languages and functional programming, setting out the basic ontology of computation and rendering it to a syntax and semantics in which calculations can be carried out. Given some notion of channel, it builds a handful of basic forms of process, the first three of which are about I/O, describing the actions of message passing.

* :code:`0` is the form of the inert or stopped process that is the ground of the model
* :code:`x?( ptrn )P` is the form of an input-guarded process waiting for a message on
  channel :code:`x` that matches a pattern, ptrn, and on receiving such a message will
  continue by executing :code:`P` in an environment where any variables in the pattern
  are bound to the values in the message
* :code:`x!( m )` is the form of sending a message, :code:`m`, on a channel :code:`x`

The second three are about the concurrent nature of processes, the creation of channels, and recursion.

* :code:`P|Q` is the form of a process that is the parallel composition of two processes P and Q where both processes are executing concurrently
* :code:`(new x)P` is the form of a process that executes a subprocess, P, in a context in which x is bound to a fresh channel, distinct from all other channels in use
* :code:`(def X( ptrn ) = P)[ m ]` and :code:`X( m )`, these are the process forms for recursive definition and invocation

These basic forms can be interpreted in terms of the operations on Tuplespaces::

 P,Q ::=                     [[-]](-) : π -> Scala =
     0                       { }
     | x?(prtn)P             { val ptrn = T.get([[x]](T)); [[T]](P) }
     | x!(m)                 T.put([[x]], m)
     | P|Q                   spawn{ [[P]](T)  }; spawn{ [[P]](T) }
     | (new x)P              { val x = T.fresh("x"); [[P]](T) }
     | (def X(ptrn) = P)(m)  object X { def apply(ptrn) = { [[P]](T) } }; X(m)
     | X(ptrn)               X(ptrn)

Monadically structured channel abstraction
-------------------------------------------------------------------------------

Meredith then pursued two distinct lines of improvement to these features. Both of them are related to channel abstraction. The first of these relates the channel abstraction to the stream abstraction that has become so popular in the reactive programming paradigm. Specifically, it is easy to prove that a channel in the asynchronous π-calculus corresponds to an unbounded and persistent queue. This queue can be viewed as a stream, and access to the stream treated monadically, as is done in the reactive programming paradigm. This has the added advantage of providing a natural syntax and semantics for the fork-join pattern so prevalent in concurrent applications supporting human decision making applications mentioned previously.

.. code-block:: none

  ( let [[data (consume ns channel pattern)]] P)

.. code-block:: scala

  for( data <- ns.consume(channel, pattern) ){ P }

This point is worth discussing in more detail. While the π-calculus does resolve the principle port limitation of the actor model, it does not provide natural syntactic or semantics support for the fork-join pattern. Some variants of the π-calculus, such as the join calculus, have been proposed to resolve this tension, but arguably those proposals suffer an entanglement of features that make them unsuited to many distributed and decentralized programming design patterns. Meanwhile, the monadic interpretation of the channel provides a much more focused and elementary refactoring of the π-calculus semantics, consistent with all existing denotational semantics of the model, that provides a natural notion of fork-join while also mapping cleanly onto the reactive programming paradigm, and thus making integration of development stacks, such as Apache Spark, relatively simple.

If we look at this from the perspective of programming language evolution, we first see a refactoring of the semantics to look like:

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

where the for-comprehension is syntactic sugar for a use of the continuation
monad. The success of this interpretation suggests a refactoring of the
**source** of the interpretation.

.. code-block:: none
   :emphasize-lines: 2

   P,Q :: = 0
            | for (ptrn <- x)P
            | x!(m)
            | P|Q
            | (new x)P
            | (def X(ptrn) = P)[m]
            | X(ptrn)

This refactoring shows up in Meredith and Stay’s work on higher categorical semantics for the π-calculus :cite:`DBLP:journals/corr/StayM15`, and is then later incorporated in the rholang design. The important point to note is that the for-comprehension-based input can now be smoothly extended to input from multiple sources, each/all of which must pass a filter, before the continuation is invoked.

.. math::

  for( ptrn_{1} \leftarrow x_{1}; \dotso; ptrn_{n} \leftarrow x_{n} if cond )P

Using a for-comprehension allows the input guard semantics to be parametric in the monad used for channels, and hence the particular join semantics can be supplied polymorphically. The significance of this cannot be overemphasized. Specifically:

* It contrasts with the join-calculus where the join is inseparably
  bound together with recursion. The monadic input guard allows for anonymous,
  one time joins, which are quite standard in fork-join patterns in human
  decision processes.
* It provides the proper setting in which to interpret Kiselyov’s
  LogicT monad transformer. Searching down each input source until a tuple of
  inputs that satisfies the conditions is found is sensitive to divergence in
  each input source. Fair interleaving, and more importantly, a means to
  programmatically describe interleaving policy is critical for reliable,
  available, and performant services. This is the actual import of LogicT
  and the right setting in which to deploy that machinery.
* We now have a syntactic form for nested transactions. Specifically,
  :code:`P` can only run in a context in which all of the state changes associated
  with the input sources and the condition are met. Further, :code:`P` can be
  yet another input-guarded process. Thus a programmer, or a program analyzer,
  can detect transaction boundaries *syntactically*. This is vital for contracts
  involving financial and other mission-critical transactions.

A pre-RChain model for smart contracts
-------------------------------------------------------------------------------

This is a precursor to the RChain model for smart contracts, as codified in the rholang design. It provides the richest set of communication primitives for building contracts proposed to date that has been driven both by theory and by industrial scale implementation and deployment. Yet, the entire set of contract primitives fits on a single line. There is not a single design proposal in this space, from the PoW-based blockchain to the EVM, that meets the quality assurance pressures this proposal has withstood. Specifically, the proposal folds in all the experiences using Rosette, Tuplespaces, and BizTalk and boils them down to a single design that meets the desiderata discovered in all of these efforts. It does so with only seven primitives, and primitives that line up with the dominant programming paradigms of the current market. Yet, as the examples from the rholang spec, and the paper on preventing the DAO bug with behavioral types show, the entire range of contracts expressible in existing blockchain technology is compactly expressed in this model.

As seen in the rholang design, however, this is only the beginning of the story. A little background is necessary to understand the import or this development. For the last 20 years a quiet revolution has been going on in computer science and logic. For many years it was known that for small, but growing fragment of the functional programming model types corresponded to propositions, and proofs corresponded to programs. If the correspondence, known variously as the proposition-as-types paradigm or the Curry-Howard isomorphism, could be made to cover a significant, practical portion of the model, it has profound implications for software development. At a minimum it means that the standard practice of type-checking programs coincides with proofs that programs enjoy certain properties as a part of their execution. The properties associated with the initial fragment covered by the Curry-Howard isomorphism largely had to do with respecting the shape of data flowing into and out of functions, effectively eliminating certain class of memory access violations by compile time checks.

With the advent of J-Y Girard’s linear logic, we have seen a dramatic expansion of the proposition-as-types paradigm. With linear logic we see the expansion of the coverage far beyond the functional model, which is strictly sequential. Instead, the coverage offered by type checking for proving properties extends to protocol conformance checks in concurrent execution. Then Caires and Cardelli discovered the spatial logics which further expanded the coverage to include structural properties of the programs internal shape. Building on these discoveries, Stay and Meredith identified an algorithm, the LADL algorithm, for generating type systems such that well typed programs would enjoy a wide variety of structural and behavioral properties ranging from safety and liveness to security properties. By the application of the LADL algorithm developed by Stay and Meredith, this untyped model of the contract primitives identified here can be given a sound and complete type system rich enough to provide compile time safeguards that ensure key safety and liveness properties expected of mission-critical applications for handling financial assets and other sensitive content. A single example of such a compile time safeguard is sufficient to have caught and prevented the bug that led to the loss of 50M USD from the DAO, at compile time.

SpecialK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The monadic treatment of channel semantics is the insight explored in the SpecialK stack. Firstly, it maps channel access to for-comprehension style monadically structured reactive programming. Secondly, it maps channels simultaneously to local storage associated with the entire node, as well as to queues in an AMQP provider based communication infrastructure between nodes. This provides the basis of a content delivery network that can be realized over a network of communicating nodes, that is integrated with a π-calculus based programming model. In particular, as can be seen in the comments in the code above, the monadic treatment of channel + pattern unifies message-passing and content delivery programming paradigms. Specifically, the channel can be seen as providing topic, while the pattern provides nested subtopic structure to the message stream. This integrates all of the standard content addressing mechanisms, such as URLs + http, as well as providing a query model. See the section below for details.


From SpecialK to RChain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As we will see, the RChain model for contracts inherits all of SpecialK’s treatment of content delivery. Yet, where SpecialK realized the pre-RChain contract model as an embedded domain specific language hosted as a set of libraries in Scala, the RChain model realizes the model as a full blown programming language to be run on a VM replicated on the blockchain, very much in the spirit of Ethereum’s architecture and design. This choice addresses several shortcomings in the Synereo V1 architecture as outlined in the first Synereo white paper. In particular, it avoids the problem of having to pay other blockchains fees to run the financial capabilities of the attention economy, and thus suffering a number of economics-based attacks on the attention economy system contracts. It also addresses technical debt in the SpecialK stack related to the Scala delimited continuations library central to the SpecialK semantics, while dramatically increasing the capability of the smart contracts supported.

Rho-calculus
-------------------------------------------------------------------------------

While the monadic abstraction provides structure on the stream of content flowing over channels a more fundamental observation provides the necessary structure to support industrial scale meta-level programming. It is important to recognize that virtually all of the major programming languages support meta-level programming. The reason is simply fact that programmers don’t write programs. Programs write programs. Programmers write the programs that write programs. This is how the enormous task of programming at Internet scale is actually accomplished, using computers to automate as much of the task as possible. From text editors to compilers to code generators to AI, this is all a part of the basic ecosystem that surrounds the production of code for services that operate at Internet scale.

Taking a more narrow perspective, it is useful to witness the painful experiences of Scala to add support for meta-level programming after the fact of the language design. Reflection in Scala was not even thread safe for years. Arguably, this experience, plus the problems with the type system were the reasons for the back-to-the-drawing board effort underlying the dotty compiler and new language design. These and other well explored efforts make it clear that providing primitives for meta-level programming from the outset of the core design of the programming model is essential for longevity and practical use. In short, a design that practically supports meta-level programming is simply more cost effective in a project that wants to get to production-ready feature set on par with say Java, C#, or Scala.

Taking a cue from Rosette’s total commitment to meta-level programming, the
**r**-eflective **h**-igher **o**-rder π-calculus, or rho-calculus, for short,
introduces reflection as part of the core model. It provides two basic primitives,
reflect and reify, that allow an ongoing computation to turn a process into
a channel, and a channel that is a reified process back into the process it
reifies. The model has been peer reviewed multiple times over the last ten years.
Prototypes providing a clear demonstration of its soundness have been available
for nearly a decade. This takes the set of contract building primitives to a
grand total of nine primitives, far fewer than found in Solidity, Ethereum’s
smart contracting language, yet the model is far more expressive than Solidity.
In particular, Solidity-based smart contracts do not enjoy internal concurrency.

Implications for resource addressing, content delivery, query, and sharding
===============================================================================

Before diving into how the model relates to resource addressing, content delivery,
query and sharding, let’s make a few quick observations about path-based addressing.
Note that paths don’t always compose. For example, take `/a/b/c` and `/a/b/d`.
These don’t compose naturally to yield a path. However, every path is automatically
a tree, and as trees these do compose to yield a new tree `/a/b/c+d`. In other words,
trees afford a composable model for resource addressing. This also works as a query
model. To see this latter half of this claim let’s rewrite our trees in this form:

.. math::
  /a/b/c \mapsto a(b(c))

.. math::
  /a/b/c+d \mapsto a(b(c, d))

Then notice that unification works as a natural algorithm for matching and
decomposing trees, and unification-based matching and decomposition provides the
basis of query.

In light of this discussion, let’s look at the I/O actions of the π-calculus:

.. code-block:: none

   input: x?(a(b(X,Y)))P ↦ for(a(b(X,Y)) <- x)P
   output: x!(a(b(c,d)))

When these are placed in concurrent execution we have:

.. code-block:: none

   for(a(b(X,Y)) <- x)P | x!(a(b(c,d)))

which evaluates to :code:`P{ X := c, Y := d }`, that is we begin to execute
:code:`P` in an environment in which :code:`X` is bound to :code:`c`, and
:code:`Y` is bound to :code:`d`. We write the evaluation step symbolically:

.. code-block:: none

   for(a(b(X,Y)) <- x)P | x!(a(b(c,d))) → P{ X := c, Y := d }

This gives rise to a very natural interpretation:

* Output places resources at locations:

.. code-block:: none

   x!(a(b(c,d)))

* Input queries for resources at locations:

.. code-block:: none

   for(a(b(X,Y)) <- x)P

This is only the beginning of the story. With reflection we admit structure on channel names, like x in the example above, themselves. This allows to subdivide the space where resources are stored via namespaces. Namespaces become the basis for a wide range of features from security to sharding.

The RChain model of smart contracts
-------------------------------------------------------------------------------

Now we have a complete characterization of the RChain model of smart contracts. It is codified in the rholang design. The number of features it enjoys as a result of reflection alone, from macros to protocol adapters, is enough to warrant consideration.Taking a step back, however, we see further that

* it enjoys a sound and correct type system
* a formal specification
* a rendering of the formal specification to working code
* it dictates a formal specification of a correct-by-construction VM
* this dictates a clear compilation strategy as a series of correct-by-construction transforms to the byte code for a VM that has been field test for 20 years

Now compare this starting point to Ethereum’s current point with Solidity and the EVM. If the goal is to produce a believable timeline over which we reach a network of blockchain nodes running formally verified, correct-by-construction code, then even with Ethereum’s network effect this approach has distinct advantages. Clearly, there is enough market interest to support the development of both options.

.. bibliography:: references.bib
   :cited:
