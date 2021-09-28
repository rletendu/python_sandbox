from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QSemaphore, QProcess
import logging
import time
import sys

class ExaJobSignals(QObject):
	"""
	User defined signals to connect independent measure Thread to gui
	"""
	start_suite = pyqtSignal(list,list,str)
	abort_suite = pyqtSignal()
	pause_suite = pyqtSignal()
	notify_progress = pyqtSignal(str, int, int)


class ExaJobThread(QObject):
	"""
	Thread that will perform the bench execution on Exatron in Background
	"""
	def __init__(self, exatron, sig, demo = False, temp_accuracy = 2.0, temp_soak=30,on_error=None):
		QObject.__init__(self)
		self.log = logging.getLogger(__name__)
		self.log.debug("ExaJobThread instance created")
		self.sig = sig
		self.abort_request = False
		self.suspended = False
		self.demo = demo
		self.exatron = exatron
		self.p = QProcess()
		self.p.finished.connect(self.process_finished)
		self.p.readyReadStandardOutput.connect(self.handle_stdout)
		self.part_list = None
		self.temp_list = None
		self.cmd = None
		self.temp_accuracy = temp_accuracy
		self.temp_soak = temp_soak

	@pyqtSlot(list, list, str)
	def run(self, temp_list, part_list, cmd):
		"""
		Main Function that performs all tests measures
		"""
		self.part_list = part_list
		self.temp_list = temp_list
		self.cmd = cmd
		self.abort_request = False
		self.suspended = False
		for part in self.part_list:
			print('Working with next part : {}'.format(part))
			self.exatron.load_next_part()
			for temperature in self.temp_list:
				self.sig.notify_progress.emit('', part, temperature)
				print('Set Working temperature to : {}'.format(temperature))
				self.exatron.set_temperature(temperature)
				while True:
					t = self.exatron.get_temperature()
					if abs( t - temperature ) < self.accuracy:

						break
					time.sleep(2)
				print("Waiting {}s soak time...".format(self.temp_soak))
				time.sleep(self.temp_soak)
				self.log.info("Running Bench with part {} at {}°C".format(part, temperature))
				exec_cmd = self.cmd.replace('{temperature}', str(temperature)).replace('{part}',str(part))
				print(exec_cmd)
				self.p.start(exec_cmd)
				self.p.waitForFinished(msecs=-1)
				self.log.info("Done")

			if self.abort_request:
				break
			self.exatron.load_next_part()

	@pyqtSlot(int)
	def process_finished(self, rcode):
		self.log.info("Process completed with {}".format(rcode))

	def handle_stdout(self):
		d = bytes(self.p.readAllStandardOutput()).decode()
		print(d)
		sys.stdout.flush()

	@pyqtSlot()
	def abort(self):
		"""
		Receiver slot for abort push button
		"""
		self.log.debug("Abort Measure Thread Event Received")
		print("Abort Request")
		self.abort_request = True


	@pyqtSlot()
	def pause(self):
		"""
		Receiver slot for pause push button
		"""
		self.log.debug("Pause Measure Thread Event Received")
		if self.suspended:
			self.suspended = False
			print("Measures Thread Resumed")
		else:
			self.suspended = True
			print("Measures Thread Paused")