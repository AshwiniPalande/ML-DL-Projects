import pygame
import heapq
import random
import time


GRID_SIZE = 15
CELL_SIZE = 45
WIDTH = HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 6

CHARGING_STATION = (7, 7)

# A* SEARCH

def astar(start, goal, obstacles):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    nodes_expanded = 0
    start_time = time.time()

    def heuristic(a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    while open_set:
        current = heapq.heappop(open_set)[1]
        nodes_expanded += 1

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], nodes_expanded, round(time.time()-start_time,4)

        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            neighbor = (current[0]+dx, current[1]+dy)

            if (0 <= neighbor[0] < GRID_SIZE and
                0 <= neighbor[1] < GRID_SIZE and
                neighbor not in obstacles):

                tentative = g_score[current] + 1

                if neighbor not in g_score or tentative < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative
                    f_score = tentative + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))

    return [], nodes_expanded, 0  


class Robot:
    def __init__(self, rid, start, color, priority):
        self.id = rid
        self.position = start
        self.color = color
        self.priority = priority
        self.battery = 100
        self.task = None
        self.path = []
        self.index = 0
        self.metrics = {}

    def assign_task(self, task, obstacles):
        self.task = task
        self.plan(obstacles)

    def plan(self, obstacles):
        if self.task:
            path, nodes, t = astar(self.position, self.task, obstacles)

            if path:  
                self.path = path
                self.index = 0
                self.metrics = {
                    "nodes": nodes,
                    "cost": len(path),
                    "time": t
                }
            else:
                self.path = []
                self.metrics = {"nodes": "-", "cost": "-", "time": "-"}

    def needs_charge(self):
        return self.battery <= 15

    def move(self, reserved_positions, obstacles):
        if self.needs_charge():
            self.task = CHARGING_STATION
            self.plan(obstacles)

        if self.index + 1 < len(self.path):
            next_pos = self.path[self.index + 1]

            if next_pos not in reserved_positions:
                self.index += 1
                self.position = next_pos
                self.battery -= 0.5
                reserved_positions.add(next_pos)
            else:
                
                self.plan(obstacles)
        else:
            if self.position == self.task:
                if self.task == CHARGING_STATION:
                    self.battery = 100
                self.task = None

class TaskManager:
    def __init__(self):
        self.tasks = []

    def generate_task(self):
        while True:
            task = (random.randint(0, GRID_SIZE-1),
                    random.randint(0, GRID_SIZE-1))
            if task != CHARGING_STATION:
                self.tasks.append(task)
                break

    def assign_tasks(self, robots, obstacles):
        for robot in robots:
            if robot.task is None and self.tasks:
                nearest = min(
                    self.tasks,
                    key=lambda t: abs(robot.position[0]-t[0]) +
                                  abs(robot.position[1]-t[1])
                )
                robot.assign_task(nearest, obstacles)
                self.tasks.remove(nearest)



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT+120))
pygame.display.set_caption("Multi-Agent Warehouse AI")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

obstacles = set()
robots = [
    Robot(1, (0,0), (255,0,0), priority=1),
    Robot(2, (14,0), (0,0,255), priority=2)
]

task_manager = TaskManager()
for _ in range(6):
    task_manager.generate_task()

makespan = 0
mouse_was_pressed = False


running = True

while running:
    clock.tick(FPS)
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pressed = pygame.mouse.get_pressed()[0]
    if mouse_pressed and not mouse_was_pressed:
        x, y = pygame.mouse.get_pos()
        if y < HEIGHT:
            cell = (x//CELL_SIZE, y//CELL_SIZE)
            obstacles.add(cell)
            for r in robots:
                r.plan(obstacles)
    mouse_was_pressed = mouse_pressed

    task_manager.assign_tasks(robots, obstacles)

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE,
                               CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (220,220,220), rect, 1)

            if (x,y) in obstacles:
                pygame.draw.rect(screen, (0,0,0), rect)

            if (x,y) == CHARGING_STATION:
                pygame.draw.rect(screen, (0,255,0), rect)

    robots_sorted = sorted(robots, key=lambda r: r.priority)
    reserved_positions = set()

    for r in robots_sorted:
        r.move(reserved_positions, obstacles)

    for task in task_manager.tasks:
        pygame.draw.circle(
            screen, (255,165,0),
            (task[0]*CELL_SIZE+CELL_SIZE//2,
             task[1]*CELL_SIZE+CELL_SIZE//2), 8
        )

    for r in robots:
        pygame.draw.circle(
            screen, r.color,
            (r.position[0]*CELL_SIZE+CELL_SIZE//2,
             r.position[1]*CELL_SIZE+CELL_SIZE//2),
            CELL_SIZE//3
        )

    panel_y = HEIGHT + 10
    for r in robots:
        text = f"Robot {r.id} | Battery: {int(r.battery)} | Task: {r.task} | Nodes: {r.metrics.get('nodes')} | Cost: {r.metrics.get('cost')} | Time: {r.metrics.get('time')}"
        screen.blit(font.render(text, True, (0,0,0)), (10, panel_y))
        panel_y += 25

    pygame.display.flip()
    makespan += 1

pygame.quit()

print("\nTotal Makespan:", makespan)
