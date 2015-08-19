from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.task.Task import Task
from panda3d.core import *
import sys
import yaml



# Globals #
Colors = {'black':(0,0,0,1),
                'white': (1,1,1,1),
                'gray':(0.6,0.6,0.6,1),
                'red':(1,0,0,1),
                'green':(0,1,0,1),
                'blue':(0,0,1,1),
                'orange':(1,0.5,0,1),
                'pink':(1,0.5,0.5,1),
                'yellow':(1,1,0,1)
                }

Collisions = {'small': (-14,0,0,14,0,0,1.5),
                'medium': (-14,0,0,14,0,0,1.5),
                'large': (-14,0,0,14,0,0,1.5)
                }


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        
        self.models = {}
        
        
        dnafile = '/home/nathan/Documents/Git/Adventure/resources/dna/room_yellow_castle.yaml'
        
        self.createRoom(dnafile)


        # localPlayer globals
        self.localColor = Colors['black']
        
        base.cam.setPos(0,0,100)
        base.cam.setHpr(0,-90,0)



    def transition(self, newroom, exittunnel, coll):
        pass

        self.createRoom(dnafile)

        # Get position of exittunnel the player is leaving
        
        tunnelpos = self.models[exittunnel].getY()
        if tunnelpos > self.player.getY():
            self.player.setY(self.models[exittunnel].getY() - 5)
        else:
            self.player.setY(self.models[exittunnel].getY() + 5)



    ### Builds the room the player is currently in ###
    def createRoom(self, dnafile):
        
        ### First things first we open the dna file ###
        with open(dnafile, 'r') as f:
            dna = yaml.load(f)

        ### Iterate over objects in the dna file.    ###
        ### Remember we're doing this in a FOR LOOP! ###
        for nodes in dna:
            
            # Setup default properties
            type = None
            name = ''
            model = ''
            pos = (0,0,0)
            hpr = (0,0,0)
            scale = (1)
            color = (1)
            collisionsize = 'small'
            exittunnel = None
            newroom = None
            
            
            ### REQUIRED PROPERTIES ###
            type = dna[nodes]['type']
            
            name = dna[nodes]['name']
            
            
            ### OPTIONAL PROPERTIES ###
            if 'model' in dna[nodes]:
                model = dna[nodes]['model']
                
            if 'pos' in dna[nodes]:
                pos_list = dna[nodes]['pos']
                pos = tuple(pos_list)
                
            if 'hpr' in dna[nodes]:
                hpr_list = dna[nodes]['hpr']
                hpr = tuple(hpr_list)
                
            if 'scale' in dna[nodes]:
                scale_list = dna[nodes]['scale']
                scale = tuple(scale_list)
                
            if 'color' in dna[nodes]:
                color_str = dna[nodes]['color']
                color = Colors[color_str]
            
            if 'exittunnel' in dna[nodes]:
                exittunnel = dna[nodes]['exittunnel']
                
            if 'newroom' in dna[nodes]:
                newroom = dna[nodes]['newroom']


            # Call the first method into the process of 
            # adding the object into the game
            self.prepareNode(type, name, model, pos, hpr, scale, color, exittunnel, newroom)



    def prepareNode(self, type, name, model, pos, hpr, scale, color, exittunnel, newroom):
        print 'Preparing node'
        print (type, name, model, pos, hpr, scale, color, exittunnel, newroom)

        ### This is so we call the corrosponding methods based ###
        ### on what kind of object we are going to load        ###

        # If the object is a tunnel...
        if type == 'tunnel':
            self.createDoor(type, name, pos, hpr, exittunnel, newroom)
            
        # If the type of the object is not a tunnel...
        else:
            self.createGenericObject(type, name, model, pos, hpr, scale, color)



    ### Creates the object with the neccisary properties and appends ###
    ### the object into a dictionary so we can easily modify it      ###
    def createGenericObject(self, type, name, model, pos, hpr, scale, color):
        self.models[name] = loader.loadModel(model)
        self.models[name].reparentTo(render)
        self.models[name].setPos(pos)
        self.models[name].setHpr(hpr)
        self.models[name].setScale(scale)
        self.models[name].setColor(color)



    def createDoor(self, type, name, pos, hpr, exittunnel, newroom):
        self.models[name] = render.attachNewNode(name)
        self.models[name].reparentTo(render)
        self.models[name].setPos(pos)
        self.models[name].setHpr(hpr)
        
        # Set the collision geometry; we need first a CollisionNode
        sensor = self.models[name].attachNewNode(CollisionNode(name))
        # We add that to our CollisionSphere geometry primitive
        sensor.node().addSolid(CollisionTube(-14,0,0,14,0,0,1.5))
        sensor.node().setFromCollideMask(BitMask32.allOff())
        sensor.node().setIntoCollideMask(1)
        sensor.show()
        
        # Collision logic
        self.accept('playersensor-into-' + name, self.transition, [newroom, exittunnel])


    
        def createPlayerItem(self, type, name, model, pos, hpr, scale, color):
            pass
            #self.createGenericObject()



    ### Destroys all nodes in the current room the player is in ###
    def destroyRoom(self):
        for nodes in self.models:
            self.models[nodes].removeNode()



app = MyApp()
app.run()