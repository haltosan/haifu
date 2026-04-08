import token_gen
import interpret

N = 15
MID = 3

jumps = {
        '1t-1' : 13+N+MID,
        '1f-2' : (2*N) + MID + N - 1,
        '2t-2' : 13+N+MID
}


tokens = token_gen.shortcut('turing.tokens', N=N, jumps=jumps)[::-1]  # program was input high->low

interpret.run(tokens, debug=True, debug2=True)
