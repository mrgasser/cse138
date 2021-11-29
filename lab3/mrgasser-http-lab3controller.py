# Lab 3 Skeleton
#
# Based on of_tutorial by James McCauley

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Firewall (object):
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

  def do_firewall (self, packet, packet_in):
    # The code in here will be executed for every packet.
    print ("doing firewall")
    tcp_packet = packet.find("tcp")
    arp_packet = packet.find("arp")
    icmp_packet = packet.find("icmp")
    ipv4_packet = packet.find("ipv4")

    if arp_packet != None: # accept any arp packets
      self.accept(packet, packet_in)

    if ipv4_packet != None: #check for ipv4
      if icmp_packet != None: # if ipv4 and icmp accept it
        self.accept(packet, packet_in)
      elif tcp_packet != None: #if ipv4 and tcp, only accept from specific ips
        if ((ipv4_packet.srcip == "20.1.1.1" and ipv4_packet.dstip == "20.1.1.10") or (ipv4_packet.srcip == "20.1.1.2" and ipv4_packet.dstip == "20.1.1.11")):
          self.accept(packet, packet_in)
        else: #otherwise drop the packet
          self.drop(packet, packet_in)
      else:
        self.drop(packet, packet_in)
    else:
      self.drop(packet, packet_in)

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_firewall(packet, packet_in)
  
  def accept (self, packet, packet_in):
    """
    If packet has been identified as good we process and accept it
    """
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 50
    msg.hard_timeout = 50
    msg.buffer_id = packet_in.buffer_id
    msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
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

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Firewall(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
