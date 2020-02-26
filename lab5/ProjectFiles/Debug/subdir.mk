################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
TCF_SRCS += \
../dsp_bios_.tcf 


# Each subdirectory must supply rules for building sources it contributes
./dsp_bios_cfg.cmd: ../dsp_bios_.tcf
	@echo 'Building file: $<'
	@echo 'Invoking: TConf'
	"/xdctools/tconf" -b -Dconfig.importPath="/packages;" "$<"
	@echo 'Finished building: $<'
	@echo ' '

./dsp_bios_cfg.s??: ./dsp_bios_cfg.cmd
./dsp_bios_cfg_c.c: ./dsp_bios_cfg.cmd
./dsp_bios_cfg.h: ./dsp_bios_cfg.cmd
./dsp_bios_cfg.h??: ./dsp_bios_cfg.cmd
./dsp_bios_.cdb: ./dsp_bios_cfg.cmd


