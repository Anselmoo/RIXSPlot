# RIXSPlot

In order to understand experimental, as well as computational RIXS results, the **RIXSPlot** is developed as a PythonQt-Interface.  **RIXSPlot** allows plotting of the *experimental* as well as the *calculated* RIXS-Maps and can generate the XAS-, XES-, and EnergyLoss-Cuts. For this reason, three subplots will be generated in the main-panel for XAS, XES, and RIXS and the RIXS-cuts can be extracted of each single windows just by clicking on the observed feature. After clicking, the data will be immediately exported as *txt*-file.
![User-Interface](https://github.com/Anselmoo/RIXSPlot/blob/master/doc/userinterface.001.png)
For visualization of the RIXS spectra, the colormap reference of [`matplotlib`](https://matplotlib.org/gallery/color/colormap_reference.html#sphx-glr-gallery-color-colormap-reference-py) is used. In addition to that, **RIXSPlot** can generate RIXS-Maps with a squared root or logarithmic contrast level, which is advantageous in case of dominating features such an elastic line or very intense rising- edge. 

**RIXSPlot** provides:

  * Visualization of RIXS-Maps and their RIXS-cuts
  * Exporting of (*opt:* averaged) XAS- and XES-Spectra from RIXS
  * Re-calibrating of the RIXS-Maps
  * Natural-Broadening-Interpolation for converting single RIXS-spectra to a complete RIXS-Map
  ![Naturual-Broadening-Interpolation](https://github.com/Anselmoo/RIXSPlot/blob/master/doc/GaussianInter.png)

**RIXSPlot** requires:
  * [PyQt5](https://riverbankcomputing.com/software/pyqt/intro)
  * [numpy](https://github.com/numpy/numpy)
  * [scipy](https://github.com/scipy/scipy)
  
Further requirements are the format of the RIXS-data. The ASCII-file should like this:

Incident Energy | Emission Energy | Intensity
------------ | ------------- | -------------
0.0 | 0.0 | 0.0
0.1… | 0.1… | 0.1…
⋮ | ⋮ | ⋮
⋮ | ⋮ | ⋮
⋮ | ⋮ | ⋮
#end | #end | #end

Installing and Running:
    
    python setup.py install
    python -m RIXSPlot
    



