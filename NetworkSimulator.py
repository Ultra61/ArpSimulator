import sqlite3 #database
import time 
#resource: https://pynative.com/python-sqlite/ --
try: #try to connect to database
    sqlite_connection = sqlite3.connect('NetworkSimulator.db')
    cursor = sqlite_connection.cursor()
    print("Successfully Connected to SQLite")
    sqlite_version_query = "select sqlite_version();"
    cursor.execute(sqlite_version_query)
    version = cursor.fetchall()
    print("SQLite Database Version is: {}".format(version[0]))
    #print("SQLite Database Version is:", version)
except sqlite3.Error as error: #if fails to connect to database raise error
    print("Error connecting to SQLite")
# --

#make sure tables are deleted before running the program in order to not attempt to create them again
try:
    cursor.execute("DROP TABLE host1ARP")
    cursor.execute("DROP TABLE host2ARP")
    cursor.execute("DROP TABLE host3ARP")
    cursor.execute("DROP TABLE host4ARP")
    cursor.execute("DROP TABLE host5ARP")
except:
    pass
    #print("host ARP tables correctly deleted previously")

#make sure tables are deleted before running the program in order to not attempt to create them again
try:
    cursor.execute("DROP TABLE ArpPacket")
except:
    pass

host_dict = {} #create dictionary for storing created hosts
host_ip_dict = {} #create dictionary for storing created IP addresses
host_mac_dict = {} #create dictionary for storing created MAC addresses

global q
global c
q = 0
c = 0
#===============================================================================================================
class HostCreation:
    def __init__(self, arp_table, hostname, ip_address, mac_address):
        self.arp_table = arp_table
        self.hostname = hostname
        self.ip_address = ip_address
        self.mac_address = mac_address
        host_dict[self.hostname] = False #add object to host_dict
        host_ip_dict[self.hostname] = self.ip_address #associate hostname with an ip_address
        host_mac_dict[self.hostname] = self.mac_address
        self.host_queries = {} #create dictionary to hold sql queries
        ext = 0
    def arp_table_entry(self, ip_address, mac_address):
        if self.hostname == "host1":
            print("Entering ARP information into host1 ARP Table")
            sql = "INSERT into host1ARP (Internet_Address, Physical_Address) VALUES (?,?)"
            arp_values = [
                (ip_address, mac_address)
            ]
            cursor.executemany(sql, arp_values)
            sqlite_connection.commit()
        elif self.hostname == "host2":
            print("Entering ARP information into host2 ARP Table")
            sql = "INSERT into host2ARP (Internet_Address, Physical_Address) VALUES (?,?)"
            arp_values = [
                (ip_address, mac_address)
            ]
            cursor.executemany(sql, arp_values)
            sqlite_connection.commit()
        elif self.hostname == "host3":
            print("Entering ARP information into host3 ARP Table")
            sql = "INSERT into host3ARP (Internet_Address, Physical_Address) VALUES (?,?)"
            arp_values = [
                (ip_address, mac_address)
            ]
            cursor.executemany(sql, arp_values)
            sqlite_connection.commit()
        elif self.hostname == "host4":
            print("Entering ARP information into host 4 Arp Table")
            sql = "INSERT into host4ARP (Internet_Address, Physical_Address) VALUES (?,?)"
            arp_values = [
                (ip_address, mac_address)
            ]
            cursor.executemany(sql, arp_values)
            sqlite_connection.commit()
        elif self.hostname == "host5":
            print("Entering ARP information into host 5 Arp Table")
            sql = "INSERT into host5ARP (Internet_Address, Physical_Address) VALUES (?,?)"
            arp_values = [
                (ip_address, mac_address)
            ]
            cursor.executemany(sql, arp_values)
            sqlite_connection.commit()
        else:
            print("error")
    #allow user to connect to host
    def connection_successful(self):
        print("connection to " + self.hostname + " successful\n")
    #create a virtual arp packet to send across network
    def create_arp_packet(self, hardware_type, protocol_type, hardware_size, sender_mac_address, sender_ip_address, target_mac_address, target_ip_address):
        cursor.execute("CREATE TABLE ArpPacket (Field varchar(255), Value varchar(255))")
        sql = "INSERT into ArpPacket (Field, Value) VALUES (?,?)"
        arp_values = [
            ('hardware_type', hardware_type),
            ('protocol_type', protocol_type),
            ('hardware_size', hardware_size),
            ('sender_mac_address', sender_mac_address),
            ('sender_ip_address', sender_ip_address),
            ('target_mac_address', target_mac_address),
            ('target_ip_address', target_ip_address)
        ]
        cursor.executemany(sql, arp_values)
        sqlite_connection.commit()
        #test to see if previous sql statements work
        cursor.execute("SELECT * FROM ArpPacket")
        ArpPacket = cursor.fetchall()
        #format sending of packet
        print("")
        print("=====ARP FRAME=====")
        for row in ArpPacket:
            print(row[0], ": ", row[1])
        print("")
    #execute sql queries specific to a host object
    def execute_host_query(self, key):
        cursor.execute(self.host_queries[key])
    #add sql queries to a dictionary specific to a host object
    def update_host_queries(self, key, query):
        self.host_queries[key] = query
    #====================output options associated with a host object====================

    def host_options(self):
        option = input("Select one of the options for " + self.hostname + ":"
              "\n1. Send Message \n2. Show Host Details \n3. Show ARP Table \n4. Clear ARP Table \n5. Change Host \n6. Exit Program\n> ") #each of these will be a different method
        option = int(option) #type cast option to an int
        if option == 1:
            print("\nPreparing to send message...")
            time.sleep(1)
            self.send_message()
        elif option == 2:
            self.show_host_details()
        elif option == 3:
            print("\nRetrieving ARP Table for " + self.hostname + "...")
            time.sleep(1)
            self.show_arp_table()
        elif option == 4:
            print("\nClearing " + self.arp_table + " table")
            time.sleep(1)
            self.clear_arp_table()
        elif option == 5:
            print("\nChanging host")
            time.sleep(1)
            self.change_host()
        elif option == 6:
            print("\nExiting program") 
            time.sleep(1)
            self.exit_program()
            
    #================host options==================#
    def send_message(self):
        host_choice_check = True
        while(host_choice_check):
            host_keys = list(host_dict.keys())
            for host in host_keys:
                if host != self.hostname:
                    print(host)
            print("Which host would you like to send a message to?")
            host_recipient = input("> ")
            if host_recipient in host_keys and host_recipient != self.hostname:
                print("Host available")
                host_choice_check = False
            elif host_recipient == self.hostname:
                print("You cannot send a message to yourself! Please choose another host")
            else:
                print("Host unavailable. Please choose another host")
        print("Enter the message that you would like to send")
        message_check = True
        while (message_check):
            message = input("> ")
            print("the message is: " + message)
            print("is the message correct? (Y/N)") #if !N continue
            message_confirm = input("> ")
            if message_confirm == 'N' or message_confirm == 'n':
                print("please re-enter your message")
            else:
                message_check = False
        #if host_recipient ip in arp table send message without arp
        self.execute_host_query("GET ARP TABLE")
        arp_table = cursor.fetchall()
        #
        send_arp_message = True
        for row in arp_table:
            #print(row[0], ":", row[1])
            if row[0] == host_ip_dict[host_recipient]:
                print("Recipient Host in ARP Table: " + row[0] + ": " + row[1])
                print("Sending message to " + row[0])
                print("Message Recieved")
                send_arp_message = False
        #if send_arp_message...
        if send_arp_message:
            print("Associated MAC Address not in ARP Table. Performing ARP Broadcast")
            self.create_arp_packet("Ethernet", "IPv4", "6", self.mac_address, self.ip_address, "00:00:00:00:00:00", host_ip_dict[host_recipient])
            #host_ip_dict.pop(self.hostname)
            host_keys = list(host_ip_dict.keys()) #make a list of only the hostnames (keys)
            host_keys.remove(self.hostname)
            for key in host_keys:
                print("broadcasting to " + host_ip_dict[key])
                time.sleep(2)
                if host_ip_dict[key] == host_ip_dict[host_recipient]:
                    print("ARP Message received by " + key) #allow host to reply to ARP 
                    print("Received ARP Packet from " + host_ip_dict[key])
                    #simulate host replying to ARP Packet
                    #get MAC address from packet for reply
                    cursor.execute("SELECT Value FROM ArpPacket WHERE Field = 'sender_mac_address'")
                    fetch = cursor.fetchone()
                    target_mac_address = fetch[0]
                    #get IP address from packet for reply
                    cursor.execute("SELECT Value FROM ArpPacket WHERE Field = 'sender_ip_address'")
                    fetch = cursor.fetchone()
                    target_ip_address = fetch[0]
                    reply_arp_packet("Ethernet", "IPv4", "6", host_mac_dict[key], host_ip_dict[key], target_mac_address, target_ip_address)
                    #get MAC address from reply to put in ARP Table
                    cursor.execute("SELECT Value FROM ArpPacketReply WHERE Field = 'sender_mac_address'")
                    fetch = cursor.fetchone()
                    arp_mac_address = fetch[0]
                    #get IP address from reply to put in ARP Table
                    cursor.execute("SELECT Value FROM ArpPacketReply WHERE Field = 'sender_ip_address'")
                    fetch = cursor.fetchone()
                    arp_ip_address = fetch[0]
                else:
                    print("ARP Messaged dropped by " + key)
            #add ip_address and associated mac address to arp table
            self.arp_table_entry(arp_ip_address, arp_mac_address)
            #send message
    #output details assocated with a host object
    def show_host_details(self):
        print("\nHostname: " + self.hostname)
        print("IP Address: " + self.ip_address)
        print("MAC Address: " + self.mac_address)
        print("ARP Table: " + self.arp_table + "\n")
    #output arp table associated with a host object
    def show_arp_table(self):
        self.execute_host_query("GET ARP TABLE")
        arp_table = cursor.fetchall()
        for row in arp_table:
            print(row[0], ":", row[1])
    #clear arp table associated with a host object
    def clear_arp_table(self):
        self.execute_host_query("CLEAR ARP TABLE")
    def change_host(self):
        global c
        c = 1
    #exit program
    def exit_program(self):
        global q
        q = 1
        quit() #exit the program

#===============================================================================================================

#===============================================================================================================
#allow the user to choose an available host 
def user_choose_host():
    flag = True
    while(flag):
        print("Which of the following hosts would you like to use?")
        available_hosts = list(host_dict.keys()) #put available hosts into a list
        for host in available_hosts:
            print(host)
        user_host = input("> ")
        #check to make sure user chooses an available host
        if user_host in available_hosts:
            print("connecting to host...")
            flag = False
        else:
            print("host unavailable")
    return user_host
#===============================================================================================================
    #experimental
def reply_arp_packet(hardware_type, protocol_type, hardware_size, sender_mac_address, sender_ip_address, target_mac_address, target_ip_address):
    time.sleep(2)
    cursor.execute("CREATE TABLE ArpPacketReply (Field varchar(255), Value varchar(255))")
    sql = "INSERT into ArpPacketReply (Field, Value) VALUES (?,?)"
    arp_values = [
        ('hardware_type', hardware_type),
        ('protocol_type', protocol_type),
        ('hardware_size', hardware_size),
        ('sender_mac_address', sender_mac_address),
        ('sender_ip_address', sender_ip_address),
        ('target_mac_address', target_mac_address),
        ('target_ip_address', target_ip_address)
    ]
    cursor.executemany(sql, arp_values)
    sqlite_connection.commit()
    #test to see if previous sql statement works
    cursor.execute("SELECT * FROM ArpPacketReply")
    ArpPacketReply = cursor.fetchall()
    #format sending of packet
    print("")
    print("======ARP FRAME REPLAY======")
    for row in ArpPacketReply:
        print(row[0], ": ", row[1])
    print("")
#===============================================================================================================
#final simulation
def arp_simulation():
    #create hosts
    host1 = HostCreation("host1ARP", "host1", "192.168.1.65", "2B-CF-88-96-92-7C")
    host2 = HostCreation("host2ARP", "host2", "192.168.1.28", "28-78-EF-E9-5E-F6")
    host3 = HostCreation("host3ARP", "host3", "192.168.1.132", "89-A1-0B-09-7C-36")
    host4 = HostCreation("host4ARP", "host4", "192.168.1.49", "01-F1-E9-76-13-F1")
    host5 = HostCreation("host5ARP", "host5", "192.168.1.121", "95-94-E3-BC-4C-75")
    #setup ARP tables for individual hosts
    cursor.execute("CREATE TABLE host1ARP (Internet_Address varchar(255), Physical_Address varchar(255))")
    #insert default values for host1
    sql = "INSERT into host1ARP (Internet_Address, Physical_Address) VALUES (?,?)"
    arp_values = [
        ('255.255.255.255', 'FF-FF-FF-FF-FF-FF')
    ]
    cursor.executemany(sql, arp_values)
    sqlite_connection.commit()
    cursor.execute("CREATE TABLE host2ARP (Internet_Address varchar(255), Physical_Address varchar(255))")
    #insert default values for host2
    sql = "INSERT into host2ARP (Internet_Address, Physical_Address) VALUES (?,?)"
    arp_values = [
        ('255.255.255.255', 'FF-FF-FF-FF-FF-FF')
    ]
    cursor.executemany(sql, arp_values)
    sqlite_connection.commit() 
    cursor.execute("CREATE TABLE host3ARP (Internet_Address varchar(255), Physical_Address varchar(255))")
    #insert default values for host3
    sql = "INSERT into host3ARP (Internet_Address, Physical_Address) VALUES (?,?)"
    arp_values = [
        ('255.255.255.255', 'FF-FF-FF-FF-FF-FF')
    ]
    cursor.executemany(sql, arp_values)
    sqlite_connection.commit()
    cursor.execute("CREATE TABLE host4ARP (Internet_Address varchar(255), Physical_Address varchar(255))")
    #insert default values for host4
    sql = "INSERT into host4ARP (Internet_Address, Physical_Address) VALUES (?,?)"
    arp_values = [
        ('255.255.255.255', 'FF-FF-FF-FF-FF-FF')
    ]
    cursor.executemany(sql, arp_values)
    sqlite_connection.commit()
    cursor.execute("CREATE TABLE host5ARP (Internet_Address varchar(255), Physical_Address varchar(255))")
    #insert default values for host5
    sql = "INSERT into host5ARP (Internet_Address, Physical_Address) VALUES (?,?)"
    arp_values = [
        ('255.255.255.255', 'FF-FF-FF-FF-FF-FF')
    ]
    cursor.executemany(sql, arp_values)
    sqlite_connection.commit()
    #add appropriate host queries
    host1.update_host_queries("GET ARP TABLE", "SELECT * FROM host1ARP") #query to retreive ARP table
    host1.update_host_queries("CLEAR ARP TABLE", "DELETE FROM host1ARP WHERE Internet_Address != '255.255.255.255'") #query to clear ARP tale except Ethernet Broadcast
    host2.update_host_queries("GET ARP TABLE", "SELECT * FROM host2ARP")
    host2.update_host_queries("CLEAR ARP TABLE", "DELETE FROM host2ARP WHERE Internet_Address != '255.255.255.255'")
    host3.update_host_queries("GET ARP TABLE", "SELECT * FROM host3ARP")
    host3.update_host_queries("CLEAR ARP TABLE", "DELETE FROM host3ARP WHERE Internet_Address != '255.255.255.255'")
    host4.update_host_queries("GET ARP TABLE", "SELECT * FROM host3ARP")
    host4.update_host_queries("CLEAR ARP TABLE", "DELETE FROM host4ARP WHERE Internet_Address != '255.255.255.255'")
    host5.update_host_queries("GET ARP TABLE", "SELECT * FROM host5ARP")
    host5.update_host_queries("CLEAR ARP TABLE", "DELETE FROM host5ARP WHERE Internet_Address != '255.255.255.255'")
    #let the user choose which host they would like to use
    loop_check = True #see if the user wants to continue the program
    print("Welcome to the Address Resolution Protocol Simulation!")
    while(loop_check):
        user_host = user_choose_host()
        try:
            if user_host == "host1":
                host1.connection_successful()
                host1.host_options()
                if c == 1: #if user chose to change host
                    continue
            elif user_host == "host2":
                host2.connection_successful()
                host2.host_options()
                if c == 1:
                    continue
            elif user_host == "host3":
                host3.connection_successful()
                host3.host_options()
                if c == 1:
                    continue
            elif user_host == "host4":
                host4.connection_successful()
                host4.host_options()
                if c == 1:
                    continue
            elif user_host == "host5":
                host5.connection_successful()
                host5.host_options()
                if c == 1:
                    continue
        except:
            if q == 0:
                print("Error connecting to host. Shutting down...")
            else:
                print("Hosts shutting down...")
        #remove the ArpPacket and ArpPacketReply tables so can be recreated later if necessary
        try:
            cursor.execute("DROP TABLE ArpPacket")
            cursor.execute("DROP TABLE ArpPacketReply")
        except:
            pass
        #if the user chose to exit the program do not ask them if they would like to do something else
        if q == 0:   
            print("Would you like to do something else? Y/N")
            loop = input("> ")
            if loop == 'N' or loop == 'n':
                print("Hosts shutting down...")
                loop_check = False
            else:
                print("Continuing simulation...")
        else:
            break

    cursor.execute("DROP TABLE host1ARP")
    cursor.execute("DROP TABLE host2ARP")
    cursor.execute("DROP TABLE host3ARP")
    cursor.execute("DROP TABLE host4ARP")
    cursor.execute("DROP TABLE host5ARP")
#===============================================================================================================

arp_simulation()



