# Map.gd - с загрузкой текстур из ресурсов
extends TextureRect

@export var normal_texture: Texture2D  # Круглая кнопка в обычном состоянии
@export var pressed_texture: Texture2D  # Круглая кнопка в нажатом состоянии
@export var disabled_texture: Texture2D

@export var button_radius: int = 40
@export var button_count: int = 10  # Можно менять в редакторе

@export var min_distance: float = 80  # Минимальное расстояние между кнопками

var dragging = false
var drag_offset = Vector2()
var min_position = Vector2(0, 0)
var max_position = Vector2(500, 500)  # Границы перемещения

# Загружаем класс через preload
const ButtonData = preload("res://ButtonData.gd")

var buttons_data: Array[ButtonData] = [] # Массив для хранения данных всех кнопок

func _ready():
	# Делаем узел кликабельным
	mouse_filter = MOUSE_FILTER_STOP
	
	#scale = Vector2(2, 2)
	size = size * Vector2(10, 10)
	print("TextureRect увеличен в 10 раз! Размер: ", size * scale)

	var screen_size   = get_viewport().get_visible_rect().size
	var screen_center = ( screen_size - size * scale ) * 0.5
	print("Размер экрана: ", screen_center)
	
	var border = screen_size / 3
	
	min_position = - size * scale + border
	max_position = screen_size - border
	
	print("borders", min_position, max_position)

	create_buttons(button_count)

	
func _on_gui_input(event: InputEvent) -> void:
	if event is InputEventScreenTouch or event is InputEventMouseButton:
		if event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
			dragging = true
			drag_offset = get_global_mouse_position() - global_position
		else:
			dragging = false
	
	if event is InputEventScreenDrag or event is InputEventMouseMotion:
		if dragging:
			var new_pos = get_global_mouse_position() - drag_offset
			# Ограничиваем перемещение
			#min_position.x = -size.x
			new_pos.x = clamp(new_pos.x, min_position.x, max_position.x)
			new_pos.y = clamp(new_pos.y, min_position.y, max_position.y)
			global_position = new_pos


func create_buttons(count: int):
	# Очищаем старые кнопки
	for data in buttons_data:
		if data.button:
			data.button.queue_free()
	buttons_data.clear()
	
	var map_size = size
	var btn_size = Vector2(button_radius * 2, button_radius * 2)
	var positions = []  # Для проверки пересечений
	
	for i in range(count):
		# Создаём кнопку
		var button = TextureButton.new()
		button.size = btn_size
		button.custom_minimum_size = btn_size
		
		# Генерируем уникальную позицию
		var pos = generate_unique_position(map_size, btn_size, positions)
		button.position = pos
		positions.append(pos + btn_size / 2)  # Сохраняем центр для проверки расстояния
		
		# Добавляем на сцену
		add_child(button)
		
		# Создаём данные для кнопки
		var data = ButtonData.new(
			button,
			i,
			normal_texture,
			pressed_texture,
			disabled_texture
		)
		
		# Подключаем сигнал нажатия
		button.button_down.connect(_on_button_pressed.bind(i))
		
		# Подключаем сигнал изменения состояния
		data.state_changed.connect(_on_button_state_changed)
		
		# Сохраняем в массив
		buttons_data.append(data)
		
		print("✅ Создана кнопка ", i, " на позиции ", pos)


# Вспомогательная функция для генерации позиции
func generate_unique_position(map_size: Vector2, btn_size: Vector2, existing_positions: Array) -> Vector2:
	var max_attempts = 100
	var half_size = btn_size / 2
	
	for attempt in range(max_attempts):
		var x = randf_range(0, map_size.x - btn_size.x)
		var y = randf_range(0, map_size.y - btn_size.y)
		var pos = Vector2(x, y)
		var center = pos + half_size
		
		# Проверяем расстояние до других кнопок
		var too_close = false
		for existing_center in existing_positions:
			if center.distance_to(existing_center) < min_distance:
				too_close = true
				break
		
		if not too_close:
			return pos
	
	# Если не нашли место - возвращаем случайное
	return Vector2(
		randf_range(0, map_size.x - btn_size.x),
		randf_range(0, map_size.y - btn_size.y)
	)

func _on_button_pressed(index: int):
	# Проверяем, что индекс существует
	if index < 0 or index >= buttons_data.size():
		print("❌ Ошибка: индекс ", index, " вне диапазона!")
		return
	
	var data = buttons_data[index]
	
	# Если кнопка отключена - игнорируем
	if not data.is_enabled:
		print("⚠️ Кнопка ", index, " отключена, нажатие игнорируется")
		return
	
	# Переключаем состояние
	data.toggle()
	
	# Можно добавить анимацию
	animate_button(data.button)

# Обработчик изменения состояния (опционально)
func _on_button_state_changed(index: int, is_toggled: bool):
	print("📢 Кнопка ", index, " изменила состояние на: ", is_toggled)
	
	# Здесь можно выполнить дополнительные действия
	# Например, сохранить состояние в БД
	save_button_state(index, is_toggled)

# Анимация при нажатии
func animate_button(button: TextureButton):
	var tween = create_tween()
	tween.tween_property(button, "scale", Vector2(0.85, 0.85), 0.1)
	tween.tween_property(button, "scale", Vector2(1, 1), 0.1)

# Сохранение состояния (пример)
func save_button_state(index: int, is_toggled: bool):
	var data = {
		"index": index,
		"toggled": is_toggled,
		"timestamp": Time.get_unix_time_from_system()
	}
	print("💾 Сохранено состояние: ", data)
