class_name ButtonData
extends RefCounted

# Состояния
var toggled: bool = false
var enabled: bool = true
var index: int = -1

# Ссылка на кнопку
var button: TextureButton

# Текстуры для разных состояний
var normal_texture: Texture2D
var pressed_texture: Texture2D
var disabled_texture: Texture2D

# Сигнал для оповещения об изменении состояния
signal state_changed(index: int, toggled: bool)

func _init(btn: TextureButton, idx: int, normal: Texture2D, pressed: Texture2D, disabled: Texture2D = null):
	button = btn
	index = idx
	normal_texture = normal
	pressed_texture = pressed
	disabled_texture = disabled if disabled != null else normal_texture  # Запасной вариант
	
	# Применяем текстуры
	update_visual()

# Переключить состояние (нажата/не нажата)
func toggle():
	if not enabled:
		print("Кнопка ", index, " отключена, нельзя переключить!")
		return
	
	toggled = !toggled
	update_visual()
	state_changed.emit(index, toggled)
	print("Кнопка ", index, " переключена: ", toggled)

# Включить/отключить кнопку
func set_enabled(value: bool):
	if enabled == value:
		return
	
	enabled = value
	button.disabled = !value
	
	# Если отключаем - сбрасываем состояние нажатия
	if not value:
		toggled = false
	
	update_visual()
	print("Кнопка ", index, " доступность: ", enabled)

# Получить состояние нажатости
func is_toggled() -> bool:
	return toggled

# Получить состояние доступности
func is_enabled() -> bool:
	return enabled

# Обновить визуальное состояние
func update_visual():
	if not enabled:
		# Отключена - серая
		button.texture_normal = disabled_texture
		button.texture_pressed = disabled_texture
	elif toggled:
		# Нажата
		button.texture_normal = pressed_texture
		button.texture_pressed = pressed_texture
	else:
		# Обычное состояние
		button.texture_normal = normal_texture
		button.texture_pressed = pressed_texture
