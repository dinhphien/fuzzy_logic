import pygame
from pygame.locals import *
# width = 640
# height = 320
# speed = [2, 2]
# GREEN = (150, 255, 150)
# RED = (255, 0, 0)
# running = True
# pygame.init()
# screen = pygame.display.set_mode((width, height))
# ball = pygame.image.load("/home/dinhphien/Pictures/Selection_001.png")
# ballrect = ball.get_rect()
# print(ballrect)
# print(ballrect.left)
# print(ballrect.right)
# print(ballrect.top)
# print(ballrect.bottom)
# clock = pygame.time.Clock()
# while running:
#     clock.tick(24)
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             running = False
#     # ballrect = ballrect.move(speed)
#     # if ballrect.left < 0 or ballrect.right > width:
#     #     speed[0] = -speed[0]
#     # if ballrect.top < 0 or ballrect.bottom > height:
#     #     speed[1] = -speed[1]
#     screen.fill(RED)
#     screen.blit(ball, ballrect)
#     pygame.display.flip()
# pygame.quit()
class Text:
    """Create a text object."""

    def __init__(self, text= "Default", pos=(0, 0), **options):
        self.text = text
        self.pos = pos

        self.fontname = None
        self.fontsize = 72
        self.fontcolor = Color('black')
        self.set_font()
        self.render()

    def set_font(self):
        """Set the Font object from name and size."""
        self.font = pygame.font.Font(self.fontname, self.fontsize)

    def render(self):
        """Render the text into an image."""
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

    def draw(self):
        """Draw the text image to the screen."""
        App.screen.blit(self.img, self.rect)

class App:
    """Create a single-window app with multiple scenes."""

    def __init__(self):
        """Initialize pygame and the application."""
        pygame.init()
        flags = RESIZABLE
        App.screen = pygame.display.set_mode((640, 240), flags)
        App.t = Text('Pygame App', pos=(20, 20))
        App.scenes = []

        App.running = True

    def run(self):
        """Run the main event loop."""
        while App.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    App.running = False

            App.screen.fill(Color('gray'))
            App.t.draw()
            pygame.display.update()

        pygame.quit()

class Scene:
    """Create a new scene (room, level, view)."""
    id = 0
    bg = Color('gray')

    def __init__(self, *args, **kwargs):
        # Append the new scene and make it the current scene
        App.scenes.append(self)
        App.scene = self
        # Set the instance id and increment the class id
        self.id = Scene.id
        Scene.id += 1
        self.nodes = []
        self.bg = Scene.bg
    def draw(self):
        """Draw all objects in the scene."""
        App.screen.fill(self.bg)
        for node in self.nodes:
            node.draw()
        pygame.display.flip()

class Demo(App):
    def __init__(self):
        super().__init__()

        Scene(caption='Intro')
        Text('Scene 0', pos = (40, 60))
        Text('Introduction screen the app', pos = (40, 100))
        #
        # Scene(bg=Color('yellow'), caption='Options', pos = (40, 60))
        # Text('Scene 1')
        # Text('Option screen of the app')
        #
        # Scene(bg=Color('green'), caption='Main')
        # Text('Scene 2')
        # Text('Main screen of the app')
        #
        # App.scene = App.scenes[2]

if __name__ == '__main__':
    Demo().run()
