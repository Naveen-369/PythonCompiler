class Token:
    """
    Declaration of the Token Class that stores the words alongs with its token type
    
    Attributes:
        tokenType(str) : The kind of token the word is identified as,
        tokenWord(str) : The input word retrieved from breakdown of input file 
    
    """
    
    def __init__(self,tokenType:str,tokenWord:str="")->None:
        """Construtor of Token Class

        Args:
            tokenType (str): Identified kind of token
            tokenWord (str, optional): The input token. Defaults to "".
        """
        self.tokenType=tokenType
        self.tokenWord=tokenWord
    
    def __repr__(self):
        """__repr method implemented in class to enable display of class attributes on usage in print function

        Returns:
            str:To display the Tokens and the category of token it belongs to
        """
        return f"('{self.tokenType}',{self.tokenWord}')"