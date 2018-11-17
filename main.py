#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 14:38:05 2018

@author: alejandroseif
"""
import random
import sys
# -------------------------------------------------------------------------- #
class io_stuff:
        
    def question_input(self,information):
        '''
        Here we will be getting input from the user and replying
        '''
        Asking_Phrases = ['I need you to tell me ','Please input the ',
                          'Please provide the ','Give me the ']
        Acknowledge_Phrases = [', got it!',', writing that down',', sweet']
        print('\n* '+random.choice(Asking_Phrases)+str(information))
        value = input()
        if value == '':
            print('Defaults will be used')
        else:
            print('* '+str(information)+' '+str(value)+random.choice(Acknowledge_Phrases))
        return value
    
    def exit_program(self,exit_condition):
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
# -------------------------------------------------------------------------- #        
class OPCUA_tools:
    '''
    Here we will store all the necessary OPCUA variables.
    The chatbot will populate them
    '''

    IP_Address = '0.0.0.0'
    OPCUA_Port = '4840/freeopcua/server/'
    Object_Name = 'MyObject'
    Client_Sleep_Time = 1
    Server_Sleep_Time = 0.5
    Variables = ''
    
# -------------------------------------------------------------------------- #        

class OPCUA_files:
    def Client_File(self,OPCUA):
        '''
        Here we will write the Client file, once all the necessary values
        have been gathered. 
        '''
        Client = open("Client.py","w+")
        
        Client.write("import sys"+'\n')       
        Client.write('sys.path.insert(0, "..")'+'\n')
        Client.write("import time"+'\n')
        Client.write("from opcua import Client"+'\n')
        Client.write('if __name__ == "__main__":'+'\n')
        Client.write('\tclient = Client("opc.tcp://localhost:4840/freeopcua/server/")'+'\n')
        Client.write("\ttry:"+'\n')
        Client.write("\t\tclient.connect()"+'\n')
        Client.write("\t\troot = client.get_root_node()"+'\n') 
        Client.write("\t\tVariables=root.get_children()[0].get_children()"+
                     "[1].get_variables()"+'\n')
        Client.write('\t\twhile True:'+'\n')
        Client.write('\t\t\ttime.sleep('+str(OPCUA.Client_Sleep_Time)+')'+'\n')
        Client.write('\t\t\tfor v in Variables:'+'\n')
        Client.write('\t\t\t\tprint(v.get_value())'+'\n')
        Client.write("\tfinally:"+'\n')
        Client.write("\t\tclient.disconnect()"+'\n')
        Client.close()
        
    
    def Server_File(self,OPCUA):
        '''
        Here we will write the Server file, once all the necessary values
        have been gathered. 
        '''
        Server = open("Server.py","w+")
        
        Server.write("import sys"+'\n')       
        Server.write('sys.path.insert(0, "..")'+'\n')
        Server.write("import time"+'\n')
        Server.write("from opcua import ua, Server"+'\n')
        Server.write('if __name__ == "__main__":'+'\n')

        Server.write('\t# setup our server'+'\n')
        Server.write('\tserver = Server()'+'\n')
        Server.write('\tserver.set_endpoint("opc.tcp://'+OPCUA.IP_Address+':'+
                                            OPCUA.OPCUA_Port+'")'+'\n')

        Server.write('\t# setup our own namespace, not really necessary but should as spec'+'\n')
        Server.write('\turi = "http://examples.freeopcua.github.io"'+'\n')
        Server.write('\tidx = server.register_namespace(uri)'+'\n')

        Server.write('\t# get Objects node, this is where we should put our nodes'+'\n')
        Server.write('\tobjects = server.get_objects_node()'+'\n')
        
        Server.write('\tmyobj = objects.add_object(idx, '+'"'+
                                                   str(OPCUA.Object_Name)+'")'+'\n')
        Server.write('\tmyvars = []'+'\n')        
        for vars in range(len(OPCUA.Variables)):
            Server.write('\tmyvars.append(myobj.add_variable(idx, '+'"'+
                                            str(OPCUA.Variables[vars])+'", 0))'+'\n')
        #Server.write('\tmyvar.set_writable()    # Set MyVariable to be writable by clients'+'\n')
        Server.write('\tserver.start()'+'\n')
        
        Server.write('\ttry:'+'\n')
        Server.write('\t\tcount = 0'+'\n')
        Server.write('\t\twhile True:'+'\n')
        Server.write('\t\t\ttime.sleep('+str(OPCUA.Server_Sleep_Time)+')'+'\n')
        Server.write('\t\t\tcount += 0.1'+'\n')
        for vars in range(len(OPCUA.Variables)):
            Server.write('\t\t\tmyvars['+str(vars)+'].set_value(count)'+'\n')
        Server.write('\tfinally:'+'\n')
        Server.write('\t\tserver.stop()'+'\n')
        
        Server.close()
# -------------------------------------------------------------------------- #
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
    def check_opcua_package(self,io):
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
            io.exit_program('Error')
            return False
    
    def greetings(self,io):
        '''
        Greets you and launches the check for necessary modules
        '''
        print("* Welcome to the OPCUA Wizard Chatbot. Together, we will setup"
              +" OPC UA clients and server files which you can run later.")
        print("We will be setting up a minimal server and client"
              +", with your input we can do this quickly")
        self.check_opcua_package(io)
        
    def get_values(self,OPCUA,io):
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
                value = io.question_input(attr)
                if value == '':
                    continue
                else:
                    setattr(OPCUA, attr,value)
            else:
                continue
        print('\nOK, so the values I have so far are\n')
        for attr in dir(OPCUA):
            if not attr.startswith("__"):
                print(attr,getattr(OPCUA,attr))
#        print("If this is not OK, write RESET") <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        if (len(OPCUA.Variables) != 0):
            OPCUA.Variables = [OPCUA.Variables]
        else:
            OPCUA.Variables = []
        print('Do yo have more variables? YES to add more'+
              ', otherwise we are done')
        Variables_Done = input()
        while (Variables_Done == 'YES'):
            OPCUA.Variables.append(io.question_input('VARIABLE NAME'))
            print('Do yo have more variables? YES to add more'+
              ', otherwise we are done')
            Variables_Done = input()
        else:            
            print('Ok, so we have {0} variables.'.format(len(OPCUA.Variables)))
        print("These are :"+str(OPCUA.Variables))
        if (len(OPCUA.Variables)== 0) :
            print('Ok, So no variables were inputted. We need that')
            io.exit_program('Error')
            
 # -------------------------------------------------------------------------- #           
def main():
    io = io_stuff()
    OPCUA = OPCUA_tools()
    bot = Chatbot()
    bot.greetings(io)
    bot.get_values(OPCUA,io)
    files = OPCUA_files()
    files.Client_File(OPCUA)
    files.Server_File(OPCUA)
    io.exit_program("Good")    
# -------------------------------------------------------------------------- #
main()