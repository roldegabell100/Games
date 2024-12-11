import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        
        self.canvas = tk.Canvas(master, width=400, height=400, bg='black')
        self.canvas.pack()
        
        self.score_label = tk.Label(master, text="Score: 0", font=("Arial", 14))
        self.score_label.pack()
        
        self.restart_button = tk.Button(master, text="Restart", command=self.restart_game, state=tk.DISABLED)
        self.restart_button.pack()
        
        self.last_food_color = None  # Initialize last food color
        self.last_collected_color = None  # Track last collected food color
        self.initialize_game()

    def initialize_game(self):
        """Initialize or reset the game state."""
        self.snake = [(200, 200)]  # Start the snake with one segment (the head)
        self.snake_colors = ['green']  # List to hold colors for each segment
        self.snake_direction = "Right"
        
        self.food_position = self.place_food()
        self.food_color = self.random_food_color()  # Initialize the food color
        self.last_food_color = self.food_color  # Store last food color
        self.score = 0
        
        self.update_score()
        
        self.master.bind("<Key>", self.change_direction)
        self.game_loop()

    def random_food_color(self):
        """Randomly select a color from a predefined list of colors, ensuring it's different from the last."""
        colors = ['red', 'blue', 'green', 'orange'] #color pool -> list of colors
        new_color = random.choice(colors)
        while new_color == self.last_food_color:  # Ensure new color is different from last
            new_color = random.choice(colors)
        self.last_food_color = new_color  # Update the last food color
        return new_color

    def place_food(self):
        """Places the food at a random position and assigns a new random color to it."""
        while True:
            x = random.randint(0, 39) * 10
            y = random.randint(0, 39) * 10
            food_color = self.random_food_color()  # Get a new color for the food
            return (x, y, food_color)  # Return position with color

    def change_direction(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            self.snake_direction = event.keysym

    def move_snake(self):
        head_x, head_y = self.snake[0]
        
        if self.snake_direction == "Up":
            new_head = (head_x, head_y - 10)
        elif self.snake_direction == "Down":
            new_head = (head_x, head_y + 10)
        elif self.snake_direction == "Left":
            new_head = (head_x - 10, head_y)
        elif self.snake_direction == "Right":
            new_head = (head_x + 10, head_y)
        
        self.snake.insert(0, new_head)  # Add new head at the front

        # Get food position and color
        food_position, food_color = self.food_position[:-1], self.food_position[-1]

        if new_head == food_position:
            self.snake_colors.insert(0, food_color)  # Change head's color to food color
            
            # Check if the color is the same as the last collected color
            if food_color == self.last_collected_color:
                self.score += 2  # Double points for collecting the same color
            else:
                self.score += 1  # Normal points for a new color

            self.last_collected_color = food_color  # Update the last collected color
            self.food_position = self.place_food()  # Place new food and change its color
        else:
            self.snake.pop()  # Remove the last segment if not eating food
            self.snake_colors.pop()  # Remove the last segment's color
            
        # Ensure synchronization if snake loses length by not eating food
        if len(self.snake_colors) < len(self.snake):
            self.snake_colors.append('green')  # Append default color for new segments if needed
        
        # Check for three consecutive segments of the same color
        self.check_two_consecutive_colors()

    def check_two_consecutive_colors(self):
        """Check for three consecutive segments of the same color."""
        for i in range(0, len(self.snake_colors) - 2, 2):  # Increment by 2
            if (self.snake_colors[i] == self.snake_colors[i + 1] == self.snake_colors[i + 2]):
                self.score += 2  # Increment score for two consecutive segments
                break  # Exit the loop after counting a set of two

    def check_collisions(self):
        head_x, head_y = self.snake[0]
        
        # Check for wall collisions
        if (head_x < 0 or head_x >= 400 or 
            head_y < 0 or head_y >= 400 or 
            len(self.snake) != len(set(self.snake))):
            self.game_over()
            return True

        return False
    
    # Enable the restart button
    def game_over(self):
        self.canvas.create_text(200, 200, text="Game Over!", fill="red", font=("Arial", 24))
        self.master.unbind("<Key>")
        self.restart_button.config(state=tk.NORMAL)  
        # ! can be used to restart the canvas once the flask files are created *FIAM
    # Disable the restart button
    def restart_game(self):
        """Reset game state and restart the game."""
        self.canvas.delete(tk.ALL)  # Clear the canvas
        self.score = 0  # Reset score
        self.update_score()  # Update score display
        self.restart_button.config(state=tk.DISABLED)  
        self.initialize_game()  # Reinitialize game state

    def update_score(self):
        """Update the score label.""" # todo: why did i put this here?
        self.score_label.config(text=f"Score: {self.score}")

#  creating the game background. which in this case im using a grid system
    def draw_grid(self):
        """Draw a grid on the canvas."""
        for i in range(0, 401, 10):  # Vertical lines
            self.canvas.create_line(i, 0, i, 400, fill='gray')
        for j in range(0, 401, 10):  # Horizontal lines
            self.canvas.create_line(0, j, 400, j, fill='gray')

    def draw_optical_illusion(self):
        """Draw optical illusions in the background."""
        for i in range(0, 400, 20):
            # Create alternating rectangles to give an illusion effect
            self.canvas.create_rectangle(i, 0, i + 20, 400, fill='lightgray' if i % 40 == 0 else 'darkgray')

    def draw_elements(self):
        self.canvas.delete(tk.ALL)  # Clear canvas before redrawing
        self.draw_optical_illusion()  # Draw the optical illusion background
        self.draw_grid()  # Draw the grid background
        
        # Draw the snake segments with their respective colors
        for i, segment in enumerate(self.snake):
            x, y = segment
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill=self.snake_colors[i])
        
        # Draw the food with the current food color
        food_x, food_y = self.food_position[:-1]  # Get food position
        self.canvas.create_oval(food_x, food_y, food_x + 10, food_y + 10, fill=self.food_position[-1])  # Get food color

    def game_loop(self):
        if not self.check_collisions():
            self.move_snake()
            self.draw_elements()
            self.update_score()  # Update the score display
            self.master.after(100, self.game_loop)

if __name__ == "__main__":
    win = tk.Tk()
    game = SnakeGame(win)
    win.mainloop()
