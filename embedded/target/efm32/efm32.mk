###############################################################################
# qkthings
###############################################################################

# Requires:
# DEVICE
# BOARD
# TOOLCHAIN_DIR

###############################################################################
# MESSAGES
###############################################################################
ifneq ($(PRINT_MESSAGES),)
ifeq ($(HAS_BOOT),1)
    ${info Bootloader enabled}
else
    ${info Bootloader disabled}
endif
endif
###############################################################################
# DEFINITIONS
###############################################################################

###############################################################################
# PATHS
###############################################################################

ENERGYMICRO = $(TOOLCHAIN_DIR)/common/energymicro
#WINDOWSCS  ?= GNU Tools ARM Embedded\4.7 2013q1
#LINUXCS    ?= /home/mribeiro/gcc-arm-none-eabi-4_7-2013q1

TOOLDIR := $(TOOLCHAIN_DIR)/linux/arm/gcc

CC      = $(QUOTE)$(TOOLDIR)/bin/arm-none-eabi-gcc$(QUOTE)
LD      = $(QUOTE)$(TOOLDIR)/bin/arm-none-eabi-ld$(QUOTE)
AR      = $(QUOTE)$(TOOLDIR)/bin/arm-none-eabi-ar$(QUOTE)
OBJCOPY = $(QUOTE)$(TOOLDIR)/bin/arm-none-eabi-objcopy$(QUOTE)
DUMP    = $(QUOTE)$(TOOLDIR)/bin/arm-none-eabi-objdump$(QUOTE)
PSIZE	= $(QUOTE)$(TOOLDIR)/bin/arm-none-eabi-size$(QUOTE)

INCLUDE_DIR += \
$(ENERGYMICRO)/CMSIS/Include \
$(ENERGYMICRO)/Device/EnergyMicro/EFM32G/Include \
$(ENERGYMICRO)/emlib/inc

###############################################################################
# FLAGS
###############################################################################

# -MMD : Don't generate dependencies on system header files.
# -MP  : Add phony targets, useful when a h-file is removed from a project.
# -MF  : Specify a file to write the dependencies to.
#DEPFLAGS = -MMD -MP -MF $(@:.o=.d)

# Add -Wa,-ahld=$(LST_DIR)/$(@F:.o=.lst) to CFLAGS to produce assembly list files
# -DDEBUG_EFM -DNDEBUG

CFLAGS += -mcpu=cortex-m3 -mthumb -mfix-cortex-m3-ldrd \
-ffunction-sections -fdata-sections -fomit-frame-pointer \
$(DEPFLAGS) -D$(DEVICE) -D$(BOARD)

ASMFLAGS += -x assembler-with-cpp -mcpu=cortex-m3 -mthumb

# NOTE: The -Wl,--gc-sections flag may interfere with debugging using gdb.

ifeq ($(HAS_BOOT),1)
	LD_FILE=efm32g_boot.ld
else
	LD_FILE=efm32g.ld
endif

#LDFLAGS += -Xlinker -Map=$(OBJ_DIR)/$(PROJECTNAME).map -mcpu=cortex-m3
#-specs=nano.specs -u _printf_float -u _scanf_float \
LDFLAGS += -mcpu=cortex-m3 -mthumb \
-T$(ENERGYMICRO)/Device/EnergyMicro/EFM32G/Source/GCC/$(LD_FILE) \
-Wl,--gc-sections

#LIBS += -Wl,--start-group -lstdc++ -lsupc++ -lc -lgcc -lnosys   -Wl,--end-group
LIBS += -Wl,--start-group -lstdc++ -lc -lgcc -lnosys  -Wl,--end-group

