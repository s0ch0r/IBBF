# IBBF - Intelligent Blackbox Fuzzer

**The IBBF is an implementation of the L*-Algorithm.**

#### Run with following parameters:
```
-d                  Debug Mode
-t                  Test Mode
-A [alphabet]       Set of characters which will represent the Alphabet used by the algorithm                    (e.g. "abc@ef")
-CQ [module_name]   use a different module for conjecture queries. The file has to be located                    in the corresponding subfolder. 
-MQ [module_name]   use a different module for membership queries. The file has to be located                    in the corresponding subfolder. 
-TM [module_name]   use a different module for handling the table. The file has to be located                    in the corresponding subfolder. 
```
### Current Modules:
##### Conjecture Query:
 - *basicCQ*: Handles Conjecture Queries by trying all possible combinations to a given maximum of characters until it finds a counterexample.
   Parameters:
```
'-l [number]'      Specifies to which lenght test strings should be generated and tested.
```

##### Membership Query:
- *regexMQ*: Handles Membership Queries by testing them against a given regular Expression
  Parameters:
```
-r [regex]         Specifies the regular Expression which should be used
``` 
##### Table:
- *basicTable*: Basic implementation of the table

### Adding new Modules:
New modules have to implement a specific class with predefined interfaces/functions which can be used by other modules.
##### ConjectureQuery:
*Classname: CQModule*
**Functions:**
- *isCorrect(DFSM)*: Returns a counterexample if one was found, otherwise returns a void string ""

##### MembershipQuery:
*Classname: MQModule*
**Functions:**
- *isMember(string)*: Tests the given string if it is a member of the language to be learned by the algorithm. Returns "1" if yes and "0" if no (Note: Return values have to be strings).

##### Table:
*Classname: TableModule*
**Functions:**
- *fixTable()*: Fixes own table and returns 1 if done and 0 if failed. After this the table must be closed and consistent.
- *getDFSM()*: Generates the DFSM which is representet by the table and returns it. This DFSM has to be a list [initialState, finalStates, transition_table, Alphabet] wheras finalStates and Alphabet is a list and transition_table a dictionary with lists as values.
- *addCounterexample(string)*: Adds a given string to the table as a counterexample from a conjecture Query




