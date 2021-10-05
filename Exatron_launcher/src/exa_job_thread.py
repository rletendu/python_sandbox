from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QSemaphore, QProcess
from PyQt5.QtWidgets import QApplication
import logging
import time
import sys
from progress import Progress_Window


ExaJobThreadSuiteSemaphore = QSemaphore(1)

class ExaJobSignals(QObject):
	"""
	User defined signals to connect independent measure Thread to gui
	"""
	start_suite = pyqtSignal(list,list,str, list)
	abort_suite = pyqtSignal()
	pause_suite = pyqtSignal()
	notify_progress = pyqtSignal(str, int, int)

	all_done = pyqtSignal()


class ExaJobThread(QObject):
	"""
	Thread that will perform the bench execution on Exatron in Background
	"""
	def __init__(self, exatron, sig, demo = False, temp_accuracy = 2.0, temp_soak=30):
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
		self.progress = Progress_Window("msg")

	@pyqtSlot(list, list, str, list)
	def run(self, temp_list, part_list, cmd, temp_offset):
		self.part_list = part_list
		self.temp_list = temp_list
		self.cmd = cmd
		self.abort_request = False
		self.suspended = False
		self.temp_offset_list = temp_offset
		for part in self.part_list:
			if self.abort_request:
				break
			temperature = self.temp_list[0]
			self.sig.notify_progress.emit('Loading {} part'.format(part), part, temperature)
			print('Loading next part : {}'.format(part))
			if not self.exatron.load_next_part():
				print("Error loading next part")
				break
			for temperature in self.temp_list:
				self.sig.notify_progress.emit('', part, temperature)
				print('Set Working temperature to : {}'.format(temperature))
				temp_offset = temperature
				for t in self.temp_offset_list:
					if t[0] == temperature:
						temp_offset = t[1]
						print("Using {} as offset temperature for {}".format(temp_offset, temperature))
				self.exatron.set_temperature(temp_offset)
				while True:
					t = self.exatron.get_temperature()
					self.sig.notify_progress.emit('Temperature is {} versus {}'.format(t,temp_offset), part, temperature)
					if abs( t - temp_offset ) < self.temp_accuracy:
						break
					if self.abort_request:
						break
					time.sleep(5)
				if self.abort_request:
					break
				self.sig.notify_progress.emit("Waiting {}s soak time...".format(self.temp_soak), part, temperature)
				end_soak_time = time.time() + self.temp_soak
				while time.time() < end_soak_time:
					if self.abort_request:
						break
					time.sleep(5)
					remaining_soak = int(end_soak_time-time.time())
					self.sig.notify_progress.emit("Waiting {}s soak time...".format(remaining_soak), part, temperature)
				if self.abort_request:
					break
				self.log.info("Running Bench with part {} at {}°C".format(part, temperature))
				exec_cmd = self.cmd.replace('{temperature}', str(temperature)).replace('{part}',str(part))
				self.sig.notify_progress.emit("Running {}".format(exec_cmd), part, temperature)
				print("Starting bench {}".format(exec_cmd))
				self.p.start(exec_cmd)
				self.p.waitForFinished(msecs=-1)
				self.log.info("Bench Done")
			self.exatron.unload_part()
			if self.abort_request:
				break
		self.log.info("Setting temp to room before EOL")
		self.exatron.set_temperature(25)
		self.exatron.end_of_lot()
		self.sig.notify_progress.emit('End of Lot', part, temperature)
		self.sig.all_done.emit()
		print("--- LOT COMPLETE ---")
		time.sleep(2)


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
		self.p.kill()


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