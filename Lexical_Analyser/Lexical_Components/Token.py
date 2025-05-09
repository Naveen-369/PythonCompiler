
from typing import override
from .TokenType import TokenType

class Token:
    """
    The Token class classifies the synthesised words from the program into tokens like identifier, constants, etc
    and stores it in the formate containing its `tokenType`, `value` and `position`.
    """
    
    tokenType:TokenType
    atr:str
    lineNo:int
    colNo:int
    
    def __init__(self, tokenType: TokenType, atr: str = None, lineNo: int = None, colNo: int = None) -> None:
        self.tokenType = tokenType
        self.atr = atr
        self.lineNo = lineNo
        self.colNo = colNo
    
    @override
    def __repr__(self,intendationLevel:int=0) ->str:
        """This method is for logging during debugging, only for dev team.

        Args:
            intendationLevel (int, optional): The amount of intendataion of gaps required before the string. Defaults to 0.

        Returns:
            str: Official String 
        """
        return "\t"*intendationLevel+f"{self.tokenType.name} : {self.atr}"

    