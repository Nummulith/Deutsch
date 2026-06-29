extends Node2D

@onready var game_world = $Scenes/GameWorld

func _ready():
	# Загружаем первую сцену по умолчанию
	load_scene("res://map.tscn")

func load_scene(path: String):
	# Очищаем GameWorld
	for child in game_world.get_children():
		child.queue_free()
	
	# Ждём один кадр для удаления
	await get_tree().process_frame
	
	# Загружаем новую сцену
	var new_scene = load(path).instantiate()
	game_world.add_child(new_scene)
