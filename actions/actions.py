
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import csv
import sys
from bs4 import BeautifulSoup
import requests
import datetime as dt



class ActionQuestionSearch(Action):

    def name(self) -> Text:
        return "action_question_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        crop = tracker.get_slot("crop_type")
        question = tracker.get_slot("kcc_question")

        csv_file = csv.reader(open("kcc_qna.csv", "r"), delimiter=",")
        answer = []
        for row in csv_file:
            if question == row[1] and crop== row[0]:
                answer.append(row[2])

        dispatcher.utter_message("Here is the answer for your querry :- \n recommended solution for your {0} crop is : {1}".format(crop,answer))
        return []
        # return [SlotSet("answer", answer)]


class ActionReturnTime(Action):

    def name(self) -> Text:
        return "action_return_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        now = dt.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        dispatcher.utter_message(text="Today's Date and time" +str(dt_string))

        return []

class ActionWebReferance(Action):
    def name(self) -> Text:
        return "action_web_referance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entity = tracker.latest_message['entities'][0]['value']
        if entity == "government schemes":
            dispatcher.utter_message(text="Please refer the following [website](https://vikaspedia.in/schemesall/schemes-for-farmers)")

        elif entity == "nutrient management":
            dispatcher.utter_message(text="Please refer the following [website](https://www.epa.gov/agriculture/agriculture-nutrient-management-and-fertilizer) ")

        elif entity == "seed":
            dispatcher.utter_message(text="Please refer the following [website](https://seednet.gov.in/Material/IndianSeedSector.aspx)")

        elif entity == "market":
            dispatcher.utter_message(text="Please refer the following [website](https://agmarknet.gov.in/Default.aspx)")

        elif entity == "paddy":
            dispatcher.utter_message(text="""Please Download Crop Darpan App developed by IIT Hydrabad faculty or 
                go on following [website](https://www.cropdarpan.com/cropdarpan/farmer/welcome) .
                On this platform ,You will get information on which disease do your paddt/cotton crop have
                and advice on dignostic of your known disease""")

        elif entity == "cotton":
            dispatcher.utter_message(text="""Please Download Crop Darpan App developed by IIT Hydrabad faculty or 
                go on following [website](https://www.cropdarpan.com/cropdarpan/farmer/welcome) .
                On this platform ,You will get information on which disease do your paddt/cotton crop have
                and advice on dignostic of your known disease""")

        else:
            dispatcher.utter_message(text="I did not understand, please be specific with your question")

        return []

class ActionCropFertilizer(Action):

    def name(self) -> Text:
        return "action_crop_fertilizer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        crop = tracker.get_slot("crop_type")
        html_page=f"https://ikisan.com/ap-{crop}-nutrient-management.html"
        if html_page:
            dispatcher.utter_message(text="For detail Information click [here]({})".format(html_page))
        else:
            dispatcher.utter_message(text="Sorry for inconvenience,your crop is not in our Database.we will update soon")

        return []

class ActionWeather(Action):
    def name(self):
        return 'action_weather'
    
    def run(self,dispatcher,tracker,domain):
        city = tracker.get_slot('location')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        c = city+" weather"
        c = c.replace(" ", "+")
        res = requests.get(f'https://www.google.com/search?q={c}&oq={c}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        location = soup.select('#wob_loc')[0].getText().strip()
        time = soup.select('#wob_dts')[0].getText().strip()
        info = soup.select('#wob_dc')[0].getText().strip()
        temp = soup.select('#wob_tm')[0].getText().strip()
        dispatcher.utter_message("""For City {0}
            today is {1}
            \n weather condition :- {2}
            \n temperature is {3}°C
            \n Have a Nice Day:)""".format(location,time,info,temp))
        return []
        # return [SlotSet("location",city)]