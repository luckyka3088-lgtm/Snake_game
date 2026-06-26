import pygame  

class Button:
    def __init__(self, image, x, y):
        self.x = x
        self.y = y
        self.image = image
    def draw(self, surface):
        
        surface.blit(self.image, (self.x, self.y))

    def is_clicked(self, mos_x, mos_y):
        if (self.x <= mos_x <= self.x + self.image.get_width() and
            self.y <= mos_y <= self.y + self.image.get_height()):
            return True

        return False
					

										
		
			
								 