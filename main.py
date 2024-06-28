import threading
from zentrale_website.main import start_website
from zentrale_websocket.main import start_websocket

website = threading.Thread(target=start_website, daemon=True)
websocket = threading.Thread(target=start_websocket, daemon=True)

website.start()
websocket.start()

website.join()
websocket.join()
