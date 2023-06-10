from controllable_mechanism import ControllableMechansim
from collision_director import CollisionDirector
from color import Color
import pygame

class Actions():
    CORE_MOVE_UP = "core_move_up"
    CORE_MOVE_DOWN = "core_move_down"
    CORE_MOVE_LEFT = "core_move_left"
    CORE_MOVE_RIGHT = "core_move_right"

class Game:
    def __init__(self, pygame_screen, time_between_frame:float, zero_vector:tuple, unit_size:int, background: str = None) -> None:
        self._players = []  # list of players(BlockMechanism)
        self._objects = []   # list of objects(like bullet)
        self._phase = "build"
        self._background = background
        self._screen = pygame_screen
        self._collision_director = CollisionDirector()
        self._time_between_frame = time_between_frame
        self._zero_vector = zero_vector
        self._unit_size = unit_size

    def run(self) -> None:
        # Call this in main loop
        clock = pygame.time.Clock()
        change_normalized_into_real = lambda zero_vector, unit_size, target_vector:(target_vector[0]*unit_size+zero_vector[0], target_vector[1]*unit_size+zero_vector[1])
        
        # Create screen
        # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        
        running = True
        game_time = 0

        while running:
            # print("Main: GAME TIME:", game_time)
            # set up the background
            self._screen.fill((0, 0, 0))

            # collision stuff
            collide = False
            for index1 in range(len(self._players)-1):
                for index2 in range(index1+1, len(self._players)):
                    collision_report = self._collision_director.detect_and_effect_collision(self._players[index1], self._players[index2], self._time_between_frame)
                    if not (collision_report == None):
                        print(collision_report)
                        collide = True
            
            # key events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if not collide:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    self.act(self._players[0], Actions.CORE_MOVE_UP)

                if keys[pygame.K_s]:
                    self.act(self._players[0], Actions.CORE_MOVE_DOWN)
                
                if keys[pygame.K_a]:
                    self.act(self._players[0], Actions.CORE_MOVE_LEFT)

                if keys[pygame.K_d]:
                    self.act(self._players[0], Actions.CORE_MOVE_RIGHT)

                if keys[pygame.K_UP]:
                    self.act(self._players[1], Actions.CORE_MOVE_UP)

                if keys[pygame.K_DOWN]:
                    self.act(self._players[1], Actions.CORE_MOVE_DOWN)

                if keys[pygame.K_LEFT]:
                    self.act(self._players[1], Actions.CORE_MOVE_LEFT)

                if keys[pygame.K_RIGHT]:
                    self.act(self._players[1], Actions.CORE_MOVE_RIGHT)

            # moving stuff
            for player in self._players:
                player.move_by_physics(self._time_between_frame)
            
            # render stuff
            self.__draw(self._zero_vector, self._unit_size)

            # ======== DEBUGGING ==========
            # Draw debugging points on the screen
            pygame.draw.circle(self._screen, Color.MID_SCREEN_COLOR, self._zero_vector, 3)

            # Draw center of mass of player1
            pygame.draw.circle(self._screen, Color.CENTER_OF_MASS_COLOR, change_normalized_into_real(self._zero_vector, self._unit_size, self._players[0].get_center_of_mass_coor()), 3)
            # Draw center of mass of player2
            pygame.draw.circle(self._screen, Color.CENTER_OF_MASS_COLOR, change_normalized_into_real(self._zero_vector, self._unit_size, self._players[1].get_center_of_mass_coor()), 3)
            # draw every blocks coor
            for _, block in self._players[0].get_blocks().items():
                pygame.draw.circle(self._screen, Color.BLOCK_COOR_COLOR, change_normalized_into_real(self._zero_vector, self._unit_size, block.get_coor()), 2)

            
            # Update screen
            pygame.display.flip()
            clock.tick(1/self._time_between_frame) # it doesnt not become super fast idk why
            game_time += 1

        # Quit Pygame
        pygame.quit()
    
    def add_players(self, player1:ControllableMechansim, player2:ControllableMechansim):
        self._players = []
        player1.set_oppo(player2)
        player2.set_oppo(player1)
        self._players.append(player1)
        self._players.append(player2)

    def get_player(self, index: int):
        # Return players[index](BlockAssembly)
        return self._players[index]

    def add_object(self, object) -> None:
        # Add object to objects
        self._objects.append(object)

    def remove_object(self, object) -> None:
        # Remove object from objects
        self._objects.remove(object)

    def get_phase(self) -> str:
        return self._phase

    def set_phase(self, phase: str) -> None:
        self._phase = phase

    def is_valid(self, instruction) -> bool:
        # Check if the instruction is valid for current stage
        condition = None
        if condition:
            return False
        return True

    def act(self, player:ControllableMechansim, action:str) -> None:
        # Apply action on the player
        if action == Actions.CORE_MOVE_UP:
            player.core_move_up(self._time_between_frame)

        elif action == Actions.CORE_MOVE_DOWN:
            player.core_move_down(self._time_between_frame)

        elif action == Actions.CORE_MOVE_LEFT:
            player.core_move_left(self._time_between_frame)
        
        elif action == Actions.CORE_MOVE_RIGHT:
            player.core_move_right(self._time_between_frame)

    def __draw(self, zero_vector:tuple, unit_size:int) -> None:
        # Draw background, players and objects(follow the order)
        # render called below are all undefined yet

        # TODO: make background alive
        # self._background.render()

        for object in self._objects:
            # TODO: add zero vector and unit size so the game wont break
            object.render(self._screen, zero_vector, unit_size)

        for player in self._players:
            player.render(self._screen, zero_vector, unit_size)
        
        pass

    def __events(self):
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                print("Nothing happens")

            if event.type == pygame.QUIT:
                running = False