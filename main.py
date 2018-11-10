#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 14:38:05 2018

@author: alejandroseif
"""
import random
import sys

def exit_program(exit_condition):
    Exit_Phrases = {'Error':["Cannot do more until you fix that",
                    "Fix that and come back","Houston, we have a problem"],
                    'Good':["Seems my job is done, bye!","That's all, enjoy!",
                            "Relax, all worked out fine. Bye!","All Done!"]}
    print('* * * '+random.choice(Exit_Phrases[exit_condition])+' * * *')
    if (exit_condition == 'Error'):
        sys.exit(0)

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
        
    def get_values(self):
        
    

def main():
    bot = Chatbot()
    bot.greetings()
    exit_program("Good")    

main()