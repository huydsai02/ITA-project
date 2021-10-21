import pygame
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 600))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)
    
 
class Button:
    """Create a button, then blit the surface in the while loop"""
 
    def __init__(self, text,  pos, font, screen, bg="black", feedback="", size = (150,50), func = None):
        self.x, self.y = pos
        self.screen = screen
        self.size = size
        self.font = pygame.font.SysFont("Arial", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)
        self.handle = func
        
 
    def change_text(self, text, bg="black"):
        ### Hàm xử lý khi click vào ###
        """Change the text whe you click"""
        self.text = self.font.render(text, 1, pygame.Color("White"))
        # self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
 
    def show(self):
        self.screen.blit(self.surface, (self.x, self.y))
 
    def click(self, event):
        x, y = pygame.mouse.get_pos()
        print(x,y)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                print(x,y)
                if self.rect.collidepoint(x, y):
                    self.change_text(self.feedback, bg="red")
                    self.handle
        pass
 
if __name__ == '__main__':
 
    button1 = Button("Click here", (100, 100), font=30,screen = screen, bg="navy", feedback="Hide")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            button1.click(event)
        
        button1.show()

        clock.tick(30)
        pygame.display.update()