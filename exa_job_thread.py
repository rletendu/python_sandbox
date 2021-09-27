from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QSemaphore, QProcess
import logging
import time

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
	def __init__(self, exatron, sig, demo = False, on_error=None):
		QObject.__init__(self)
		self.log = logging.getLogger(__name__)
		self.log.debug("ExaJobThread instance created")
		self.sig = sig
		self.abort_request = False
		self.suspended = False
		self.demo = demo
		self.exatron = exatron
	

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
			for temperature in self.temp_list:
				print('Set Working temperature to : {}'.format(temperature))
				self.log.info("Running Bench with part {} at {}°C".format(part, temperature))
				exec = self.cmd.replace('{temperature}', str(temperature)).replace('{part}',str(part))
				self.sig.notify_progress.emit(exec, part, temperature)
				print(exec)
				self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
				#self.p.start("python3", ['dummy_script.py'])
				self.p.start("cmd")
				time.sleep(0.1)
			if self.abort_request:
				break



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