class GameStateManager :
    STATES = {
        "MAIN_MENU" : {},
        "GAME" : {},
        "SETTINGS" : {},
        "CREDITS" : {},
        "QUIT" : {},
    }
    
    def __init__(self) :
        self.state = "MAIN_MENU"

    def change_state(self, new_state) :
        print(f"Changing state to: {new_state}")
        self.state = new_state