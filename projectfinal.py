# SIP Client (Soft phone prototype)
# Created by Arpit Singh
# Run the server before running this file "$sudo asterisk -r" in other terminal
#In user URI enter only the Called user name



import sys

import pjsua as pj

import threading

import time



# Log of callback class

def log_cb(level, str, len):

    print(str),



# Account Callback class to get notifications of Account registration

class MyAccountCallback(pj.AccountCallback):

    def __init__(self, acc):

        pj.AccountCallback.__init__(self, acc)



# Call Callback to receive events from Call

class SRCallCallback(pj.CallCallback):

    def __init__(self, call=None):

        pj.CallCallback.__init__(self, call)

    

    

    def on_state(self):

        print("Call is :", self.call.info().state_text),

        print("last code :", self.call.info().last_code),

        print("(" + self.call.info().last_reason + ")")

        

# Notification when call's media state is changed

    def on_media_state(self):

        global lib

        if self.call.info().media_state == pj.MediaState.ACTIVE:

            # Connect the call to sound device

            call_slot = self.call.info().conf_slot

            lib.conf_connect(call_slot, 0)

            lib.conf_connect(0, call_slot)

            print("Hey !!!!! Can you hear me !!!!!!!!!!")

            print (lib)


# Main loop

try:

    # Start of the Main Class

    # Create library instance of Lib class

    lib = pj.Lib()



    # Instantiate library with default config

    lib.init(log_cfg = pj.LogConfig(level=3, callback=log_cb))



    # Configuring one Transport Object and setting it to listen at 5060 port and UDP protocol

    trans_conf = pj.TransportConfig()

    print "____________________REGISTRATION PROCESS BEGINS_______________________"
    print "\n\n"

    # 12345 is default port for SIP
    trans_conf.port = 12345       
    
    # Here the client address is same as the Servers Address
    a=raw_input("Please Enter the IP address of the Client: ")
    print "Not Using the default port number, Instead using: 12345"

    trans_conf.bound_addr = a

    transport = lib.create_transport(pj.TransportType.UDP,trans_conf)



    # Starting the instance of Lib class

    lib.start()

    lib.set_null_snd_dev()



    # Configuring Account class to register with Registrar server

    # Giving information to create header of REGISTER SIP message

    
    # Hardcoded these values
    ab4="192.168.131.152" # Server's address
    ab='2020' # This clients User name
    ab1="password" # Password same as "password"
    ab2='y'
    
    ab3=ab
    

    acc_conf = pj.AccountConfig(domain = ab4, username = ab, password =ab1, display = ab3)

    # registrar = 'sip:'+ab4+':5060', proxy = 'sip:'+ab4+':5060')

    acc_conf.id ="sip:"+ab

    acc_conf.reg_uri ='sip:'+ab4+':12345'

    acc_callback = MyAccountCallback(acc_conf)

    acc = lib.create_account(acc_conf,cb=acc_callback)



    # creating instance of AccountCallback class

    acc.set_callback(acc_callback)



    print('\n')
    print "Registration Complete-----------"
    print('Status= ',acc.info().reg_status, \

         '(' + acc.info().reg_reason + ')')



    

	# Starting Calling process.
    b=raw_input("Enter the username to be called: ")
	#sip and address are hard coded here
    b1="sip:"+ str(b)+"@192.168.0.1:5066"

    call = acc.make_call(b1, SRCallCallback())





        
    print('Press <ENTER> to exit and destroy library')

    input = sys.stdin.readline().rstrip('\r\n')



        # Shutting down the library
    lib.destroy()

    lib = None

    

except pj.Error, e:

    print("Exception, error occured at : " + str(e))

    lib.destroy()

    lib = None

    sys.exit(1)


