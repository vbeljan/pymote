import unittest
from pymote.networkgenerator import NetworkGenerator
from pymote.algorithm import Algorithm, NodeAlgorithm, NetworkAlgorithm,\
                             PymoteAlgorithmException
from pymote.network import PymoteNetworkError

def set_algorithms(net, algorithms):
    net.algorithms = algorithms
    

class SomeNodeAlgorithm(NodeAlgorithm):
    required_params = ('rp1',
                       'rp2',
                       'rp3')
    default_params = {'dp1':'dp1_value',
                      'dp2':'dp2_value',
                      'dp3':'dp3_value'}


class SomeNetworkAlgorithm(NetworkAlgorithm):
    default_params = {'dp1':'dp1_value',
                      'dp2':'dp2_value',
                      'dp3':'dp3_value'}

class SomeAlgorithmWhereDpIsRp(NetworkAlgorithm):
    required_params = ('rdp1',)
    default_params = {'rdp1':'dp1_value',}


class TestAlgorithmsSetter(unittest.TestCase):
    
    def setUp(self):
        net_gen = NetworkGenerator(100)
        self.net = net_gen.generate_random_network()
        self.algorithms_ok = ((SomeNodeAlgorithm,
                              {'rp1': 1,
                               'rp2': 2,
                               'rp3': 3,
                               }),
                
                              (SomeNetworkAlgorithm,
                              {}),
                              )
        self.check = [
                      (PymoteNetworkError, [(SomeNodeAlgorithm, {'rp1': 1, 'rp2': 2,'rp3': 3}),]),                         # wrong_format
                      (PymoteNetworkError, ((SomeNodeAlgorithm),)),                             # wrong_format
                      (PymoteNetworkError, ((Algorithm, {}),)),                                 # wrong_base_class
                      (PymoteAlgorithmException, ((SomeNodeAlgorithm,{'rp1': 1,}),)),           # missing_req_params
                      (PymoteAlgorithmException, ((SomeAlgorithmWhereDpIsRp,{'rdp1': 1,}),)),   # dp_is_rp
                      ]

                  
    def test_setter(self):
        """Test different algorithm initialization formats and params."""
        set_algorithms(self.net, self.algorithms_ok)
        for exc,alg in self.check:
            self.assertRaises(exc, set_algorithms, self.net, alg)


    def test_default_params(self):
        """Test default params."""
        self.net.algorithms = ((SomeNetworkAlgorithm,{'dp2': 'overriden_dp2_value',}),)
        self.assertTrue(self.net.algorithms[0].dp1=='dp1_value')
        self.assertTrue(self.net.algorithms[0].dp2=='overriden_dp2_value')
        self.assertTrue(self.net.algorithms[0].dp3=='dp3_value')

    
    
