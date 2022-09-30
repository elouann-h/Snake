import random
import pygame


class Snake:
    def __init__(self, start_coords=(13, 13), start_size=4, direction="nord"):
        self.start_coords = start_coords
        self.start_size = start_size
        self.direction = direction
        self.queue = [(self.start_coords[0], self.start_coords[1], self.direction)]
        self.generate_snake()

    def generate_snake(self):
        x, y = self.start_coords[0], self.start_coords[1]
        for i in range(self.start_size - 1):
            if self.direction == "est":
                x -= 1
            elif self.direction == "ouest":
                x += 1
            elif self.direction == "nord":
                y += 1
            elif self.direction == "sud":
                y -= 1
            self.add_shard()

    def add_shard(self):
        previous = self.queue[0]
        x, y = previous[0], previous[1]
        if previous[2] == "est":
            x -= 1
        elif previous[2] == "ouest":
            x += 1
        elif previous[2] == "nord":
            y += 1
        elif previous[2] == "sud":
            y -= 1
        self.queue.insert(0, (x, y, previous[2]))

    def move(self):
        new_queue = []
        for i in range(len(self.queue)):
            shard = self.queue[i]
            x, y = shard[0], shard[1]
            direction = shard[2]

            if i == len(self.queue) - 1:
                direction = self.direction
            else:
                direction = self.queue[i + 1][2]

            if shard[2] == "est":
                x += 1
            elif shard[2] == "ouest":
                x -= 1
            elif shard[2] == "nord":
                y -= 1
            elif shard[2] == "sud":
                y += 1

            new_queue.append((x, y, direction))

        self.queue = new_queue

    def change_direction(self, direction):
        self.direction = direction

    def collide_with_queue(self):
        head = self.queue[-1]
        for shard in self.queue[:-1]:
            if head[0] == shard[0] and head[1] == shard[1]:
                return True
        return False

    def collide_with_wall(self, width, height):
        head = self.queue[-1]
        if head[0] < 0 or head[0] >= width or head[1] < 0 or head[1] >= height:
            return True
        return False

    def draw_snake(self, screen, square_dims):
        for i in range(len(self.queue)):
            shard = self.queue[i]
            if i == len(self.queue) - 1:
                self.draw_shard(shard, screen, square_dims=square_dims, previous_shard=self.queue[-2])
            if i == 0:
                self.draw_shard(shard, screen, square_dims=square_dims, next_shard=self.queue[1])
            elif i < len(self.queue) - 1:
                self.draw_shard(shard,
                                screen,
                                square_dims=square_dims,
                                previous_shard=self.queue[i + 1],
                                next_shard=self.queue[i - 1])

    @staticmethod
    def get_radius(shard, prev=None, nex=None, tail_radius=15, head_radius=12, angle_radius=7):
        topl, topr, bottoml, bottomr = 0, 0, 0, 0
        if nex is None:
            adir, pdir = shard[2], prev[2]
            if adir == "nord":
                if pdir == "nord":
                    topl, topr = head_radius, head_radius
                elif pdir == "est":
                    topr, bottomr = head_radius, angle_radius
                elif pdir == "ouest":
                    topl, bottoml = head_radius, angle_radius
            elif adir == "est":
                if pdir == "est":
                    topr, bottomr = head_radius, head_radius
                if pdir == "nord":
                    topl, topr = angle_radius, head_radius
                if pdir == "sud":
                    bottoml, bottomr = angle_radius, head_radius
            elif adir == "ouest":
                if pdir == "ouest":
                    topl, bottoml = head_radius, head_radius
                elif pdir == "nord":
                    topr, topl = angle_radius, head_radius
                elif pdir == "sud":
                    bottoml, bottomr = head_radius, angle_radius
            elif adir == "sud":
                if pdir == "sud":
                    bottoml, bottomr = head_radius, head_radius
                elif pdir == "est":
                    topr, bottomr = angle_radius, head_radius
                elif pdir == "ouest":
                    topl, bottoml = angle_radius, head_radius
        elif nex is not None and prev is not None:
            ndir, adir, pdir = nex[2], shard[2], prev[2]
            if adir == "nord":
                if ndir == "est":
                    bottomr = angle_radius
                if ndir == "ouest":
                    bottoml = angle_radius
            elif adir == "est":
                if ndir == "nord":
                    topl = angle_radius
                elif ndir == "sud":
                    bottoml = angle_radius
            elif adir == "ouest":
                if ndir == "nord":
                    topr = angle_radius
                elif ndir == "sud":
                    bottomr = angle_radius
            elif adir == "sud":
                if ndir == "est":
                    topr = angle_radius
                elif ndir == "ouest":
                    topl = angle_radius

        return topl, topr, bottoml, bottomr

    @staticmethod
    def draw_shard(shard, screen, square_dims, previous_shard=None, next_shard=None):
        color = (0, 210, 0)

        if next_shard is None:
            color = (0, 255, 0)

        shard_radius = Snake.get_radius(shard, prev=previous_shard, nex=next_shard)

        x, y = shard[0] * square_dims, shard[1] * square_dims
        pygame.draw.rect(screen,
                         color,
                         (x, y, square_dims, square_dims),
                         0,
                         border_top_left_radius=shard_radius[0],
                         border_top_right_radius=shard_radius[1],
                         border_bottom_left_radius=shard_radius[2],
                         border_bottom_right_radius=shard_radius[3])

class Apple:
    def __init__(self, coords=(0, 0)):
        self.coords = coords

    def summon(self, snake, width, height):
        valid_coords = []
        for x in range(width):
            for y in range(height):
                if (x, y) not in tuple(map(lambda shard: (shard[0], shard[1]), snake.queue)):
                    valid_coords.append((x, y))
        self.coords = random.choice(valid_coords)

    def eaten(self, snake):
        head = snake.queue[-1]
        return self.coords == (head[0], head[1])

    def draw_apple(self, screen, square_dims):
        x, y = self.coords[0] * square_dims, self.coords[1] * square_dims
        pygame.draw.circle(screen, (255, 0, 0), (x + square_dims // 2, y + square_dims // 2), square_dims // 2, 0)