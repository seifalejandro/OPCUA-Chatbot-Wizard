#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 14:38:05 2018

@author: alejandroseif
"""
import random
import sys

def question_input(information):
    '''
    Here we will be getting input from the user and replying
    '''
    Asking_Phrases = ['I need you to tell me ','Please input the ',
                      'Please provide the ','Give me the ']
    Acknowledge_Phrases = [', got it!',', writing that down',', sweet']
    print('* '+random.choice(Asking_Phrases)+str(information))
    value = input()
    if value == '':
        print('Defaults will be used')
    else:
        print('* '+str(information)+' '+str(value)+random.choice(Acknowledge_Phrases))
    return value

def exit_program(exit_condition):
    '''
    Tells you error/success phrases. Exits after error
    '''
    Exit_Phrases = {'Error':["Cannot do more until you fix that",
                    "Fix that and come back","Houston, we have a problem"],
                    'Good':["Seems my job is done, bye!","That's all, enjoy!",
                            "Relax, all worked out fine. Bye!","All Done!"]}
    print('* * * '+random.choice(Exit_Phrases[exit_condition])+' * * *')
    if (exit_condition == 'Error'):
        sys.exit(0)
        
class OPCUA_variables:
    '''
    Here we will store all the necessary OPCUA variables.
    The chatbot will populate them
    '''

    IP_Address = '192.168.1.1'
    OPCUA_Port = '4840/freeopcua/server/'
    Object_Name = 'MyObject'
    Client_Sleep_Time = 1
    Server_Sleep_Time = 0.5

class Chatbot:
    '''
    This class contains the whole chatbot opcua builder experience.
    These are the functions available:
        greetings:   
            This one greets the user and checks for necessary modules
            installed in the system. 
        exit_program:
            Gives you a phrase regarding if you exit with Error or Good. 
            If you have an error, exits the program on the spot
        check_opcua_package:
            This one checks that you have the opcua package, if not
            exits the program (using exit_program)letting you know whats wrong
    '''
    def check_opcua_package(self):
        '''
        Checks for opcua module installed. 
        '''
        try: 
            import opcua
            print("* Seems like OPCUA python is installed. Which is good"+
                  " because we need that")
            return True
        except ModuleNotFoundError:
            print("ERROR!: It seems you have not installed the opcua python package.")
            print("Just go ahead and pip install it in a terminal "+
                  "so we can continue. Do this:")
            print("\n"+">>>>$pip install opcua")
            exit_program('Error')
            return False
    
    def greetings(self):
        '''
        Greets you and launches the check for necessary modules
        '''
        print("* Welcome to the OPCUA Wizard Chatbot. Together, we will setup"
              +" OPC UA clients and server files which you can run later.")
        print("We will be setting up a minimal server and client"
              +", with your input we can do this quickly")
        self.check_opcua_package()
        
    def get_values(self,OPCUA):
        '''
        Asks how many variables in the object, as well as sleep times
        in the server and client.
        If an attribute is not given, keep the defaults
        '''
        print("*OK, now I need you to tell me a few things so I can set up"
              +" the client an server files.")
        print("Namely those are: \nIP address (e.g. 192.168.1.1)"
             +"\nObject name (e.g. Fridge)"
             +"\nInput name of variables one at the time (e.g. Temperature))")
        print("You can RESET the OPCUA values by writing RESET")
        print("\n Also, there are default values there. So if you don't know," 
              +" keep em defaults and see if it still works")
        for attr in dir(OPCUA):
            if not attr.startswith("__"):
                value = question_input(attr)
                if value == '':
                    continue
                else:
                    setattr(OPCUA, attr,value)
            else:
                continue
        Variables_List = []
        print('\nOK, so the variables I have so far are\n')
        for attr in dir(OPCUA):
            if not attr.startswith("__"):
                print(attr,getattr(OPCUA,attr))
#        print("If this is not OK, write RESET") <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        print("When you have added all the variables you want, type in DONE")
        while(True):
            if (question_input('VARIABLE NAME') == 'DONE'):
                print(question_input('VARIABLE NAME'))
                break
            Variables_List.append(question_input('VARIABLE NAME'))
        print('Ok, so we have {0} variables.'.format(len(Variables_List)))
        print("These are :"+str(Variables_List))
            
            
def main():
    OPCUA = OPCUA_variables()
    bot = Chatbot()
    bot.greetings()
    bot.get_values(OPCUA)
    exit_program("Good")    

main()