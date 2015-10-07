import xmlrpclib
import socket
import struct
import time
import sys
import argparse
import json

# from gnuradio import eng_notation
# from gnuradio.eng_option import eng_option
from optparse import OptionParser
from array import array


class occupation_control():
    def __init__(self):

        self.id_measure = 0  # ID_medicion
        self.min_freq = 0  # min freq medicion total
        self.max_freq = 0  # max freq medicion total
        self.device_span = 0  # span maximo del dispositivo
        self.service_start_freq = 0  # freq inicial de un servicio
        self.service_stop_freq = 0  # freq final de un servicio
        self.bandwidth_service = 0  # ancho de banda del servicio
        self.service_canalization = 0  # canalizacion del servicio
        self.channels_number = 0  # cantidad de canales del servicio
        self.measure_counter = 0  # cantidad de mediciones para un servicio
        self.measure_span = 0  # span de una medicion en curso
        self.measure_start_freq = 0  # frecuencia inicial de medicion en curso
        self.measure_center_freq = 0  # frecuencia central de medicion en curso
        self.measure_stop_freq = 0  # frecuencia final de medicion en curso
        self.trace = 0  # traza recibida del SIMON
        self.occupation_channels = 0  # lista de ocupacion de canales medidos
        self.noise_floor = 0  # piso de ruido
        self.fft_size = 0  # numero de coeficientes de FFT
        self.average = 0
        self.initial_time = 0
        self.final_time = 0

        min_freq = float(sys.stdin.readline())
        max_freq = float(sys.stdin.readline())
        canalization = float(sys.stdin.readline())
        span = float(sys.stdin.readline())

        usage = "usage: %prog [options] min_freq max_freq span"
        parser = argparse.ArgumentParser(description='RNI parameters')
        parser.add_argument('-i', '--id_measure', type=float, default=60e3,
                            help="minimun frequency in Hz [default=%default]")
        parser.add_argument('-n', '--min_freq', type=float, default=min_freq,
                            help="minimun frequency in Hz [default=%default]")
        parser.add_argument('-x', '--max_freq', type=float, default=max_freq, help="maximun frequency in Hz")
        parser.add_argument('-s', '--service_start_freq', type=float, default=88e6,
                            help="service start frequency in Hz")
        parser.add_argument('-f', '--service_stop_freq', type=float, default=108e6, help="service stop frequency in Hz")
        parser.add_argument('-c', '--canalization', type=float, default=canalization, help="service canalization")
        parser.add_argument('-p', '--span', type=float, default=span, help="span in Hz")
        parser.add_argument('-a', '--fft_size', type=float, default=1024, help="FFT beans")
        parser.add_argument('-v', '--average', type=float, default=10, help="span in Hz")

        args = parser.parse_args()

        print "inicia"
        self.initial_time = time.time()
        self.data_validation(args)
        self.service_measurement_configuration()
        self.get_proxy()
        open_socket_usrp('127.0.0.1', 65234)
        self.change_usrp_parameters()
        # self.proxy.set_center_freq(self.center_freq)
        # self.proxy.set_samp_rate(self.span)
        # self.proxy.set_canalization(self.canalization)
        time.sleep(2)
        self.measures = 0
        while self.device_span != 0 and self.measures < self.measure_counter:
            print "entra a while"
            self.trace = self.receive_signal()
            self.occupation_channels = self.threshold_detector()
            self.measures += 1
            self.send_measure()
            self.measurement_configuration()
            time.sleep(2)

    def data_validation(self, args):
        if type(args.min_freq) not in (int, float, long):
            raise TypeError, "Mininum frequency has to be a number"
        elif type(args.min_freq) not in (int, float, long):
            raise TypeError, "Mininum frequency has to be a number"
        elif type(args.span) not in (int, float, long):
            raise TypeError, "Mininum frequency has to be a number"
        elif type(args.canalization) not in (int, float, long):
            raise TypeError, "Mininum frequency has to be a number"
        else:
            self.min_freq = args.min_freq
            self.max_freq = args.max_freq
            self.service_start_freq = args.service_start_freq
            self.service_stop_freq = args.service_stop_freq
            self.device_span = args.span
            self.canalization = args.canalization
            self.average = args.average
            self.fft_size = args.fft_size

    # Determinar la cantidad de mediciones que se deben realizar para un servicio y configurar la primera medicion del servicio
    def service_measurement_configuration(self):
        self.service_bandwidth = self.service_stop_freq - self.service_start_freq
        if self.device_span < self.service_bandwidth:
            self.measure_span = self.device_span
        else:
            self.measure_span = self.service_bandwidth
        self.measure_start_freq = self.service_start_freq
        self.measure_center_freq = self.measure_start_freq + (self.measure_span / 2)
        self.measure_stop_freq = self.service_start_freq + self.measure_span
        self.measure_counter = self.service_bandwidth / self.measure_span
        self.channels_number = self.measure_span / self.canalization;
        print self.measure_counter
        print self.channels_number

    # Configurar los parametros de la siguiente medicion:
    def measurement_configuration(self):
        self.measure_start_freq = self.measure_start_freq + self.measure_span
        temp_stop_freq = self.measure_stop_freq + self.measure_span
        if temp_stop_freq > self.service_stop_freq:
            temp_stop_freq = self.service_stop_freq
        self.measure_stop_freq = temp_stop_freq
        self.measure_span = self.measure_stop_freq - self.measure_start_freq
        self.measure_center_freq = self.measure_start_freq + (self.measure_span / 2)
        self.channels_number = self.measure_span / self.canalization

    def set_parameters(self):
        if self.min_freq > self.max_freq:
            self.min_freq, self.max_freq = self.max_freq, self.min_freq  # swap them
        self.start_freq = self.min_freq
        self.stop_freq = self.start_freq + self.span
        if self.stop_freq > self.max_freq:
            self.stop_freq = self.max_freq
            self.span = self.stop_freq - self.start_freq
        self.center_freq = self.start_freq + (self.span / 2)

    # Enviar parametros a usrp
    def change_usrp_parameters(self):
        self.proxy.set_center_freq(self.measure_center_freq)
        self.proxy.set_samp_rate(self.measure_span)

    def next_step(self):
        temp_stop_freq = self.stop_freq + self.span
        if temp_stop_freq > self.max_freq:
            temp_stop_freq = self.max_freq
        temp_start_freq = self.start_freq + self.span
        self.span = temp_stop_freq - temp_start_freq
        # print self.span
        self.start_freq = temp_start_freq
        self.center_freq = self.start_freq + (self.span / 2)
        self.stop_freq = temp_stop_freq
        self.proxy.set_center_freq(self.center_freq)
        self.proxy.set_samp_rate(self.span)

    # Recibe la traza enviada por el usrp
    def receive_signal(self):
        float_values = array("f")
        size = 0
        channels = 0
        i = 0
        items = 0
        temp_value = 0
        for x in range(0, 1024):
            float_values.insert(x, 0)
        for j in range(0, self.average):
            index = 0
            size = 0
            while size < 1024:
                data, add = socket_usrp.recvfrom(2048)
                size += len(data) / 4
                if (size == 368 and len(data) == 1472) or (size == 736 and len(data) == 1472) or (
                        size == 1024 and len(data) == 1152):
                    i = 0
                    while i < len(data):
                        byte_array = data[i:i + 4]
                        i += 4
                        value = struct.unpack('f', byte_array)[0]
                        temp_value = float_values[index] + value
                        float_values[index] = temp_value
                        index += 1
                else:
                    i = 0
                    size = 0
                    float_values = []
                    index = 0
                # j = 0
                # print index
                # print j
        for x in range(0, len(float_values)):
            float_values[x] = float_values[x] / self.average
        return float_values

    def threshold_detector(self):
        channels_list = []
        count = 0
        noise_trace = sorted(self.trace)
        print noise_trace
        for i in range(0, len(noise_trace) / 4):
            self.noise_floor = self.noise_floor + noise_trace[i]
        print self.noise_floor
        self.noise_floor = self.noise_floor / (len(noise_trace) / 4)
        # print self.noise_floor
        fft_per_channel = int(self.fft_size // self.channels_number)  # Coeficientes de FFT para cada canal
        # print self.fft_size
        # VALORES QUE SUPERAN EL PISO DE RUIDO*/
        while count < self.channels_number:
            # print count
            fft_count = 0
            fft_init = count * fft_per_channel
            fft_end = (count + 1) * fft_per_channel
            j = 0
            # print fft_init
            # print fft_end
            # print (fft_init + fft_per_channel)
            for x in range(fft_init, fft_end):
                if (self.trace[x] > self.noise_floor):
                    fft_count = fft_count + 1

            if (fft_count >= fft_per_channel * 0.8):
                channels_list.insert(count, 5.0)
            # print channels_list[count]
            else:
                channels_list.insert(count, 1.0)
            # print channels_list[count]
            count = count + 1
        return channels_list

    def send_measure(self):
        self.final_time = time.time()
        duration = self.final_time - self.initial_time
        print duration
        data = {}
        data['name_measurement'] = "occ"
        data['scheduled_date'] = self.final_time
        data['umbral'] = self.noise_floor
        data['samples_trace'] = self.average
        data['duration'] = duration
        data['id_band'] = "id_band"
        data['id_measure'] = self.measures
        data['start_freq'] = self.measure_start_freq
        data['stop_freq'] = self.measure_stop_freq
        data['sample_trace'] = self.occupation_channels
        data['ref_level'] = 5
        data['sweep_time'] = 1000
        data['res_bwitdh'] = 14
        data['video_bwitdh'] = 15
        data['power_att'] = 10
        data['scale_pdif'] = 10
        data['span'] = 5
        data['location'] = {"latitude": 0, "longitude": 0, "altitude": 0}

        json_data = json.dumps(data)
        print "send"
        print json_data

    def get_proxy(self):
        self.proxy = xmlrpclib.ServerProxy("http://127.0.0.1:65123/")


def open_socket_usrp(usrp_ip_address, port):
    global socket_usrp
    socket_usrp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_usrp.bind((usrp_ip_address, port))
    print 'socket'

    def inicio():
        get_proxy()
        open_socket_usrp('127.0.0.1', 65234)
        # proxy.get_center_freq()
        # print self.center_freq
        print 'center_freq_sc'
        # proxy.set_center_freq(self.center_freq)
        # proxy.set_samp_rate(self.span)
        time.sleep(3)
        while True:
            trace = receive_signal()
            # print proxy.get_center_freq()
            print 'freq'
            print trace[0]
            print self.span
            self.center_freq += self.span
            # proxy.set_center_freq(self.center_freq)
            time.sleep(3)

        # for x in range(0,10):
        #	print ("Set center_freq: %d", proxy.set_center_freq(98000000+x))
        #	print ("Get center_freq: %d", proxy.get_center_freq())


if __name__ == '__main__':
    control = occupation_control()
    control.start()
