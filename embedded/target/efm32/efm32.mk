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
ifeq ($(HAS_BOOT),1)
    ${info Bootloader enabled}
else
    ${info Bootloader disabled}
endif

###############################################################################
# PATHS
###############################################################################

ENERGYMICRO = $(TOOLCHAIN_DIR)/common/energymicro
#WINDOWSCS  ?= GNU Tools ARM Embedded\4.7 2013q1
#LINUXCS    ?= /home/mribeiro/gcc-arm-none-eabi-4_7-2013q1

# Try autodetecting the environment
ifeq ($(SHELLNAMES),)
  # Assume we are making on a Linux platform
  #TOOLDIR := $(LINUXCS)
  TOOLDIR := $(TOOLCHAIN_DIR)/linux/arm/gcc
else
  QUOTE :="
  ifneq ($(COMSPEC),)
    # Assume we are making on a mingw/msys/cygwin platform running on Windows
    # This is a convenient place to override TOOLDIR, DO NOT add trailing
    # whitespace chars, they do matter !
    #TOOLDIR := $(PROGRAMFILES)/$(WINDOWSCS)
    TOOLDIR := $(TOOLCHAIN_DIR)/win/arm/gcc
    ifeq ($(findstring cygdrive,$(shell set)),)
      # We were not on a cygwin platform
      NULLDEVICE := NUL
    endif
  else
    # Assume we are making on a Windows platform
    # This is a convenient place to override TOOLDIR, DO NOT add trailing
    # whitespace chars, they do matter !
    SHELL      := $(SHELLNAMES)
    #TOOLDIR    := $(ProgramFiles)/$(WINDOWSCS)
    TOOLDIR := $(TOOLCHAIN_DIR)/win/arm/gcc
    RMDIRS     := rd /s /q
    RMFILES    := del /s /q
    ALLFILES   := \*.*
    NULLDEVICE := NUL
  endif
endif

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

#C_SRC += \
#$(ENERGYMICRO)/Device/EnergyMicro/EFM32G/Source/system_efm32g.c

#S_SRC += $(ENERGYMICRO)/Device/EnergyMicro/EFM32G/Source/GCC/startup_efm32g.S

###############################################################################
# FLAGS
###############################################################################

# -MMD : Don't generate dependencies on system header files.
# -MP  : Add phony targets, useful when a h-file is removed from a project.
# -MF  : Specify a file to write the dependencies to.
DEPFLAGS = -MMD -MP -MF $(@:.o=.d)

# Add -Wa,-ahld=$(LST_DIR)/$(@F:.o=.lst) to CFLAGS to produce assembly list files
# -DDEBUG_EFM -DNDEBUG

CFLAGS += -Wall -Wextra -mcpu=cortex-m3 -mthumb -mfix-cortex-m3-ldrd \
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
LDFLAGS += -mcpu=cortex-m3 -mthumb \
-T$(ENERGYMICRO)/Device/EnergyMicro/EFM32G/Source/GCC/$(LD_FILE) \
-Wl,--gc-sections

LIBS = -lm -Wl,--start-group -lgcc -lc -lnosys   -Wl,--end-group 

