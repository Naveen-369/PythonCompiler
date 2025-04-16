import typing;

class GrammarError(Exception):
    """The error to be thrown incase of encoutering error

    Attributes:
        message(str) : The error message to be displayed
        token (optional) : The token that caused the error
        expected (optional) : Denotes the token that is excepted in the place of problematic token
    """
    
    '''Constructor Declaration'''
    def __init__(self,message:str,token:str=None,excepted:typing.Union[str,list[str]]=None):
        # Assignment section
        self.message=message
        self.token=token
        self.excepted=excepted
        error_message=(f"Encountered Grammar Error : {message}"
        +f"\nFound : {token}" if (token) else ""
        +f"\nExcepted : {excepted}" if(excepted) else "")
        # To display the error, pass it to Exception (Super) class
        super().__init__(error_message)