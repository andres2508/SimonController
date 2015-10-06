#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: UDP Synchronization Power bladeRF
# Author: lvbernal
# Generated: Tue Sep  2 17:40:49 2014
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import SimpleXMLRPCServer
import math
import osmosdr
import threading
import time
import sys

class i2t_udp_synchronization_power_bladeRF(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "UDP Synchronization Power bladeRF")

        ##################################################
        # Variables
        ##################################################
        self.fft_size = fft_size = 1024
        self.samp_rate = samp_rate =1100000
        self.fft_window = fft_window = window.blackmanharris(fft_size)
        self.power = power = sum(x*x for x in fft_window)
        self.center_freq = center_freq = 870e6
        self.bandwidth = bandwidth = samp_rate
        self.stop_freq = stop_freq = center_freq+(bandwidth/2)
        self.start_freq = start_freq = center_freq-(bandwidth/2)
        self.simon_port = simon_port = 65123
        self.simon_ip = simon_ip = '192.168.160.95'
        self.server_port = server_port = 65234
        self.server_ip = server_ip = '192.168.160.120'
        self.n = n = max(1, int(samp_rate/fft_size/15L))
        self.k = k = -20*math.log10(fft_size)-10*math.log10(power/fft_size)-20*math.log10(2.0/2)
        self.device = device = 'bladerf,fpga=/home/pi/bladeRF/pre-built/hostedx115.rbf'

        ##################################################
        # Blocks
        ##################################################
#        self.xmlrpc_server_0 = SimpleXMLRPCServer.SimpleXMLRPCServer((simon_ip, simon_port), allow_none=True)
#        self.xmlrpc_server_0.register_instance(self)
#        threading.Thread(target=self.xmlrpc_server_0.serve_forever).start()
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff(1.0, fft_size)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + device )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(center_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(bandwidth, 0)
          
        self.fft_vxx_0 = fft.fft_vcc(fft_size, True, (fft_window), True, 1)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, fft_size)
        self.blocks_vector_insert_x_0 = blocks.vector_insert_f((309448288, ), fft_size+1, 0)
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_float*1, server_ip, server_port, 1472, True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_size)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(20, fft_size, k)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*fft_size, n)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1024)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.osmosdr_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_vector_insert_x_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.single_pole_iir_filter_xx_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.blocks_vector_insert_x_0, 0), (self.blocks_udp_sink_0, 0))
		
# QT sink close method reimplementation
    def prueba(self):
	return "si esta creando blade"
    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size
        self.set_fft_window(window.blackmanharris(self.fft_size))
        self.set_n(max(1, int(self.samp_rate/self.fft_size/15L)))
        self.set_k(-20*math.log10(self.fft_size)-10*math.log10(self.power/self.fft_size)-20*math.log10(2.0/2))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_n(max(1, int(self.samp_rate/self.fft_size/15L)))
        self.set_bandwidth(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_fft_window(self):
        return self.fft_window

    def set_fft_window(self, fft_window):
        self.fft_window = fft_window
        self.set_power(sum(x*x for x in self.fft_window))

    def get_power(self):
        return self.power

    def set_power(self, power):
        self.power = power
        self.set_k(-20*math.log10(self.fft_size)-10*math.log10(self.power/self.fft_size)-20*math.log10(2.0/2))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.set_stop_freq(self.center_freq+(self.bandwidth/2))
        self.set_start_freq(self.center_freq-(self.bandwidth/2))
        self.osmosdr_source_0.set_center_freq(self.center_freq, 0)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.set_stop_freq(self.center_freq+(self.bandwidth/2))
        self.set_start_freq(self.center_freq-(self.bandwidth/2))
        self.osmosdr_source_0.set_bandwidth(self.bandwidth, 0)

    def get_stop_freq(self):
        return self.stop_freq

    def set_stop_freq(self, stop_freq):
        self.stop_freq = stop_freq

    def get_start_freq(self):
        return self.start_freq

    def set_start_freq(self, start_freq):
        self.start_freq = start_freq

    def get_simon_port(self):
        return self.simon_port

    def set_simon_port(self, simon_port):
        self.simon_port = simon_port

    def get_simon_ip(self):
        return self.simon_ip

    def set_simon_ip(self, simon_ip):
        self.simon_ip = simon_ip

    def get_server_port(self):
        return self.server_port

    def set_server_port(self, server_port):
        self.server_port = server_port

    def get_server_ip(self):
        return self.server_ip

    def set_server_ip(self, server_ip):
        self.server_ip = server_ip

    def get_n(self):
        return self.n

    def set_n(self, n):
        self.n = n
        self.blocks_keep_one_in_n_0.set_n(self.n)

    def get_k(self):
        return self.k

    def set_k(self, k):
        self.k = k

    def get_device(self):
        return self.device

    def set_device(self, device):
        self.device = device

    def stop_udp(self):
	blocks.udp_sink_sptr.disconnect(self.blocks_udp_sink_0)
        

if __name__ == '__main__':
   
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = i2t_udp_synchronization_power_bladeRF()
    tb.start()
    
    tiempo = sys.stdin.readline()
    t = float(tiempo)
    counter = 0
    continuar = True

    while counter < t and continuar:
	time.sleep(1)
	counter = counter + 1
	sys.stdout.write("Avance cadena "+str(counter))
	cadena = sys.stdin.readline()
	
	if cadena == "Stop\n":
		continuar = False
	
	else:
		sys.stdout.write("Blade ACK" + "\n")
		sys.stdout.flush()
#	try:
#		cadena = sys.stdout.readline().strip()
#		sys.stdin.write("Script AC")
#	except IOError:
#		pass

    sys.stdout.write("Finish" + "\n")
    sys.stdout.flush()
    tb.stop_udp()
    tb.stop()
