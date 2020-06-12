import itertools
from typing import Tuple, Mapping, Union, Callable

import numpy as np

from adapter_covid19.datasources import DataSource, Reader
from adapter_covid19.enums import (
    Sector,
    Age,
    FinalUse,
    PrimaryInput,
    Decile,
    Region,
    RegionUK,
)

ALL_ENUMS = [Sector, Age, FinalUse, PrimaryInput, Decile]


class DataSourceUK(DataSource):
    def __init__(self, filename: str, agg_func: Callable = np.mean):
        """
        Read and parse a dataset from disk
        Parameters
        ----------
        filename: filename of dataset
        agg_func: function to aggregate UK metrics to one single region
        """
        super().__init__(filename)
        self.agg_func = agg_func


class RegionDataSource(DataSourceUK):
    def load(
        self, reader: Reader
    ) -> Union[Mapping[Region, float], Mapping[str, Mapping[Region, float]]]:
        data = reader.load_csv(self.filename, orient="dict", index_col=0)
        # data = {k: {UKRegion[kk]: vv for kk, vv in v.items()} for k, v in data.items()}
        data = {
            k: {Region.ALL: self.agg_func([vv for _, vv in v.items()])}
            for k, v in data.items()
        }
        if len(data) > 1:
            return data
        return next(iter(data.values()))


class RegionSectorAgeDataSource(DataSourceUK):
    def load(
        self, reader: Reader,
    ) -> Union[
        Mapping[Tuple[Region, Sector, Age], float],
        Mapping[str, Mapping[Tuple[Region, Sector, Age], float]],
    ]:
        data = reader.load_csv(self.filename, orient="dict", index_col=[0, 1, 2])
        data = {
            k: {
                (RegionUK[kk[0]], Sector[kk[1]], Age[kk[2]]): vv for kk, vv in v.items()
            }
            for k, v in data.items()
        }
        data = {
            k: {
                (Region.ALL, sector, age): self.agg_func(
                    [v[(region_uk, sector, age)] for region_uk in RegionUK]
                )
                for sector, age in itertools.product(Sector, Age)
            }
            for k, v in data.items()
        }
        if len(data) > 1:
            return data
        return next(iter(data.values()))


class RegionDecileSource(DataSourceUK):
    def load(self, reader: Reader) -> Mapping[Tuple[Region, Decile], float]:
        frame = reader.load_csv(self.filename)
        data = {
            (RegionUK[t.Region], Decile[t.Decile]): t[-1]
            for t in frame.itertuples(index=False)
        }
        data = {
            decile: self.agg_func([data[(region_uk, decile)] for region_uk in RegionUK])
            for decile in Decile
        }
        return data


class RegionSectorDecileSource(DataSourceUK):
    def load(self, reader: Reader) -> Mapping[Tuple[Region, Sector, Decile], float]:
        frame = reader.load_csv(self.filename)
        data = {
            (RegionUK[t.Region], Sector[t.Sector], Decile[t.Decile]): t[-1]
            for t in frame.itertuples(index=False)
        }
        data = {
            (sector, decile): self.agg_func(
                [data[(region_uk, sector, decile)] for region_uk in RegionUK]
            )
            for sector, decile in itertools.product(Sector, Decile)
        }
        return data
