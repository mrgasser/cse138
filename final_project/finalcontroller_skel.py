# Final Skeleton
#
# Hints/Reminders from Lab 3:
#
# To check the source and destination of an IP packet, you can use
# the header information... For example:
#
# ip_header = packet.find('ipv4')
#
# if ip_header.srcip == "1.1.1.1":
#   print "Packet is from 1.1.1.1"
#
# Important Note: the "is" comparison DOES NOT work for IP address
# comparisons in this way. You must use ==.
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. The following modifications have 
    # been made from Lab 3:
    #   - port_on_switch: represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet.
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    # You should use these to determine where a packet came from. To figure out where a packet 
    # is going, you can use the IP header information.
    print("Do final")

    #check for packets
    icmp_packet = packet.find("icmp")
    ipv4_packet = packet.find("ipv4")

    #if ipv4 packet need to check which switch its on
    if(ipv4_packet != None):
      if(switch_id == 1):
        # Switch 1
        # Floor 1 Switch 1
        # Hosts: laptop, labmachine
        # Switches: Core Switch (s3)
        print("S1")
        if (port_on_switch == 8): 
          # Source is laptop
          if(ipv4_packet.dstip == "20.2.1.20"):
            # destination is labmachine, send on port 9
            self.accept(packet,packet_in, 9)
          else:
            # otherwise send on port 11
            self.accept(packet, packet_in, 11)
        elif(port_on_switch == 9):
          # Source is Labmachine
          if(ipv4_packet.dstip == "20.2.1.10"):
            # Destination is Laptop, send on port 8
            self.accept(packet, packet_in, 8)
          else:
            # otherwise send on port 11
            self.accept(packet, packet_in, 11)
        elif(port_on_switch == 11):
          #souce is port 11
          if(ipv4_packet.dstip == "20.2.1.20"):
            # destination is labmachine, send on port 9
            self.accept(packet,packet_in, 9)
          elif(ipv4_packet.dstip == "20.2.1.10"):
            # Destination is Laptop, send on port 8
            self.accept(packet, packet_in, 8)
          else:
            # else drop the packet
            self.drop(packet, packet_in)
        else:
          #else drop the packet
          self.drop(packet, packet_in)

      elif(switch_id == 2):
        # Switch 2
        # Floor 1 Switch 2
        # hosts: Device1, Device 2
        # Switches: Core Switch
        print("S2")
        if (port_on_switch == 8): 
          # Source is Device 1
          if(ipv4_packet.dstip == "20.2.1.40"):
            # destination is Device2, send on port 9
            self.accept(packet,packet_in, 9)
          else:
            # otherwise send on port 11
            self.accept(packet, packet_in, 11)
        elif(port_on_switch == 9):
          # Source is Device 2
          if(ipv4_packet.dstip == "20.2.1.30"):
            # Destination is Device 1, send on port 8
            self.accept(packet, packet_in, 8)
          else:
            # otherwise send on port 11
            self.accept(packet, packet_in, 11)
        elif(port_on_switch == 11):
          #souce is port 11
          if(ipv4_packet.dstip == "20.2.1.40"):
            # destination is device 2, send on port 9
            self.accept(packet,packet_in, 9)
          elif(ipv4_packet.dstip == "20.2.1.30"):
            # Destination is device 1, send on port 8
            self.accept(packet, packet_in, 8)
          else:
            # else drop the packet
            self.drop(packet, packet_in)
        else:
          #else drop the packet
          self.drop(packet, packet_in)

      elif(switch_id == 3):
        #Switch 3
        #Core Switch
        # hosts: h_trusted, h_untrusted
        # Switches: s1, s2, s4, s5, s6
        print("S3")
        if(icmp_packet != None):
          #we have an icmp packet
          if(port_on_switch == 9):
            #source is untrusted host
            #untrusted host can only send ICMP to trusted host
            if(ipv4_packet.dstip == "104.24.32.100"):
              #if destination is trusted host, accept on port 8
              self.accept(packet,packet_in,8)
            else:
              #else drop everythin else
              self.drop(packet,packet_in)
          elif(port_on_switch == 8):
            #source is trusted host
            #can send to Untrusted host and floor 2
            if(ipv4_packet.dstip == "108.44.83.103"):
              #destination is untrusted host, accept on port 9
              self.accept(packet,packet_in, 9)
            elif(ipv4_packet.dstip == "10.2.7.10" or ipv4_packet.dstip == "10.2.7.20"):
              #destination is floor 2, accecpt on port 3
              self.accept(packet,packet_in, 3)
            else:
              #else drop the packet
              self.drop(packet, packet_in)
          elif(port_on_switch == 1):
            # source is floor 1 switch 1
            if(ipv4_packet.dstip == "20.2.1.30" or ipv4_packet.dstip == "20.2.1.40"):
              #destination is s2 floor 1
              self.accept(packet,packet_in, 2)
            elif(ipv4_packet.dstip == "30.1.4.66"):
              #destination is webserver
              self.accept(packet,packet_in,5)
            else:
              self.drop(packet,packet_in)
          elif(port_on_switch == 2):
            # source is floor 1 switch 2
            if(ipv4_packet.dstip == "20.2.1.10" or ipv4_packet.dstip == "20.2.1.20"):
              #destination is floor 1 s 1
              self.accept(packet,packet_in, 1)
            elif(ipv4_packet.dstip == "30.1.4.66"):
              #destination is webserver
              self.accept(packet,packet_in,5)
            else:
              self.drop(packet,packet_in)
          
          elif(port_on_switch == 3):
            #source is floor 2 s 1
            if(ipv4_packet.dstip == "30.1.4.66"):
              #destination is webserver
              self.accept(packet,packet_in,5)
            else:
              self.drop(packet,packet_in)

          elif(port_on_switch == 5):
            #source web server
            if(ipv4_packet.dstip == "20.2.1.30" or ipv4_packet.dstip == "20.2.1.40"):
              #destination is s2 floor 1
              self.accept(packet,packet_in, 2)
            elif(ipv4_packet.dstip == "20.2.1.10" or ipv4_packet.dstip == "20.2.1.20"):
              #destination is floor 1 s 1
              self.accept(packet,packet_in, 1)
            elif(ipv4_packet.dstip == "10.2.7.10" or ipv4_packet.dstip == "10.2.7.20"):
              #destination is floor 2 s1
              self.accept(packet,packet_in, 3)
            else:
              self.drop(packet, packet_in)
          
          else:
            # drop all non allowed ICMP_PACKETS
            self.drop(packet,packet_in)
            
        elif(ipv4_packet.srcip == "108.44.83.103" or ipv4_packet.dstip == "30.1.4.66"):
          #untrusted host cannot send IP traffic to server
          self.drop(packet,packet_in)
        else:
          #IP packet all authorized
          self.accept(packet,packet_in, of.OFPP_FLOOD)

      elif(switch_id == 4):
        #Switch 4
        #Data Center Switch
        # Hosts: Web server
        # Switches: Core Switch
        print("S4")
        if(port_on_switch == 8):
          # source is Server, send out port 11
          self.accept(packet, packet_in, 11)
        elif(port_on_switch == 11):
          # source is on port 11, send to port 8
          self.accept(packet, packet_in, 8)
        else:
          self.drop(packet, packet_in)

      elif(switch_id == 5):
        #Switch 5
        #Air Gapped Floor
        #Devices can only communicated Amoungst themselves
        print("S5")
        if(port_on_switch == 8):
          # source is sc1
          if(ipv4_packet.dstip == "40.2.5.20"):
            # destination is sc2, send on port 9
            self.accept(packet,packet_in, 9)
          elif(ipv4_packet.dstip == "40.2.7.30"):
            # destination is sc3, send on port 10
            self.accept(packet,packet_in, 10)
          elif(ipv4_packet.dstip == "40.2.7.40"):
            # destination is sc4, send on port 11
            self.accept(packet,packet_in, 11)
          elif(ipv4_packet.dstip == "40.2.7.50"):
            # destination is sc5, send on port 12
            self.accept(packet,packet_in, 12)
          elif(ipv4_packet.dstip == "40.2.7.60"):
            # destination is sc6, send on port 13
            self.accept(packet,packet_in, 13)
          else:
            #else drop the packet
            self.drop(packet, packet_in)

        elif(port_on_switch == 9):
          # source is sc2
          if(ipv4_packet.dstip == "40.2.5.10"):
            # destination is sc1, send on port 8
            self.accept(packet,packet_in, 8)
          elif(ipv4_packet.dstip == "40.2.7.30"):
            # destination is sc3, send on port 10
            self.accept(packet,packet_in, 10)
          elif(ipv4_packet.dstip == "40.2.7.40"):
            # destination is sc4, send on port 11
            self.accept(packet,packet_in, 11)
          elif(ipv4_packet.dstip == "40.2.7.50"):
            # destination is sc5, send on port 12
            self.accept(packet,packet_in, 12)
          elif(ipv4_packet.dstip == "40.2.7.60"):
            # destination is sc6, send on port 13
            self.accept(packet,packet_in, 13)
          else:
            #else drop the packet
            self.drop(packet, packet_in)

        elif(port_on_switch == 10):
          # source is sc3
          if(ipv4_packet.dstip == "40.2.5.20"):
            # destination is sc2, send on port 9
            self.accept(packet,packet_in, 9)
          elif(ipv4_packet.dstip == "40.2.7.10"):
            # destination is sc1, send on port 8
            self.accept(packet,packet_in, 8)
          elif(ipv4_packet.dstip == "40.2.7.40"):
            # destination is sc4, send on port 11
            self.accept(packet,packet_in, 11)
          elif(ipv4_packet.dstip == "40.2.7.50"):
            # destination is sc5, send on port 12
            self.accept(packet,packet_in, 12)
          elif(ipv4_packet.dstip == "40.2.7.60"):
            # destination is sc6, send on port 13
            self.accept(packet,packet_in, 13)
          else:
            #else drop the packet
            self.drop(packet, packet_in)

        elif(port_on_switch == 11):
          # source is sc4
          if(ipv4_packet.dstip == "40.2.5.20"):
            # destination is sc2, send on port 9
            self.accept(packet,packet_in, 9)
          elif(ipv4_packet.dstip == "40.2.7.30"):
            # destination is sc3, send on port 10
            self.accept(packet,packet_in, 10)
          elif(ipv4_packet.dstip == "40.2.7.10"):
            # destination is sc1, send on port 8
            self.accept(packet,packet_in, 8)
          elif(ipv4_packet.dstip == "40.2.7.50"):
            # destination is sc5, send on port 12
            self.accept(packet,packet_in, 12)
          elif(ipv4_packet.dstip == "40.2.7.60"):
            # destination is sc6, send on port 13
            self.accept(packet,packet_in, 13)
          else:
            #else drop the packet
            self.drop(packet, packet_in)

        elif(port_on_switch == 12):
          # source is sc5
          if(ipv4_packet.dstip == "40.2.5.20"):
            # destination is sc2, send on port 9
            self.accept(packet,packet_in, 9)
          elif(ipv4_packet.dstip == "40.2.7.30"):
            # destination is sc3, send on port 10
            self.accept(packet,packet_in, 10)
          elif(ipv4_packet.dstip == "40.2.7.40"):
            # destination is sc4, send on port 11
            self.accept(packet,packet_in, 11)
          elif(ipv4_packet.dstip == "40.2.7.10"):
            # destination is sc1, send on port 8
            self.accept(packet,packet_in, 8)
          elif(ipv4_packet.dstip == "40.2.7.60"):
            # destination is sc6, send on port 13
            self.accept(packet,packet_in, 13)
          else:
            #else drop the packet
            self.drop(packet, packet_in)
        
        elif(port_on_switch == 13):
          # source is sc6
          if(ipv4_packet.dstip == "40.2.5.20"):
            # destination is sc2, send on port 9
            self.accept(packet,packet_in, 9)
          elif(ipv4_packet.dstip == "40.2.7.30"):
            # destination is sc3, send on port 10
            self.accept(packet,packet_in, 10)
          elif(ipv4_packet.dstip == "40.2.7.40"):
            # destination is sc4, send on port 11
            self.accept(packet,packet_in, 11)
          elif(ipv4_packet.dstip == "40.2.7.50"):
            # destination is sc5, send on port 12
            self.accept(packet,packet_in, 12)
          elif(ipv4_packet.dstip == "40.2.7.10"):
            # destination is sc6, send on port 8
            self.accept(packet,packet_in, 8)
          else:
            #else drop the packet
            self.drop(packet, packet_in)
        else:
          #drop the packet
          self.drop(packet,packet_in)

      elif(switch_id == 6): 
        #Switch 6
        # Floor 2 Switch 1
        # Hosts: Host 1
        # Switch: Core Switch
        print("S6")
        if (port_on_switch == 8): 
          # Source is Host1
          if(ipv4_packet.dstip == "10.2.7.20"):
            # destination is host2, send on port 9
            self.accept(packet,packet_in, 9)
          else:
            # otherwise send on port 11
            self.accept(packet, packet_in, 11)
        elif(port_on_switch == 9):
          # Source is Host2
          if(ipv4_packet.dstip == "10.2.7.10"):
            # Destination is host 1, send on port 8
            self.accept(packet, packet_in, 8)
          else:
            # otherwise send on port 11
            self.accept(packet, packet_in, 11)
        elif(port_on_switch == 11):
          #souce is port 11
          if(ipv4_packet.dstip == "10.2.7.20"):
            # destination is host 2, send on port 9
            self.accept(packet,packet_in, 9)
          elif(ipv4_packet.dstip == "10.2.7.10"):
            # Destination is host, send on port 8
            self.accept(packet, packet_in, 8)
          else:
            # else drop the packet
            self.drop(packet, packet_in)
        else:
          #else drop the packet
          self.drop(packet, packet_in)
      else:
        #Flood all non IP packets
        self.accept(packet, packet_in, of.OFPP_FLOOD)


  def accept (self, packet, packet_in, out_port):
    """
    If packet has been identified as good we process and accept it
    """
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 50
    msg.hard_timeout = 50
    msg.buffer_id = packet_in.buffer_id
    msg.actions.append(of.ofp_action_output(port = out_port))
    msg.data = packet_in
    self.connection.send(msg)

  def drop (self, packet, packet_in):
    """
    this funtion drops a packet if it has been marked to be droped
    """
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 50
    msg.hard_timeout = 50
    msg.buffer_id = packet_in.buffer_id
    self.connection.send(msg)


  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
