extends TextureRect

var dragging := false
var last_position := Vector2.ZERO

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func clamp_position():
	var viewport_size = get_viewport_rect().size
	var tex_size = texture.get_size() * scale

	position.x = clamp(position.x, viewport_size.x - tex_size.x, 0)
	position.y = clamp(position.y, viewport_size.y - tex_size.y, 0)
	
func _on_gui_input(event: InputEvent) -> void:
	# начало касания / нажатия мыши
	if event is InputEventScreenTouch or event is InputEventMouseButton:
		if event.pressed:
			dragging = true
			last_position = event.position
		else:
			dragging = false

	# движение пальца / мыши
	if event is InputEventScreenDrag or event is InputEventMouseMotion:
		if dragging:
			var delta = event.position - last_position
			position += delta
			last_position = event.position
#			clamp_position()
