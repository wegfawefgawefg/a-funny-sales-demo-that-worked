import pygame, sys, math, random

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 1200, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sales Demo Presentation")

# Load and scale images to a base size of 200x200
image_files = ["assets/phone.png", "assets/gandk.png", "assets/10percent.png"]
base_size = (200, 200)
base_images = [pygame.image.load(path).convert_alpha() for path in image_files]
base_images = [pygame.transform.smoothscale(img, base_size) for img in base_images]

# Define positions for left, middle, and right options
positions = [
    (screen_width * 0.25, screen_height * 0.5),
    (screen_width * 0.5, screen_height * 0.5),
    (screen_width * 0.75, screen_height * 0.5),
]

selected = 0  # Currently selected image index
clock = pygame.time.Clock()

# Lists for confetti particles and balloons
confetti_particles = []
balloons = []


# Define the ConfettiParticle class
class ConfettiParticle:
    def __init__(self, pos):
        self.pos = list(pos)
        # Random velocity for a burst effect
        self.vel = [random.uniform(-3, 3), random.uniform(-8, -3)]
        # Basic colors: red, green, yellow, blue
        self.color = random.choice(
            [
                (255, 0, 0),  # red
                (0, 255, 0),  # green
                (255, 255, 0),  # yellow
                (0, 0, 255),  # blue
            ]
        )
        self.life = random.uniform(2, 4)  # lifespan in seconds
        self.size = random.randint(3, 6)
        self.time_alive = 0

    def update(self, dt):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.time_alive += dt

    def is_dead(self):
        return self.time_alive >= self.life

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (*self.pos, self.size, self.size))


# Define the Balloon class
class Balloon:
    def __init__(self):
        self.x = random.uniform(50, screen_width - 50)
        self.y = screen_height + random.randint(10, 50)
        self.speed = random.uniform(1, 3)
        # Basic colors: red, green, yellow, blue
        self.color = random.choice(
            [
                (255, 0, 0),  # red
                (0, 255, 0),  # green
                (255, 255, 0),  # yellow
                (0, 0, 255),  # blue
            ]
        )
        self.size = random.randint(30, 50)

    def update(self, dt):
        self.y -= self.speed

    def is_off_screen(self):
        return self.y + self.size < 0

    def draw(self, surface):
        # Draw an ellipse to represent the balloon
        balloon_rect = (self.x, self.y, self.size, int(self.size * 1.2))
        pygame.draw.ellipse(surface, self.color, balloon_rect)
        # Draw a white string beneath the balloon
        string_start = (self.x + self.size / 2, self.y + int(self.size * 1.2))
        string_end = (self.x + self.size / 2, self.y + int(self.size * 1.2) + 20)
        pygame.draw.line(surface, (255, 255, 255), string_start, string_end, 2)


while True:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                selected = (selected - 1) % len(base_images)
            elif event.key == pygame.K_RIGHT:
                selected = (selected + 1) % len(base_images)
            elif event.key in [pygame.K_q, pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_SPACE:
                # Spawn a burst of confetti from the selected option's position
                for _ in range(50):
                    confetti_particles.append(ConfettiParticle(positions[selected]))
                # Spawn a few balloons from the bottom of the screen
                for _ in range(5):
                    balloons.append(Balloon())

    screen.fill((30, 30, 30))  # Background color

    # Calculate pulse scale using a sine wave
    t = pygame.time.get_ticks() / 500.0
    pulse_scale = 1 + 0.1 * math.sin(t)

    # Draw each image at its designated position
    for i, img in enumerate(base_images):
        scale = pulse_scale if i == selected else 1.0
        new_size = (int(base_size[0] * scale), int(base_size[1] * scale))
        scaled_img = pygame.transform.smoothscale(img, new_size)
        img_rect = scaled_img.get_rect(center=positions[i])
        screen.blit(scaled_img, img_rect)

    # Update and draw confetti particles
    for particle in confetti_particles[:]:
        particle.update(dt)
        particle.draw(screen)
        if particle.is_dead():
            confetti_particles.remove(particle)

    # Update and draw balloons
    for balloon in balloons[:]:
        balloon.update(dt)
        balloon.draw(screen)
        if balloon.is_off_screen():
            balloons.remove(balloon)

    pygame.display.flip()
