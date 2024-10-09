from kivy.lang import Builder
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.core.camera import Camera

import cv2
from pyzbar import pyzbar

KV = '''
BoxLayout:
    orientation: 'vertical'

    Image:
        id: img
        allow_stretch: True
        keep_ratio: False

    Label:
        id: label
        text: 'Skanowanie...'
        size_hint_y: 0.1
'''

class BarcodeScannerApp(App):
    def build(self):
        self.camera = None
        self.img1 = None
        return Builder.load_string(KV)

    def on_start(self):
        # Inicjalizacja kamery
        self.camera = cv2.VideoCapture(0)

        # Ustawienie aktualizacji obrazu co określony czas
        Clock.schedule_interval(self.update, 1.0/30.0)

    def update(self, dt):
        ret, frame = self.camera.read()
        if ret:
            # Konwersja obrazu OpenCV do tekstury Kivy
            buffer = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.root.ids.img.texture = texture

            # Skanowanie kodów kreskowych
            barcodes = pyzbar.decode(frame)
            for barcode in barcodes:
                barcode_data = barcode.data.decode('utf-8')
                barcode_type = barcode.type
                self.root.ids.label.text = f'Znaleziono kod: {barcode_data} ({barcode_type})'
                # Możesz dodać tutaj dowolne działanie po zeskanowaniu kodu

    def on_stop(self):
        if self.camera:
            self.camera.release()

if __name__ == '__main__':
    BarcodeScannerApp().run()
