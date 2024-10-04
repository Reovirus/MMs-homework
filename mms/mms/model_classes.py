import numpy as np
import math
import operator

from itertools import islice
from collections import deque

from .errors import DifferentAlphabetError

class BasicModel():
    def __init__(self, depth, pseudocounts=1):
        self.pc = pseudocounts
        self.depth = depth

    def fit(self, fit_data, alphabet=None):
        if not alphabet:
            alphabet = set(fit_data)
        l_alp = len(alphabet)
        alphabet = {i: j for i, j in enumerate(alphabet)}
        r_alp = {alphabet[i]: i for i in alphabet.keys()}
        k_mers = [np.zeros(shape=(l_alp,) * k) for k in range(1, self.depth + 2)]
        fs = r_alp[fit_data[0]]
        letters_q = deque([fs], maxlen=self.depth + 1)
        for i in islice(fit_data, 1, len(fit_data), 1):
            letters_q.append(r_alp[i])
            list_let = tuple(letters_q)
            for k, letter in enumerate(list_let):
                k_mers[k][list_let[k::-1]] += 1
        while len(letters_q) > 0:
            letters_q.popleft()
            list_let = tuple(letters_q)
            for k, letter in enumerate(list_let):
                k_mers[k][list_let[:k + 1]] += 1
        k_mers = [i + self.pc for i in k_mers]
        k_mers = [i / np.sum(i) for i in k_mers]
        zaebal_srany_yandex = 1
        for i, j in enumerate(k_mers):
            k_mers[i] = j / zaebal_srany_yandex
            zaebal_srany_yandex = j
        one_mers = [k_mers[0]/np.sum(k_mers[0], axis = -1)] 
        m_mers = [i/np.sum(i, axis = -1)[:, np.newaxis] for i in islice(k_mers, 1, self.depth + 2)]
        k_mers = one_mers + m_mers
        return FittedModel(fit_data, k_mers, alphabet, r_alp, self)

    def fit_predict(self, fit_data, alphabet=None):
        res = self.fit(fit_data, alphabet=alphabet)
        res2 = res.loglikelihood
        return res, res2

    def __str__(self):
        return f'''Markov model. Parameters:
        depth: {self.depth}
        pseudocounts: {self.pc}'''


class FittedModel():
    @staticmethod
    def calculate_aic(k, ll):
        return -2 * ll + 2 * k

    @staticmethod
    def calculate_bic(k, ll, n):
        return math.log(n) * k - 2 * ll

    def __init__(self, fit_data, params, states, r_states, model):
        self._model = model
        self._depth = self._model.depth
        self._states = states
        self._r_states = r_states
        self._params = params
        self._fit_data = fit_data
        ll = self.predict_prob(fit_data)
        pn = sum([np.product(i.shape) for i in params])
        n = len(fit_data) - model.depth
        self.loglikelihood = ll
        self.parameters_num = pn
        self.aic = self.calculate_aic(pn, ll)
        self.bic = self.calculate_bic(pn, ll, n)
        
    def predict_prob(self, data):
        ll = 0
        if data[0] not in self._r_states.keys():
            raise DifferentAlphabetError(data[0])
        fs = self._r_states[data[0]]
        letters_q = deque([fs], maxlen=self._depth + 1)
        for i in islice(data, 1, len(data), 1):
            if i not in self._r_states.keys():
                raise DifferentAlphabetError(i)
            letters_q.append(self._r_states[i])
            list_let = tuple(letters_q)
            pr = self._params[len(list_let)-1][list_let[::-1]]
            if pr == 0:
                return float('-inf')
            ll += math.log(pr)
        return ll

    def generate_seq(self, seq_len):
        letters_q = deque(maxlen=self._depth)
        lets_to_choice = tuple(
            map(lambda x: x[0],
                sorted(self._r_states.items(), key=operator.itemgetter(1)))
        )
        for i in range(seq_len):
            list_let = tuple(letters_q)
            p = self._params[len(list_let)][(slice(None),) + tuple(list_let[::-1])]
            p = p/np.sum(p)
            letter = np.random.choice(lets_to_choice, p=p)
            letters_q.append(self._r_states[letter])
            yield letter

    def __str__(self):
        return f'''Fitted MM:
        Basic model: {self._model}
        Last counted aic: {round(self.aic, 3)} 
        Last counted bic: {round(self.bic, 3)}
        Last counted LogLikelihood: {round(self.loglikelihood, 3)}
        Model fit data: {self._fit_data[:min(len(self._fit_data), 20)]}...
        Length model fit data: {len(self._fit_data)}
        Number of model parameters: {self.parameters_num}
        Model states: {self._r_states.keys()}
        Don't worry, be happy)))'''

    def log_likelihood_counter(self, data):
        return self.predict_prob(data)

    def aic_counter(self, data):
        LL = self.predict_prob(data)
        return self.calculate_aic(self.parameters_num, LL)

    def bic_counter(self, data):
        LL = self.predict_prob(data)
        n = len(self._fit_data) - self._depth
        return self.calculate_bic(self.parameters_num, LL, n)


