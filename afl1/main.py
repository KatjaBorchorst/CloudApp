import httpx
import xmltodict
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

def get_enabled_events(graph_id: str, sim_id: str, auth: (str, str)):
    next_activities_response = httpx.get(
        "https://repository.dcrgraphs.net/api/graphs/" + graph_id +
        "/sims/" + sim_id + "/events?filter=only-enabled",
        auth=auth)
    
    events_xml = next_activities_response.text
    events_xml_no_quotes = events_xml[1:len(events_xml)-1]
    events_xml_clean = events_xml_no_quotes.replace('\\\"', "\"")
    events_json = xmltodict.parse(events_xml_clean)

    return events_json


def create_buttons_of_enabled_events(
    graph_id: str,
    sim_id: str,
    auth: (str, str),
    button_layout: BoxLayout):

    events_json = get_enabled_events(
        graph_id,
        sim_id,
        auth)
    
    button_layout.clear_widgets()
    events = []
    # distinguish between one and multiple events
    if not isinstance(events_json['events']['event'], list):
        events = [events_json['events']['event']]
    else:
        events = events_json['events']['event']

    # add a custom button, that stores the event id
    for e in events_json['events']['event']:
        s = SimulationButton(
            #the actual event id
            e['@id'],
            graph_id,
            sim_id,
            auth[0],
            auth[1],
            #the label of the event
            e['@label']
        )
        s.manipulate_box_layout = button_layout
    
        if e['@pending'] == 'true':
            s.text_color = (1, 1, 0, 1)  # Yellow color: (R=1, G=1, B=0, A=1)
    
    button_layout.add_widget(s)


# source code provided in exercise sheet
class SimulationButton(Button):
    def __init__(self, event_id: int,
            graph_id: str,
            simulation_id: str,
            username: str,
            password: str,
            text: str):
        Button.__init__(self)
        self.event_id = event_id
        self.text = text
        self.graph_id = graph_id
        self.simulation_id = simulation_id
        self.username = username
        self.password = password
        self.manipulate_box_layout = BoxLayout()
        self.bind(on_press=self.execute_event)
        
    def execute_event(self, instance):
        url = (f"https://repository.dcrgraphs.net/api/graphs/{self.graph_id}/sims/"
            f"{self.simulation_id}/events/{self.event_id}")
        newsim_response = httpx.post(url, auth=(self.username.text, self.password.text))
        create_buttons_of_enabled_events(self.graph_id, self.simulation_id, (self.username, self.password), self.manipulate_box_layout)


class MainApp(App):
    def __init__(self):
        App.__init__(self)
        self.login_button = Button(text='Start Instance')
        self.username = TextInput(hint_text="Enter username")
        self.password = TextInput(hint_text="Enter password", password=True)
        self.graph_id = TextInput(hint_text="Enter graph id")  

    
    def build(self):
        b_outer = BoxLayout(orientation='horizontal')
        b_left = BoxLayout(orientation='vertical')
        b_leftup = BoxLayout(orientation='horizontal')
        b_leftupright = BoxLayout(orientation='vertical')
        b_leftupleft = BoxLayout(orientation='vertical')
        b_leftdown = BoxLayout()
        b_right = BoxLayout(orientation='vertical')

        b_leftupright.add_widget(self.username)
        b_leftupright.add_widget(self.password)
        b_leftupright.add_widget(self.graph_id)

        b_leftupleft.add_widget(Label(text="Username"))
        b_leftupleft.add_widget(Label(text="Password"))
        b_leftupleft.add_widget(Label(text="Graph ID"))
        
        self.b_right = BoxLayout(orientation='vertical')
        self.login_button.bind(on_press=self.start_sim)
        b_leftdown.add_widget(self.login_button)
        b_leftup.add_widget(b_leftupleft)
        b_leftup.add_widget(b_leftupright)
        b_left.add_widget(b_leftup)
        b_left.add_widget(b_leftdown)
        
        b_outer.add_widget(b_left)
        b_outer.add_widget(self.b_right)
        return b_outer
    

    # def start_sim(self, instance):
    #     newsim_response = httpx.post(
    #         url=f"https://repository.dcrgraphs.net/api/graphs/{self.graph_id}/sims/",
    #         auth=(self.username.text, self.password.text))
    
    #     # self.simulation_id = newsim_response.headers['simulationID']
    #     # print("New simulation created with id:", self.simulation_id)

    #     # create_buttons_of_enabled_events(self.graph_id, self.simulation_id, (self.username, self.password))

    def start_sim(self, instance):
        newsim_response = httpx.post(
            url=f"https://repository.dcrgraphs.net/api/graphs/{self.graph_id.text}/sims/",
            auth=(self.username.text, self.password.text))

        # Logging the response headers and body for debugging
        print("Response Headers:", newsim_response.headers)
        print("Response Body:", newsim_response.text)

        if 'simulationID' in newsim_response.headers:
            self.simulation_id = newsim_response.headers['simulationID']
        else:
            print("Error: 'simulationID' not found in response headers.")
            # Check if simulationID is in the response body
            # Implement logic to extract it from the body if necessary
            return

        create_buttons_of_enabled_events(self.graph_id.text, self.simulation_id, (self.username.text, self.password.text), self.b_right)
        
        
if __name__ == '__main__':
    mainApp = MainApp()
    MainApp().run()
