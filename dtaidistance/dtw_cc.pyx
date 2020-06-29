"""
dtaidistance.dtw_cc
~~~~~~~~~~~~~~~~~~~

Dynamic Time Warping (DTW), C implementation.

:author: Wannes Meert
:copyright: Copyright 2017-2020 KU Leuven, DTAI Research Group.
:license: Apache License, Version 2.0, see LICENSE for details.

"""
from cpython cimport array
import array
from libc.stdlib cimport abort, malloc, free, abs, labs
from libc.stdint cimport intptr_t

cimport dtaidistancec


cdef class DTWBlock:
    cdef  dtaidistancec.DTWBlock _block

    def __cinit__(self):
        pass

    def __init__(self, rb, re, cb, ce):
        self._block.rb = rb
        self._block.re = re
        self._block.cb = cb
        self._block.ce = ce

    @property
    def rb(self):
        return self._block.rb

    @property
    def re(self):
        return self._block.re

    @property
    def cb(self):
        return self._block.cb

    @property
    def ce(self):
        return self._block.ce

    def __str__(self):
        return f'DTWBlock(rb={self.rb},re={self.re},cb={self.cb},ce={self.ce})'


cdef class DTWSettings:
    cdef dtaidistancec.DTWSettings _settings

    def __cinit__(self):
        pass

    def __init__(self, **kwargs):
        self._settings = dtaidistancec.dtw_default_settings()
        if "window" in kwargs:
            if kwargs["window"] is None:
                self._settings.window = 0
            else:
                self._settings.window = kwargs["window"]
        if "max_dist" in kwargs:
            if kwargs["max_dist"] is None:
                self._settings.max_dist = 0
            else:
                self._settings.max_dist = kwargs["max_dist"]
        if "max_step" in kwargs:
            if kwargs["max_step"] is None:
                self._settings.max_step = 0
            else:
                self._settings.max_step = kwargs["max_step"]
        if "max_length_diff" in kwargs:
            if kwargs["max_length_diff"] is None:
                self._settings.max_length_diff = 0
            else:
                self._settings.max_length_diff = kwargs["max_length_diff"]
        if "penalty" in kwargs:
            if kwargs["penalty"] is None:
                self._settings.penalty = 0
            else:
                self._settings.penalty = kwargs["penalty"]
        if "psi" in kwargs:
            if kwargs["psi"] is None:
                self._settings.psi = 0
            else:
                self._settings.psi = kwargs["psi"]

    @property
    def window(self):
        return self._settings.window

    @property
    def max_dist(self):
        return self._settings.max_dist

    @property
    def max_step(self):
        return self._settings.max_step

    @property
    def max_length_diff(self):
        return self._settings.max_length_diff

    @property
    def penalty(self):
        return self._settings.penalty

    @property
    def psi(self):
        return self._settings.psi

    def __str__(self):
        return (
            "DTWSettings {\n"
            f"  window = {self.window}\n"
            f"  max_dist = {self.max_dist}\n"
            f"  max_step = {self.max_step}\n"
            f"  max_length_diff = {self.max_length_diff}\n"
            f"  penalty = {self.penalty}\n"
            f"  psi = {self.psi}\n"
            "}")

cdef class DTWSeriesPointers:
    cdef double **_ptrs = NULL
    cdef int **_lengths = NULL
    cdef int _nb_ptrs = 0

    def __cinit__(self, int nb_series):
        self._ptrs = <double **> malloc(nb_series * sizeof(double*))
        self._nb_ptrs = nb_series
        if not self._ptrs:
            self._ptrs = NULL
            raise MemoryError()
        self._lengths = <double **> malloc(nb_series * sizeof(int*))
        if not self._lengths:
            self._lengths = NULL
            raise MemoryError()

    def __dealloc__(self):
        if self._ptrs is not NULL:
            free(self._ptrs)
        if self._lengths is not NULL:
            free(self._lengths)

    @property
    def ptrs(self):
        return self._ptrs

    @property
    def lengths(self):
        return self._lengths

    @property
    def nb_ptrs(self):
        return self._nb_ptrs


cdef class DTWSeriesMatrix:
    cdef double[:,:] _data = NULL

    def __cinit__(self, double[:, :] data):
        self._data = data

    @property
    def matrix(self):
        return self._data

    @property
    def nb_rows(self):
        return self._data.shape[0]

    @property
    def nb_cols(self):
        return self._data.shape[1]


def dtw_series_from_data(data):
    if isinstance(data, list) or isinstance(data, set) or isinstance(data, tuple):
        ptrs = DTWSeriesPointers(len(data), diff_lengths=True)
        cdef intptr_t ptr
        for i in range(len(data)):
            ptr = data[i].ctypes.data  # uniform for memoryviews and numpy
            ptrs._ptrs[i] = <double *> ptr
            ptrs._lengths[i] = len(data[i])
        return ptrs
    try:
        ptrs = DTWSeriesMatrix(data)
        return ptrs
    except ValueError:
        raise ValueError(f"Cannot convert data of type {type(data)}")


def distance(double[:] s1, double[:] s2, **kwargs):
    """DTW distance.

    Assumes C-contiguous arrays.

    See distance().
    :param s1: First sequence (buffer of doubles)
    :param s2: Second sequence (buffer of doubles)
    :param kwargs: Settings (see DTWSettings)
    """
    # Assumes C contiguous
    settings = DTWSettings(**kwargs)
    return dtaidistancec.dtw_distance(&s1[0], len(s1), &s2[0], len(s2), &settings._settings)


def warping_paths(double[:, :] dtw, double[:] s1, double[:] s2, **kwargs):
    # Assumes C contiguous
    settings = DTWSettings(**kwargs)
    return dtaidistancec.dtw_warping_paths(&dtw[0, 0], &s1[0], len(s1), &s2[0], len(s2),
                                           True, True, &settings._settings)


def distance_matrix(cur, block=None, **kwargs):
    """Compute a distance matrix between all sequences given in `cur`.
    This method calls a pure c implementation of the dtw computation that
    avoids the GIL.

    Assumes C-contiguous arrays.

    :param cur: DTWSeriesMatrix or DTWSeriesPointers
    :param block: see DTWBlock
    :param kwargs: Settings (see DTWSettings)
    :return: The distance matrix as a list representing the triangular matrix.
    """
    cdef int length = 0
    cdef int block_rb=0
    cdef int block_re=0
    cdef int block_cb=0
    cdef int block_ce=0
    cdef ri = 0
    if block is not None and block != 0.0:
        block_rb = block[0][0]
        block_re = block[0][1]
        block_cb = block[1][0]
        block_ce = block[1][1]

    settings = DTWSettings(**kwargs)
    block = DTWBlock(rb=block_rb, re=block_re, cb=block_cb, ce=block_ce)
    length = dtaidistancec.dtw_distances_length(block._block, len(cur))

    cdef array.array dists = array.array('d')
    dists.resize(length)

    if isinstance(cur, DTWSeriesMatrix) or isinstance(cur, DTWSeriesPointers):
        pass
    elif cur.__class__.__name__ == "SeriesContainer":
        cur = cur.c_data()
    else:
        cur = dtw_series_from_data(cur)

    if isinstance(cur, DTWSeriesPointers):
        dtaidistancec.dtw_distances_ptrs(cur.ptrs, cur.nb_ptrs, cur.lengths,
                                         dists.as_doubles, &block._block, &settings._settings)
    elif isinstance(cur, DTWSeriesMatrix):
        dtaidistancec.dtw_distances_matrix(cur.matrix, cur.nb_rows, cur.nb_cols,
                                           dists.as_doubles, &block._block, &settings._settings)

    return dists
