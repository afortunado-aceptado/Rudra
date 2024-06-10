def shunting_yard(tokens):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    rpntokens = []
    opstack = []
    for token in tokens:
        if isinstance(token, int):
            rpntokens.append(token)
        else:
            while opstack and precedence[token] <= precedence[opstack[-1]]:
                rpntokens.append(opstack.pop())
            opstack.append(token) # Fixed by adding the current operator to the stack
    while opstack:
        rpntokens.append(opstack.pop())
    return rpntokens
'''
The faulty code did not handle the operator tokens correctly: it omitted pushing the current operator onto the operator stack (\textit{opstack}). After identifying the bug, I added \textit{opstack.append(token)} within the \textit{else} block but outside the \textit{while} loop. This change ensures that each operator token is correctly pushed onto the stack after popping off all operators of higher or equal precedence. This fix aligns the code's behavior with Dijkstra's shunting-yard algorithm, which mandates managing operators based on their precedence to correctly convert infix expressions to Reverse Polish Notation (RPN).

'''