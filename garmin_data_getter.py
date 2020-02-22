# Gets data from garmin

# v0 is login + fetch data

from datetime import date

from garminconnect import (Garmin, GarminConnectAuthenticationError,
                           GarminConnectConnectionError,
                           GarminConnectTooManyRequestsError)

# print(client.get_heart_rates(today.isoformat()))
from weight_garmin import (BodyCompMeasurement, BodyStats, WeightGarmin)
from functools import lru_cache

class GarminDataGetter():
    def __init__(self):
        self.client = self.login()

    def login(self):
        """Login to portal using specified credentials"""
        try:
            with open('garmin_credentials') as f:
                user, pwd = map(lambda x: x.strip(), f.readlines())
            client = WeightGarmin(user, pwd)
            return client
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
        ) as err:
            print(f"Error occured during Garmin Connect Client setup: {err}")
            print(err.status)
            return None
        except Exception:  # pylint: disable=broad-except
            print("Unknown error occured during Garmin Connect Client setup")
            return None

    def _get_body_stats(self, start_date: date):
        """Fetch your body compostion rates"""
        # response = {'startDate': '2020-01-01', 'endDate': '2020-02-21', 'dateWeightList': [{'samplePk': 1581985961435, 'date': 1581967920000, 'calendarDate': '2020-02-17', 'weight': 108408.57643, 'bmi': None, 'bodyFat': None, 'bodyWater': None, 'boneMass': None, 'muscleMass': None, 'physiqueRating': None, 'visceralFat': None, 'metabolicAge': None, 'sourceType': 'MANUAL', 'timestampGMT': 1581985920000, 'weightDelta': None}, {'samplePk': 1582124832000, 'date': 1582106832000, 'calendarDate': '2020-02-19', 'weight': 110029.99877929688, 'bmi': 34.0, 'bodyFat': 34.11000061035156, 'bodyWater': 48.09000015258789, 'boneMass': 6389, 'muscleMass': 41540, 'physiqueRating': None, 'visceralFat': None, 'metabolicAge': None, 'sourceType': 'INDEX_SCALE', 'timestampGMT': 1582124832000, 'weightDelta': 1621.422349296874}, {'samplePk': 1582216449000, 'date': 1582198449000, 'calendarDate': '2020-02-20', 'weight': 109080.00183105469, 'bmi': 33.70000076293945, 'bodyFat': 33.7599983215332, 'bodyWater': 48.349998474121094, 'boneMass': 6360, 'muscleMass': 41310, 'physiqueRating': None, 'visceralFat': None, 'metabolicAge': None, 'sourceType': 'INDEX_SCALE', 'timestampGMT': 1582216449000, 'weightDelta': -949.9969482421875}, {'samplePk': 1582308954000, 'date': 1582290954000, 'calendarDate': '2020-02-21', 'weight': 108669.99816894531, 'bmi': 33.5, 'bodyFat': 33.59000015258789, 'bodyWater': 48.470001220703125, 'boneMass': 6340, 'muscleMass': 41209, 'physiqueRating': None, 'visceralFat': None, 'metabolicAge': None, 'sourceType': 'INDEX_SCALE', 'timestampGMT': 1582308954000, 'weightDelta': -410.003662109375}], 'totalAverage': {'from': 1577836800000, 'until': 1582329599999, 'weight': 109047.14380232422, 'bmi': 33.733333587646484, 'bodyFat': 33.81999969482422, 'bodyWater': 48.3033332824707, 'boneMass': 6363, 'muscleMass': 41353, 'physiqueRating': None, 'visceralFat': None, 'metabolicAge': None, 'weightCount': 4, 'bmiCount': 3, 'bodyFatCount': 3, 'bodyWaterCount': 3, 'boneMassCount': 3, 'muscleMassCount': 3, 'physiqueRatingCount': 0, 'visceralFatCount': 0, 'metabolicAgeCount': 0}}
        # Debugging
        
        response = self.client.get_body_composition(start_date)
        response['dateWeightList'] = list(map(lambda x: BodyCompMeasurement(**x), response['dateWeightList']))
        return BodyStats(**response)

    @property
    def current_body_stats(self):
        #TODO some logic for caching
        return self._get_body_stats(start_date=date.today().isoformat())

    def get_weight_points(self, unit='imp'):
        """ """
        body_stats = self.current_body_stats
        weights = []
        for body_comp in body_stats.dateWeightList:
            weight = body_comp.norm_weight * 2.20462 if unit == 'imp' else 1 # Default is kg
            weights.append((date.fromtimestamp(body_comp.date/1000), weight))
        print("Weights are", weights)
        return weights

if __name__ == '__main__':
    gdg = GarminDataGetter()
    raw_body_comp = gdg.current_body_stats 
    print(raw_body_comp)
    weight_points = gdg.get_weight_points()
    print(weight_points)

# """Get Full name"""
# print(client.get_full_name())

# """Get Unit system"""
# print(client.get_unit_system())

# """Fetch your activities data"""
# print(client.get_stats(today.isoformat()))

# """Fetch your logged heart rates"""
