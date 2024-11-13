import turtle

# Set up the screen
screen = turtle.Screen()
screen.title("Click to store coordinates")

# Load the background image
# Replace 'car.gif' with the path to your image
screen.bgpic("car.gif")

# List to store coordinates
coordinates = []

# Function to handle click and store coordinates
def store_coordinates(x, y):
    coordinates.append((x, y))
    print(f"Clicked at: ({x}, {y})")

# Register the click event
screen.onclick(store_coordinates)

# Keep the window open until closed by the user
turtle.done()
