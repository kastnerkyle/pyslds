from __future__ import division
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

import pyhsmm
from pyhsmm.basic.distributions import Regression, Gaussian
from autoregressive.distributions import AutoRegression

from states import HMMSLDSStates, HMMSLDSStatesEigen, HSMMSLDSStates, \
        HSMMSLDSStatesEigen, GeoHSMMSLDSStates

class _SLDSMixin(object):
    def __init__(self,dynamics_distns,emission_distns,init_dynamics_distns,**kwargs):
        assert all(isinstance(d,Gaussian) for d in init_dynamics_distns)
        assert all(isinstance(d,AutoRegression) for d in dynamics_distns)
        assert all(isinstance(d,Regression) for d in emission_distns)
        self.init_dynamics_distns = init_dynamics_distns
        self.dynamics_distns = dynamics_distns
        self.emission_distns = emission_distns
        super(_SLDSMixin,self).__init__(obs_distns=self.dynamics_distns,**kwargs)

    def resample_parameters(self):
        self.resample_init_dynamics_distns()
        self.resample_dynamics_distns()
        self.resample_emission_distns()
        super(_SLDSMixin,self).resample_parameters()

    def resample_init_dynamics_distns():
        for state, d in enumerate(self.init_dynamics_distns):
            d.resample([s.gaussian_states[0]
                for s in self.states_list if s.stateseq[0] == state])
        self._clear_caches()

    def resample_dynamics_distns(self):
        for state, d in enumerate(self.dynamics_distns):
            d.resample([s.strided_gaussian_states[s.stateseq[1:] == state]
                for s in self.states_list])
        self._clear_caches()

    def resample_emission_distns(self):
        for state, d in enumerate(self.emission_distns):
            d.resample([s.data[s.stateseq == state] for s in self.states_list])
        self._clear_caches()

    def resample_obs_distns(self):
        pass


class HMMSLDSPython(_SLDSMixin,pyhsmm.models.HMMPython):
    _states_class = HMMSLDSStates

class HMMSLDS(_SLDSMixin,pyhsmm.models.HMM):
    _states_class = HMMSLDSStatesEigen

class HSMMSLDSPython(_SLDSMixin,pyhsmm.models.HSMMPython):
    _states_class = HSMMSLDSStates

class HSMMSLDS(_SLDSMixin,pyhsmm.models.HSMM):
    _states_class = HSMMSLDSStatesEigen


class WeakLimitHDPHMMSLDS(_SLDSMixin,pyhsmm.models.WeakLimitHDPHMM):
    _states_class = HMMSLDSStatesEigen

class WeakLimitHDPHSMMSLDS(_SLDSMixin,pyhsmm.models.WeakLimitHDPHSMM):
    _states_class = HSMMSLDSStatesEigen


# TODO PossibleChangepoints classes

