bl_info = {
    "name": "Distribute",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Edit Tab > Distribute",
    "description": "An addon to distribute objects evenly on the X, Y, and Z axes",
    "category": "Object"
}

import bpy

class DistributeSelectedOperator(bpy.types.Operator):
    """Operator to distribute selected objects evenly"""
    bl_idname = "object.distribute_selected"
    bl_label = "Distribute Selected"
    
    axis: bpy.props.StringProperty()
    
    def execute(self, context):
        # Get the selected objects and sort them by their position on the specified axis
        selected_objects = bpy.context.selected_objects
        selected_objects.sort(key=lambda obj: obj.location[int(self.axis)])
        
        # Get the first and last selected objects
        first_object = selected_objects[0]
        last_object = selected_objects[-1]
        
        # Calculate the total distance between the first and last objects
        total_distance = last_object.location[int(self.axis)] - first_object.location[int(self.axis)]
        
        # Calculate the spacing between each object
        spacing = total_distance / (len(selected_objects) - 1)
        
        # Loop through the selected objects and set their position on the specified axis
        for i, obj in enumerate(selected_objects):
            pos = list(obj.location)
            pos[int(self.axis)] = first_object.location[int(self.axis)] + (i * spacing)
            obj.location = tuple(pos)
        
        return {'FINISHED'}

class VIEW3D_PT_distribute_panel(bpy.types.Panel):
    """Panel to house the distribute buttons"""
    bl_idname = "VIEW3D_PT_distribute_panel"
    bl_label = "Distribute"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Edit"
    
    def draw(self, context):
        layout = self.layout
        
        # Add the Dist X button
        layout.operator("object.distribute_selected", text="Dist X").axis = "0"
        
        # Add the Dist Y button
        layout.operator("object.distribute_selected", text="Dist Y").axis = "1"
        
        # Add the Dist Z button
        layout.operator("object.distribute_selected", text="Dist Z").axis = "2"

def register():
    bpy.utils.register_class(DistributeSelectedOperator)
    bpy.utils.register_class(VIEW3D_PT_distribute_panel)

def unregister():
    bpy.utils.unregister_class(DistributeSelectedOperator)
    bpy.utils.unregister_class(VIEW3D_PT_distribute_panel)

if __name__ == "__main__":
    register()
