import pygame, os, time, random, bisect

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

class WeightedList(object):
    def __init__(self, choises) -> None:
        super().__init__()
        self.values, self.weights = zip(*choises)
        self.total = 0
        self.cumulativeWeights = []
        for x in self.weights:
            self.total += x
            self.cumulativeWeights.append(self.total)
    
    def draw(self):
        pick = random.random() * self.total
        index = bisect.bisect(self.cumulativeWeights, pick)
        return self.values[index]


class Room(object):
    def __init__(self, row, col) -> None:
        self.wall_list = pygame.sprite.Group()
        self.treasure_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.pathed = False
        self.save = False
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

        self.carvePaths(0, 0)
        self.buildMaze(GREEN)

    def populate(self, mult):
        enemyCount = WeightedList([[0, 100], [1, 60 + 10 * mult], [2, 20 * mult], [3, 10 * mult],[4, 7 * mult]])        
        
        for row in range(len(self.rooms)):
            for room in range(len(self.rooms[row])):
                    currentRoom = self.rooms[row][room]
                    if currentRoom.save == False:
                        count = enemyCount.draw()
                        if count:
                            for enemy in range(count):
                                # decide direction of the enemy
                                direction = random.randint(1, 4)

                                # horizontal
                                # 80% width, same height
                                if direction == 1: # start left
                                    height = random.randint(60, 540)
                                    currentRoom.createEnemy(80, height, 720, height, 5, RED)
                                if direction == 2: # start right
                                    height = random.randint(60,540)
                                    currentRoom.createEnemy(720, height, 80, height, 5, RED)
                                # vertical
                                # 80% height, same width
                                if direction == 3: #start top
                                    width = random.randint(80, 720)
                                    currentRoom.createEnemy(width, 60, width, 540, 5, RED)
                                if direction == 4: # start bottom
                                    width = random.randint(80, 720)
                                    currentRoom.createEnemy(width, 540, width, 60, 5, RED)
        
    def buildMaze(self, color):
        for row in self.rooms:
            for room in row:
                room.build(color)

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
        treasureRow = loc.y
        treasureCol = loc.x
        # print('treasure at: x ' + str(treasureCol) + " y " + str(treasureRow))

        self.rooms[treasureRow][treasureCol].createTreasure(375, 275, 50, 50, color)

class MazeRunner():
    def __init__(self):
        os.environ['SDL_AUDODRIVER'] = 'dsp'
        pygame.init()
        self.screen = pygame.display.set_mode([800, 600])
        pygame.display.set_caption("Maze runner")
        self.screen.fill(BLACK)
        pygame.display.flip()

        self.transtionFont = pygame.font.SysFont('Arial', 120)
        self.UIFont = pygame.font.SysFont('Arial', 18, bold=True)

        self.player = Player(50, 50)
        self.movingSprites = pygame.sprite.Group()
        self.movingSprites.add(self.player)

        self.depth = 1

        self.room_limit_x = 5 
        self.room_limit_y = 5 
      
        self.maze = Maze(self.room_limit_x, self.room_limit_y)

        self.startroom = self.pickSaveRoom()        
        self.maze.placeTreasure(YELLOW, self.pickSaveRoom(True))

        self.maze.populate(5)

        self.currentRoomRow = self.startroom.y
        self.currentRoomCol = self.startroom.x
        self.changeRoom()

        self.heart = pygame.image.load(
            os.path.join("src/heart.png")).convert_alpha()

        self.clock = pygame.time.Clock()

    def pickSaveRoom(self, checkspawn=False):
        room = self.pickRoom(checkspawn)

        self.maze.rooms[room.y][room.x].save = True

        return room

    def pickRoom(self, checkspawn=False):
        room_x = random.randint(0, self.room_limit_x - 1)
        room_y = random.randint(0, self.room_limit_y - 1)
        
        if checkspawn:
            if  room_x == self.startroom.x and room_y == self.startroom.y :
                retry = self.pickRoom(True)
                room_x = retry.x
                room_y = retry.y

        return Vector2(room_y, room_x)

    def changeRoom(self):
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
            if self.depth < 5:
                self.dive()
            else:
                self.win()

    def dive(self):
        time.sleep(1)
        self.screen.fill(BLACK)

        mainString = self. transtionFont.render('You Dive Deeper', True, WHITE)
        fontsize = self.transtionFont.size('You Dive Deeper')
        subscriptString = "Press Space or Enter to Continue !!"
        subscript = self.UIFont.render(subscriptString , True, WHITE)
        subscriptSize = self.UIFont.size(subscriptString)

        self.screen.blit(
            mainString, (int(400 - fontsize[0] / 2), int(300 - fontsize[1] / 2)))
        self.screen.blit(
            subscript, (int(400 - subscriptSize[0]/ 2), int(400 - subscriptSize[1]/ 2))
        )
        pygame.display.flip()

        restart = False

        while not restart:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        restart = True

        self.restart(True)

    def win(self):
        time.sleep(1)
        self.screen.fill(YELLOW)
        
        win = self.transtionFont.render('You Win!', True, RED)
        fontsize = self.transtionFont.size("You Win!")
        subscriptString = "Press Space or Enter to restart !!"
        subscript = self.UIFont.render(subscriptString , True, RED)
        subscriptSize = self.UIFont.size(subscriptString)


        self.screen.blit(
            win, (int(400 - fontsize[0] / 2), int(300 - fontsize[1] / 2)))
        self.screen.blit(
            subscript, (int(400 - subscriptSize[0]/ 2), int(400 - subscriptSize[1]/ 2))
        )
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
        gameover = self.transtionFont.render('Game Over!', True, BLACK)
        fontsize = self.transtionFont.size("Game Over!")
        self.screen.blit(
            gameover, (int(400 - fontsize[0] / 2), int(300 - fontsize[1] / 2)))
        subscriptString = "Press Space or Enter to restart !!"
        subscript = self.UIFont.render(subscriptString , True, BLACK)
        subscriptSize = self.UIFont.size(subscriptString)
        self.screen.blit(
            subscript, (int(400 - subscriptSize[0]/ 2), int(400 - subscriptSize[1]/ 2))
        )

        pygame.display.flip()

        restart = False

        while not restart:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        restart = True

        self.restart()

    def restart(self, dive=False):
        self.player.rect.x = 50
        self.player.start_x = self.player.rect.x
        self.player.rect.y = 50
        self.player.start_y = self.player.rect.y

        if dive == False:
            self.depth = 1
            self.player.lives = 3
        else:
            self.depth += 1

        self.room_limit_x = 4 + self.depth
        self.room_limit_y = 4 + self.depth

        self.maze = Maze(self.room_limit_x, self.room_limit_y)

        self.startroom = self.pickSaveRoom()
        self.maze.placeTreasure(YELLOW, self.pickSaveRoom(True))

        self.maze.populate(5 * self.depth)

        self.player.change_x = 0
        self.player.change_y = 0

        self.currentRoomCol = self.startroom.y
        self.currentRoomRow = self.startroom.x

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
        
        currentMapLocation = self.UIFont.render(locationString, True, BLUE)
        locFontsize = self.UIFont.size(locationString)
        self.screen.blit(currentMapLocation, (int(700 - locFontsize[0] / 2), int(600 - locFontsize[1]) - 2))
        

        # depth display
        depthString = 'Depth:  ' +  str(self.depth)

        depthUIelement = self.UIFont.render(depthString, True, BLUE)
        depthfontsize = self.UIFont.size(depthString)
        self.screen.blit(depthUIelement, (int(0 + depthfontsize[0] / 2), 0))
        pygame.display.flip()


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
