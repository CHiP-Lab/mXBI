import psignifit as ps
import numpy as np




# dualina
# data = [[[0,2,6],#1 session
#           [15,2,5],
#           [30,1,5],
#           [45,4,6],
#           [60,5,9],
#           [70,5,6],
#           [80,5,6],
#           ],
#           [[0,4,14],#2 session
#           [15,2,13],
#           [30,7,15],
#           [45,10,16],
#           [60,10,16],
#           [70,14,16],
#           [80,13,16]
#           ],
#           [[0,2,11],#3 session
#           [15,3,10],
#           [30,4,10],
#           [45,9,11],
#           [60,10,10],
#           [70,10,11],
#           [80,9,10]
#           ],
#           [[0,0,5],#4 session
#           [15,0,4],
#           [30,1,4],
#           [45,1,4],
#           [60,4,6],
#           [70,3,5],
#           [80,3,4]
#           ],
#           [[0,1,12],#5 session
#           [15,5,14],
#           [30,2,15],
#           [45,5,13],
#           [60,9,15],
#           [70,12,15],
#           [80,12,13],
#           ]]
# data = np.array( #total
#     [[0,9,48],
#      [15,12,46],
#      [30,15,49],
#      [45,29,50],
#      [60,39,53],
#      [70,44,53],
#      [80,42,49]]
#     )
#-----------------
# elero
# data = [[[0,0,7],#1
#           [15,1,7],
#           [30,2,6],
#           [45,5,8],
#           [60,5,9],
#           [70,6,6],
#           [80,6,8]
#           ],
#           [[0,4,15],#2
#           [15,6,16],
#           [30,9,17],
#           [45,11,17],
#           [60,10,19],
#           [70,10,17],
#           [80,13,17]
#           ],
#           [[0,2,7],#3
#           [15,3,9],
#           [30,3,8],
#           [45,5,10],
#           [60,7,10],
#           [70,5,11],
#           [80,6,7]
#           ],
#           [[0,1,12],#4
#           [15,3,11],
#           [30,5,12],
#           [45,9,16],
#           [60,8,15],
#           [70,12,12],
#           [80,9,13],
#           ],
#           [[0,3,16],#5
#           [15,2,15],
#           [30,3,17],
#           [45,7,22],
#           [60,8,20],
#           [70,12,20],
#           [80,13,19],
#        	]]

# data = np.array(
#     [[0,10,57],
#       [15,15,58],
#       [30,22,60],
#       [45,37,73],
#       [60,38,73],
#       [70,45,66],
#       [80,47,64]]
#     )
#--------------
# ivy
# data = [[[0,0,7],#1
#           [15,2,8],
#           [30,3,7],
#           [45,7,9],
#           [60,7,7],
#           [70,5,7],
#           [80,7,7]
#           ],
#           [[0,0,14],#2
#           [15,2,15],
#           [30,4,15],
#           [45,11,21],
#           [60,13,13],
#           [70,13,15],
#           [80,14,15]
#           ],
#           [[0,1,13],#3
#           [15,0,12],
#           [30,3,12],
#           [45,10,13],
#           [60,11,13],
#           [70,11,12],
#           [80,12,12]
#           ],
#           [[0,1,16],#4
#           [15,2,15],
#           [30,4,15],
#           [45,14,15],
#           [60,14,18],
#           [70,15,15],
#           [80,15,15]
#           ]]
# data = np.array([[0,2,50],#total
#                   [15,6,50],
#                   [30,14,49],
#                   [45,42,58],
#                   [60,45,51],
#                   [70,44,49],
#                   [80,48,49]
#                   ])

# data = np.array([[0, 50, 56], [30, 58, 61], [60, 54, 59], [70, 56, 59], [80, 51, 58]])
# data = np.array(data[4])

options = dict()
options['sigmoidName'] = 'norm'   # choose a cumulative Gauss as the sigmoid
options['expType']     = '2AFC'
options['fixedPars']   = np.nan*np.ones(5)
options['fixedPars'][2] = 0.01
options['fixedPars'][3] = 0.0
res=ps.psignifit(data,options)




def test_plotPsych():
    plt.figure()
    ps.psigniplot.plotPsych(res,showImediate=False)
    plt.close('all')
    assert True

def test_plotMarginal():
    plt.figure()
    ps.psigniplot.plotMarginal(res,0,showImediate=False)
    plt.close('all')
    assert True

def test_plot2D():
    plt.figure()
    ps.psigniplot.plot2D(res,0,1,showImediate=False)
    plt.close('all')
    assert True

def test_fixedPars():
    #Check that fit and borders are actually set to the fixed parametervalues
    assert np.all(res['Fit'][np.isfinite(options['fixedPars'])]== options['fixedPars'][np.isfinite(options['fixedPars'])])
    assert np.all(res['options']['borders'][np.isfinite(options['fixedPars']),0]==options['fixedPars'][np.isfinite(options['fixedPars'])])
    assert np.all(res['options']['borders'][np.isfinite(options['fixedPars']),1]==options['fixedPars'][np.isfinite(options['fixedPars'])])


# fig = plt.figure()
# figGrid = gridspec.GridSpec(ncols = 1, nrows = 2, figure = fig)

# fig = plt.figure(constrained_layout=True)
# spec = gridspec.GridSpec(ncols=1, nrows=2, figure=fig)

# ax1 = fig.add_subplot(spec[0,0]) # HR      
# ax2 = fig.add_subplot(spec[1,0]) # Number of trials
# ax3 = fig.add_subplot(figGrid[3,:]) # Number of ignored trials


# plt.figure()
ax1 = ps.psigniplot.plotPsych(res, showImediate=True)
# ax2 = ps.psigniplot.plotPsych(res, showImediate=True)
# ax1 = ps.psigniplot.plotMarginal(res,showImediate=True)





cls = [[0.5764705882352941, 0.47058823529411764, 0.3764705882352941],
       [0.5058823529411764, 0.4470588235294118, 0.7019607843137254],
       [0.2980392156862745, 0.4470588235294118, 0.6901960784313725]]

figure6A_height = (120 / 25.4) * sizeMult
figure6A_width = (180 / 25.4) * sizeMult

f, axs = plt.subplots(2, 3, sharey=False, sharex=False, gridspec_kw={'width_ratios': [1, 1, 1]},
                      constrained_layout=False, figsize=(figure6A_width, figure6A_height))
axs = axs.ravel()
sub_pos = [0, 1, 4, 1, 3, 5]

un_animals = ['dualina', 'elero', 'ivvy']
for mm in range(0, len(un_animals)):
    test = AMP_df[(AMP_df.animal == un_animals[mm]) & (AMP_df.stimulus == 'voc')]
    test = test[["level", "correct", "total"]].to_numpy()
    test = test.astype(int)

    options = dict()
    options['sigmoidName'] = 'norm'
    options['expType'] = '2AFC'
    options['fixedPars'] = np.nan * np.ones(5)
    # options['fixedPars'][2] = 0.01
    # options['fixedPars'][3] = 0.0

    res = ps.psignifit(test, options)
    ps.psigniplot.plotPsych(res,
                            xLabel=None,
                            yLabel=None,
                            plotAsymptote=True,
                            fontSize=10,
                            extrapolLength=0,
                            showImediate=False,
                            dataColor=cls[mm],
                            axisHandle=axs[mm])

for mm in range(0, len(un_animals)):
    test = AMP_df[(AMP_df.animal == un_animals[mm]) & (AMP_df.stimulus == 'voc')]
    test = test[["level", "correct", "total"]].to_numpy()
    test = test.astype(int)

    options = dict()
    options['sigmoidName'] = 'norm'
    options['expType'] = '2AFC'
    options['fixedPars'] = np.nan * np.ones(5)
    options['fixedPars'][2] = 0.01
    options['fixedPars'][3] = 0.0

    res = ps.psignifit(test, options)
    ps.psigniplot.plotPsych(res,
                            xLabel=None,
                            yLabel=None,
                            plotAsymptote=False,
                            fontSize=10,
                            extrapolLength=0,
                            showImediate=False,
                            dataColor=cls[mm],
                            axisHandle=axs[mm+3])