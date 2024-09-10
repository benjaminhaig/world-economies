import requests
from config import COUNTRY_CODES, TESTING_COUNTRY_CODES, GLOBAL_TESTING

def test_routes(codes):
    for i in codes:
        r = requests.get(f'http://127.0.0.1:8000/country/{i}')
        if (r.ok):
            passed_routes.append(i)
        else:
            failed_routes.append(i)
    
    print("Passed Routes: " + str(passed_routes))
    print("Passed Route Count: " + str(len(passed_routes)))
    print("**********************************")
    print("Failed Routes: " + str(failed_routes))
    print("Failed Routes Count: " + str(len(failed_routes)))
        
if __name__ == "__main__":
    passed_routes = []
    failed_routes = []
    if GLOBAL_TESTING:
        # Currently testing state with only 10 countries
        test_routes(TESTING_COUNTRY_CODES)
    else:
        test_routes(COUNTRY_CODES)


