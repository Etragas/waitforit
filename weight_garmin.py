

from garminconnect import (MODERN_URL, Garmin,
                           GarminConnectAuthenticationError,
                           GarminConnectConnectionError,
                           GarminConnectTooManyRequestsError)


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

        if response.status_code == 429:
            raise GarminConnectTooManyRequestsError("Too many requests")

        return response.json()