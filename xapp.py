import xapp_sdk as ric
import time
import os
import pdb


####################
#### MAC INDICATION CALLBACK
####################

#  MACCallback class is defined and derived from C++ class mac_cb
class MACCallback(ric.mac_cb):
    # Define Python class 'constructor'
    def __init__(self):
        # Call C++ base class constructor
        ric.mac_cb.__init__(self)
    # Override C++ method: virtual void handle(swig_mac_ind_msg_t a) = 0;
    def handle(self, ind):
        # Print swig_mac_ind_msg_t
        if len(ind.ue_stats) > 0:
            for id, ue in enumerate(ind.ue_stats):
                t_now = time.time_ns() / 1000.0
                t_mac = ind.tstamp / 1.0
                t_diff = t_now - t_mac
                print('MAC Indication tstamp = ' + str(t_mac) + ' latency = ' + str(t_diff) + ' μs')
                print('UE ID: ' + str(id))
                print('DL BER: ' + str(ue.dl_bler))
                print('UL BER: ' + str(ue.ul_bler))
                print('BSR: ' + str(ue.bsr))  # Example metric
                print('WB CQI: ' + str(ue.wb_cqi))  # Example metric
                print('DL SCHED RB: ' + str(ue.dl_sched_rb))
                print('UL SCHED RB: ' + str(ue.ul_sched_rb))
                print('PUSCH SNR: ' + str(ue.pusch_snr))
                print('PUCCH SNR: ' + str(ue.pucch_snr))
                print('DL AGGR PRB: ' + str(ue.dl_aggr_prb))
                print('UL AGGR PRB: ' + str(ue.ul_aggr_prb))
                print('DL MCS1: ' + str(ue.dl_mcs1))
                print('UL MCS2: ' + str(ue.ul_mcs2))
                print('---------------------------------------')
                
####################
#### RLC INDICATION CALLBACK
####################

class RLCCallback(ric.rlc_cb):
    # Define Python class 'constructor'
    def __init__(self):
        # Call C++ base class constructor
        ric.rlc_cb.__init__(self)
    # Override C++ method: virtual void handle(swig_rlc_ind_msg_t a) = 0;
    def handle(self, ind):
        # Print swig_rlc_ind_msg_t
        if len(ind.rb_stats) > 0:
            t_now = time.time_ns() / 1000.0
            t_rlc = ind.tstamp / 1.0
            t_diff = t_now - t_rlc
            print('RLC Indication tstamp = ' + str(ind.tstamp) + ' latency = ' + str(t_diff) + ' μs')
            for id, rb in enumerate(ind.rb_stats):
                print('UE ID: ' + str(id))
                #print('RLC RNTI: ' + str(rb.rnti))
                print('RLC PDU TX retransmitted packets: ' + str(rb.txpdu_retx_pkts))  # Example metric
                print('RLC PDU TX dropped packets: ' + str(rb.txpdu_dd_pkts))  # Example metric

####################
#### PDCP INDICATION CALLBACK
####################

class PDCPCallback(ric.pdcp_cb):
    # Define Python class 'constructor'
    def __init__(self):
        # Call C++ base class constructor
        ric.pdcp_cb.__init__(self)
   # Override C++ method: virtual void handle(swig_pdcp_ind_msg_t a) = 0;
    def handle(self, ind):
        # Print swig_pdcp_ind_msg_t
        if len(ind.rb_stats) > 0:
            t_now = time.time_ns() / 1000.0
            t_pdcp = ind.tstamp / 1.0
            t_diff = t_now - t_pdcp
            print('PDCP Indication tstamp = ' + str(ind.tstamp) + ' latency = ' + str(t_diff) + ' μs')
            for id, rb in enumerate(ind.rb_stats):
                print('UE ID: ' + str(id))
                #print('PDCP RNTI: ' + str(rb.rnti))
                print('PDCP total PDU TX in bytes: ' + str(rb.txpdu_bytes))  # Example metric
                print('PDCP total PDU RX in bytes: ' + str(rb.rxpdu_bytes))  # Example metric

####################
#### GTP INDICATION CALLBACK
####################

# Create a callback for GTP which derived it from C++ class gtp_cb
class GTPCallback(ric.gtp_cb):
    def __init__(self):
        # Inherit C++ gtp_cb class
        ric.gtp_cb.__init__(self)
    # Create an override C++ method 
    def handle(self, ind):
        if len(ind.gtp_stats) > 0:
            t_now = time.time_ns() / 1000.0
            t_gtp = ind.tstamp / 1.0
            t_diff = t_now - t_gtp
            print('GTP Indication tstamp = ' + str(ind.tstamp) + ' diff = ' + str(t_diff) + ' μs')
            for id, stat in enumerate(ind.gtp_stats):
                print('UE ID: ' + str(id))
                print('GTP Tunnel ID: ' + str(stat.tunnel_id))
                print('GTP QoS flow indicator: ' + str(stat.qfi))  # Example metric
                print('GTP gNB tunnel identifier: ' + str(stat.teidgnb))  # Example metric



####################
####  GENERAL 
####################

ric.init()

conn = ric.conn_e2_nodes()
assert(len(conn) > 0)
for i in range(0, len(conn)):
    print("Global E2 Node [" + str(i) + "]: PLMN MCC = " + str(conn[i].id.plmn.mcc))
    print("Global E2 Node [" + str(i) + "]: PLMN MNC = " + str(conn[i].id.plmn.mnc))

####################
#### MAC INDICATION
####################

mac_hndlr = []
for i in range(0, len(conn)):
    mac_cb = MACCallback()
    hndlr = ric.report_mac_sm(conn[i].id, ric.Interval_ms_10, mac_cb)
    mac_hndlr.append(hndlr)     
    time.sleep(1)

####################
#### RLC INDICATION
####################

rlc_hndlr = []
for i in range(0, len(conn)):
    rlc_cb = RLCCallback()
    hndlr = ric.report_rlc_sm(conn[i].id, ric.Interval_ms_10, rlc_cb)
    rlc_hndlr.append(hndlr) 
    time.sleep(1)

####################
#### PDCP INDICATION
####################

pdcp_hndlr = []
for i in range(0, len(conn)):
    pdcp_cb = PDCPCallback()
    hndlr = ric.report_pdcp_sm(conn[i].id, ric.Interval_ms_10, pdcp_cb)
    pdcp_hndlr.append(hndlr) 
    time.sleep(1)

####################
#### GTP INDICATION
####################

gtp_hndlr = []
for i in range(0, len(conn)):
    gtp_cb = GTPCallback()
    hndlr = ric.report_gtp_sm(conn[i].id, ric.Interval_ms_10, gtp_cb)
    gtp_hndlr.append(hndlr)
    time.sleep(1)

time.sleep(10)

### End

for i in range(0, len(mac_hndlr)):
    ric.rm_report_mac_sm(mac_hndlr[i])

for i in range(0, len(rlc_hndlr)):
    ric.rm_report_rlc_sm(rlc_hndlr[i])

for i in range(0, len(pdcp_hndlr)):
    ric.rm_report_pdcp_sm(pdcp_hndlr[i])

for i in range(0, len(gtp_hndlr)):
    ric.rm_report_gtp_sm(gtp_hndlr[i])




# Avoid deadlock. ToDo revise architecture 
while ric.try_stop == 0:
    time.sleep(1)

print("Test finished")
