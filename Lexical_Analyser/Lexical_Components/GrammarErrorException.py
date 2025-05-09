from .TokenType import TokenType

class GrammarError(Exception): # Inherit the default exception class
    def __init__(self,Errmessage:str,token:TokenType=None,excepted:TokenType=None):
        self.token=token
        self.excepted=excepted
        error_message=f"Grammer Error : {Errmessage}"
        if token:
            error_message += f" | Found : {token.tokenType} : '{token.atr}' at Line - {token.lineNo} Col - {token.colNo}"
        if excepted:
            error_message+=f" | Excepted : {excepted}"
        super().__init__(error_message)