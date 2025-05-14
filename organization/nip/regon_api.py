from RegonAPI import RegonAPI


def nip_search(nip: int):
    api = RegonAPI(bir_version="bir1.1", is_production=True)
    # Authenticate with your API key
    # You can get your API key from https://api.stat.gov.pl/Home/RegonApi
    api.authenticate(key="abcde12345abcde12345")  # Replace with your actual API key
    return api.searchData(nip=str(nip))
