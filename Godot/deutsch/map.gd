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

# Переменные для масштабирования
var min_scale: float = 0.1
var max_scale: float = 5.0
var zoom_speed: float = 0.1

# Для мультитача (два пальца)
var touch_points = {}  # Словарь для хранения точек касания
var initial_distance: float = 0.0
var initial_scale: float = 1.0

# Загружаем класс через preload
const ButtonData = preload("res://ButtonData.gd")

var buttons_data: Array[ButtonData] = [] # Массив для хранения данных всех кнопок

func _ready():
	# Делаем узел кликабельным
	mouse_filter = MOUSE_FILTER_STOP
	
	#scale = Vector2(2, 2)
#	size = size * Vector2(10, 10)
	print("TextureRect увеличен в 10 раз! Размер: ", size * scale)

	var screen_size   = get_viewport().get_visible_rect().size
	var screen_center = ( screen_size - size * scale ) * 0.5
	print("Размер экрана: ", screen_center)
	
	var border = screen_size / 3
	
	min_position = - size * scale + border
	max_position = screen_size - border
	
	print("borders", min_position, max_position)

	create_buttons(button_count)

	scale = Vector2(1, 1)

	
func _on_gui_input(event: InputEvent) -> void:
	#if event is InputEventScreenTouch or event is InputEventMouseButton:
		#if event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
			#dragging = true
			#drag_offset = get_global_mouse_position() - global_position
		#else:
			#dragging = false
	
	if event is InputEventMouseButton:
		# Левая кнопка - перетаскивание
		if event.button_index == MOUSE_BUTTON_LEFT:
			if event.pressed:
				dragging = true
				drag_offset = get_global_mouse_position() - global_position
			else:
				dragging = false
		
		# Колесико мыши - масштабирование
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			if event.pressed:
				zoom_in(get_global_mouse_position())
		
		if event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			if event.pressed:
				zoom_out(get_global_mouse_position())
	#
	if event is InputEventScreenDrag or event is InputEventMouseMotion:
		if dragging:
			var new_pos = get_global_mouse_position() - drag_offset
			# Ограничиваем перемещение
			new_pos.x = clamp(new_pos.x, min_position.x, max_position.x)
			new_pos.y = clamp(new_pos.y, min_position.y, max_position.y)
			global_position = new_pos
			#
			#
	# === ОБРАБОТКА МУЛЬТИТАЧ (ДВА ПАЛЬЦА) ===
	if event is InputEventScreenTouch:
		var touch_event = event as InputEventScreenTouch
		var index = touch_event.index
		
		if touch_event.pressed:
			# Палец коснулся экрана
			touch_points[index] = touch_event.position
			
			# Если два пальца на экране
			if touch_points.size() == 2:
				initial_distance = get_touch_distance()
				initial_scale = scale.x
				print("Два пальца! Дистанция: ", initial_distance)
		
		else:
			# Палец оторвался от экрана
			touch_points.erase(index)
			
			# Если остался один палец - переключаемся в режим перетаскивания
			if touch_points.size() == 1:
				# Начинаем перетаскивание одним пальцем
				var pos = touch_points.values()[0]
				dragging = true
				drag_offset = pos - global_position

# === ФУНКЦИИ ДЛЯ МУЛЬТИТАЧА ===

func get_touch_distance() -> float:
	if touch_points.size() < 2:
		return 0.0
	
	var positions = touch_points.values()
	return positions[0].distance_to(positions[1])

func get_touch_center() -> Vector2:
	if touch_points.size() < 2:
		return Vector2.ZERO
	
	var positions = touch_points.values()
	return (positions[0] + positions[1]) / 2

# === ФУНКЦИИ МАСШТАБИРОВАНИЯ ===

func zoom_in(center: Vector2 = Vector2.ZERO):
	var new_scale = scale.x + zoom_speed
	new_scale = clamp(new_scale, min_scale, max_scale)
	zoom_around_point(center, new_scale)

func zoom_out(center: Vector2 = Vector2.ZERO):
	var new_scale = scale.x - zoom_speed
	new_scale = clamp(new_scale, min_scale, max_scale)
	zoom_around_point(center, new_scale)

func zoom_around_point(point: Vector2, new_scale: float):
	if point == Vector2.ZERO:
		# Если точка не задана - масштабируем относительно центра объекта
		point = global_position + size * 0.5 * scale
	
	# Сохраняем мировые координаты точки
	var world_point = point
	var old_scale = scale.x
	
	# Применяем новый масштаб
	scale = Vector2(new_scale, new_scale)
	
	# Корректируем позицию, чтобы точка осталась на месте
	var scale_factor = new_scale / old_scale
	global_position = world_point - (world_point - global_position) * scale_factor / old_scale * old_scale
	
	# Ограничиваем позицию
	clamp_position(global_position)

func clamp_position(pos: Vector2) -> Vector2:
	var new_pos = pos
	new_pos.x = clamp(new_pos.x, min_position.x, max_position.x)
	new_pos.y = clamp(new_pos.y, min_position.y, max_position.y)
	return new_pos



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
