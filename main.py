import pygame
from pygame.locals import *

from collections import deque

# initialize game
pygame.init()

# create screen
screen_width, screen_height = 1500, 750
screen = pygame.display.set_mode((screen_width, screen_height))

# Background
background = pygame.image.load('img.png')

# Caption and Icon
pygame.display.set_caption("Algoritmul lui Karatsuba")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ACTIVE_COLOR = (0, 102, 255)
INACTIVE_COLOR = (153, 204, 255)
ACTIVE_COLOR2 = (0, 204, 153)
INACTIVE_COLOR2 = (153, 255, 204)

# Fonts
font = pygame.font.Font(None, 100)
font_nod = pygame.font.Font(None, 50)

# Multiplication sign
signImg = pygame.image.load('multiplication.png')
new_size = (100, 100)
signImg = pygame.transform.scale(signImg, new_size)
signX = 100
signy = 300

# Input box 1
input_box_rect = pygame.Rect(60, 100, 200, 70)
input_text = ""
input_number = None
input_active = False
box_color = INACTIVE_COLOR

# Input box 2
input_box_rect2 = pygame.Rect(60, 550, 200, 70)
input_text2 = ""
input_number2 = None
input_active2 = False
box_color2 = INACTIVE_COLOR2


# Karatsuba

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.poz = 1
        self.z0 = None
        self.z1 = None
        self.z2 = None
        self.result = None


def karatsuba(x, y):
    node = Node(x, y)

    if x < 10 or y < 10:
        node.result = x * y
        return node

    # Calculate the number of digits in x and y
    num_digits = max(len(str(x)), len(str(y)))
    split_pos = num_digits // 2

    # Split the numbers into high and low parts
    high1, low1 = divmod(x, 10 ** split_pos)
    high2, low2 = divmod(y, 10 ** split_pos)

    # Recursively calculate the three multiplications
    node.z0 = karatsuba(low1, low2)

    node.z1 = karatsuba((low1 + high1), (low2 + high2))

    node.z2 = karatsuba(high1, high2)

    # Karatsuba formula for the final result
    node.result = (node.z2.result * (10 ** (2 * split_pos))) + (
            (node.z1.result - node.z2.result - node.z0.result) * (10 ** split_pos)) + node.z0.result

    return node


def print_tree(root, xc, yc, xdist, level, parent_x=None, parent_y=None):
    node = root
    node_size = 200 - (level * 50)  # Calculate the node size based on the level
    node_rect = pygame.Rect(xc - node_size/2, yc + 100, node_size, 50)

    if node.z0:
        print_tree(node.z0, xc - xdist, yc + 150, xdist / 3, level + 1, xc, yc + 100)
    if node.z1:
        print_tree(node.z1, xc, yc + 150, xdist / 3, level + 1, xc, yc + 100)
    if node.z2:
        print_tree(node.z2, xc + xdist, yc + 150, xdist / 3, level + 1, xc, yc + 100)

    pygame.draw.rect(screen, WHITE, node_rect)
    pe_ecran = f"{node.x} x {node.y}"
    surface = font_nod.render(pe_ecran, False, (0, 102, 255))
    text_rect = surface.get_rect(center=node_rect.center)
    screen.blit(surface, text_rect)

    # Draw line from parent to current node
    if parent_x is not None and parent_y is not None:
        pygame.draw.line(screen, WHITE, (parent_x, parent_y), (xc, yc + 100), 2)


# String to number
def is_number(text):
    try:
        int(text)
        return True
    except ValueError:
        return False


# Game loop
running = True
result = None
while running:
    screen.fill((0, 0, 0))
    # Background
    screen.blit(background, (0, 0))
    # Multiplication
    screen.blit(signImg, (signX, signy))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke pressed
        if event.type == MOUSEBUTTONDOWN:
            if input_box_rect.collidepoint(event.pos):
                input_active = not input_active
                box_color = ACTIVE_COLOR if input_active else INACTIVE_COLOR
            if input_box_rect2.collidepoint(event.pos):
                input_active2 = not input_active2
                box_color2 = ACTIVE_COLOR2 if input_active2 else INACTIVE_COLOR2
            if input_active2:
                input_active = False
                box_color = INACTIVE_COLOR
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                if is_number(input_text):
                    input_number = float(input_text)
                    print("Entered number 1:", input_number)
                if is_number(input_text2):
                    input_number2 = float(input_text2)
                    print("Entered number 2:", input_number2)
                input_text2 = ""
                input_active2 = False
                box_color2 = INACTIVE_COLOR2
                input_text = ""
                input_active = False
                box_color = INACTIVE_COLOR
                result = karatsuba(int(input_number), int(input_number2))
                print(result.result)
            if input_active:
                if event.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

            if input_active2:
                if event.key == K_BACKSPACE:
                    input_text2 = input_text2[:-1]
                else:
                    input_text2 += event.unicode
    if result is not None:
       print_tree(result, 850, 0, 400, 0)
    if result is not None:
        # Render "Rezultatul este:" text
        result_text = font.render("Rezultatul este: " + str(result.result), True, ACTIVE_COLOR2)
        result_rect = result_text.get_rect()
        result_rect.bottom = screen_height - 20
        result_rect.centerx = screen_width // 2 + 100

        # Draw "Rezultatul este:" text on the screen
        screen.blit(result_text, result_rect)
    # Draw the input box
    box_color = ACTIVE_COLOR if input_active else INACTIVE_COLOR
    pygame.draw.rect(screen, box_color, input_box_rect, 2)
    pygame.draw.rect(screen, box_color, input_box_rect.inflate(-2, -2))

    # Draw the input box2
    box_color2 = ACTIVE_COLOR2 if input_active2 else INACTIVE_COLOR2
    pygame.draw.rect(screen, box_color2, input_box_rect2, 2)
    pygame.draw.rect(screen, box_color2, input_box_rect2.inflate(-2, -2))

    # Text in input box 1
    text_surface = font.render(input_text, True, BLACK)
    screen.blit(text_surface, (input_box_rect.x + 5, input_box_rect.y + 5))

    # Text in input box 2
    text_surface2 = font.render(input_text2, True, BLACK)
    screen.blit(text_surface2, (input_box_rect2.x + 5, input_box_rect2.y + 5))

    pygame.display.update()
