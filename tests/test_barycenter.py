import os
import sys
import time
import tempfile
import pytest
import logging
from pathlib import Path

from dtaidistance import dtw_barycenter, util_numpy
import dtaidistance.dtw_visualisation as dtwvis
from dtaidistance.exceptions import MatplotlibException, PyClusteringException
from dtaidistance.clustering.kmeans import KMeans


logger = logging.getLogger("be.kuleuven.dtai.distance")
directory = None
numpyonly = pytest.mark.skipif("util_numpy.test_without_numpy()")
scipyonly = pytest.mark.skipif("util_numpy.test_without_scipy()")


@pytest.mark.skip
@numpyonly
def test_pair():

    with util_numpy.test_uses_numpy() as np:
        s = np.array([
            [0.5, 1, 2, 3, 2.0, 2.1, 1.0, 0, 0, 0],
            [0.4, 0, 1, 1.5, 1.9, 2.0, 0.9, 1, 0, 0]
        ])
        # s = np.array([
        #     [5.4407042e-01, 6.5786304e-01, 6.1123908e-01, 5.4541312e-01, 5.3215608e-01, 5.9301252e-01, 5.9528021e-01, 5.3827698e-01, 5.6342901e-01, 5.9595647e-01, 6.3291485e-01, 5.8464636e-01, 6.2318725e-01, 6.0595466e-01, 5.9037231e-01, 6.2702137e-01, 6.1348560e-01, 6.2305276e-01, 5.4601808e-01, 6.4113615e-01, 5.4939481e-01, 6.1069654e-01, 5.7797370e-01, 6.3566551e-01, 5.7421817e-01, 6.0636056e-01, 6.3805334e-01, 6.4059697e-01, 6.0581139e-01, 6.5486549e-01, 6.2933728e-01, 6.7354635e-01, 6.4083011e-01, 6.7106754e-01, 5.9539175e-01, 5.8942609e-01, 6.1587013e-01, 6.6703825e-01, 6.0380075e-01, 6.3386067e-01, 6.4719272e-01, 6.4482981e-01, 6.4368627e-01, 6.2349955e-01, 5.6237133e-01, 6.1063165e-01, 6.0773194e-01, 6.4240876e-01, 5.7791595e-01, 6.8620718e-01, 6.1297880e-01, 1.0087818e+00, 2.3082535e+00, 3.4865161e+00, 3.8273665e+00, 3.8177745e+00, 1.0119979e+00, -1.2480659e+00, -1.8793527e+00, -1.9483470e+00, -1.9013292e+00, -1.9191206e+00, -1.9221467e+00, -1.9814806e+00, -1.9719053e+00, -1.9875261e+00, -1.8793638e+00, -1.9005814e+00, -1.8825048e+00, -1.8736002e+00, -1.8876155e+00, -1.9502441e+00, -1.8904222e+00, -1.8784054e+00, -1.8606558e+00, -1.9099004e+00, -1.8661716e+00, -1.8816032e+00, -1.8314015e+00, -1.7828515e+00, -1.7619036e+00, -1.8435448e+00, -1.8210940e+00, -1.7934786e+00, -1.7384911e+00, -1.7141641e+00, -1.7810861e+00, -1.7017178e+00, -1.7586494e+00, -1.6361580e+00, -1.6761555e+00, -1.6352849e+00, -1.6648909e+00, -1.6537056e+00, -1.5992698e+00, -1.5857011e+00, -1.5706887e+00, -1.5565333e+00, -1.5257045e+00, -1.5343949e+00, -1.5144240e+00, -1.4585244e+00, -1.4340508e+00, -1.3994088e+00, -1.4395239e+00, -1.3883845e+00, -1.3141078e+00, -1.2873144e+00, -1.2437876e+00, -1.2662198e+00, -1.2174011e+00, -1.1404096e+00, -1.0779149e+00, -1.0360995e+00, -1.0235959e+00, -9.4192680e-01, -9.6460812e-01, -9.2692898e-01, -8.0692488e-01, -8.1502916e-01, -8.0227687e-01, -7.7763514e-01, -7.1609000e-01, -7.1871558e-01, -5.9853322e-01, -6.2256531e-01, -6.4287218e-01, -6.1775796e-01, -5.5449064e-01, -5.1017090e-01, -5.0237049e-01, -3.8755927e-01, -4.0832809e-01, -3.6083551e-01, -3.3675164e-01, -2.7108165e-01, -2.3104480e-01, -2.5503431e-01, -1.9585961e-01, -1.3165326e-01, -9.1146626e-02, -1.9168974e-02, -1.3373473e-01, -7.6407845e-02, -6.3702210e-02, -5.8617472e-02, -1.0619203e-02, 7.1343850e-02, 2.1105735e-02, 1.0268053e-01, 1.1936396e-01, 1.1838773e-01, 1.5021707e-01, 1.4664151e-01, 1.4904700e-01, 1.6199376e-01, 2.4104677e-01, 2.3775815e-01, 2.7550593e-01, 3.1824048e-01, 3.7817589e-01, 3.7694541e-01, 3.0430703e-01, 3.5849188e-01, 2.9257194e-01, 3.3785668e-01, 3.7219016e-01, 3.7010148e-01, 4.0480926e-01, 3.7049106e-01, 4.1597004e-01, 4.0382502e-01, 4.3679156e-01, 4.0612548e-01, 4.0152885e-01, 4.7647383e-01, 4.4169304e-01, 4.4384292e-01, 3.8545218e-01, 4.6372423e-01, 4.4630043e-01, 4.4484963e-01, 4.8374203e-01, 4.8585592e-01, 5.3424775e-01, 5.3889814e-01, 4.6434472e-01, 5.1374644e-01, 4.9446973e-01, 5.3983401e-01, 5.2213212e-01, 5.1881301e-01, 5.2453233e-01, 5.6395751e-01, 5.5313703e-01, 6.0116005e-01, 5.5151348e-01, 5.4741656e-01, 5.4669622e-01, 5.8659053e-01, 5.2656235e-01, 5.4569127e-01, 5.7221179e-01, 5.2088122e-01, 5.8197830e-01, 5.7022402e-01, 5.6669003e-01, 5.7069312e-01, 5.6999052e-01, 5.4572128e-01, 5.9778768e-01, 5.7268841e-01, 5.7180281e-01, 6.3555668e-01, 5.0059640e-01, 5.5195177e-01, 5.9130039e-01, 5.5103119e-01, 5.7287569e-01, 5.5867501e-01, 5.9223111e-01, 5.8432069e-01, 5.7091733e-01, 6.0559221e-01, 6.5693579e-01, 5.6511058e-01, 5.5240516e-01, 5.6491058e-01, 5.8311869e-01, 6.3398184e-01, 5.7997700e-01, 6.2535219e-01, 5.8981952e-01, 5.7572385e-01, 6.0549305e-01, 5.3555521e-01, 5.4941540e-01, 5.5352685e-01, 5.9538265e-01, 5.3455956e-01, 5.3054529e-01, 6.1195102e-01, 5.8604957e-01, 5.4530951e-01, 5.5091084e-01, 5.6394117e-01, 6.0954467e-01, 5.3654038e-01, 5.9055258e-01, 5.5313359e-01, 5.8818908e-01, 5.3334192e-01, 5.8794384e-01, 5.8296638e-01, 5.9814783e-01, 6.0032051e-01, 5.6657579e-01, 6.7193951e-01, 6.2128079e-01, 5.5514667e-01, 5.8124140e-01, 6.7463871e-01, 5.7606997e-01, 6.3720999e-01, 5.7822404e-01, 5.8822587e-01, 5.7788588e-01, 5.9806934e-01, 5.8369488e-01, 6.0287742e-01, 5.5426348e-01, 5.1414728e-01, 6.0377304e-01, 5.9633124e-01, 5.8322427e-01],
        #     [5.4137206e-01, 5.7190786e-01, 5.6214670e-01, 5.2095091e-01, 5.2749375e-01, 6.0404306e-01, 5.4052105e-01, 5.8038292e-01, 5.0058210e-01, 5.9781245e-01, 5.5531829e-01, 5.0399817e-01, 4.8721503e-01, 5.2919197e-01, 5.7732146e-01, 5.8306679e-01, 5.6387021e-01, 5.1736838e-01, 5.5365038e-01, 6.3540910e-01, 5.2845206e-01, 5.6114973e-01, 5.0572623e-01, 6.4666921e-01, 5.6247629e-01, 5.6586631e-01, 5.7505220e-01, 6.1367060e-01, 5.9094675e-01, 5.4806871e-01, 5.3635967e-01, 5.8288635e-01, 6.2479649e-01, 5.4263060e-01, 5.3727177e-01, 5.4420961e-01, 4.6516908e-01, 5.1660881e-01, 5.6632066e-01, 5.8851816e-01, 5.5663496e-01, 5.3749507e-01, 6.2990795e-01, 5.2720783e-01, 5.8189400e-01, 6.1033741e-01, 5.6246110e-01, 5.9735452e-01, 5.8936942e-01, 6.2465823e-01, 5.7547395e-01, 5.7821937e-01, 6.3206557e-01, 5.9249883e-01, 5.6148297e-01, 5.9005716e-01, 5.7541260e-01, 6.4415288e-01, 6.1059152e-01, 6.0653983e-01, 6.8802537e-01, 1.0147607e+00, 2.3145332e+00, 3.5409618e+00, 3.8384987e+00, 3.8225459e+00, 3.1880896e+00, -1.3082260e+00, -1.9498738e+00, -1.9228263e+00, -2.0425930e+00, -1.9294838e+00, -2.0234096e+00, -1.9554894e+00, -1.9346159e+00, -1.9389827e+00, -1.9903105e+00, -1.9996996e+00, -1.9364940e+00, -1.9481327e+00, -1.9478419e+00, -1.9529609e+00, -1.8885611e+00, -1.9274720e+00, -1.9067925e+00, -1.8492225e+00, -1.8022711e+00, -1.8571755e+00, -1.8731676e+00, -1.7942706e+00, -1.8352960e+00, -1.8129494e+00, -1.8213582e+00, -1.7435004e+00, -1.7834703e+00, -1.6825393e+00, -1.6991139e+00, -1.6781857e+00, -1.7190823e+00, -1.6429358e+00, -1.5756199e+00, -1.6127048e+00, -1.6271342e+00, -1.5669044e+00, -1.5274913e+00, -1.5603284e+00, -1.5284419e+00, -1.4536210e+00, -1.4746732e+00, -1.4013397e+00, -1.3672767e+00, -1.4367848e+00, -1.3940244e+00, -1.3391982e+00, -1.3087654e+00, -1.2541147e+00, -1.2509465e+00, -1.1480202e+00, -1.1584576e+00, -1.0661748e+00, -1.0838297e+00, -1.0605984e+00, -1.0545557e+00, -9.8054161e-01, -9.7516375e-01, -9.0965554e-01, -9.3395351e-01, -8.3288487e-01, -8.7299559e-01, -7.9129969e-01, -7.9793562e-01, -7.7723834e-01, -6.8966425e-01, -6.8607855e-01, -6.2673536e-01, -6.0840173e-01, -5.7696618e-01, -5.3084902e-01, -5.2748290e-01, -4.3871482e-01, -4.9210561e-01, -4.3981229e-01, -3.2472595e-01, -3.3753481e-01, -2.8367354e-01, -2.7158593e-01, -2.1485086e-01, -2.3176371e-01, -1.5325167e-01, -1.9440216e-01, -1.0415893e-01, -2.4629932e-02, -4.5354485e-02, -3.6301485e-02, 2.0418909e-02, 1.0027844e-01, 8.8132967e-02, 1.2071415e-01, 2.1155213e-02, 9.2120760e-02, 9.1224315e-02, 1.5286046e-01, 1.8740585e-01, 2.0764562e-01, 2.2897012e-01, 1.6721991e-01, 2.4065580e-01, 3.4694248e-01, 1.9462176e-01, 3.1338695e-01, 2.7861734e-01, 3.0417210e-01, 2.9476327e-01, 3.3008070e-01, 3.3258469e-01, 3.5294907e-01, 3.9032386e-01, 3.7415578e-01, 3.7775534e-01, 3.8227615e-01, 4.1445601e-01, 3.7363077e-01, 4.1116205e-01, 4.1717600e-01, 3.9964844e-01, 4.0182791e-01, 3.9896304e-01, 4.6554637e-01, 4.3096288e-01, 4.7565329e-01, 4.7633896e-01, 4.7028428e-01, 4.7656642e-01, 4.2424559e-01, 5.8662101e-01, 4.7144488e-01, 5.0448089e-01, 5.3749633e-01, 4.8611158e-01, 4.8701654e-01, 4.3499943e-01, 4.9157679e-01, 4.8762772e-01, 4.5786105e-01, 5.5207149e-01, 5.5383578e-01, 5.1621105e-01, 5.3562938e-01, 5.3433077e-01, 4.8763878e-01, 5.7401483e-01, 5.9950807e-01, 5.0169837e-01, 5.7199426e-01, 5.7622109e-01, 4.9258166e-01, 5.6401024e-01, 5.8920374e-01, 5.3761485e-01, 5.5162361e-01, 5.0071393e-01, 5.1108397e-01, 5.0957378e-01, 5.0310495e-01, 5.3417705e-01, 5.6347038e-01, 5.5544608e-01, 5.0517001e-01, 5.4170490e-01, 5.5768119e-01, 6.1605762e-01, 5.2684445e-01, 5.6026650e-01, 4.9761039e-01, 5.7826229e-01, 4.9039267e-01, 5.5444683e-01, 5.5327922e-01, 5.7359620e-01, 5.3077316e-01, 5.3897197e-01, 5.1796237e-01, 5.2855358e-01, 5.1671037e-01, 5.9622412e-01, 6.1819121e-01, 5.7296705e-01, 5.5145456e-01, 5.0723387e-01, 5.5503681e-01, 5.4870379e-01, 5.1063454e-01, 5.0387017e-01, 5.2631419e-01, 5.6185307e-01, 5.5370395e-01, 5.5088067e-01, 5.0169928e-01, 5.5612542e-01, 5.0657189e-01, 5.2409481e-01, 5.2284798e-01, 5.9391410e-01, 5.6873552e-01, 5.4726018e-01, 5.8600009e-01, 6.2647159e-01, 6.0961628e-01, 5.5428459e-01, 5.3946531e-01, 5.3351539e-01, 5.5775245e-01, 5.0782548e-01, 5.1376850e-01, 5.2813152e-01]
        #     # [6.4599204e-01, 5.8009481e-01, 6.1606415e-01, 6.1071098e-01, 6.1859521e-01, 6.1274416e-01, 5.6404645e-01, 6.2055753e-01, 5.3794194e-01, 6.3609172e-01, 6.0945935e-01, 5.5504533e-01, 5.6271107e-01, 5.5380374e-01, 6.0596144e-01, 5.6616977e-01, 6.2227118e-01, 5.9801028e-01, 6.3691294e-01, 6.5189082e-01, 5.6928840e-01, 5.9739031e-01, 6.2144372e-01, 5.5423491e-01, 6.1966872e-01, 5.9997056e-01, 5.9309788e-01, 5.9097654e-01, 6.6743532e-01, 6.2585670e-01, 6.4283290e-01, 6.1084533e-01, 6.0601246e-01, 6.5786714e-01, 6.1675659e-01, 5.8428597e-01, 5.7911015e-01, 6.1814446e-01, 6.5467570e-01, 6.2327132e-01, 6.1820943e-01, 6.7392847e-01, 6.0636712e-01, 6.4118791e-01, 6.1282180e-01, 5.8978860e-01, 6.7797797e-01, 7.1699196e-01, 1.0117528e+00, 2.2726181e+00, 3.4698210e+00, 3.8304702e+00, 3.8196334e+00, 3.2619192e+00, 1.0205306e+00, -1.2214097e+00, -1.7390308e+00, -1.8675370e+00, -1.8828808e+00, -1.9184427e+00, -1.8976587e+00, -1.8388410e+00, -1.9245830e+00, -1.8400097e+00, -1.8427256e+00, -1.8667457e+00, -1.7722318e+00, -1.8766957e+00, -1.8453581e+00, -1.7864935e+00, -1.8080930e+00, -1.8282433e+00, -1.7986122e+00, -1.8028363e+00, -1.7642486e+00, -1.7948663e+00, -1.7103064e+00, -1.7080497e+00, -1.7272006e+00, -1.7985161e+00, -1.7146590e+00, -1.6627331e+00, -1.7296342e+00, -1.6556524e+00, -1.6513342e+00, -1.6131169e+00, -1.7312787e+00, -1.6266636e+00, -1.5899808e+00, -1.5773010e+00, -1.5944990e+00, -1.5456211e+00, -1.5613456e+00, -1.5233710e+00, -1.4942540e+00, -1.4886351e+00, -1.4576059e+00, -1.4864930e+00, -1.4694330e+00, -1.3648873e+00, -1.3591080e+00, -1.3182067e+00, -1.2946644e+00, -1.3112402e+00, -1.3143085e+00, -1.3002664e+00, -1.2457161e+00, -1.1826555e+00, -1.1478405e+00, -1.1393425e+00, -1.1818354e+00, -1.0905381e+00, -1.1134195e+00, -1.0568539e+00, -1.0096635e+00, -9.9456280e-01, -9.4615698e-01, -9.6722803e-01, -8.9581465e-01, -8.5329021e-01, -8.0415690e-01, -7.8231323e-01, -7.5747249e-01, -6.9181889e-01, -6.6083636e-01, -7.1778461e-01, -6.3738983e-01, -6.5927655e-01, -5.6273476e-01, -5.4926631e-01, -4.5594428e-01, -4.7428247e-01, -4.5613309e-01, -3.5143676e-01, -3.8044406e-01, -2.8879577e-01, -2.9708038e-01, -3.0873051e-01, -2.5243644e-01, -1.8748736e-01, -1.2681093e-01, -2.0259857e-01, -1.0690861e-01, -1.5195203e-01, -9.5526833e-02, -1.2628887e-01, -3.7242313e-02, -2.3766929e-02, 4.9910492e-02, -8.1735932e-03, 2.0913314e-02, 4.7210633e-02, 6.9717876e-02, 9.9995072e-02, 1.4030909e-01, 1.7352288e-01, 1.3181121e-01, 2.1229484e-01, 1.8366278e-01, 2.1271492e-01, 2.5346393e-01, 1.9855797e-01, 2.6804769e-01, 3.0556837e-01, 3.1518281e-01, 2.9710565e-01, 3.0082077e-01, 3.3285803e-01, 3.6951418e-01, 4.2511496e-01, 3.9051354e-01, 3.3237006e-01, 3.5956342e-01, 3.1772785e-01, 3.8804607e-01, 5.0094976e-01, 4.0347956e-01, 4.5050806e-01, 4.6945845e-01, 4.2596043e-01, 4.1725340e-01, 4.5567870e-01, 4.5973729e-01, 5.3553104e-01, 5.1218158e-01, 4.8497334e-01, 4.8960637e-01, 4.9621481e-01, 4.2483759e-01, 5.0125449e-01, 5.9456671e-01, 5.3640062e-01, 5.0674797e-01, 4.9412346e-01, 5.2386933e-01, 5.6600273e-01, 5.3306648e-01, 5.2529226e-01, 5.1029361e-01, 4.9331903e-01, 5.0693239e-01, 5.1490854e-01, 5.6811201e-01, 5.7341867e-01, 5.7849439e-01, 5.2703544e-01, 5.5386148e-01, 5.8900738e-01, 5.2480575e-01, 5.6596905e-01, 5.2460600e-01, 5.7997364e-01, 6.0908832e-01, 5.8077073e-01, 5.3383030e-01, 6.1826030e-01, 5.1965089e-01, 5.9340016e-01, 5.7225953e-01, 5.7117192e-01, 5.9511521e-01, 5.1910997e-01, 6.1595223e-01, 5.4929296e-01, 5.6567802e-01, 5.6199596e-01, 5.3658150e-01, 5.3073311e-01, 5.0845425e-01, 5.2633724e-01, 6.2759642e-01, 6.0729269e-01, 6.2850204e-01, 5.5503403e-01, 6.4417801e-01, 5.9421709e-01, 5.4251513e-01, 6.3298142e-01, 6.3688128e-01, 5.5519935e-01, 6.1786844e-01, 6.0465278e-01, 5.7177749e-01, 6.0314338e-01, 5.4351271e-01, 6.1584186e-01, 5.4914328e-01, 6.5036590e-01, 5.6558653e-01, 6.4837370e-01, 5.4398120e-01, 5.8070264e-01, 6.1290281e-01, 6.1060894e-01, 5.5958162e-01, 6.4370850e-01, 5.5792888e-01, 6.4400948e-01, 6.3940254e-01, 5.1763647e-01, 6.1151425e-01, 6.1301439e-01, 5.7474884e-01, 5.9040337e-01, 5.9723567e-01, 5.7600326e-01, 6.1296410e-01, 5.3629869e-01, 6.3200031e-01, 6.4605875e-01, 6.6053779e-01, 6.1220579e-01, 5.8413897e-01, 6.4785446e-01, 5.9291996e-01]
        # ])

        t = s.shape[1]
        # c = np.array([0.0, 0.5, 1.5, 2.5, 2, 2, 1, 0.5, 0, 0])
        # c = np.zeros((s.shape[1],))
        c = s[0, :]
        max_it = 1
        avgs = [c]

        tic = time.perf_counter()
        avg, avgs = dtw_barycenter.dba_loop(s, c, max_it=max_it, thr=0.0001, keep_averages=True,
                                            use_c=False)
        toc = time.perf_counter()
        print(f'DBA_loop: {toc - tic:0.4f} sec')
        print(avg)

        # tic = time.perf_counter()
        # for it in range(max_it):
        #     avg = dtw_barycenter.dba(s, c, use_c=True)
        #     avgs.append(avg)
        #     c = avg
        # toc = time.perf_counter()
        # print(f'DBA: {toc - tic:0.4f} sec')

        if directory and not dtwvis.test_without_visualization():
            try:
                import matplotlib.pyplot as plt
            except ImportError:
                raise MatplotlibException("No matplotlib available")
            fig, ax = plt.subplots(nrows=max_it, ncols=1)
            fn = directory / "test_pair_barycenter.png"
            for it in range(len(avgs)):
                dtwvis.plot_average(s[0, :], s[1, :], avgs[it], None, None, ax=ax[it])
                ax[it].set_title(f'Iteration {it}')
            fig.savefig(str(fn))
            plt.close()


@numpyonly
def test_trace():
    with util_numpy.test_uses_numpy() as np:
        rsrc_fn = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'rsrc', 'Trace_TRAIN.txt')
        data = np.loadtxt(rsrc_fn)
        labels = data[:, 0]
        # series = data[:, 1:]
        series = data[labels == 1, 1:][:2,:].copy()
        # c = series[0, :]
        print(type(series))
        print(series.shape)

        tic = time.perf_counter()
        avg = dtw_barycenter.dba_loop(series, c=None, max_it=100, thr=0.000001,
                                      nb_initial_samples=4, use_c=True)
        toc = time.perf_counter()
        print(f'DBA: {toc - tic:0.4f} sec')

        if directory and not dtwvis.test_without_visualization():
            try:
                import matplotlib.pyplot as plt
            except ImportError:
                raise MatplotlibException("No matplotlib available")
            fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10,4))
            fn = directory / "test_trace_barycenter.png"

            for serie in series:
                ax[0].plot(serie, alpha=0.5)
            ax[1].plot(avg)

            fig.savefig(str(fn))
            plt.close()


@numpyonly
def test_trace_mask():
    with util_numpy.test_uses_numpy() as np:
        rsrc_fn = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'rsrc', 'Trace_TRAIN.txt')
        data = np.loadtxt(rsrc_fn)
        labels = data[:, 0]
        series = data[:, 1:]
        mask = np.full((len(labels),), False, dtype=bool)
        mask[:] = (labels == 1)
        # c = series[0, :]
        print(type(series))
        print(series.shape)

        tic = time.perf_counter()
        avg = dtw_barycenter.dba_loop(series, c=None, max_it=100, thr=0.000001, mask=mask, use_c=True)
        toc = time.perf_counter()
        print(f'DBA: {toc - tic:0.4f} sec')

        if directory and not dtwvis.test_without_visualization():
            try:
                import matplotlib.pyplot as plt
            except ImportError:
                raise MatplotlibException("No matplotlib available")
            fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10,4))
            fn = directory / "test_trace_barycenter.png"

            for idx, serie in enumerate(series):
                if mask[idx]:
                    ax[0].plot(serie, alpha=0.5)
            ax[1].plot(avg)

            fig.savefig(str(fn))
            plt.close()


@numpyonly
def test_trace_kmeans():
    with util_numpy.test_uses_numpy() as np:
        k = 4
        max_it = 10
        max_dba_it = 20
        rsrc_fn = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'rsrc', 'Trace_TRAIN.txt')
        data = np.loadtxt(rsrc_fn)
        labels = data[:, 0]
        series = data[:, 1:]
        mask = np.full((len(labels),), False, dtype=bool)
        mask[:] = (labels == 1)
        # c = series[0, :]
        print(type(series))
        print(series.shape)
        window = int(series.shape[1] * 1.0)

        # Z-normalize sequences
        series = (series - series.mean(axis=1)[:, None]) / series.std(axis=1)[:, None]
        # Align start and/or end values
        avg_start = series[:, :20].mean(axis=1)
        avg_end = series[:, 20:].mean(axis=1)
        series = (series - avg_end[:, None])

        # Perform k-means
        tic = time.perf_counter()
        model = KMeans(k=k, max_it=max_it, max_dba_it=max_dba_it, drop_stddev=1,
                       dists_options={"window": window},
                       initialize_with_kmedoids=True)
        try:
            cluster_idx, performed_it = model.fit(series, use_c=True, use_parallel=False)
        except PyClusteringException:
            return
        toc = time.perf_counter()
        print(f'DBA ({performed_it} iterations: {toc - tic:0.4f} sec')

        if directory and not dtwvis.test_without_visualization():
            try:
                import matplotlib.pyplot as plt
            except ImportError:
                raise MatplotlibException("No matplotlib available")
            fig, ax = plt.subplots(nrows=k, ncols=2, figsize=(10,4),
                                   sharex='all', sharey='all')
            fn = directory / "test_trace_barycenter.png"

            all_idx = set()
            for ki in range(k):
                ax[ki, 0].plot(model.means[ki])
                for idx in cluster_idx[ki]:
                    ax[ki, 1].plot(series[idx], alpha=0.3)
                    if idx in all_idx:
                        raise Exception(f'Series in multiple clusters: {idx}')
                    all_idx.add(idx)
            assert(len(all_idx) == len(series))
            fig.savefig(str(fn))
            plt.close()

            fig, ax = plt.subplots(nrows=k, ncols=1, figsize=(5, 4),
                                   sharex='all', sharey='all')
            fn = directory / "test_trace_barycenter_solution.png"
            for i in range(len(labels)):
                ax[int(labels[i]) - 1].plot(series[i], alpha=0.3)
            fig.savefig(str(fn))
            plt.close()


if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    directory = Path(os.environ.get('TESTDIR', Path(__file__).parent))
    print(f"Saving files to {directory}")
    # test_pair()
    test_trace()
    # test_trace_mask()
    # test_trace_kmeans()
