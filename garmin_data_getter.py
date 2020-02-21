# Gets data from garmin

# v0 is login + fetch data

from datetime import date

from garminconnect import (Garmin, GarminConnectAuthenticationError,
                           GarminConnectConnectionError,
                           GarminConnectTooManyRequestsError)

from weight_garmin import WeightGarmin

today = date.today()
"""Login to portal using specified credentials"""
try:
    with open('garmin_credentials') as f:
        user, pwd = map(lambda x: x.strip(), f.readlines())
        print(user.strip())
        print(pwd.strip())
    client = WeightGarmin(user, pwd)
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print(f"Error occured during Garmin Connect Client setup: {err}")
    print(err.status)
    # return
except Exception:  # pylint: disable=broad-except
    print("Unknown error occured during Garmin Connect Client setup")
    # return

# """Get Full name"""
# print(client.get_full_name())

# """Get Unit system"""
# print(client.get_unit_system())

# """Fetch your activities data"""
# print(client.get_stats(today.isoformat()))

# """Fetch your logged heart rates"""
# print(client.get_heart_rates(today.isoformat()))

"""Fetch your body compostion rates"""
print(client.get_body_composition(today.isoformat()))
