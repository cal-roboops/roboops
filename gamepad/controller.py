import pygame
import time
import xbox360

MIN_DETECTION=.1 #to account for misc. numbers in resting state
DELAY=.2 #to avoid sending excessive info

class controller():

	def __init__(self, id) :
		pygame.init()
		pygame.joystick.init()
		self.controller = pygame.joystick.Joystick(id)
		self.controller.init()

		self.button_funcs = [[[],[],[],0] for i in range(self.controller.get_numbuttons())]
		self.axis_funcs = [[[], 0] for i in range(self.controller.get_numaxes())]
		self.hat_funcs = [[[], 0] for i in range(self.controller.get_numhats())]

		self.is_active = True

	def bind_button_up(self, button_id, func) :
		self.button_funcs[button_id][0].append(func)

	def bind_button_down(self, button_id, func) :
		self.button_funcs[button_id][1].append(func)

	def bind_button_hold(self, button_id, func) :
		self.button_funcs[button_id][2].append(func)

	def bind_axis(self, axis_id, func) :
		self.axis_funcs[axis_id][0].append(func)

	def bind_hat(self, hat_id, func) :
		self.hat_funcs[hat_id][0].append(func)

	def update_loop(self) :
		while(self.is_active) :
			for event in pygame.event.get() :        
				if event.type == pygame.JOYBUTTONDOWN :
					for i in range(self.controller.get_numbuttons()) :
						if self.controller.get_button(i) and not self.button_funcs[i][3] :
							self.button_funcs[i][3] = 1
							for f in self.button_funcs[i][1] :
								f()
						elif self.controller.get_button(i):
							for f in self.button_funcs[i][2] :
								f()

				if event.type == pygame.JOYBUTTONUP :
					for i in range(self.controller.get_numbuttons()) :
						if not self.controller.get_button(i) and self.button_funcs[i][3] :
							self.button_funcs[i][3] = 0
							for f in self.button_funcs[i][1] :
								f()

				for i in range(self.controller.get_numaxes()) :
					if self.axis_funcs[i][1] < time.time() and (abs(self.controller.get_axis(i)) > MIN_DETECTION):
						for f in self.axis_funcs[i][0] :
							f(self.controller.get_axis(i))
						self.axis_funcs[i][1] = time.time() + DELAY

				if i in range(self.controller.get_numhats()) :
					if self.hat_funcs[i][1] < time.time() and self.controller.get_hat(i) != (0,0) :
						for f in self.hat_funcs[i][0] :
							f(self.controller.get_hat(i))
						self.hat_funcs[i][1] = time.time() + DELAY

	def shut_off(self) :
		self.is_active = False

class robotController(controller) :

	def __init__(self, id, queue_out):
		controller.__init__(self, id)

		self.drive_sensitivity = 100

		def drive_left(magnitude) :
			queue_out.put("L:" + str(int(-self.drive_sensitivity*magnitude)))

		def drive_right(magnitude) :
			queue_out.put("R:" + str(int(-self.drive_sensitivity*magnitude)))

		self.bind_axis(xbox360.L_ANALOG_Y, drive_left)
		self.bind_axis(xbox360.R_ANALOG_Y, drive_right)

	def set_drive_sensitivity(number) :
		self.drive_sensitivity = number

def main() :
	"""
	Testing code. It works.
	"""
	pygame.init()
	pygame.joystick.init()
	if(pygame.joystick.get_count()) :
		joy = pygame.joystick.Joystick(0)
		joy.init()
		print("Axes: " + str(joy.get_numaxes()))
		print("Balls: " + str(joy.get_numballs()))
		print("Buttons : " + str(joy.get_numbuttons()))
		print("Hats : " + str(joy.get_numhats()))
	t = True
	while(t) :
		for event in pygame.event.get(): # User did something
			if event.type == pygame.QUIT: # If user clicked close
				done=True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
			if event.type == pygame.JOYBUTTONDOWN:
				print("Joystick button pressed.")
				print([joy.get_button(i) for i in range(0, joy.get_numbuttons())])
				if(joy.get_button(2)) :
					t = False
			if event.type == pygame.JOYBUTTONUP:
				print("Joystick button released.")

			if event.type == pygame.JOYAXISMOTION:
				print([joy.get_axis(i) for i in range(0, joy.get_numaxes())])

			if event.type == pygame.JOYHATMOTION:
				print([joy.get_hat(i) for i in range(0, joy.get_numhats())])
	print("exited")
	pygame.quit()

if __name__ == "__main__" :
	main()