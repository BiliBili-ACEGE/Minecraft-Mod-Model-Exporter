import bpy
import os
import json

class ExportOBJToJsonOperator(bpy.types.Operator):
    bl_idname = "export_scene.model_to_minecraft_mod"
    bl_label = "Export Model to Minecraft Mod"
    bl_description = "Export selected model objects to Minecraft Mod Item JSON format"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype='FILE_PATH', default="")
    mod_namespace: bpy.props.StringProperty(name="Mod Namespace", default="")

    def execute(self, context):
        # 检查文件路径是否存在
        if not self.filepath:
            self.report({'ERROR'}, "未设置文件路径")
            return {'CANCELLED'}

        # 检查是否设置了模组的命名空间
        if not self.mod_namespace:
            self.report({'ERROR'}, "未设置模组的命名空间")
            return {'CANCELLED'}

        # 获取当前文件的纹理路径
        texture_path = bpy.path.abspath(bpy.data.filepath)
        texture_folder = os.path.dirname(texture_path)

        # 获取选中的物体
        selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

        # 生成 Minecraft Item JSON 数据
        minecraft_item_json = {
            "credit": "Made with Blender",
            "texture_size": [32, 32],
            "textures": {},
            "elements": [],
            "display": {}
        }

        # 遍历每个选中的物体
        for i, obj in enumerate(selected_objects):
            # 定义物品 ID
            item_id = f"{self.mod_namespace}:{obj.name.lower()}"

            # 获取当前物体使用的纹理文件名（不包含后缀）
            texture_name = ""
            for slot in obj.material_slots:
                if slot.material and slot.material.use_nodes:
                    for node in slot.material.node_tree.nodes:
                        if node.type == 'TEX_IMAGE':
                            texture_name = os.path.splitext(os.path.basename(node.image.filepath))[0]
                            break
                    if texture_name:
                        break

            # 设置物品纹理
            minecraft_item_json["textures"][f"{i}"] = f"{self.mod_namespace}:item/{texture_name}"

            # 定义元素信息
            element_data = {
                "name": obj.name,
                "from": [0, 0, 0],
                "to": [16, 16, 16],  # 这里根据实际情况设置大小
                "faces": {
                    "north": {"uv": [0, 0, 16, 16], "texture": f"#{i}"},
                    "east": {"uv": [0, 0, 16, 16], "texture": f"#{i}"},
                    "south": {"uv": [0, 0, 16, 16], "texture": f"#{i}"},
                    "west": {"uv": [0, 0, 16, 16], "texture": f"#{i}"},
                    "up": {"uv": [0, 0, 16, 16], "texture": f"#{i}"},
                    "down": {"uv": [0, 0, 16, 16], "texture": f"#{i}"}
                }
            }

            # 将元素信息添加到 JSON 数据中
            minecraft_item_json["elements"].append(element_data)

        # 写入 JSON 文件
        with open(self.filepath, 'w') as f:
            json.dump(minecraft_item_json, f, indent=4)

        return {'FINISHED'}

    def invoke(self, context, event):
        # 打开文件浏览器选择保存路径
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "mod_namespace")

def menu_func_export(self, context):
    self.layout.operator(ExportOBJToJsonOperator.bl_idname, text="Minecraft Item JSON (.json)")

def register():
    bpy.utils.register_class(ExportOBJToJsonOperator)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_class(ExportOBJToJsonOperator)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
