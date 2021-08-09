# Python implementation of Reflow formulas
from reflow_server.formula.utils.lexer import Lexer
from reflow_server.formula.utils.settings import Settings
from reflow_server.formula.utils.parser import Parser
from reflow_server.formula.utils.interpreter import Interpreter
from reflow_server.formula.utils.context import Context

################
# HOW TO DEBUG #
################
# at least, how i was able to create this. A Token, a parser node in the AST and last but not least
# a object are all classes inside of the formulas, this makes it hard for debugging. so how you should debug? 
# simple, just add "print(node.__dict__)" this way the object is displayed as a dict, at it becomes a LOT EASIER to debug
def evaluate(expression, context=None):
    """
    Yeah, you guessed it right, we've built our own programming language and you might ask yourself how.
    And although we see creators of programming languages similar to gods, it's not difficult at all.

    It's actually a pretty common knowledge that you probably use everyday when using stuff like esbuild, sass, scss, webpack, babel, etc.

    First let me introduce to you to some GREAT stuff on the internet that can serve as an inspiration:
    1.: https://ruslanspivak.com/lsbasi-part1/ (read the hole tutorial, this is the first source of information for a reason
    it is quick to read and more approachable than a book)
    2.: https://pt.wikipedia.org/wiki/Formalismo_de_Backus-Naur_Estendido#:~:text=EBNF%20%C3%A9%20um%20c%C3%B3digo%20que,combinados%20em%20uma%20sequ%C3%AAncia%20v%C3%A1lida.
    3.: https://monkeylang.org/ (it's in Go, i also don't know Go, but it's not that difficult to follow along)
    4.: https://github.com/python/cpython/blob/main/Grammar/python.gram (It can be quite intimidating, but it's not difficult to understand actually)
    5.: https://github.com/elixir-lang/elixir/blob/master/lib/elixir/src/elixir_parser.yrl (I don't know Erlang either, but it's easy to follow along
    this was of my main sources of inspiration)
    6.: https://github.com/haifenghuang/magpie (This guy took Monkey Lang Book an added steroids to it, nice source of inspiration too)

    Okay, so how does actually a programming language work? 
    Some might respond "with magic", others might respond with zeroes and ones. Both are right, and both are wrong. Actually the second one
    is more right than wrong but anyway the idea is simple.

    We have 2 types of programming languages: Compiled and Interpreted (i think that there can be others). Python and Javascript are both
    interpreted. If you use CPython it generally is interpreted, if you use Javascript, with V8 it's actually compiled with a JIT
    compiler (Just-in-Time compilation is the process of compiling the code as the code run). Compiling code is actually more low level stuff
    than just interpreting the code, the steps are basically the same on both but usually in compiled languages we have more steps.

    In Java we run:
    javac MyProgram.java -> This will compile the code and create a binary file
    java MyProgram -> This effectively run the compiled code

    In Python, which is interpreted we do:
    python my_program.py -> This interprets the code. Underlying everything you do with python there is C.

    Compiled languages are out of the scope here, we do not compile the code because first it's more difficult to do and second it is unecessary
    for our use case.

    So we have an interpreted language, okay, how does this work?
    Usually the process is the same on every language:
    
    Lexer -> Parser -> Abstract Syntax Tree (AST) -> Interpret

    AST is actually the most important part, you can write an interpreter relatively easily if you have an AST. 

    As the name suggests Abstract Syntax Trees is actually a Tree (and you though you would never use this knowledge in
    your work after college, at least, that's what i thought. I've never passed the class Algoritimos E Estrutura de Dados while
    i was still coursing Information Systems in which we learn about trees. But it's funny because, i'm working with trees now)
    Anyway, although trees are a really complex topic in programming this one is relatively easy, we don't have to deal about 
    balancing and any of this stuff.

    If you've never knew about trees let me introduce them to you quickly:

         10
        /  \
       4    5
      / \
     2   3 

    This is a tree, and is like the tree is on the opposite direction. We call 10 as the root, root is the first node.
    2, 3 and 5 are leafs because they are in the edge. And that's it. But how do we represent it in code?

    >>> class Node:
            def __init__(self, value):
                self.value = value
                self.right = None
                self.left = None
    
    >>> root = Node(10)
        value4 = Node(4)
        value5 = Node(5)
        value2 = Node(2)
        value3 = Node(3)
    
    >>> root.left = value4
        root.right = value5
        value4.left = value2
        value4.right = value3
    
    This is how we represent trees in python. Kinda easy right? I know it's abstract but if you feel stuck try to read some
    articles on the web about it.

    So what are abstract syntax trees. Suppose the following code:
    
        variable = 1
        variable + 2

    This two lines code can be represented as (in json for easier understanding) 

    
    {
        node_type: BLOCK,
        instructions: [
            {
                node_type: ASSIGN,
                left: "variable",
                right: 1
            },
            {
                node_type: BINARY_OPERATION,
                left: {
                    node_type: VARIABLE,
                    value: "variable"
                },
                right: 2,
                operation: "+"
            },
        ]
    }
    
    So let's dig in: every dict with the key "node_type" IS A NODE. But each node can be of each type, so let's understand
    The first node is BLOCK. and what it means is a block of code, a block of code is a block of instructions to run. 
    So what are the instructions?
    On the first line we have ASSIGN and assign is exactly that, assign a value to a variable named "variable". This is what the block tells us.
    On the second line we have a BINARY_OPERATION that is exactly that. A binary operation between two numbers. But left of the BinaryOperation 
    is a Variable which is something that the abstract tree tells us. 
    The right is 2 and the operation we are making is a adition.

    That's it, that's a AST. Now let's look at some things: Not every node is equal, ones have "operation" key, other has "instrunction" key and so
    on. We need to be aware of those differences. Second, usually the values as not represented as-is, but they are tokens, tokens is an another type
    of class that we use in the lexer, put things in tokens helps our parser knows if a thing is a String or if a thing is a Integer.

    So okay, how do we create this AST? We create this with parsers, but first we need the lexer (the thing that puts things into tokens)

    The idea of the lexer is to divide the text by each character
    |v|a|r|i|a|b|l|e| |=| |1|\n|v|a|r|i|a|b|l|e| |+| |2|
    Then the job of the lexer is transform this into tokens:
    v -> is it divided by a space or any other character? No
    a -> "   "       "
    r -> "   "       "
    .
    .
    .
    e -> is it divided by a space or any other character? Yes

    Token(value="variable", token_type="IDENTITY")
    Token(value="=", token_type="ASSIGN")
    Token(value="1", token_type="INTEGER")
    .
    .
    .
    Token(value="2", token_type="INTEGER")

    The job of the parser is to get those Tokens and transform into the abstract syntax tree, and for that you might need to understand recursion
    and probably it's a lot easier if you understood EBNF.

    So on the Parser is when the magic happens and transforms everything into a NODE.

    The Tree is then interpreted in the programming language we are using (on this case python) and then that's it, we've got 
    yourself a programming language interpreter.

    I recommend you to read at least the first article (all of those 19 parts). This will help you have a better understanding about this.
    Especially about parsers that i know that i didn't explained very well. Parsers seems difficult, but it's easier once you understand that
    with a good grammar, writing your parser will be really easy.

    If you want to go further:
    https://www.youtube.com/watch?v=7MuQQQWVzU4
    https://en.wikipedia.org/wiki/Compiler-compiler
    https://en.wikipedia.org/wiki/LL_parser

    and so on.

    Args:
        expression (str): The actual formula
        context (reflow_server.formula.utils.context.Context, optional): The context object so you can translate the formula to other languages. Defaults to None.

    Returns:
        reflow_server.formula.utils.builtins.objects.*: Returns a object instance. Check the builtins.object to see the possible objects that can be returned
    """
    if context == None:
        context = Context()
    settings = Settings(context)
    lexer = Lexer(expression, settings)
    parser = Parser(lexer, settings)
    ast = parser.parse()

    interpreter = Interpreter(settings)
    value = interpreter.evaluate(ast)
    return value