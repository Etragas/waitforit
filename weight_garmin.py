

from garminconnect import (MODERN_URL, Garmin,
                           GarminConnectAuthenticationError,
                           GarminConnectConnectionError,
                           GarminConnectTooManyRequestsError)
from typing import List, Dict, NamedTuple, Any, Tuple
import requests
from datetime import date
import numpy as np

class WeightGarmin(Garmin):
    """ WIP WHILE WAITING FOR https://github.com/cyberjunky/python-garminconnect/pull/3/files TO MERGE """

    url_body_composition = MODERN_URL + '/proxy/weight-service/weight/daterangesnapshot'

    def get_body_composition(self, cdate):   # cDate = 'YYYY-mm-dd'
        """
        Fetch available body composition data (only for cDate)
        """
        bodycompositionurl = self.url_body_composition + '?startDate=' + '2020-01-01' + '&endDate=' + cdate
        self.logger.debug("Fetching body compostion with url %s", bodycompositionurl)
        try:
            response = self.req.get(bodycompositionurl, headers=self.headers)
            self.logger.debug("Body Composition response code %s, and json %s", response.status_code, response.json())
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            self.logger.debug("Exception occured during body compostion retrieval - perhaps session expired - trying relogin: %s" % err)
            self.login(self.email, self.password)
            try:
                response = self.req.get(bodycompositionurl, headers=self.headers)
                self.logger.debug("Body Compostion response code %s, and json %s", response.status_code, response.json())
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                self.logger.debug("Exception occured during stats retrieval, relogin without effect: %s" % err)
                raise GarminConnectConnectionError("Error connecting")
        print("Responsse is", response)
        if response.status_code == 429:
            raise GarminConnectTooManyRequestsError("Too many requests")

        return response.json()

class BodyCompMeasurement(NamedTuple):
    samplePk: int
    date: int
    calendarDate: str #yyyy-mm-dd
    weight: float
    bmi: float
    bodyFat: float
    bodyWater: float
    boneMass: int
    muscleMass: int
    physiqueRating: Any #idk
    visceralFat: Any
    metabolicAge: Any
    sourceType: str
    timestampGMT: int #time
    weightDelta: float

    @property
    def norm_weight(self):
        """Returns weight in a human readable format"""
        # Goal is 3 decimals
        # Default is grams
        return self.weight/1000

class BodyStats(NamedTuple):
    startDate: str
    endDate: str
    dateWeightList: List[BodyCompMeasurement] #TODO New class for sub?
    totalAverage: Dict # Ignore this


def gen_target_weights(dates: List[date], start_weight: float, daily_loss_goal: float) -> List[Tuple[date, float]]:
    """[summary]
    
    Arguments:
        start_date {date} -- The first day of the weight loss regime
        start_weight {float} -- The starting weight
        daily_loss_goal {float} -- The target loss in lbs
    
    Returns:
        List[Tuple[date, float]] -- A list of target weight loss points
    """
    # 
    target_weights = [start_weight]
    pdate = dates[0]
    date_since_start = 0
    for cdate in dates[1:]:
        date_since_start += (cdate-pdate).days
        target_weights.append(start_weight-(daily_loss_goal*date_since_start))
        pdate = cdate
    return target_weights

def get_average_measures(measures: List[float]) -> List[float]:
    """Implement a rolling window averaging over last 10 days with expontential discounting"""

    weights = np.array([0.9**x for x in range(9, -1, -1)])
    smoothed_measures = []
    for i in range(-9, len(measures)-9):
        cur_vals = list(measures[max(i, 0): i+10])
        remainder = 10 - len(cur_vals)
        cur_vals = [0] * remainder + cur_vals
        norm_sum = sum(weights[remainder:])
        normalized_smoothed_weight = np.dot(weights, cur_vals) / (norm_sum)
        smoothed_measures.append(normalized_smoothed_weight)
    return smoothed_measures

def compute_weekly_loss(dates: List[date], smoothed_measures: List[float]):
    weeks_passed = ((dates[-1] - dates[0]).days) / 7
    from math import ceil
    weeks_passed_up = ceil(weeks_passed)
    weight_deficit = -(smoothed_measures[-1] - smoothed_measures[0])
    interpol_ratio = weeks_passed/weeks_passed_up
    return weight_deficit/weeks_passed*interpol_ratio

def compute_average_daily_cal_deficit(dates: List[date], smoothed_measures: List[float]):
    days_passed = ((dates[-1] - dates[0]).days)
    weight_deficit = -(smoothed_measures[-1] - smoothed_measures[0])
    return weight_deficit*3500/days_passed