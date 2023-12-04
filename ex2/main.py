from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import xmltodict
import httpx

class MyDCRApp(App):
    def __init__(self):
        App.__init__(self)
        self.password = TextInput(hint_text="Enter password", password=True)
        self.username = TextInput(hint_text="Enter username")   
        
    def b_press(self, instance):
        self.create_instance()
        
    def build(self):
        b = Button(text="Create New Instance")
        self.b_outer = BoxLayout()
        b_inner = BoxLayout()
        b_inner.add_widget(self.username)
        b_inner.add_widget(self.password)
        b.bind(on_press=self.b_press)

        self.b_outer.add_widget(b)
        self.b_outer.add_widget(b_inner)
        return self.b_outer

    def create_instance(self):
        newsim_response = httpx.post(
            url="https://repository.dcrgraphs.net/api/graphs/1702928/sims",
            auth=(self.username.text, self.password.text))
        
        self.simulation_id = newsim_response.headers['simulationID']
        print("New simulation created with id:", self.simulation_id)

        next_activities_response = httpx.get(
            "https://repository.dcrgraphs.net/api/graphs/" + self.graph_id +
            "/sims/" + self.simulation_id + "/events?filter=only-enabled",
            auth=(self.username.text, self.password.text))
        
        events_xml = next_activities_response.text
        events_xml_no_quotes = events_xml[1:len(events_xml)-1]
        events_xml_clean = events_xml_no_quotes.replace('\\\"', "\"")
        events_json = xmltodict.parse(events_xml_clean)
        
        for e in events_json['events']['event']:
            self.layout_box.add_widget(Label(text=e['@label']))
            print(e['@label'])

        self.layout_box = BoxLayout(orientation='vertical')
        self.b_outer.add_widget(self.layout_box)
    

if __name__ == '__main__':
    MyDCRApp().run()
