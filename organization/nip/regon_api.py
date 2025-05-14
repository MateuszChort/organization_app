from RegonAPI import RegonAPI
from django.conf import settings


def nip_search(nip: int):
    api = RegonAPI(bir_version="bir1.1", is_production=True)
    # Authenticate with your API key
    # You can get your API key from https://api.stat.gov.pl/Home/RegonApi
    api.authenticate(key=settings.REGONAPIKEY)
    return api.searchData(nip=str(nip))
