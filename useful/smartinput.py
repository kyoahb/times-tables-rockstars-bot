from typing import Callable

class Input:
    # Input error enum. This is a string as the Input.get_response() only returns strings, so this keeps the format.
    Fail = "-1"


    def __init__(self, question : str):
        """
        A smart input class that asks for input with various checks. Returns input if all checks are passed.
        Useful for if you want to get back parameters you have checked for, even after the user response, or if you want to see the tries taken.
        Parameters:
        question (str): The question to ask.
        tries (int): The number of tries allowed. If it runs out of tries, it will return -1.
        choices (list): The choices to check for. If the input is not in the choices, the input will be rejected.
        choices_hidden (bool): If True, the choices will not be shown to the user.
        match_function (Callable): The function to check against. If the function does not return true given the input, the input will be rejected.
        data_type (type): The data type to check for. If it does not match the data type, the input will be rejected.
        """
        self.question = question
        
        self.data_type = None
        self.type_fail = None
        
        self.choices_hidden = None
        self.lower_choices = None
        self.str_choices = None
        self.sentence_choices = None
        self.choices = None
        self.choice_fail = None
        
        self.match_function = None
        self.func_fail = None
        self.pre_pass_args = None

        self.initial_tries = None
        self.tries_fail = None
        self.tries_taken = 0 # Will be incremented each loop, regardless of whether tries is set or not.

    # Initialisation functions. Separated out from def __init__ as there are too many parameters
    def add_choices(self, choices : list = [], choices_hidden : bool = False, match_case : bool = False, fail_text : str = None):
        """
        Parameters:
        choices (list) : List of allowed possible responses to the question.
        choices_hidden (bool) DEFAULT=False: Whether the choices are explicitly shown to the user.
        match_case (bool) DEFAULT=False: Whether the case should matter when comparing response to choices.
        fail_text (str) DEFAULT=None: Fail message to show the user"
        """
        assert(len(choices) > 0), "Must be more than one choice to add to input"
        
        self.choices_hidden = choices_hidden
        self.choices = choices
        self.str_choices = [str(choice) for choice in self.choices]
        self.lower_choices = [str(str_choice).lower() for str_choice in self.str_choices]
        self.sentence_choices = f"<Choices> {', '.join(self.str_choices)}"
        self.choice_fail = fail_text

    def add_tries(self, tries : int = 0, fail_text : str = None):
        """
        Parameters:
        tries (int): Max tries the user has before program exits.
        fail_text (str) DEFAULT=None: Fail message to show the user"
        """
        assert(tries > 0), "Allowed tries must be greater than 0 (or tries not set)"
        self.initial_tries = tries
        self.tries_fail = fail_text

    def add_function(self, match_function : Callable = None, fail_text : str = None, pre_pass_args = None):
        """
        Parameters:
        match_function (Callable): match_function(response) must return True for the response to be valid.
        fail_text (str) DEFAULT=None: Fail message to show the user"
        """
        assert(match_function != None), "Function cannot be none when adding function to input"
        self.match_function = match_function
        self.func_fail = fail_text
        self.pre_pass_args = pre_pass_args

    def add_data_type(self, data_type : type = None, fail_text : str = None):
        """
        Parameters:
        data_type (type): Type the response must match for the response to be valid.
        fail_text (str) DEFAULT=None: Fail message to show the user"
        """
        assert(data_type != None), "Data type cannot be none when adding data type to input"
        self.data_type = data_type
        self.type_fail = fail_text
    
    def get_response(self) -> str:
        """
        Asks user the question and returns the response if all checks are passed.


        Returns:
        str: The response from the user if passed, -1 if failed
        """
        answer = ""
        while True:
            # tries check
            if self.initial_tries != None:
                if self.tries_taken >= self.initial_tries:
                    print(f"<Ran out of tries>")
                    return Input.Fail # Exceeded maximum tries
                else:
                    if self.tries_fail != None:
                        print(self.tries_fail) # Prints custom fail text
                    else:
                        print(f"<{(self.initial_tries - self.tries_taken)} tries left>")


            self.tries_taken += 1


            if self.choices and not self.choices_hidden: print(self.sentence_choices)
            answer = str(input(f"<Input> {self.question}")).strip()
            # data type check
            if self.data_type != None:
                try:
                    self.data_type(answer)
                except:
                    if self.type_fail != None:
                        print(self.type_fail) # Prints custom fail text
                    else:
                        print(f"<Invalid input, does not match data type {str(self.data_type).lstrip("<class ").rstrip(" >")}>")
                    continue


            # choices check
            if self.choices != None:
                if not answer.lower() in self.lower_choices:
                    if not self.choices_hidden: print(f"<Invalid input, not in {self.sentence_choices}>")
                    else:
                        if self.choice_fail != None:
                            print(self.choice_fail) # Prints custom fail text
                        else:
                            print(f"<Invalid input, not in possible choices>")
                    continue


            # match_function check
            if self.match_function:
                if self.match_function(input_arg=answer, pre_pass_args=self.pre_pass_args) != True:
                    if self.func_fail != None:
                        print(self.func_fail) # Prints custom fail text
                    else:
                        print(f"<Invalid input, does not match function>")
                    continue


            # All conditions have been met: can return
            # Match output to choice:
            if self.choices: return str(self.choices[self.lower_choices.index(answer.lower())])


            # Return as normal if not choices
            return str(answer)
