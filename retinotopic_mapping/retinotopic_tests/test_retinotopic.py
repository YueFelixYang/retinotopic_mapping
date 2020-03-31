import os
import retinotopic_mapping
import retinotopic_mapping.tools.FileTools as ft
import retinotopic_mapping.RetinotopicMapping as rm
import tifffile as tf
import matplotlib.pyplot as plt

# move to package example folder
package_folder = "/home/mariad/retinotopic_mapping/"                            # retinotopic_mapping.__path__
example_folder = "/home/mariad/retinotopic_mapping/examples/signmap_analysis"   # os.path.join(package_folder[0], 'examples')
os.chdir(example_folder)

# reading example vasculature image
vasculature_map = tf.imread('example_vasculature_map.tif')
_ = plt.imshow(vasculature_map, cmap='gray', interpolation='nearest')
_ = plt.colorbar()
plt.show()

# reading example retinotopic maps
altitude_map = tf.imread('example_altitude_map.tif')
azimuth_map = tf.imread('example_azimuth_map.tif')
altitude_power_map = tf.imread('example_altitude_power_map.tif')
azimuth_power_map = tf.imread('example_azimuth_power_map.tif')

f = plt.figure(figsize=(15, 12))
ax1 = f.add_subplot(221)
fig1 = ax1.imshow(altitude_map, vmin=-40, vmax=60, cmap='hsv', interpolation='nearest')
ax1.set_axis_off()
ax1.set_title('altitude map')
_ = f.colorbar(fig1)

ax2 = f.add_subplot(222)
fig2 = ax2.imshow(azimuth_map, vmin=0, vmax=120, cmap='hsv', interpolation='nearest')
ax2.set_axis_off()
ax2.set_title('azimuth map')
_ = f.colorbar(fig2)

ax3 = f.add_subplot(223)
fig3 = ax3.imshow(altitude_power_map, vmin=0, vmax=1, cmap='hot', interpolation='nearest')
ax3.set_axis_off()
ax3.set_title('altitude power map')
_ = f.colorbar(fig3)

ax4 = f.add_subplot(224)
fig4 = ax4.imshow(azimuth_power_map, vmin=0, vmax=1, cmap='hot', interpolation='nearest')
ax4.set_axis_off()
ax4.set_title('azimuth power map')
_ = f.colorbar(fig4)

plt.show()

# Defining image analysis parameters
# details at:///tmp/mozilla_mariad0/elife-18372-supp1-v2.htm
params = {
          'phaseMapFilterSigma': 0.5,
          'signMapFilterSigma': 8.,
          'signMapThr': 0.4,
          'eccMapFilterSigma': 15.0,
          'splitLocalMinCutStep': 5.,
          'closeIter': 3,
          'openIter': 3,
          'dilationIter': 15,
          'borderWidth': 1,
          'smallPatchThr': 100,
          'visualSpacePixelSize': 0.5,
          'visualSpaceCloseIter': 15,
          'splitOverlapThr': 1.1,
          'mergeOverlapThr': 0.1
          }

# Creating the RetinotopicMappingTrail object
trial = rm.RetinotopicMappingTrial(altPosMap=altitude_map,
                                   aziPosMap=azimuth_map,
                                   altPowerMap=altitude_power_map,
                                   aziPowerMap=azimuth_power_map,
                                   vasculatureMap=vasculature_map,
                                   mouseID='test',
                                   dateRecorded='160612',
                                   comments='This is an example.',
                                   params=params)
print trial

# 8. Generating visual sign map
_ = trial._getSignMap(isPlot=True)
plt.show()

# 9. Binarizing filtered visual signmap
_ = trial._getRawPatchMap(isPlot=True)
plt.show()

# 10. Generating raw patches
_ = trial._getRawPatches(isPlot=True)
plt.show()

# 11. Generating determinant map
_ = trial._getDeterminantMap(isPlot=True)
plt.show()

# 12. Generating eccentricity map for each patch
_ = trial._getEccentricityMap(isPlot=True)
plt.show()

# 13. Splitting overlapping patches
_ = trial._splitPatches(isPlot=True)
plt.show()

# 14. Merging non-overlapping patches
_ = trial._mergePatches(isPlot=True)
plt.show()

# Note: The methods from 8 to 14 are protected by leading underscore!
# Here they were used separately to show every single image analysis step.
# In real life, the steps from cell 8 to cell 14 can be consolidated into one single method:
# trial.processTrial(isPlot=True)

# 15. Plotting results
_ = trial.plotFinalPatchBorders2()
plt.show()

# Annotating segmented patches
names = [
    ['patch01', 'V1'],
    ['patch02', 'PM'],
    ['patch03', 'RL'],
    ['patch04', 'P'],
    ['patch05', 'LM'],
    ['patch06', 'AM'],
    ['patch07', 'LI'],
    ['patch08', 'MMA'],
    ['patch09', 'AL'],
    ['patch10', 'RLL'],
    ['patch11', 'LLA'],
    #          ['patch12', 'MMP'],
    ['patch13', 'MMP']
]

finalPatchesMarked = dict(trial.finalPatches)

for i, namePair in enumerate(names):
    currPatch = finalPatchesMarked.pop(namePair[0])
    newPatchDict = {namePair[1]: currPatch}
    finalPatchesMarked.update(newPatchDict)

trial.finalPatchesMarked = finalPatchesMarked

# Ploting final results
_ = trial.plotFinalPatchBorders2()
plt.show()

# Generating dictionary for saving
trialDict = trial.generateTrialDict()
trialDict.keys()

# Saving results
# ft.saveFile("path_to_save", trialDict)

