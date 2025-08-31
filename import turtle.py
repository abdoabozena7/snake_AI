import turtle
import random
from collections import deque

screen = turtle.Screen()
screen.title("Snake game")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)

class Snake:
    def __init__(self):
        self.body = []
        self.create_snake()
        self.head = self.body[0]

    def create_snake(self):
        positions = [(0, 0), (-20, 0), (-40, 0)]
        for position in positions:
            self.add_segment(position)

    def add_segment(self, position):
        segment = turtle.Turtle("square")
        segment.color("green")
        segment.penup()
        segment.goto(position)
        self.body.append(segment)
        self.body
    def extend(self):
        self.add_segment(self.body[-1].position())

    def move(self, path=None):
        if path:
            next_position = path[0]
            for i in range(len(self.body) - 1, 0, -1):
                self.body[i].goto(self.body[i - 1].position())
            self.head.goto(next_position)
        else:
            for i in range(len(self.body) - 1, 0, -1):
                self.body[i].goto(self.body[i - 1].position())
            self.head.forward(20)

    def get_positions(self):
        return [segment.position() for segment in self.body]

class Food:
    def __init__(self):
        self.food = turtle.Turtle("circle")
        self.food.color("red")
        self.food.penup()
        self.refresh()

    def refresh(self):
        x = random.randint(-280, 280) // 20 * 20
        y = random.randint(-280, 280) // 20 * 20
        self.food.goto(x, y)

    def position(self):
        return self.food.position()

# خوارزمية BFS
def bfs(start, goal, obstacles):
    queue = deque([start])
    visited = {start: None}

    directions = [(20, 0), (-20, 0), (0, 20), (0, -20)]

    while queue:
        current = queue.popleft()
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = visited[current]
            return path[::-1]
        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if neighbor not in visited and neighbor not in obstacles and -300 < neighbor[0] < 300 and -300 < neighbor[1] < 300:
                queue.append(neighbor)
                visited[neighbor] = current

    return None  # إذا لم يكن هناك طريق

# اللعبة
snake = Snake()
food = Food()

def game_loop():
    obstacles = set(snake.get_positions())
    food_position = food.position()
    snake_head_position = snake.head.position()

    path = bfs(snake_head_position, food_position, obstacles)

    if path and len(path) > 1:
        snake.move(path[1:2])
    else:
        snake.move()

    # إذا أكل الثعبان الطعام
    if snake.head.distance(food.food) < 20:
        food.refresh()
        snake.extend()

    # إذا اصطدم الثعبان بنفسه
    if snake.head.position() in obstacles:
        print("Game Over")
        return

    screen.update()
    screen.ontimer(game_loop, 100)

# تشغيل اللعبة
screen.listen()
screen.ontimer(game_loop, 100)
screen.mainloop()
