from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
import requests
import threading
import time

# உங்கள் API KEY-ஐ இங்கே போடவும்
API_KEY = "r8_Dvn5DbPUp7UXgJFkIIwWMh6KgIHRIRi2mKMod"

class VideoApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # உள்ளீடு (Input)
        self.prompt_input = TextInput(hint_text='Enter prompt (e.g., A flying cat)', size_hint=(1, 0.2))
        self.layout.add_widget(self.prompt_input)
        
        # பட்டன் (Button)
        self.btn = Button(text='Generate Video', size_hint=(1, 0.2), background_color=(0, 1, 0, 1))
        self.btn.bind(on_press=self.start_generation)
        self.layout.add_widget(self.btn)
        
        # நிலை (Status Label)
        self.status_label = Label(text='Ready', size_hint=(1, 0.1))
        self.layout.add_widget(self.status_label)

        return self.layout

    def start_generation(self, instance):
        self.status_label.text = "Generating... Please wait..."
        threading.Thread(target=self.generate_video).start()

    def generate_video(self):
        prompt = self.prompt_input.text
        if not prompt:
            self.status_label.text = "Please enter a prompt!"
            return

        headers = {"Authorization": f"Token {API_KEY}", "Content-Type": "application/json"}
        data = {
            "version": "147932427de11297d86f2c336b9980d297905b38743132e0e5a8873f1c1e549d",
            "input": {"prompt": prompt}
        }

        try:
            # Step 1: Request
            response = requests.post("https://api.replicate.com/v1/predictions", json=data, headers=headers)
            if response.status_code != 201:
                self.status_label.text = "Error: " + response.text
                return

            get_url = response.json()["urls"]["get"]
            
            # Step 2: Polling (Wait for video)
            while True:
                status_check = requests.get(get_url, headers=headers).json()
                if status_check["status"] == "succeeded":
                    video_url = status_check["output"]
                    self.status_label.text = f"Success! Video created."
                    print(video_url) # In a real app, you would download/play this
                    break
                elif status_check["status"] == "failed":
                    self.status_label.text = "Generation Failed."
                    break
                time.sleep(2)
        except Exception as e:
            self.status_label.text = str(e)

if __name__ == '__main__':
    VideoApp().run()
