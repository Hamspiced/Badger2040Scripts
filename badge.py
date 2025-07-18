import badger2040
import jpegdec
import os
import time

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

IMAGE_WIDTH = 104

COMPANY_HEIGHT = 30
DETAILS_HEIGHT = 20
NAME_HEIGHT = HEIGHT - COMPANY_HEIGHT - (DETAILS_HEIGHT * 2) - 2
TEXT_WIDTH = WIDTH - IMAGE_WIDTH - 1

COMPANY_TEXT_SIZE = 0.6
DETAILS_TEXT_SIZE = 0.5

LEFT_PADDING = 5
NAME_PADDING = 20
DETAIL_SPACING = 10

BADGE_DIR = "/badges"
DEFAULT_IMAGE = "/badges/badge.jpg"

# Button pins
BUTTON_UP = 11
BUTTON_DOWN = 15

# Setup
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(badger2040.UPDATE_NORMAL)
display.set_thickness(2)
jpeg = jpegdec.JPEG(display.display)

# Find all badgeX.txt files
badge_files = sorted([f for f in os.listdir(BADGE_DIR) if f.startswith("badge") and f.endswith(".txt")])
badge_index = 0
NUM_BADGES = len(badge_files)

# Fallback content
company = "missing"
name = "badge"
detail1_title = "file"
detail1_text = "not"
detail2_title = "found"
detail2_text = "!"
badge_image = DEFAULT_IMAGE

def truncatestring(text, text_size, width):
    while True:
        length = display.measure_text(text, text_size)
        if length > 0 and length > width:
            text = text[:-1]
        else:
            return text

def load_badge(index):
    global company, name, detail1_title, detail1_text, detail2_title, detail2_text, badge_image
    try:
        with open(f"{BADGE_DIR}/{badge_files[index]}", "r") as badge:
            company = badge.readline().strip()
            name = badge.readline().strip()
            detail1_title = badge.readline().strip()
            detail1_text = badge.readline().strip()
            detail2_title = badge.readline().strip()
            detail2_text = badge.readline().strip()
            badge_image = badge.readline().strip()
    except:
        company = "error"
        name = badge_files[index]
        detail1_title = "couldn't"
        detail1_text = "read"
        detail2_title = "file"
        detail2_text = "!"

    company = truncatestring(company, COMPANY_TEXT_SIZE, TEXT_WIDTH)
    detail1_title = truncatestring(detail1_title, DETAILS_TEXT_SIZE, TEXT_WIDTH)
    detail1_text = truncatestring(detail1_text, DETAILS_TEXT_SIZE,
                                  TEXT_WIDTH - DETAIL_SPACING - display.measure_text(detail1_title, DETAILS_TEXT_SIZE))
    detail2_title = truncatestring(detail2_title, DETAILS_TEXT_SIZE, TEXT_WIDTH)
    detail2_text = truncatestring(detail2_text, DETAILS_TEXT_SIZE,
                                  TEXT_WIDTH - DETAIL_SPACING - display.measure_text(detail2_title, DETAILS_TEXT_SIZE))

def draw_badge():
    display.set_pen(0)
    display.clear()

    try:
        jpeg.open_file(badge_image)
        jpeg.decode(WIDTH - IMAGE_WIDTH, 0)
        display.set_pen(0)
        display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - 1, 0)
        display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - IMAGE_WIDTH, HEIGHT - 1)
        display.line(WIDTH - IMAGE_WIDTH, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)
        display.line(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)
    except:
        display.text("Image load error", 10, 10, WIDTH, 0.6)

    display.set_pen(15)
    display.set_font("serif")
    display.text(company, LEFT_PADDING, (COMPANY_HEIGHT // 2) + 1, WIDTH, COMPANY_TEXT_SIZE)

    display.set_pen(15)
    display.rectangle(1, COMPANY_HEIGHT + 1, TEXT_WIDTH, NAME_HEIGHT)

    display.set_pen(0)
    display.set_font("sans")
    name_size = 2.0
    while True:
        name_length = display.measure_text(name, name_size)
        if name_length >= (TEXT_WIDTH - NAME_PADDING) and name_size >= 0.1:
            name_size -= 0.01
        else:
            display.text(name, (TEXT_WIDTH - name_length) // 2,
                         (NAME_HEIGHT // 2) + COMPANY_HEIGHT + 1, WIDTH, name_size)
            break

    display.set_pen(15)
    display.rectangle(1, HEIGHT - DETAILS_HEIGHT * 2, TEXT_WIDTH, DETAILS_HEIGHT - 1)
    display.rectangle(1, HEIGHT - DETAILS_HEIGHT, TEXT_WIDTH, DETAILS_HEIGHT - 1)

    display.set_pen(0)
    display.set_font("sans")
    d1 = display.measure_text(detail1_title, DETAILS_TEXT_SIZE)
    d2 = display.measure_text(detail2_title, DETAILS_TEXT_SIZE)

    display.text(detail1_title, LEFT_PADDING, HEIGHT - ((DETAILS_HEIGHT * 3) // 2), WIDTH, DETAILS_TEXT_SIZE)
    display.text(detail1_text, LEFT_PADDING + d1 + DETAIL_SPACING, HEIGHT - ((DETAILS_HEIGHT * 3) // 2), WIDTH, DETAILS_TEXT_SIZE)

    display.text(detail2_title, LEFT_PADDING, HEIGHT - (DETAILS_HEIGHT // 2), WIDTH, DETAILS_TEXT_SIZE)
    display.text(detail2_text, LEFT_PADDING + d2 + DETAIL_SPACING, HEIGHT - (DETAILS_HEIGHT // 2), WIDTH, DETAILS_TEXT_SIZE)

    display.update()

# Initial load
load_badge(badge_index)
draw_badge()

# Main loop
while True:
    display.keepalive()

    if display.pressed(BUTTON_DOWN):
        badge_index = (badge_index + 1) % NUM_BADGES
        load_badge(badge_index)
        draw_badge()

    elif display.pressed(BUTTON_UP):
        badge_index = (badge_index - 1 + NUM_BADGES) % NUM_BADGES
        load_badge(badge_index)
        draw_badge()

    display.halt()