from openai import OpenAI
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from time import sleep

load_dotenv()

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

client = OpenAI(api_key=os.environ.get("OPENAI_KEY"))

instructions = """
    You are an AI tool that receives input from a python script and
    provides an output. The input will be in the form of a list of 6 items
    separated by commas. All 5 commas will always be included in the input.
    If the input received does not match that format, your output should
    merely be "INVALID INPUT". The output should also be a comma separated
    list, but an additional item should be included, that being an integer
    between 0-100 indicating certainty percentage (no % should be
    included). In all cases, your output should consist of a list of 7
    items separated by commas. All 6 commas should always be included in
    the output. Some of the input list items may be empty, and your task
    will be to use the other items in the list to determine some of the
    missing items. The output should be formatted in all caps.

    Your response should contain the output and nothing else.

    The input will be a partial address or intersection corresponding to a
    call for service at the Jackson County Sheriff's Office. The list will
    be in the order of: STREET ADDRESS, CITY, STATE, ZIP CODE, LATITUDE,
    LONGITUDE. As stated before, one or more of those items may be missing
    from the input. The latitude and longitude will not normally be
    provided.

    Input formatting of the street address for intersections may vary, but
    the output should always be the two intersecting roadways separated by
    a backslash (e.g. "EXAMPLE ST/SAMPLE AVE").  The roadway type (St, Ave,
    Blvd, etc.) and direction should always be determined and included.
    Some of the CITY items provided in the input will be "UNINCORPORATED"
    or "JACKSON COUNTY". In such cases, you should determine the city
    associated with the mailing address. You do not need to attempt to find
    the ZIP CODE, LATITUDE, or LONGITUDE items. If these items were
    provided, merely pass them through to your output. If those items were
    left empty, then pass an empty item through to your output.

    Most, but not all, of the input addresses will be located within
    Jackson County, MO. If no CITY, STATE, or ZIP CODE is specified, assume
    the location is in Jackson County, MO, and attempt to determine the
    CITY.

    When a STREET ADDRESS is an intersection and one of the roadways is
    merely a number, that roadway is likely a state or US highway. If no
    such highway exists in that CITY or STATE, then assume it is a numbered
    street. If an input STREET ADDRESS contains an unabbreviated roadway
    type or direction, your output should use the appropriate
    abbreviations.

    You should attempt to find as complete an address as possible and check
    each list item against the others for accuracy. You should not fully
    trust the information provided in the input. The STREET ADDRESS item
    will likely be the most complicated and least trustworthy part. These
    addresses were entered by Dispatchers and Deputies, and each individual
    may have a slightly different method for notating certain information.
    The street type and direction may have also been entered incorrectly
    when recorded. Some calls for service are located some distance in some
    direction from the given address, and that information is normally
    notated in the STREET ADDRESS item as an abbreviation (e.g. "JN" for
    "Just North," etc.). There may also be erroneous or accidental characters
    in the STREET ADDRESS.

    You should make 3 separate attempts to find the correct address, and
    the attempts should not influence nor refer to each other.  Each check
    should be performed as though you were starting from the beginning, and
    you should attempt to locate all of the requested information during
    each. Then you will determine the most likely address from the 3
    attempts and output it. The certainty percentage should reflect the
    similarity between the 3 attempts. Identical findings in the 3 attempts
    would give 100% output certainty, and completely dissimilar findings
    would give 0% output certainty. The certainty percentage should also be
    influenced by how many items were provided in the INPUT. An input with
    all items provided would be 100% output certainty, and one with all
    items empty would be 0% output certainty. Multiplying the two output
    certainties will give you the total output certainty.
    """

input = "PINKHILL/BB,GRAIN VALLEY,MO,64075"

response = client.responses.create(
    model="gpt-4o",
    instructions=instructions,
    input=input,
)

ai_result = response.output_text.split(",")

ai_address = ",".join(ai_result[0:3]).replace("/","&")

print(ai_address)

# plug everything into Lat-Long Finder to get the correct ZIP, lat, and long.

service = webdriver.EdgeService(executable_path=os.path.join(__location__, "msedgedriver.exe"))
driver = webdriver.Edge(service=service)

driver.implicitly_wait(10)
driver.get("https://www.arcgis.com/apps/Viewer/index.html?appid=8919c0bd5d0a4a419c121022fd411d5f")

address_box = driver.find_element(by=By.ID, value="search_input")
measure_btn = driver.find_element(by=By.ID, value="panelTool_measure")

address_box.clear()
address_box.send_keys(ai_address, Keys.RETURN)

sleep(1)

measure_btn.click()

sleep(1)

location_btn = driver.find_element(by=By.ID, value="dijit_form_ToggleButton_2")

ActionChains(driver) \
    .move_to_element(location_btn) \
    .click() \
    .perform()
    
coord = driver.find_element(by=By.ID, value="mapDiv_graphics_layer")

ActionChains(driver) \
    .move_to_element(coord) \
    .perform()
    
measurement_row = driver.find_element(by=By.CLASS_NAME, value="esriMeasurementTableRow")
search_result = driver.find_element(by=By.CLASS_NAME, value="moreItem")

latlng = measurement_row.text.split()
lat = latlng[0]
lng = latlng[1]

address = search_result.text.split(",")
for i in address:
    address[address.index(i)] = i.lstrip(" ")
street_address = address[0]
city = address[1]
state = address[2]
zip = address[3]

results = [street_address.replace(" & ", "/"), city, state, zip, lat, lng]

driver.quit()

print(results)