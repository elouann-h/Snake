import pygame
import classes
import time

pygame.init()
clock = pygame.time.Clock()
sps = 5

screen = pygame.display.set_mode((750, 750))
pygame.display.set_caption("Snake")

snake = classes.Snake(start_size=10)
apple = classes.Apple()

apple.summon(snake, 25, 25)

timer = time.time()
last_change = time.time()

while True:
    screen.fill((40, 100, 40))
    for i in range(25):
        for j in range(25):
            pygame.draw.rect(screen, (70, 130, 70), (i * 30, j * 30, 30, 30), 1)

    if (time.time() - timer) >= (1/sps):
        snake.move()
        if snake.collide_with_wall(25, 25) or snake.collide_with_queue():
            pygame.quit()
            quit()
        if apple.eaten(snake):
            apple.summon(snake, 25, 25)
            snake.add_shard()
        timer = time.time()

    apple.draw_apple(screen, 30)
    snake.draw_snake(screen, 30)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            pressed = event.key
            if time.time() - last_change >= (1/(sps+1)):
                if pressed == pygame.K_UP:
                    if snake.direction != "sud":
                        snake.change_direction("nord")
                elif pressed == pygame.K_DOWN:
                    if snake.direction != "nord":
                        snake.change_direction("sud")
                elif pressed == pygame.K_LEFT:
                    if snake.direction != "est":
                        snake.change_direction("ouest")
                elif pressed == pygame.K_RIGHT:
                    if snake.direction != "ouest":
                        snake.change_direction("est")
                last_change = time.time()

    pygame.display.flip()
    clock.tick(60)