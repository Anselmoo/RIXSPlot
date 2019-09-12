#!/usr/bin/env python

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import os
import matplotlib.pylab as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

import numpy as np
from scipy.io import loadmat

# Import Windows
from Interface import *
# Import own libraries & classes
from RIXSPlot import *


# noinspection PyAttributeOutsideInit
class MainWindow(QtWidgets.QWidget, main_window.Ui_Form):
	def __init__(self, parent=None):
		QtWidgets.QWidget.__init__(self, parent)
		self.setupUi(self)
		self.RIXSPlot.clicked.connect(self.handleButton)
		self.openFILE.clicked.connect(self.getfiles)
		"""Test"""
		self.pathway = os.path.abspath("./")
		self.check = {'file': False, 'type': 'RIXS', 'data': np.zeros((3, 3)), 'filename': '.', 'pathway': self.pathway,
		              'mode': 0, 'cbar': 'linear', 'cont_n': 0, 'cont': False, 'syle': 'jet', 'aver_x': 0, 'aver_y': 0,
		              'grid': 500, 'shift_x': 0, 'shift_y': 0, 'x0': 0, 'x1': 0, 'y0': 0, 'y1': 0, 'inter': 0,
		              'dir': '/Users/'}

	def handleButton(self):
		if self.check['file']:
			""" Reading all intial inputs"""
			self.check['grid'] = int(self.gridPOINTS.value())
			self.check['mode'] = int(self.kindRIXS.currentIndex())
			self.check['filename'] = str(self.fileNAME.text())
			self.check['cbar'] = str(self.kindCONT.currentText())
			self.check['cont'] = bool(self.checkContour.isChecked())
			self.check['cont_n'] = int(self.contPOINTS.value())
			self.check['style'] = str(self.kindIMG.currentText())
			self.check['aver_x'], self.check['aver_y'] = float(self.inc_AVSpinBox.value()), float(
				self.em_AVSpinBox.value())
			self.check['shift_x'], self.check['shift_y'] = float(self.enSHIFT_X.value()), float(self.enSHIFT_Y.value())
			self.check['inter'] = int(self.kindINTER.currentIndex())
			self.check['x0'], self.check['x1'] = float(self.en_x0.value()), float(self.en_x1.value())
			self.check['y0'], self.check['y1'] = float(self.en_y0.value()), float(self.en_y1.value())
			# Starting first the interplation class
			result = inp.interpolation(self.check)
			data = result.guess()
			# Link to the matplotlib class
			self.window1 = RIXS(data, self.check)
			self.window1.show()
		else:
			self.window2 = w_message(self)
			self.window2.show()

	def getfiles(self):

		dlg = QFileDialog()
		dlg.setFileMode(QFileDialog.AnyFile)
		dlg.setNameFilter("Text files (*.out *.dat *.txt *.mat)")
		# filenames = QtCore.QStringList()
		if dlg.exec_():
			filenames = dlg.selectedFiles()
			# file = os.path.join(os.getcwd(), os.listdir(os.getcwd())[0])
			self.check['pathway'] = os.path.dirname(str(filenames[0]))
			# not sure if needed
			# filename = filenames[0].split('.')
			if 'el_inel' in filenames[0]:
				try:
					with open(filenames[0], 'r') as f:
						self.check['data'] = np.genfromtxt(f, dtype=float)
						self.window3 = o_loading(self)
						self.window3.show()
						self.check['file'], self.check['type'] = True, 'ORCA'

				except ValueError:
					# Error Handling is not working proper
					"""msg = QMessageBox()
					msg.setIcon(QMessageB

					msg.setText("This is a message box")
					msg.setInformativeText("This is additional information")
					msg.setWindowTitle("MessageBox demo")
					msg.setDetailedText("The details are as follows:")
					msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
					msg.buttonClicked.connect(msgbtn)"""
					pass
			elif '.mat' in filenames[0]:
				try:
					with open(filenames[0], 'r') as f:
						data = loadmat(f)
						try:
							xx, yy, zz = np.nan_to_num(data['XX']), np.nan_to_num(data['YY']), np.nan_to_num(
								data['MDfci'])
						except ValueError:
							try:
								xx, yy, zz = np.nan_to_num(data['XX']), np.nan_to_num(data['ZZ']), np.nan_to_num(
									data['MDfci'])
							except ValueError:
								pass
						data = np.zeros((np.prod(np.shape(zz), dtype=int), 3), dtype=float)
						count = 0
						for i in range(np.shape(xx)[0]):
							for j in range(np.shape(yy)[1]):
								data[count, 0] = xx[i, j]
								data[count, 1] = yy[i, j]
								data[count, 2] = zz[i, j]
								count += 1

						self.check['data'] = data
						self.window3 = c_loading(self)
						self.window3.show()
						self.check['file'], self.check['type'] = True, 'CTM'
				except ValueError:
					pass
			# elif '.pol' in filename[0]:
			#    with open(filenames[0],'r') as f:

			else:
				try:
					with open(filenames[0], 'r') as f:
						self.check['data'] = np.nan_to_num(np.genfromtxt(f, dtype=float))
						self.window4 = r_loading(self)
						self.window4.show()
						self.check['file'], self.check['type'] = True, 'RIXS'
				# print self.check['data']
				except ValueError:
					pass


class RIXS(QtWidgets.QWidget, subwindow_RIXS.Ui_RIXS):
	def __init__(self, data, check, parent=None):
		QtWidgets.QWidget.__init__(self, parent)
		self.setupUi(self)
		self.amp = data['RIXS']
		self.x, self.y = data['XAS'], data['XES']
		self.aver_x, self.aver_y = check['aver_x'], check['aver_y']
		self.filename = check['filename']
		self.pathway = check['pathway']
		self.mode = check['mode']
		self.stretch = check['cbar']
		self.cont_t = check['cont']
		self.cont_n = check['cont_n']
		self.style = check['style']
		try:
			self.plot_contour()
		except ValueError:
			pass

	# init figure and canvas
	def plot_contour(self):
		try:  # close previous test if open
			plt.close(1)
		except Exception:
			pass
		self.fig = plt.figure(1, figsize=(6, 6))
		# init nav toolbar
		self.canvas = FigureCanvas(self.fig)
		self.toolbar = NavigationToolbar(self.canvas, self)
		# Add plot button
		# discards the old graph
		# plot data
		self.ax1 = plt.subplot(221)
		self.ax2 = plt.subplot(223)
		self.ax3 = plt.subplot(122)
		self.ax2.set_xlabel('Incident Energy (eV)')
		self.ax3.set_xlabel('Incident Energy (eV)')
		if self.mode == 0:
			self.ax1.set_xlabel('Emission Energy (eV)')
			self.ax3.set_ylabel('Emission Energy (eV)')
		else:
			self.ax1.set_xlabel('Energy Transfer (eV)')
			self.ax3.set_ylabel('Energy Transfer (eV)')
		if self.cont_t:
			if self.cont_n != 0:
				self.cont = self.ax3.contour(self.x, self.y, self.amp, self.cont_n, cmap=plt.get_cmap(self.style))
			else:
				self.cont = self.ax3.contour(self.x, self.y, self.amp, cmap=plt.get_cmap(self.style))
			self.cont.set_norm(
				norm.MyNormalize(vmin=self.amp.min(), vmax=self.amp.max(), stretch=self.stretch, clip=True))
		else:
			extent = (min(self.x), max(self.x), min(self.y), max(self.y))
			if self.cont_n != 0:
				self.cont = self.ax3.contour(self.x, self.y, self.amp, self.cont_n, colors='w', aspect='auto',
				                             linewidths=0.75, origin='lower')
				self.im = self.ax3.imshow(self.amp, extent=extent, cmap=plt.get_cmap(self.style), aspect='auto',
				                          interpolation='bilinear', origin='lower')
				self.cont.set_norm(
					norm.MyNormalize(vmin=self.amp.min(), vmax=self.amp.max(), stretch=self.stretch, clip=True))
				self.im.set_norm(
					norm.MyNormalize(vmin=self.amp.min(), vmax=self.amp.max(), stretch=self.stretch, clip=True))
			else:
				self.im = self.ax3.imshow(self.amp, extent=extent, cmap=plt.get_cmap(self.style), aspect='auto',
				                          interpolation='bilinear', origin='lower')
				self.im.set_norm(
					norm.MyNormalize(vmin=self.amp.min(), vmax=self.amp.max(), stretch=self.stretch, clip=True))
		# self.cbar = self.fig.colorbar(self.cont,format='%05.3f')

		# catch error if deviding by zero for normalization
		# But not working
		try:
			self.fig.canvas.mpl_connect('button_press_event', self.onpick)
			self.fig.canvas.mpl_connect('button_press_event', self.zoompick)
		except (RuntimeError, TypeError, NameError):
			pass
		# Dynamic CBar
		# self.press = None
		# self.cycle = sorted([i for i in dir(plt.cm) if hasattr(getattr(plt.cm,i),'N')])
		# self.index = self.cycle.index(self.cbar.get_cmap().name)
		self.fig.canvas.mpl_connect('motion_notify_event', self.onmotion)
		self.ax1init = self.ax1.fill_between(self.y, np.zeros(len(self.x)), color='#FF6666', alpha=0.5, lw=1)
		self.ax2init = self.ax2.fill_between(self.x, np.zeros(len(self.y)), color='#FF6666', alpha=0.5, lw=1)
		self.Legend_Button.clicked.connect(self.show_legend)
		self.Save_Button.clicked.connect(self.save_fig_Plane)
		self.Clear_Button.clicked.connect(self.clean_subplots)
		# set the layout
		layout = QtWidgets.QVBoxLayout()
		layout.addWidget(self.toolbar)
		layout.addWidget(self.canvas)
		self.setLayout(layout)

	# self.connect()
	# scalling cbar is not working
	# print self.value
	def save_fig_Plane(self, event):
		"""Save RIXS-Plane as png"""
		newpath = r'/Figures_' + self.filename
		if not os.path.exists(self.pathway + newpath): os.makedirs(self.pathway + newpath)
		os.chdir(self.pathway + newpath)
		self.fig.savefig(self.pathway + newpath + '/RIXS_Plane_' + self.filename + '.png', dpi=300)
		os.chdir('..')

	"""def save_fig_CUTs(self,event):
		newpath = r'/Figures_'+self.filename
		if not os.path.exists(self.pathway+newpath): os.makedirs(self.pathway+newpath)
		os.chdir(self.pathway+newpath)
		self.fig.savefig(self.pathway+newpath+'/RIXS_CUTs_'+self.filename+'.png', dpi=300)   # save the figure to file
		os.chdir('..')
	"""

	def clean_subplots(self, event):
		"""Clears the subplots."""
		for j in [self.ax1, self.ax2, self.ax3]:
			j.lines = []
			j.legend_ = None

		self.fig.canvas.draw()

	def onmotion(self, event):
		if event.inaxes != self.ax3:
			return
		xpos = int(np.argmin(np.abs(event.xdata - self.x)))
		ypos = int(np.argmin(np.abs(event.ydata - self.y)))
		self.ax1init.remove()
		self.ax1init = self.ax1.fill_between(self.y, self.amp[:, xpos], facecolor='#FFA93A', alpha=0.5, lw=1)
		self.ax2init.remove()
		self.ax2init = self.ax2.fill_between(self.x, self.amp[ypos, :], facecolor='#FFA93A', alpha=0.5, lw=1)
		self.fig.canvas.draw()

	def show_legend(self, event):
		"""Shows legend for the plots"""
		for pl in [self.ax1, self.ax2]:
			if len(pl.lines) > 0:
				pl.legend()
		self.fig.canvas.draw()

	def zoompick(self, event):
		if event.inaxes != self.ax1 and event.inaxes != self.ax2:
			return
		elif event.inaxes == self.ax1 and event.button == 1:
			ypos = int(np.argmin(np.abs(event.xdata - self.y)))
			if self.aver_y == 0:
				int_xas = self.amp[ypos, :]
			else:
				ypos_up = int(np.argmin(np.abs(event.xdata + self.aver_y - self.y)))
				ypos_down = int(np.argmin(np.abs(event.xdata - self.aver_y - self.y)))
				int_xas = np.zeros(len(self.x))
				count = 0
				for i in range(ypos_down, ypos_up + 1):
					count += 1
					int_xas = np.array(int_xas) + np.array(self.amp[i, :])
				int_xas /= count
			# For XAS -CUTS
			int_norm = self.norm_XAS(int_xas)
			CUT_XAS = np.array([self.x, int_norm, int_xas])
			label = str("%.4f" % self.y[ypos])
			c, = self.ax2.plot(CUT_XAS[0], CUT_XAS[2], label=label)
			self.ax3.axhline(self.y[ypos], color=c.get_color(), lw=1.25, alpha=0.75)
			newpath = r'/XAS_CUTs_' + self.filename  # +'_'+self.mode
			if not os.path.exists(self.pathway + newpath): os.makedirs(self.pathway + newpath)
			os.chdir(self.pathway + newpath)
			np.savetxt(self.pathway + newpath + '/XAS_Cut_at_' + label + '.txt', CUT_XAS.T, delimiter='\t',
			           newline='\n', header='En\tnorm.Int\tInt', fmt="%.4f")
			os.chdir('..')
		elif event.inaxes == self.ax2 and event.button == 1:
			xpos = int(np.argmin(np.abs(event.xdata - self.x)))
			if self.aver_x == 0:
				int_xes = self.amp[:, xpos]
			else:
				ypos_up = int(np.argmin(np.abs(event.xdata + self.aver_x - self.x)))
				ypos_down = int(np.argmin(np.abs(event.xdata - self.aver_x - self.x)))
				int_xes = np.zeros(len(self.x))
				count = 0
				for i in range(ypos_down, ypos_up + 1):
					count += 1
					int_xes = np.array(int_xes) + np.array(self.amp[:, i])
				int_xes = int_xes / count
			# For XES -CUTS
			# Adding an elastic line normalization
			int_norm = self.norm_XES(int_xes, self.mode)
			CUT_XES = np.array([self.y, int_norm, int_xes])
			label = str("%.4f" % self.x[xpos])
			c, = self.ax1.plot(CUT_XES[0], CUT_XES[2], label=label)
			self.ax3.axvline(self.x[xpos], color=c.get_color(), lw=1.25, alpha=0.75)
			newpath = r'/XES_CUTs_' + self.filename  # +'_'+self.mode
			if not os.path.exists(self.pathway + newpath): os.makedirs(self.pathway + newpath)
			os.chdir(self.pathway + newpath)
			np.savetxt(self.pathway + newpath + '/XES_Cut_at_' + label + '.txt', CUT_XES.T, delimiter='\t',
			           newline='\n', header='En\tnorm.Int\tInt', fmt="%.4f")
			os.chdir('..')
		self.fig.canvas.draw()

	def onpick(self, event):
		"""
		Capture the click event, find the corresponding data point, then update accordingly.
		"""
		if event.inaxes != self.ax3:
			return
		elif event.inaxes == self.ax3:
			if event.button == 1:
				xpos = int(np.argmin(np.abs(event.xdata - self.x)))
				if self.aver_x == 0:
					int_xes = self.amp[:, xpos]
				else:
					ypos_up = int(np.argmin(np.abs(event.xdata + self.aver_x - self.x)))
					ypos_down = int(np.argmin(np.abs(event.xdata - self.aver_x - self.x)))
					int_xes = np.zeros(len(self.x))
					count = 0
					for i in range(ypos_down, ypos_up + 1):
						count += 1
						int_xes = np.array(int_xes) + np.array(self.amp[:, i])
					int_xes = int_xes / count
				# For XES -CUTS
				# Adding an elastic line normalization
				int_norm = self.norm_XES(int_xes, self.mode)
				CUT_XES = np.array([self.y, int_norm, int_xes])
				label = str("%.4f" % self.x[xpos])
				c, = self.ax1.plot(CUT_XES[0], CUT_XES[2], label=label)
				self.ax3.axvline(self.x[xpos], color=c.get_color(), lw=1.25, alpha=0.75)
				newpath = r'/XES_CUTs_' + self.filename  # +'_'+self.mode
				if not os.path.exists(self.pathway + newpath): os.makedirs(self.pathway + newpath)
				os.chdir(self.pathway + newpath)
				np.savetxt(self.pathway + newpath + '/XES_Cut_at_' + label + '.txt', CUT_XES.T, delimiter='\t',
				           newline='\n', header='En\tnormInt\tInt', fmt="%.4f")
				os.chdir('..')
			elif event.button == 3:
				ypos = int(np.argmin(np.abs(event.ydata - self.y)))
				if self.aver_y == 0:
					int_xas = self.amp[ypos, :]
				else:
					ypos_up = int(np.argmin(np.abs(event.ydata + self.aver_y - self.y)))
					ypos_down = int(np.argmin(np.abs(event.ydata - self.aver_y - self.y)))
					int_xas = np.zeros(len(self.x))
					count = 0
					for i in range(ypos_down, ypos_up + 1):
						count += 1
						int_xas = np.array(int_xas) + np.array(self.amp[i, :])
					int_xas = int_xas / count
				# For XAS -CUTS
				int_norm = self.norm_XAS(int_xas)
				CUT_XAS = np.array([self.x, int_norm, int_xas])
				label = str("%.4f" % self.y[ypos])
				c, = self.ax2.plot(CUT_XAS[0], CUT_XAS[2], label=label)
				self.ax3.axhline(self.y[ypos], color=c.get_color(), lw=1.25, alpha=0.75)
				newpath = r'/XAS_CUTs_' + self.filename  # +'_'+self.mode
				if not os.path.exists(self.pathway + newpath): os.makedirs(self.pathway + newpath)
				os.chdir(self.pathway + newpath)
				np.savetxt(self.pathway + newpath + '/XAS_Cut_at_' + label + '.txt', CUT_XAS.T, delimiter='\t',
				           newline='\n', header='Energy\tnormInt\tInt', fmt="%.4f")
				os.chdir('..')
		# Now drawing Cuts in the subplots for the RIXS plane
		self.fig.canvas.draw()



	@staticmethod
	def norm_XAS(data):
		if np.max(data) != 0:
			norm = data / np.max(data)
		else:
			norm = data
		return norm

	def norm_XES(self, data, mode):
		if np.max(data) != 0:
			if mode == 0:
				norm = data / np.max(data)
			else:
				i = np.argmin(np.abs(self.y - 0.))
				norm = data / data[i]
		else:
			norm = data
		return norm

	def connect(self):
		"""connect to all the events we need for the colorbar"""
		self.cidpress = self.cbar.patch.figure.canvas.mpl_connect(
			'button_press_event', self.on_press)
		self.cidrelease = self.cbar.patch.figure.canvas.mpl_connect(
			'button_release_event', self.on_release)
		self.cidmotion = self.cbar.patch.figure.canvas.mpl_connect(
			'motion_notify_event', self.on_motion)
		self.keypress = self.cbar.patch.figure.canvas.mpl_connect(
			'key_press_event', self.key_press)
		"""Here the functions for real time cut are working"""

	"""
	def update_coeff(self, a1,a2):
		'''update the AR(2) coefficients choice
		and the roots of the AR polynomial'''
		# Update the title
		#self.a.set_title('Choose AR(2) coefficients: '
		#                   '$(a_1, a_2)$=(%.2f, %.2f) \n'
		#                   'process $X_k = a_1 X_{k-1} + a_2 X_{k-2} + Z_k$'\
		#                   % (a1, a2))
		# Move the circle
		print a1, a2
		self.circ.center = a1, a2
		# Move the guiding lines
		#coeff_line.set_data([a1, a1, 0], [0,a2,a2])
		# Move the roots:
		#poly_ar2 = Polynomial([-a2, -a1, 1])
		#root1, root2 = poly_ar2.roots().astype(complex)
		#self.fig.set_data([root1.real, root2.real],
		#                    [root1.imag, root2.imag])
	def update_response(self, a1,a2):
		'''update the plots of the filter responses
		(impulse and frequency)'''
		print a1, a2
		#h_ir = lfilter([1], [1, -a1, -a2], dirac)
		#ir_line.set_data(k, h_ir)
		#spectrum_line.set_data(omega_list/np.pi, spectrum_ar2(a1,a2,omega_list))
		#self.spec_poly.remove()
		#self.spec_poly = ax_spec.fill_between(omega_list/np.pi,
		#                                      spectrum_ar2(a1,a2,omega_list),
		#                                      color='#FFAA00', alpha=0.5, lw=0)
	### Event handlers
	def onpress(self, event):
		'''mouse press = move the circle + follow the mouse'''
		if event.inaxes!=self.fig: return
		self.update_coeff(a1=event.xdata, a2=event.ydata)
		print event.xdata
		self.update_response(a1=event.xdata, a2=event.ydata)
		self.fig.canvas.draw()
		#fig_res.canvas.draw()
		self.pressevent = event

	def onrelease(self, event):
		'''mouse release = stop following the mouse'''
		if self.pressevent is None: return

		self.update_coeff(a1=event.xdata, a2=event.ydata)
		self.update_response(a1=event.xdata, a2=event.ydata)
		self.fig.canvas.draw()
		#fig_res.canvas.draw()
		self.pressevent = None
		print('a1, a2 = (%.2f, %.2f)' % circ.center)
	def onmove(self, event):
		'''mouse move = move the circle'''
		if self.pressevent is None or event.inaxes!=self.pressevent.inaxes: return

		self.update_coeff(a1=event.xdata, a2=event.ydata)
		self.update_response(a1=event.xdata, a2=event.ydata)
		self.fig.canvas.draw()
		self.fig.canvas.draw()
	"""

	def on_press(self, event):
		"""Data will be stored depending if you are in the RIXS-MAP-, XAS- or XES-Plot"""
		if event.inaxes != self.cbar.ax: return
		self.press = event.x, event.y

	def key_press(self, event):
		"""Genereting new cmap-ranges"""
		if event.key == 'down':
			self.index += 1
		elif event.key == 'up':
			self.index -= 1
		if self.index < 0:
			self.index = len(self.cycle)
		elif self.index >= len(self.cycle):
			self.index = 0
		cmap = self.cycle[self.index]
		self.cbar.set_cmap(cmap)
		self.cbar.draw_all()
		self.cont.set_cmap(cmap)
		self.cont.get_axes().set_title(cmap)
		self.cbar.patch.figure.canvas.draw()

	def on_motion(self, event):
		"""If moving mouse over RIXS-Plane instantly the resonant XAS- and XES-Plot will be generated as preview"""
		if self.press is None:
			return
		if event.inaxes != self.cbar.ax:
			return
		xprev, yprev = self.press
		dx = event.x - xprev
		dy = event.y - yprev
		self.press = event.x, event.y
		scale = self.cbar.norm.vmax - self.cbar.norm.vmin
		perc = 0.01
		if event.button == 1 and dy != 0 and dx != 0:
			self.cbar.norm.vmin -= (perc * scale) * np.sign(dy) - 0.001
			self.cbar.norm.vmax += (perc * scale) * np.sign(dy) + 0.001  # Maybe Signume error before!
		elif event.button == 3 and dy != 0 and dx != 0:
			self.cbar.norm.vmin -= (perc * scale) * np.sign(dy) - 0.001
			self.cbar.norm.vmax += (perc * scale) * np.sign(dy) + 0.001
		self.cbar.draw_all()
		# self.contour.set_norm(self.cbar.norm)
		self.cont.set_norm(self.cbar.norm)
		self.cbar.patch.figure.canvas.draw()

	def on_release(self, event):
		"""Reset all plotted data and cut-lines"""
		self.press = None
		self.cont.set_norm(self.cbar.norm)
		# self.contour.set_norm(self.cbar.norm)
		self.cbar.patch.figure.canvas.draw()

	def disconnect(self):
		"""Disconnect all the stored connection ids"""
		self.cbar.patch.figure.canvas.mpl_disconnect(self.cidpress)
		self.cbar.patch.figure.canvas.mpl_disconnect(self.cidrelease)
		self.cbar.patch.figure.canvas.mpl_disconnect(self.cidmotion)

	"""
		def onpick(self, event):
		'''Capture the click event, find the corresponding data
		point, then update accordingly.'''
		# the click locations
		try:
			x = event.mouseevent.xdata
			y = event.mouseevent.ydata
			dx = np.array(x - self.x[event.ind], dtype=float)
			dy = np.array(y - self.y[event.ind], dtype=float)
			distances = np.hypot(dx, dy)
			print distances
			indmin = distances.argmin()
			dataind = event.ind[indmin]
			#self.lastind = dataind
			self.update()
		except Exception:
			pass
		def update(self):
		'''Update the main graph and call my response function.'''
		#if self.lastind is None:
		#    return
		#dataind = self.lastind
		self.selected.set_visible(True)
		self.selected.set_data(self.xexp, self.yexp)
		#self.logic.test_fit(dataind)
		self.fig.canvas.draw()
	"""


# Message Window classes#
class w_message(QtWidgets.QWidget, warning.Ui_Form):
	def __init__(self, value, parent=None):
		QtWidgets.QWidget.__init__(self, parent)
		self.setupUi(self)


class r_loading(QtWidgets.QWidget, loading_RIXS.Ui_Form):
	def __init__(self, value, parent=None):
		QtWidgets.QWidget.__init__(self, parent)
		self.setupUi(self)


class o_loading(QtWidgets.QWidget, loading_ORCA.Ui_Form):
	def __init__(self, value, parent=None):
		QtWidgets.QWidget.__init__(self, parent)
		self.setupUi(self)


class c_loading(QtWidgets.QWidget, loading_CTM.Ui_Form):
	def __init__(self, value, parent=None):
		QtWidgets.QWidget.__init__(self, parent)
		self.setupUi(self)


if __name__ == '__main__':
	import sys

	app = QtWidgets.QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())
