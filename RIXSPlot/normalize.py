import numpy as np
import numpy.ma as ma
import matplotlib.cbook as cbook
from matplotlib.colors import Normalize


class MyNormalize(Normalize):
	def __init__(self, stretch='Linear', exponent=5, vmid=None, vmin=None, vmax=None, clip=False):
		"""
		MyNormalize-class is used for re-scalling the color-scheme

		Parameters
		----------
		stretch: str
			The stretch function to use (default is 'linear') for re-ordering the color-scaling.
			The options are:
				*'linear'
				*'log'
				*'sqrt'
				*'arcsinh'
				*'arccosh'
				*'power'
				*'exp'
		exponent: float
			exponent is set the 'power' of the exponent if used use.
		vmin: float
			Minimum pixel value to use for the scaling.
		vmax: float
			Maximum pixel value to use for the scaling.
		vmid: float
			Mid-pixel value used for the log and arcsinh stretches. If set to None, a default value is picked.
		clip: bool
			If clip is True and the given value falls outside the range,
			the returned value will be 0 or 1, whichever is closer.
		"""

		if vmax < vmin:
			raise Exception("vmax should be larger than vmin")

		# Call original initalization routine
		Normalize.__init__(self, vmin=vmin, vmax=vmax, clip=clip)

		# Save parameters
		self.stretch = stretch
		self.exponent = exponent

		if stretch == 'Power' and np.equal(self.exponent, None):
			raise Exception("For stretch=='Power', an exponent should be specified")

		if stretch == 'Log':
			if np.equal(vmid, None):
				if vmin <= 0:
					vmin = 0.00001
				self.midpoint = vmax / vmin
			else:
				if vmin < vmid:
					raise Exception("When using a Log stretch, vmin should be larger than vmid")
				self.midpoint = (vmax - vmid) / (vmin - vmid)
		elif stretch in ['Arcsinh', 'Arccosh']:
			self.midpoint = -1. / 30.
		else:
			self.midpoint = None

	def __call__(self, value, clip=None):

		# read in parameters
		method = self.stretch
		exponent = self.exponent
		midpoint = self.midpoint

		# ORIGINAL MATPLOTLIB CODE

		if clip is None:
			clip = self.clip

		if np.iterable(value):
			vtype = 'array'
			val = ma.asarray(value).astype(np.float)
		else:
			vtype = 'scalar'
			val = ma.array([value]).astype(np.float)

		self.autoscale_None(val)
		vmin, vmax = self.vmin, self.vmax
		if vmin > vmax:
			raise ValueError("minvalue must be less than or equal to maxvalue")
		elif vmin == vmax:
			return 0.0 * val
		else:
			if clip:
				mask = ma.getmask(val)
				val = ma.array(np.clip(val.filled(vmax), vmin, vmax), mask=mask)
			result = (val - vmin) * (1.0 / (vmax - vmin))

			# CUSTOM APLPY CODE

			# Keep track of negative values
			negative = result < 0.

			if self.stretch == 'Linear':

				pass

			elif self.stretch == 'Log':

				# result = np.log(result * (self.midpoint - 1.) + 1.) \
				#        / np.log(self.midpoint)
				result = ma.log10(result * (self.midpoint - 1.) + 1.) \
				         / ma.log10(self.midpoint)

			elif self.stretch == 'Sqrt':

				result = ma.sqrt(ma.abs(result))

			elif self.stretch == 'Arcsinh':

				result = ma.arcsinh(result / self.midpoint) \
				         / ma.arcsinh(1. / self.midpoint)

			elif self.stretch == 'Arccosh':

				result = ma.arccosh(result / self.midpoint) \
				         / ma.arccosh(1. / self.midpoint)

			elif self.stretch == 'Power':

				result = ma.power(result, exponent)

			elif self.stretch == 'Exp':

				result = np.exp(result)

			else:

				raise Exception("Unknown stretch in APLpyNormalize: %s" % self.stretch)

			# Now set previously negative values to 0, as these are
			# different from true NaN values in the FITS image
			result[negative] = -np.inf

		if vtype == 'Scalar':
			result = result[0]

		return result

	def inverse(self, value):

		# ORIGINAL MATPLOTLIB CODE

		if not self.scaled():
			raise ValueError("Not invertible until scaled")

		vmin, vmax = self.vmin, self.vmax

		# CUSTOM APLPY CODE

		if cbook.iterable(value):
			val = ma.asarray(value)
		else:
			val = value

		if self.stretch == 'Linear':

			pass

		elif self.stretch == 'Log':

			val = (ma.power(10., val * ma.log10(self.midpoint)) - 1.) / (self.midpoint - 1.)

		elif self.stretch == 'Sqrt':

			val = val * val

		elif self.stretch == 'Arcsinh':

			val = self.midpoint * \
			      ma.sinh(val * ma.arcsinh(1. / self.midpoint))

		elif self.stretch == 'Arccosh':

			val = self.midpoint * \
			      ma.cosh(val * ma.arccosh(1. / self.midpoint))

		elif self.stretch == 'Power':

			val = ma.power(val, (1. / self.exponent))

		elif self.stretch == 'Exp':

			val = 1. / np.exp(val)



		else:

			raise Exception("Unknown stretch in APLpyNormalize: %s" % self.stretch)

		return vmin + val * (vmax - vmin)
