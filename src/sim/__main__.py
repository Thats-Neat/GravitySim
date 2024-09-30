import pygame

pygame.init()
pygame.display.set_caption("Heliocentric - Single Body Orbit/Gravity Sim")
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

header_font = pygame.font.SysFont("monospace", 24)
text_font = pygame.font.SysFont("monospace", 12)

G = 6.67430e-11

# 1 pixel represents 1,000,000 meters
scale = 1e6

# Change below numbers for a different parent (star)
parent_vector = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
parent_mass = 1.988416e30  # kilograms

frames_passed = 0

start_point = [(screen.get_width() / 2) - 100, (screen.get_height() / 2) + 100]

# Change below numbers for a different child (planet)
child_vector = pygame.Vector2(start_point[0], start_point[1])
child_mass = 3.3011e20  # kilograms
child_velocity = pygame.Vector2(1000, 0)  # meters per second

trail = []

orbit_info = False


def create_vector():
    # Get distance between parent and child
    distance_vector = parent_vector - child_vector
    distance = distance_vector.length() * scale  # Convert distance to meters   
    
    # Calculate the gravitational force applied to child
    force_magnitude = G * (parent_mass * child_mass) / (distance ** 2)
    
    # Get the direction of the force (movement towards parent)
    force_direction = distance_vector.normalize()
    
    # Calculate the gravitational force as a vector
    force_vector = force_direction * (force_magnitude / child_mass) * dt
    
    return force_vector, force_magnitude

def populate_trail(decay_trail=True):
    # Adding child position to list
    trail.append(child_vector.xy)

    if decay_trail:
        if len(trail) > 100:
            trail.pop(0)
            
    screen.fill("white")
    
    if len(trail) > 1:
        pygame.draw.lines(screen, "blue", False, trail, 2)
        
        
def draw_bodies():
    pygame.draw.circle(screen, "yellow", parent_vector, 27)
    pygame.draw.circle(screen, "gray", child_vector, 10)


def draw_stats(force_magnitude):
    if orbit_info == False:
        orbit_text = "Unknown/Uncompleted"
    else:        
        orbit_text = "Completed"
        
    header = header_font.render("Child Body:", True, (0, 0, 0), None)
    grav = text_font.render(f"Gravitational Force: {round(force_magnitude, 3)}", True, (0, 0, 0), None)
    orbit = text_font.render(f"Orbit: {orbit_text}", True, (0, 0, 0), None)
    time = text_font.render(f"Passed Frames: {frames_passed}", True, (0, 0, 0), None)
    
    screen.blit(header, (10, 10))
    screen.blit(grav, (10, 45))
    screen.blit(orbit, (10, 65))
    screen.blit(time, (10, 85))
    
    
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    vector_data = create_vector()

    force_vector = vector_data[0]
    force_magnitude = vector_data[1]
    
    # Update the child's velocity using the force
    child_velocity += force_vector / scale
    
    # Update the child's position using the velocity
    child_vector += child_velocity * dt / scale 
        
    if frames_passed > 100:
        if child_vector.x > start_point[0] - 10 and child_vector.x < start_point[0] + 10:
            if child_vector.y > start_point[1] - 10 and child_vector.y < start_point[1] + 10:
                orbit_info = True

    populate_trail(decay_trail=True)
    
    draw_bodies()
    
    draw_stats(force_magnitude)

    pygame.display.flip()

    frames_passed += 1

    dt = clock.tick(60) * 100  # Frame time in seconds

pygame.quit()
