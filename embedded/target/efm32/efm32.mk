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

INIT_CLKFREQ = 14000000

###############################################################################
# DIRS and FILES
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
$(ENERGYMICRO)/emlib/inc

ifeq ($(FAMILY),)
$(error EFM32 FAMILY not defined)
endif



ifeq ($(FAMILY), EFM32G)
INCLUDE_DIR += $(ENERGYMICRO)/Device/EnergyMicro/EFM32G/Include
C_SRC += $(ENERGYMICRO)/Device/EnergyMicro/EFM32G/Source/system_efm32g.c
S_SRC += $(ENERGYMICRO)/Device/EnergyMicro/EFM32G/Source/GCC/startup_efm32g.S
ifeq ($(HAS_BOOT),1)
LINKER_SCRIPT = $(ENERGYMICRO)/Device/EnergyMicro/EFM32G/Source/GCC/efm32g_boot.ld
else
LINKER_SCRIPT = $(ENERGYMICRO)/Device/EnergyMicro/EFM32G/Source/GCC/efm32g.ld
endif
endif

ifeq ($(FAMILY), EFM32TG)
INCLUDE_DIR += $(ENERGYMICRO)/Device/EnergyMicro/EFM32TG/Include
C_SRC += $(ENERGYMICRO)/Device/EnergyMicro/EFM32TG/Source/system_efm32tg.c
S_SRC += $(ENERGYMICRO)/Device/EnergyMicro/EFM32TG/Source/GCC/startup_efm32tg.S
ifeq ($(HAS_BOOT),1)
LINKER_SCRIPT = $(ENERGYMICRO)/Device/EnergyMicro/EFM32TG/Source/GCC/efm32tg_boot.ld
else
LINKER_SCRIPT = $(ENERGYMICRO)/Device/EnergyMicro/EFM32TG/Source/GCC/efm32tg.ld
endif
endif

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
$(DEPFLAGS) \
-D$(DEVICE) -D$(BOARD) 

ASMFLAGS += -x assembler-with-cpp -mcpu=cortex-m3 -mthumb

# NOTE: The -Wl,--gc-sections flag may interfere with debugging using gdb.


#LDFLAGS += -Xlinker -Map=$(OBJ_DIR)/$(PROJECTNAME).map -mcpu=cortex-m3
#-specs=nano.specs -u _printf_float -u _scanf_float
LDFLAGS = -mcpu=cortex-m3 -mthumb \
-T$(LINKER_SCRIPT) \
-Wl,--gc-sections

#LIBS += -Wl,--start-group -lstdc++ -lsupc++ -lc -lgcc -lnosys   -Wl,--end-group
LIBS += -Wl,--start-group -lstdc++ -lc -lgcc -lnosys  -Wl,--end-group


###############################################################################
# UPLOAD
###############################################################################
EFM32_LOADER=/home/mribeiro/bitbucket/qkthings/software/qkloader/efm32_loader/release/efm32_loader
UPLOAD_CMD = $(EFM32_LOADER) $(PORT) $(FILE)

