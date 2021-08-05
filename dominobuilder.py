import bpy
import math
import mathutils

bl_info = {
    "name": "Dominobuilder",
    "blender": (2, 93, 1),
    "category": "Node",
    }


def getSpreadPoints(amount, curveName):
    
    pospoints = []
    bpy.ops.object.empty_add()
    bpy.ops.object.constraint_add(type = 'FOLLOW_PATH')
    
    curve = bpy.context.scene.objects[curveName]
    
    bpy.context.object.constraints["Follow Path"].target = curve
    bpy.context.object.constraints["Follow Path"].use_curve_follow = True
    
    empty = bpy.context.object
    
    empty.location = mathutils.Vector([0, 0, 0])
    
    empty.constraints["Follow Path"].offset = bpy.context.scene.frame_current

    curve.data.path_duration = amount - 1
    
    for i in range(0, amount):
        empty.constraints["Follow Path"].offset -= 1
        bpy.context.view_layer.update()
        pospoints.append([empty.matrix_world.translation.copy(),
                          empty.matrix_world.copy().to_euler()])
                          
    bpy.data.objects.remove(empty)
    
    return pospoints

def getDominoAmount(dominoSourceName, curveName, spacing, scale):
    length = bpy.data.curves[curveName].splines[0].calc_length()
    dominoLength = bpy.data.objects[dominoSourceName].dimensions[1]
    spaceOnCurvePerDomino = dominoLength * scale * (1 + spacing)
    return math.floor(length / spaceOnCurvePerDomino)
    
    
def setDominos(standard, curveName, size, amount, mass):
	
    points = getSpreadPoints(amount, curveName)
    scale = [size, size, size]
    
    for point in points:
        ob = bpy.data.objects.new("DominoBuilderObject", bpy.data.objects[standard].data)
        
        try:
            bpy.data.collections["Dominoes"].objects.link(ob)
        except KeyError:
            bpy.data.collections.new("Dominoes")
            bpy.context.collection.children.link(bpy.data.collections["Dominoes"])
            bpy.data.collections["Dominoes"].objects.link(ob)

        
        ob.name = "DominoBuilderObject"
        
        try:
            bpy.context.scene.rigidbody_world.collection.objects.link(ob)
        except AttributeError:
            bpy.ops.rigidbody.world_add()
            bpy.data.collections.new("RigidBodyWorld")
            bpy.context.scene.rigidbody_world.collection = bpy.data.collections["RigidBodyWorld"]
            bpy.context.scene.rigidbody_world.collection.objects.link(ob)
        
        ob.rigid_body.mass = mass
        ob.rigid_body.collision_shape = 'BOX'
        bpy.data.objects[ob.name].location = point[0]
        ob.location = point[0]
        ob.rotation_euler = point[1]
        ob.scale = scale
        
def setDominosBySpace(dominoSourceName, curveName, scale, spacing, mass):
    setDominos(dominoSourceName, curveName, scale, 
               getDominoAmount(dominoSourceName, curveName, spacing, scale),
               mass)
        
        
def removeDominos():
    for obj in bpy.context.scene.objects:
        if "DominoBuilderObject" in obj.name:
            bpy.data.objects.remove(obj)
        

def updateDominos(self, context):
    db = context.scene.dominobuilder
    
    removeDominos()
    
    if db.use_absolute:
        setDominos(db.sourceName, db.curveName, db.scale, db.amount, db.mass)
    else:
        setDominosBySpace(db.sourceName, db.curveName, db.scale, db.spacing, db.mass)

from bpy.props import StringProperty, PointerProperty, IntProperty, BoolProperty, FloatProperty, CollectionProperty, EnumProperty

from bpy.types import PropertyGroup, Operator

class DominoProperties(bpy.types.PropertyGroup):
    amount: IntProperty(
        name="Amount of dominos",
        update = updateDominos
        )
    spacing: FloatProperty(
        name = "Spacing",
        update = updateDominos,
        default = 1.0
        )
    use_absolute: BoolProperty(
        name = "Set exact amount",
        default = False,
        update = updateDominos
        )
    scale: FloatProperty(
        name = "Scale of each domino",
        default = 1.0,
        update = updateDominos
        )
    curveName: StringProperty(
        name = "Curve",
        update = updateDominos
        )
    sourceName: StringProperty(
        name = "Dominobrick",
        update = updateDominos
        )
    mass: FloatProperty(
        name = "Mass of each domino",
        default = 1.0,
        update = updateDominos
        )

# Panel class, creates the sidebar panel in the viewport
class DominoPanel(bpy.types.Panel):
    bl_idname = "DOMINO_PT_PANEL"
    bl_label = "Domino"
    bl_category = "Domino"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        
        layout = self.layout
        dominobuilder = context.scene.dominobuilder

        layout.prop(dominobuilder, "use_absolute")
        if dominobuilder.use_absolute:
            layout.prop(dominobuilder, "amount")
        else:
            layout.prop(dominobuilder, "spacing")
        
        layout.prop(dominobuilder, "scale")
        layout.prop(dominobuilder, "mass")

        layout.prop_search(dominobuilder, "sourceName", context.scene, "objects", icon="MESH_CUBE")
        layout.prop_search(dominobuilder, "curveName", bpy.data, "curves", icon="CURVE_PATH")
        
        layout.operator("dominobuilder.updatedominoes")
        
class UpdateDominoes(bpy.types.Operator):
    bl_idname = "dominobuilder.updatedominoes"
    bl_label = "Update dominoes"
    bl_description = "Update the dominoes"
    
    def execute(self, context):
        updateDominos(self, context)
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(UpdateDominoes)
    bpy.utils.register_class(DominoProperties)
    bpy.utils.register_class(DominoPanel)

    bpy.types.Scene.dominobuilder = PointerProperty(type=DominoProperties)


def unregister():
    bpy.utils.unregister_class(UpdateDominoes)
    bpy.utils.unregister_class(DominoProperties)
    bpy.utils.unregister_class(DominoPanel)


if __name__ == "__main__":
    register()
