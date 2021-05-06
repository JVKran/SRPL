## Course requirements
The Hogeschool Utrecht also demands some other things that are required for passing the course 'Advanced Technical Programming'.

### Turing Completeness
First of all, the language should be Turing Complete. It is stated that any language is *certainly* turing complete if it has conditional branching (which is the case with the implemented if-else-statement), it has the ability to change an arbitrary amount of memory (with, for example, the implemented variables) and it can run forever (with, again for example, the supported while-loop or plain recursion). Furthermore, it should be able to use infinite memory. Of course this is limited by the hardware, but SRPL doesn't restrict the amount of memory usage. Hence, we can conclude SRPL is Turing Complete. The recursively typed *certaintly* has a reason though; a language doesn't have to specifically support these things (Brainf*ck for example is also Turing Complete), but they do prove a language is Turing Complete. (Minsky, 1961)

### Functional programming
Second of all, the entire codebase should be written in a _Functional_ way. That's almost entirely the case. I've used some exceptions for handing key- and recursion errors and print statements for notifying the user about errors in a way that enables the lexer, parser and interpreter to continue as good as possible. Other than that, I don't think there's other non-functional programming present.

### Classes
Apart from programming functionally, one also has to use classes with inheritance. That one luckily isn't so hard. Implementing a lexer, parser and intepreter without them would be quite messy I think. I've used four classes in total. The [Context](interpret/context.py) with the Symbol Table, the [Function](interpret/function.py) for execution of functions, the [Number](interpret/number.py) for enabling the user to use arithmetics, the [Tokens](lex/token.py) for easily building a tokenlist and, last but not least, the [Nodes](parse/nodes.py) for relatively easy building and interpretation of the Abstract Syntax Tree. All of these classes have a reprint method.

Only one of these features inheritance; the [Tokens](lex/token.py). This has one very good reason; by implementing some neat mechanism to automatically create the right kind of subclass based on the given word, one prevents a lot of if-statements.

### Decorators
I've found one *I think* good use for decorators. The parser had three occurences of it needing to iterate over the tokenlist until some specific kind of token was reached. Hence, I defined a decorator for it (in [parser.py](parse/parser.py) at line 11) and use it in the same file at lines 121, 151 and 191. The logic for iterating over the tokenlist until a specific token is reached is now implemented only once. That's an improvement in my book.

### Type annotations
Furthermore, we had to use type annotations. In the beginning I thought of them as being a chore to maintain, but in the end I have to say that they have some good uses. They make you think a lot more about the input and output of a function and that being logical or not. The requirement of providing Haskell Style type annotations however, really didn't add any extra value; that really was a chore. Nevertheless, both the Python and Haskell Style annotations have been implemented.

### Higher order functions
In contrary of the type annotations, I was a fan of them right after the minute I heard of them during the lecture. I'm also a great fan of the C++ Standard Library, so that didn't really come as a surprise. I've used them quite extensively.

The higher order function ```reduce``` is used in [interpreter.py](interpret/interpreter.py) at line 95 for determining wether there's a returning node in the list of nodes. No matter how convenient reduce() is, I've found more uses for ```map``` and ```zip```. I've used zip, for example in [function.py](interpret/function.py) at lines 22 - 23 for zipping the argument names with their values so I can easily append them to the symbol table of the current context. Zip has also been used in the [lexer](lex/lexer.py) at line 45 for zipping the list with words and the list with line numbers.

Map however, gained the crown with 4 uses. In [interpreter.py](interpret/interpreter.py) at line 79 and 105 for example, it has been used to append the value of an argument to the arguments or elements (for line 105) list. Very useful when the argument isn't a number, but a variable or an expression... In the same file at line 94 it's used for creating a list with booleans representing wether the node at that index is a ReturnNode. This is later used by reduce, as already stated.

Last but not least, ```filter``` has also been used. More specifically in [interpreter.py](interpret/interpreter.py) at line 106 for removing all None elements from the list and in [lexer.py](lex/lexer.py) at line for removing empty strings.

### Loops
My language supports loops, but also lambdas. Go-to statements have not and will not be implemented. For an example, checkout the main [README](README.md).

#### Sources
Minsky, M. L. (1961). Recursive Unsolvability of Post’s Problem of “Tag” and other Topics in Theory of Turing Machines. Wolframscience. Published. https://www.wolframscience.com/prizes/tm23/images/Minsky.pdf
