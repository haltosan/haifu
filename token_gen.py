import haifu_common
from haifu_common import TokenType, ElementType, VariableToken
import parse
from parse import ParserToken

N = 15

offsets = {
        'N-1' : N-1,
        'N+1' : N+1,
        'N+2' : N+2
}

jumps = {}

NOP = ParserToken(TokenType.INT, 1)

lookup = {
        'heaven' : TokenType.HEAVEN,
        'promote' : TokenType.PROMOTE,
        'demote' : TokenType.DEMOTE,
        'blossom' : TokenType.BLOSSOM,
        'rise' : TokenType.RISE,
        'fall' : TokenType.FALL,
        'listen' : TokenType.LISTEN,
        'speak' : TokenType.SPEAK,
        'count' : TokenType.COUNT,
        'create' : TokenType.CREATE,
        'destroy' : TokenType.DESTROY,
        'fear' : TokenType.FEAR,
        'love' : TokenType.LOVE,
        'become' : TokenType.BECOME,
        'like' : TokenType.LIKE,
        'negative' : TokenType.NEGATIVE,
        'operate' : TokenType.OPERATE,
        'rand' : TokenType.RAND
}


def shortcut(file_name, jumps=jumps, N=N):

    x = open(file_name, 'r')
    raw = x.read()
    for offset in offsets:
        raw = raw.replace(offset, str(offsets[offset]))
    raw = raw.replace('N', str(N))
    lines = raw.split('\n')[:-1]
    x.close()

    tokens = []
    for line in lines:
        # special macros
        if line in jumps:
            tokens.append(ParserToken(TokenType.INT, jumps[line]))
        elif 'nop-' in line:
            for i in range(int(line.split('-')[-1])):
                tokens.append(NOP)
        # regular parsing
        elif line in lookup:
            tokens.append(ParserToken(lookup[line])) 
        else:
            try:
                num = int(line)
                tokens.append(ParserToken(TokenType.INT, num))
            except:
                if not line.isalpha():
                    tokens.append(ParserToken(TokenType.PUNC))
                else:
                    element_t = parse.get_element_type(line)
                    tokens.append(ParserToken(TokenType.VAR, VariableToken(line, element_t)))
    return tokens

if __name__ == '__main__':
    import sys
    for i in shortcut(sys.argv[1]):
        print(i)
