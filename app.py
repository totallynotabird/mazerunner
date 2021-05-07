import pygame, os, time, random

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.start_x = x
        self.start_y = y

        self.change_x = 0
        self.change_y = 0

        self.lives = 3

    def changeSpeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def move(self, walls, enemies):

        # collision detection horizontal
        self.rect.x += self.change_x

        block_list_hit = pygame.sprite.spritecollide(self, walls, False)
        for block in block_list_hit:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        # collision detection vertical
        self.rect.y += self.change_y

        block_list_hit = pygame.sprite.spritecollide(self, walls, False)
        for block in block_list_hit:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        # collision detection enemies
        block_list_hit = pygame.sprite.spritecollide(self, enemies, False)

        for enemy in block_list_hit:
            self.hitEnemy()

    def hitEnemy(self):
        time.sleep(1)
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.lives -= 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x_start, y_start, x_stop, y_stop, speed, color) -> None:
        super().__init__()

        self.image = pygame.Surface([15, 15])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x_start
        self.rect.y = y_start

        self.speed = speed

        if x_start < x_stop:
            self.min_x = x_start
            self.max_x = x_stop
            self.x_dir = 1
        else:
            self.min_x = x_stop
            self.max_x = x_start
            self.x_dir = 1

        if y_start < y_stop:
            self.min_y = y_start
            self.max_y = y_stop
            self.y_dir = 1
        else:
            self.min_y = y_stop
            self.max_y = y_start
            self.y_dir = 1

    def move(self):

        if self.x_dir == 1:
            if self.rect.x < self.max_x:
                self.rect.x += self.speed
            else:
                self.x_dir = -1
        else:
            if self.rect.x > self.min_x:
                self.rect.x -= self.speed
            else:
                self.x_dir = 1

        if self.y_dir == 1:
            if self.rect.y < self.max_y:
                self.rect.y += self.speed
            else:
                self.y_dir = -1
        else:
            if self.rect.y > self.min_y:
                self.rect.y -= self.speed
            else:
                self.y_dir = 1


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Treasure(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color) -> None:
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Vector2(object):
    def __init__(self, row, col) -> None:
        super().__init__()
        self.x = col
        self.y = row

    def offset(self, offset) -> None:
        self.x += offset.x
        self.y += offset.y        

    def difference(self, offset) -> None:
        self.x = offset.x - self.x
        self.y = offset.y - self.y

    def toString(self) -> str:
        return "[" + str(self.x) + ', ' + str(self.y) + "]"

class Cardinals(object):
    def __init__(self , value=True) -> None:
        super().__init__()
        self.north = value
        self.south = value
        self.east = value
        self.west = value


class Room(object):
    def __init__(self, row, col) -> None:
        self.wall_list = pygame.sprite.Group()
        self.treasure_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.pathed = False
        self.location = Vector2(row, col)
        self.walls = Cardinals()

    def build(self, color):
        if self.walls.east:
            self.createWall(780, 0, 20, 600, color)  # right wall
        else:
            self.createWall(780, 0, 20, 250, color)  # right wall
            self.createWall(780, 350, 20, 250, color)  # right wall 2        
        if self.walls.west:
            self.createWall(0, 0, 20, 600, color)  # left wall
        else:
            self.createWall(0, 0, 20, 250, color)  # left wall
            self.createWall(0, 350, 20, 250, color)  # left wall 2
        if self.walls.north:
            self.createWall(0, 0, 800, 20, color)  # top wall
        else:
            self.createWall(0, 0, 350, 20, color)  # top wall 1
            self.createWall(450, 0, 350, 20, color)  # top wall 2
        if self.walls.south:
            self.createWall(0, 580, 800, 20, color)  # bottom wall
        else:
            self.createWall(0, 580, 350, 20, color)  # bottom wall 1
            self.createWall(450, 580, 350, 20, color)  # bottom wall 2
     

    def createWall(self, x, y, width, height, color):
        wall = Wall(x, y, width, height, color)
        self.wall_list.add(wall)

    def createTreasure(self, x, y, width, height, color):
        treasure = Treasure(x, y, width, height, color)
        self.treasure_list.add(treasure)

    def createEnemy(self, x_start, y_start, x_stop, y_stop, speed, color):
        enemy = Enemy(x_start, y_start, x_stop, y_stop, speed, color)
        self.enemy_list.add(enemy)

class Maze(object):
    def __init__(self, x_lim, y_lim) -> None:
        super().__init__()
        self.roomCount = x_lim * y_lim
        self.rooms = []

        for i in range (y_lim):
            self.rooms.append([])
            for j in range (x_lim):
                self.rooms[i].append(Room(j, i))
                
                pass
            pass

        
        
        # self.buildBorders(GREEN)
        self.carvePaths(0, 0)
        self.buildMaze(GREEN)
        
        

        
    def buildMaze(self, color):
        for row in self.rooms:
            for room in row:
                room.build(color)

        pass

    def buildBorders(self, color):
        
        # top border across the top of the maze
        for room in self.rooms[0]:
            room.createWall(0, 0, 800, 20, color)  # top wall

        # bottom border across the bottom of the maze
        for room in self.rooms[self.rooms.__len__() - 1]:
            room.createWall(0, 580, 800, 20, color)  # bottom wall

        # left border on the left of the maze
        for row in self.rooms:
            row[0].createWall(0, 0, 20, 600, color)  # left wall

        # right border on the right on the maze
        for row in self.rooms:
            row[row.__len__() - 1].createWall(780, 0, 20, 600, color)  # right wall

    def carvePaths(self, row, col):
        roomsVisited = 0
        pathStack = []

        currentRoom = Vector2(row, col)
        
        while roomsVisited < self.roomCount:

            self.rooms[currentRoom.y][currentRoom.x].pathed = True
            roomsVisited += 1

            # gather neighbors of this room, ignoring borders and pathed rooms
            neighbors = self.findNeighbors(currentRoom.y, currentRoom.x)
            # then pick one 
            if neighbors:
                pathStack.append(currentRoom)
                nextRoom = random.choice(neighbors)                     
                # print(currentRoom.toString() + " -> "+ nextRoom.toString())
            
                direction = Vector2(currentRoom.y, currentRoom.x)
                direction.difference(nextRoom)
                # print(direction.toString())
                self.placeDoor(direction, currentRoom)

                currentRoom = nextRoom
            else:
                if roomsVisited == self.roomCount:
                    break
                # print("dead end" + pathStack[-1].toString())
                
                pathStack.pop()
                # print(pathStack[-1].toString())
                currentRoom = pathStack[-1]
                # print(str(roomsVisited) + 'rooms visited')
                roomsVisited -= 1
                
        
    
    def placeDoor(self, direction, currentRoom):
        if direction.y < 0:
            self.rooms[currentRoom.y][currentRoom.x].walls.north = False
            self.rooms[currentRoom.y - 1][currentRoom.x].walls.south = False
            
        if direction.y > 0:
            self.rooms[currentRoom.y][currentRoom.x].walls.south = False
            self.rooms[currentRoom.y + 1][currentRoom.x].walls.north = False
            
        if direction.x > 0:
            self.rooms[currentRoom.y][currentRoom.x].walls.east = False
            self.rooms[currentRoom.y][currentRoom.x + 1].walls.west = False
            
        if direction.x < 0:
            self.rooms[currentRoom.y][currentRoom.x].walls.west = False
            self.rooms[currentRoom.y][currentRoom.x - 1].walls.east = False
            
        

    def findNeighbors(self, row, col) -> list:
        neighbors = []
        # gether neighbors of this room, ignoring borders
        if row > 0:
            if not self.rooms[row-1][col].pathed:
                neighbors.append(Vector2(row - 1, col))
        if row < self.rooms.__len__() - 1:
            if not self.rooms[row+1][col].pathed:
                neighbors.append(Vector2(row + 1, col))
        if col > 0:
            if not self.rooms[row][col-1].pathed:
                neighbors.append(Vector2(row, col - 1))
        if col < self.rooms.__len__() - 1:
            if not self.rooms[row][col+1].pathed:
                neighbors.append(Vector2(row, col + 1))

        return neighbors

    def placeTreasure(self, color, loc):
        treasureRow = loc[1]
        treasureCol = loc[0]
        print('treasure at: x ' + str(treasureCol) + " y " + str(treasureRow))

        self.rooms[treasureRow][treasureCol].createTreasure(375, 275, 50, 50, color)

# room with enemy template

# class Room0(Room):
#     def __init__(self):
#         super().__init__([0, 0])

#         self.createWall(0, 0, 20, 600, GREEN)  # left wall
#         self.createWall(780, 0, 20, 250, GREEN)  # right wall
#         self.createWall(780, 350, 20, 250, GREEN)  # right wall 2
#         self.createWall(20, 0, 760, 20, GREEN)  # top wall
#         self.createWall(20, 580, 330, 20, GREEN)  # bottom wall 1
#         self.createWall(450, 580, 330, 20, GREEN)  # bottom wall 2

            # horizontal enemy
#         self.createEnemy(100, 300, 700, 300, 5, RED)
            # vertical enemy
#         self.createEnemy(400, 100, 400, 500, 5, RED)


class MazeRunner():
    def __init__(self):
        os.environ['SDL_AUDODRIVER'] = 'dsp'
        pygame.init()
        self.screen = pygame.display.set_mode([800, 600])
        pygame.display.set_caption("Maze runner")
        self.screen.fill(BLACK)
        pygame.display.flip()

        self.player = Player(50, 50)
        self.movingSprites = pygame.sprite.Group()
        self.movingSprites.add(self.player)

        self.room_limit_x = 10
        self.room_limit_y = 10

        self.maze = Maze(self.room_limit_x, self.room_limit_y)
        self.maze.placeTreasure(YELLOW, self.pickRoom())


        self.startroom = self.pickRoom()
        self.currentRoomRow = self.startroom[0]
        self.currentRoomCol = self.startroom[1]
        self.changeRoom()

        self.heart = pygame.image.load(
            os.path.join("src/heart.png")).convert_alpha()

        self.clock = pygame.time.Clock()

    def pickRoom(self):
        room_x = random.randint(0, self.room_limit_x - 1)
        room_y = random.randint(0, self.room_limit_y - 1)
        
        return [room_x, room_y]

    def changeRoom(self):
        # TODO: bounds check


        self.currentRoom = self.maze.rooms[self.currentRoomRow][self.currentRoomCol]
        self.player.start_x = self.player.rect.x
        self.player.start_y = self.player.rect.y

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.changeSpeed(-5, 0)
                if event.key == pygame.K_RIGHT:
                    self.player.changeSpeed(5, 0)
                if event.key == pygame.K_UP:
                    self.player.changeSpeed(0, -5)
                if event.key == pygame.K_DOWN:
                    self.player.changeSpeed(0, 5)
                # escape closes the game now
                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.changeSpeed(5, 0)
                if event.key == pygame.K_RIGHT:
                    self.player.changeSpeed(-5, 0)
                if event.key == pygame.K_UP:
                    self.player.changeSpeed(0, 5)
                if event.key == pygame.K_DOWN:
                    self.player.changeSpeed(0, -5)

    def movePlayer(self):
        self.player.move(self.currentRoom.wall_list,
                         self.currentRoom.enemy_list)

        if self.player.rect.x > 795:
            self.currentRoomCol += 1
            self.player.rect.x = 0
            self.changeRoom()

        if self.player.rect.x < -10:
            self.currentRoomCol -= 1
            self.player.rect.x = 790
            self.changeRoom()

        if self.player.rect.y > 595:
            self.currentRoomRow += 1
            self.player.rect.y = 0
            self.changeRoom()

        if self.player.rect.y < -10:
            self.currentRoomRow -= 1
            self.player.rect.y = 590
            self.changeRoom()

        block_hit_list = pygame.sprite.spritecollide(
            self.player, self.currentRoom.treasure_list, False)

        if block_hit_list:
            self.win()

    def win(self):
        time.sleep(1)
        self.screen.fill(YELLOW)
        myfont = pygame.font.SysFont('Arial', 120)
        win = myfont.render('You Win!', True, RED)
        fontsize = myfont.size("You Win!")
        self.screen.blit(
            win, (int(400 - fontsize[0] / 2), int(300 - fontsize[1] / 2)))
        pygame.display.flip()

        restart = False

        while not restart:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        restart = True

        self.restart()

    def gameOver(self):
        self.screen.fill(RED)
        myfont = pygame.font.SysFont('Arial', 120)
        gameover = myfont.render('Game Over!', True, BLACK)
        fontsize = myfont.size("Game Over!")
        self.screen.blit(
            gameover, (int(400 - fontsize[0] / 2), int(300 - fontsize[1] / 2)))
        pygame.display.flip()

        restart = False

        while not restart:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        restart = True

        self.restart()

    def restart(self):
        self.player.rect.x = 50
        self.player.start_x = self.player.rect.x
        self.player.rect.y = 50
        self.player.start_y = self.player.rect.y

        self.maze = Maze(self.room_limit_x, self.room_limit_y)
        self.maze.placeTreasure(YELLOW, self.pickRoom())

        self.player.change_x = 0
        self.player.change_y = 0

        self.currentRoomCol = 0
        self.currentRoomRow = 0

        self.player.lives = 3

        self.changeRoom()

    def drawRoom(self):
        self.screen.fill(BLACK)
        self.currentRoom.wall_list.draw(self.screen)
        self.currentRoom.treasure_list.draw(self.screen)
        self.currentRoom.enemy_list.draw(self.screen)
        self.movingSprites.draw(self.screen)

        # live counter
        for x in range(self.player.lives):
            self.screen.blit(self.heart, (20 + 25 * x, 578, 20, 20))

        # location display
        locationString = 'loc: ['+ str(self.currentRoomCol) + ', ' + str(self.currentRoomRow)+ ']'
        myfont = pygame.font.SysFont('Arial', 18, bold=True)
        currentMapLocation = myfont.render(locationString, True, BLUE)
        fontsize = myfont.size(locationString)
        self.screen.blit(currentMapLocation, (int(700 - fontsize[0] / 2), int(600 - fontsize[1]) - 2))
        pygame.display.flip()

        # TODO: depth display

    def main(self):
        while True:

            for enemy in self.currentRoom.enemy_list:
                enemy.move()

            if self.player.lives < 1:
                self.gameOver()

            self.checkEvents()
            self.movePlayer()

            self.drawRoom()
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    mazeRunner = MazeRunner()
    mazeRunner.main()
