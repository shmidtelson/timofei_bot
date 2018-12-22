import time
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint

class GenerateGif:
    api_instance = giphy_client.DefaultApi()
    api_key = 'dc6zaTOxFJmzC' # str | Giphy API Key.
    tag = 'terminator' # str | Search query term or prhase.
    limit = 1 # int | The maximum number of records to return. (optional) (default to 25)
    rating = 'g' # str | Filters results by specified rating. (optional)
    fmt = 'json' # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)

    def main(self):
        try:
            api_response = self.api_instance.gifs_random_get(self.api_key, tag=self.tag, rating=self.rating,
                                                             fmt=self.fmt)
            return api_response.data.image_original_url
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)

