
import pygame 

class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        self.X_BUTTON = 0
        self.C_BUTTON = 1

        """Initialize the joystick components"""
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)

        print(pygame.joystick.Joystick(0))

        self.controller.init()

    def listen(self):
        """Listen for events to happen"""
        
        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)


    def update(self): 
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self.axis_data[event.axis] = float(event.value)
            elif event.type == pygame.JOYBUTTONDOWN:
                self.button_data[event.button] = True
            elif event.type == pygame.JOYBUTTONUP:
                self.button_data[event.button] = False
            elif event.type == pygame.JOYHATMOTION:
                self.hat_data[event.hat] = event.value

    def get_button(self, button_id): 
        return self.button_data[button_id] 

    def get_axis(self): 
        """
            Get all the read axis as vector 
        """
        dx, dy, dz = 0.0, 0.0, 0.0 # Init 
        axis_data = self.axis_data
        
        # Positions 
        dx =  axis_data.get(0) if not axis_data.get(0) == None else 0.0
        dy =  axis_data.get(1) if not axis_data.get(1) == None else 0.0
        dz =  axis_data.get(2) if not axis_data.get(2) == None else 0.0

        dX = [dx, dy, dz]
        dX = [0.0 if abs(element) < 0.05 else element for element in dX] # Filter for deleting 

        return dX 
