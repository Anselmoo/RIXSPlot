import numpy as np
from scipy.interpolate import griddata


class interpolation():
	def __init__(self, check):
		self.check = check
		self.RIXS = {'XAS': np.zeros(10), 'XES': np.zeros(10), 'RIXS': np.zeros((10, 10))}
		self.x, self.y, self.z = np.zeros(10, dtype=float), np.zeros(10, dtype=float), np.zeros(10, dtype=float)
		self.x_0, self.x_1 = np.zeros(10, dtype=float), np.zeros(10, dtype=float)
		self.y_0, self.y_1 = np.zeros(10, dtype=float), np.zeros(10, dtype=float)

	def guess(self):
		try:
			self.EnergyLoss()
			self.EnergyRanges()
			if self.check['type'] == 'ORCA' or self.check['type'] == 'CTM' or self.check['type'] == 'XCLAIM':
				grid_p = int(len(self.x) / len(np.unique(self.x))) * 3
				xii = np.linspace(self.x_0, self.x_1, grid_p, dtype=float)
				yii = np.linspace(self.y_0, self.y_1, grid_p, dtype=float)
				xi, yi = np.meshgrid(xii, yii)
				Plane = griddata((self.x, self.y), self.z, (xi, yi), method='linear')
				self.RIXS['XAS'], self.RIXS['XES'], self.RIXS['RIXS'] = xii, yii, np.nan_to_num(Plane)
			elif self.check['type'] == 'RIXS':
				if self.check['inter'] == 0:
					grid_p = self.check['grid']
					xii = np.linspace(self.x_0, self.x_1, grid_p, dtype=float)
					yii = np.linspace(self.y_0, self.y_1, grid_p, dtype=float)
					xi, yi = np.meshgrid(xii, yii)
					Plane = griddata((self.x, self.y), self.z, (xi, yi), method='linear')
					self.RIXS['XAS'], self.RIXS['XES'], self.RIXS['RIXS'] = xii, yii, np.nan_to_num(Plane)
				elif self.check['inter'] == 1:
					grid_p = self.check['grid']
					xii = np.linspace(self.x_0, self.x_1, grid_p, dtype=float)
					yii = np.linspace(self.y_0, self.y_1, grid_p, dtype=float)
					xi, yi = np.meshgrid(xii, yii)
					Plane = griddata((self.x, self.y), self.z, (xi, yi), method='nearest')
					self.RIXS['XAS'], self.RIXS['XES'], self.RIXS['RIXS'] = xii, yii, np.nan_to_num(Plane)
				elif self.check['inter'] == 2:
					grid_p = self.check['grid']
					xii = np.linspace(self.x_0, self.x_1, grid_p, dtype=float)
					yii = np.linspace(self.y_0, self.y_1, grid_p, dtype=float)
					xi, yi = np.meshgrid(xii, yii)
					Plane = griddata((self.x, self.y), self.z, (xi, yi), method='cubic')
					self.RIXS['XAS'], self.RIXS['XES'], self.RIXS['RIXS'] = xii, yii, np.nan_to_num(Plane)
				elif self.check['inter'] == 3:
					grid_p = self.check['grid']
					inpt = {'x': self.x, 'y': self.y, 'z': self.z, 'fwhm_x': 0.75, 'fwhm_y': 0.25, 'points': grid_p}
					gaus = Gaussian_Grid(inpt)
					Plane, xii, yii = gaus.griddata()
					self.RIXS['XAS'], self.RIXS['XES'], self.RIXS['RIXS'] = xii, yii, np.nan_to_num(Plane)
				""" Can only work if XAS points are equal to XES points so now """
			# elif self.check['inter'] == 3:
			#    grid_p = self.check['grid']
			#    x0 = np.unique(self.x)

			#    xii = np.linspace(self.x_0, self.x_1,grid_p,dtype=float)
			#    yii = np.linspace(self.y_0, self.y_1,grid_p,dtype=float)
			#    xi, yi = len(x0) , len(self.x)/len(x0)
			#    inter = interp2d(x0, self.y,np.reshape(self.z,(xi,yi)), kind='quintic')
			#    Plane = inter(xii,yii)
			#    self.RIXS['XAS'],self.RIXS['XES'],self.RIXS['RIXS'] = xii, yii, np.nan_to_num(Plane)
			return self.RIXS
		except ValueError:
			raise

	def EnergyLoss(self):
		"""
		Transform the Emission Spectra to an Energy Loss Spectra
		"""
		try:
			data = self.check['data']
			self.x = data[:, 0] + self.check['shift_x']
			self.y = data[:, 1] + self.check['shift_y']
			self.z = data[:, 2]
			if self.check['mode'] == 1:
				x0 = np.unique(self.x)
				cut = np.zeros(len(x0) + 1, dtype=int)
				for i, xi in enumerate(x0):
					cut[i] = np.argmin(np.abs(self.x - xi))
				cut[-1] = len(self.x)
				for i in range(len(cut) - 1):
					self.y[cut[i]:cut[i + 1]] = - self.y[cut[i]:cut[i + 1]] + self.x[cut[i]:cut[i + 1]]
		except ValueError:
			raise

	def EnergyRanges(self):
		"""
		Gives the energy range for the xyz-plot
		"""
		try:
			x0, x1 = self.check['x0'], self.check['x1']
			y0, y1 = self.check['y0'], self.check['y1']
			if x0 != 0.0 and x1 != 0.0 and y0 == 0.0 and y1 == 0.0:
				self.x_0, self.x_1, self.y_0, self.y_1 = x0, x1, min(self.y), max(self.y)
			elif y0 != 0.0 and y1 != 0.0 and x0 == 0.0 and x1 == 0.0:
				self.x_0, self.x_1, self.y_0, self.y_1 = min(self.x), max(self.x), y0, y1
			elif y0 != 0.0 and y1 != 0.0 and x0 != 0.0 and x1 != 0.0:
				self.x_0, self.x_1, self.y_0, self.y_1 = x0, x1, y0, y1
			else:
				self.x_0, self.x_1, self.y_0, self.y_1 = min(self.x), max(self.x), min(self.y), max(self.y)
		except ValueError:
			raise


class Gaussian_Grid():
	def __init__(self, inpt):
		self.x, self.y, self.z = inpt['x'], inpt['y'], inpt['z']
		self.offset = 0.5
		sig = 1. / 2. / np.sqrt(np.log(2.))
		self.sigma_x, self.sigma_y = sig * inpt['fwhm_x'], sig * inpt['fwhm_y']
		self.points = inpt['points']
		self.retbin, self.retloc = False, False

	def griddata(self):
		"""
		Place unevenly spaced 2D data on a grid by 2D gaussians (nearest
		neighbor interpolation).

		Parameters
		----------
		x : ndarray (1D)
			The idependent data x-axis of the grid.
		y : ndarray (1D)
			The idependent data y-axis of the grid.
		z : ndarray (1D)
			The dependent data in the form z = f(x,y).
		offset : scalar, optional
			The offset can extend the area of the interpolated grid.
		fwhm_x, fwhm_y: scalar, optional
			The full width half maximum specified the area of
			the Gaussian interpolation for x and y directions.
		points : scalar, optional
			The points defines the point density for the interpolated grid.
		retbin : boolean, optional
			Function returns `bins` variable (see below for description)
			if set to True.  Defaults to True.
		retloc : boolean, optional
			Function returns `wherebins` variable (see below for description)
			if set to True.  Defaults to True.

		Returns
		-------
		grid : ndarray (2D)
			The evenly gridded data.  The value of each cell is the median
			value of the contents of the bin.
		xi, yi :ndarray (2D)
			The corresponding grid for the interpolations. Comes from the min/max of x and y
		bins : ndarray (2D)
			A grid the same shape as `grid`, except the value of each cell
			is the number of points in that bin.  Returns only if
			`retbin` is set to True.
		wherebin : list (2D)
			A 2D list the same shape as `grid` and `bins` where each cell
			contains the indicies of `z` which contain the values stored
			in the particular bin.
	   Revisions
	   ---------
			25.12.2018  Anselm Hahn
		 """
		# Input Variables

		# get extrema values.

		# make coordinate arrays.
		# make the initial grid
		# cdef np.ndarray[double, ndim=1]  xi      = np.linspace(ranges[0]-offset, ranges[1]+offset, points)
		# cdef np.ndarray[double, ndim=1]  yi      = np.linspace(ranges[2]-offset, ranges[3]+offset, points)
		# x_grid,  y_grid = np.meshgrid(xi,yi)
		# cdef np.ndarray[double, ndim=2] xx = x_grid
		# cdef np.ndarray[double, ndim=2] yy = y_grid

		# cdef double sigma_x = fwhm_x/2.0/np.sqrt(np.log(2.0))
		# cdef double sigma_y = fwhm_y/2.0/np.sqrt(np.log(2.0))

		# make the grid.
		# cdef np.ndarray[double, ndim=2] grid  = np.zeros((points,points), dtype=x.dtype)
		xi = np.linspace(min(self.x) - self.offset, max(self.x) + self.offset, self.points)
		yi = np.linspace(min(self.y) - self.offset, max(self.y) + self.offset, self.points)
		xx, yy = np.meshgrid(xi, yi)
		grid = np.zeros((self.points, self.points), dtype=float)
		if self.retbin: bins = np.copy(grid)
		# create list in same shape as grid to store indices
		if self.retloc:
			wherebin = np.copy(grid)
			wherebin = wherebin.tolist()
		# cdef int row, col, i
		# fill in the grid.
		for row in range(self.points):
			for col in range(self.points):
				xc = xx[row, col]  # x coordinate.
				yc = yy[row, col]  # y coordinate.
				# find the position that xc and yc correspond to.
				posx = np.abs(self.x - xc)
				posy = np.abs(self.y - yc)
				# Parametrization for the level of interpolation dependet on the given fwhm
				ibin = np.logical_and(posx <= self.sigma_x, posy <= self.sigma_y)
				ind = np.where(ibin == True)[0]
				# fill the bin
				bin = self.z[ibin]
				if self.retloc: wherebin[row][col] = ind
				if self.retbin: bins[row, col] = bin.size
				if bin.size != 0:
					binval = np.zeros((self.points, self.points), dtype=float)
					for i in ind:
						# Here the Gaussian Interpolation is running
						pre = self.z[i]
						if pre > 10e-4:
							xpart = np.exp(-np.square(xx - self.x[i]) / self.sigma_x)
							ypart = np.exp(-np.square(yy - self.y[i]) / self.sigma_y)
							binval += pre * xpart * ypart
						else:
							binval += np.zeros((self.points, self.points), dtype=float)
					grid += binval
				# grid[row, col] = np.average(binval)
			# else:
			# grid[row, col] = 0   #former np.nan fill empty bins with nans.
		# return the grid
		if self.retbin:
			if self.retloc:
				return grid, xi, yi, bins, wherebin
			else:
				return grid, xi, yi, bins
		else:
			if self.retloc:
				return grid, xi, yi, wherebin
			else:
				return grid, xi, yi
