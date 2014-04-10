####################################################################
# QkThings                                                         
####################################################################

TOOLCHAIN_DIR = shared/toolchain

####################################################################
# DEFINITIONS                                                      
####################################################################

.SUFFIXES:
.PHONY: all clean upload

ifeq ($(PROJECT),)
  $(error PROJECT or TEST must be defined)
endif

PROJECT_NAME=$(PROJECT)
BUILD_DIR = $(PROJECT_NAME)/build
OBJ_DIR = $(BUILD_DIR)/obj
BIN_DIR = $(BUILD_DIR)/bin
LIB_DIR = $(BUILD_DIR)/lib/$(TARGET_NAME)/$(TARGET_VARIANT)

ifeq ($(TARGET),)
  -include saved.target
  ifeq ($(TARGET),)
    ${info TARGET not defined, using default target 'arduino.uno'}
    TARGET=arduino.uno
  else
    ${info TARGET not defined, using saved target '$(TARGET)'}
  endif
else
    ${info TARGET = '$(TARGET)'}
endif

get_target_name = $(firstword $(subst ., ,$1))
get_target_variant = $(or $(word 2,$(subst ., ,$1)),$(value 2))

TARGET_NAME=$(call get_target_name,$(TARGET))
TARGET_VARIANT=$(call get_target_variant,$(TARGET),$(TARGET_NAME))
TARGET_DIR=$(BUILD_DIR)/target

TARGET_GLOBAL=target/$(TARGET_NAME).mk

OPTIMIZE = 0
OFORMAT = binary

# Try autodetecting the environment
ifeq ($(SHELLNAMES),)
  # Assume we are making on a Linux platform
else
  QUOTE :="
  ifneq ($(COMSPEC),)
    # Assume we are making on a mingw/msys/cygwin platform running on Windows
    # This is a convenient place to override TOOLDIR, DO NOT add trailing
    # whitespace chars, they do matter !
    ifeq ($(findstring cygdrive,$(shell set)),)
      # We were not on a cygwin platform
      NULLDEVICE := NUL
    endif
  else
    # Assume we are making on a Windows platform
    # This is a convenient place to override TOOLDIR, DO NOT add trailing
    # whitespace chars, they do matter !
    SHELL      := $(SHELLNAMES)
    RMDIRS     := rd /s /q
    RMFILES    := del /s /q
    ALLFILES   := \*.*
    NULLDEVICE := NUL
  endif
endif

RMDIRS     := rm -rf
RMFILES    := rm -rf
ALLFILES   := /*.*
NULLDEVICE := /dev/null
SHELLNAMES := $(ComSpec)$(COMSPEC)

####################################################################
# DIRS AND FLAGS                     
####################################################################

include $(BUILD_DIR)/$(PROJECT_NAME).mk

CFLAGS += -O$(OPTIMIZE) -g3 -Wall
LIBS += -lm
ARFLAGS = rcs

INCLUDEPATHS = $(addprefix -I, $(INCLUDE_DIR))
C_SRC = $(wildcard $(addsuffix /*.c, $(C_SRC_DIR)))

# Create directories and do a clean which is compatible with parallell make
$(shell mkdir $(OBJ_DIR)>$(NULLDEVICE) 2>&1)
$(shell mkdir $(BIN_DIR)>$(NULLDEVICE) 2>&1)
$(shell mkdir -p $(LIB_DIR)>$(NULLDEVICE) 2>&1)
ifeq (clean,$(findstring clean, $(MAKECMDGOALS)))
  ifneq ($(filter $(MAKECMDGOALS),all debug release),)
    $(shell $(RMFILES) $(OBJ_DIR)$(ALLFILES)>$(NULLDEVICE) 2>&1)
    $(shell $(RMFILES) $(BIN_DIR)$(ALLFILES)>$(NULLDEVICE) 2>&1)
    $(shell $(RMFILES) $(LST_DIR)$(ALLFILES)>$(NULLDEVICE) 2>&1)
  endif
endif

###############################################################################
# FILES
###############################################################################
C_FILES = $(notdir $(C_SRC) )
S_FILES = $(notdir $(S_SRC) $(s_SRC) )
C_PATHS = $(sort $(dir $(C_SRC) ) )
S_PATHS = $(sort $(dir $(S_SRC) $(s_SRC) ) )
C_OBJS = $(addprefix $(OBJ_DIR)/, $(C_FILES:.c=.o))
C_DEPS = $(addprefix $(OBJ_DIR)/, $(C_FILES:.c=.d))
S_OBJS = $(if $(S_SRC), $(addprefix $(OBJ_DIR)/, $(S_FILES:.S=.o)))
s_OBJS = $(if $(s_SRC), $(addprefix $(OBJ_DIR)/, $(S_FILES:.s=.o)))
OBJS = $(C_OBJS) $(S_OBJS) $(s_OBJS)

vpath %.c $(C_PATHS)
vpath %.s $(S_PATHS)
vpath %.S $(S_PATHS)

###############################################################################
# BUILD
###############################################################################
all: lib

app:    $(BIN_DIR)/$(PROJECT_NAME).bin
lib:	$(LIB_DIR)/lib$(PROJECT_NAME).a
test:	app

# Create objects from C SRC files
$(OBJ_DIR)/%.o: %.c
	@echo Compiling $<
	$(CC) $(CFLAGS) $(INCLUDEPATHS) -c -o $@ $<

# Assemble .s/.S files
$(OBJ_DIR)/%.o: %.s
	@echo Assembling $<
	$(CC) $(ASMFLAGS) $(INCLUDEPATHS) -c -o $@ $<

$(OBJ_DIR)/%.o: %.S
	@echo Assembling $<
	$(CC) $(ASMFLAGS) $(INCLUDEPATHS) -c -o $@ $<

# Link
$(BIN_DIR)/$(PROJECT_NAME).out: $(OBJS)
	@echo Linking target: $@
	$(CC) $(LDFLAGS) $(OBJS) $(LIBS) -o $(BIN_DIR)/$(PROJECT_NAME).out
	
# Create static library
$(LIB_DIR)/lib$(PROJECT_NAME).a: $(OBJS)
	@echo Creating static library: $@
	$(AR) $(ARFLAGS) $(LIB_DIR)/lib$(PROJECT_NAME).a $(OBJS)
	$(RMDIRS) $(OBJ_DIR) 

# Create binary file
$(BIN_DIR)/$(PROJECT_NAME).bin: $(BIN_DIR)/$(PROJECT_NAME).out
	@echo Creating binary file
	$(OBJCOPY) -O $(OFORMAT) $(BIN_DIR)/$(PROJECT_NAME).out $(BIN_DIR)/$(PROJECT_NAME).bin
	$(RMDIRS) $(OBJ_DIR) 
	$(PSIZE) $(BIN_DIR)/$(PROJECT_NAME).out
# Uncomment next line to produce assembly listing of entire program
#	$(DUMP) -h -S -C $(BIN_DIR)/$(PROJECT_NAME).out>$(LST_DIR)/$(PROJECT_NAME)out.lst

clean:
ifeq ($(filter $(MAKECMDGOALS),all ),)
	$(RMDIRS) $(OBJ_DIR) $(BIN_DIR) $(LIB_DIR)
endif

# include auto-generated dependency files (explicit rules)
ifneq (clean,$(findstring clean, $(MAKECMDGOALS)))
-include $(C_DEPS)
endif

savetarget:
	-@rm -f saved.target
	@echo "saving target"
	@echo >saved.target "TARGET = $(TARGET)"

###############################################################################
# UPLOAD
###############################################################################
PORT ?= comm_port
FILE ?= file_to_upload
upload:
	$(UPLOAD_CMD)

