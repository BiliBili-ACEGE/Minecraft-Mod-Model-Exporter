bl_info = {
    "name": "Model Export to Minecraft Mod",
    "blender": (2, 80, 0),
    "category": "Import-Export",
    "author": "ACEGE_",
    "version": (1, 1),
    "location": "File > Export > Minecraft Item JSON (.json)",
    "description": "Export selected model objects to Minecraft Mod Item JSON format",
    "warning": "",
    "wiki_url": "",
    "tracker_url": ""
}

if "bpy" in locals():
    import importlib
    if "model_to_minecraft_mod" in locals():
        importlib.reload(model_to_minecraft_mod)

import bpy

from . import model_to_minecraft_mod

def register():
    model_to_minecraft_mod.register()

def unregister():
    model_to_minecraft_mod.unregister()

if __name__ == "__main__":
    register()
