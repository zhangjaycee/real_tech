# Coherence & Consistency


### 1. Consistency

#### 1.1 Consistency (Database and Filesystem)

WAL (logging, journaling), soft update, CoW ...

#### 1.2 Memory Consistency (Distributed)

#### 1.3 Crash Consistency & Application Consistency (backup system) ???

### 2. Cache Coherence 


### 3. Consensus (Distributed)

> 摘自[1] 
>
>This is actually Tannenbaum’s defintion of “strict consistency”; I disagree with the way he organizes things. He says that “strict consistency” is “impossible to implement in a distributed system” and that sequential consistency “is a slightly weaker model than strict consistency.” Both statements are, in my view, misleading.
Strict coherence can be implemented in a distributed system by having a lock manager hand out read and write tokens to client caches and having it ensure that when a cache holds a write token on an object, no other caches hold a read or write token on that object (e.g., via invalidations.)
Sequential consistency is a weaker condition than strict coherence in some sense: strict coherence relies on a global notion of time while sequential consistency allows the final “sequential order” to differ from the “real-time order” of requests. For example Amol Nayate recently built a system that enforces sequential consistency and enforces a separate maximum staleness.
But in another sense, sequential consistency is stronger than strict coherence. In particular, sequential consistency also requires that all operations complete in program order even if they are to different memory locations. Thus sequential consistency constrains operations on different objects while strict coherence only constrains operations on the same object.
Tannenbaum’s definition of “strict consistency” appears to differ by assuming that all operations are instantaneous and non-blocking; I think his assertions may be true under these assumptions, but I find these assumptions strange.


> 摘自[2] 
>
> We can divide the universe into four types of consensus algorithms:
> 
> Known participants, non-byzantine failure: Paxos, Raft
Unknown participants, limited attack modes: Chord (original) and other distributed hash tables
Known participants, byzantine failure: PBFT, UpRight, Byzantine Paxos
Unknown participants, byzantine failure: Proof of Work, Proof of Stake, S-Chord


[1] AFS and distributed file systems, www.cs.utexas.edu/users/dahlin/Classes/GradOS/lectures/afs.ps

[2] Are consensus algorithms only proof-of-work, proof-of-stake, proof-of-elapsed time etc.? Or, can we write our own consensus algorithm by our needs mostly to develop an application for a start-up? https://www.quora.com/Are-consensus-algorithms-only-proof-of-work-proof-of-stake-proof-of-elapsed-time-etc-Or-can-we-write-our-own-consensus-algorithm-by-our-needs-mostly-to-develop-an-application-for-a-start-up