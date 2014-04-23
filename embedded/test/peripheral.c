#include <qk_program.h>
#include <qk_peripheral.h>

void qk_setup()
{
	qk_peripheral_setup();

	qk_gpio_set_mode(QK_GPIO_PORT_A, 0, QK_GPIO_MODE_OUTPUT);
}

int main()
{
	return qk_main();
}
